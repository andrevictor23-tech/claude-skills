# -*- coding: utf-8 -*-
"""Dashboard de desempenho MPSP — skill `desempenho`.

Cruza bancos de questões e exports de erros de quiz-data/ com
wiki/revisao/erros.md e gera um HTML autocontido (tema escuro).

Uso:
  python build_dashboard.py --base "<pasta de estudos>" [--out <arquivo.html>]
"""

import argparse
import html
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

# Pesos oficiais da prova objetiva MPSP 97º (100 questões) — wiki/indice.md.
PESOS = {
    "Penal": 15,
    "Tutela Coletiva": 14,
    "Constitucional": 12,
    "Processo Penal": 12,
    "Civil": 10,
    "Processo Civil": 10,
    "Administrativo": 10,
    "Infância e Juventude": 6,
    "Empresarial": 4,
    "Direitos Humanos": 4,
    "Eleitoral": 3,
}

DISCIPLINAS_CONHECIDAS = set(PESOS) | {"Institucional"}


def _slug(texto):
    s = unicodedata.normalize("NFKD", texto or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


ALIASES = {
    "penal": "Penal", "direito penal": "Penal",
    "tutela coletiva": "Tutela Coletiva",
    "tutela de interesses difusos e coletivos": "Tutela Coletiva",
    "difusos e coletivos": "Tutela Coletiva",
    "constitucional": "Constitucional", "direito constitucional": "Constitucional",
    "processo penal": "Processo Penal", "direito processual penal": "Processo Penal",
    "civil": "Civil", "direito civil": "Civil",
    "processo civil": "Processo Civil", "direito processual civil": "Processo Civil",
    "administrativo": "Administrativo", "direito administrativo": "Administrativo",
    "infancia e juventude": "Infância e Juventude",
    "direito da infancia e juventude": "Infância e Juventude",
    "infancia": "Infância e Juventude", "eca": "Infância e Juventude",
    "empresarial": "Empresarial", "comercial": "Empresarial",
    "direito comercial/empresarial": "Empresarial",
    "direito empresarial": "Empresarial",
    "direitos humanos": "Direitos Humanos", "dh": "Direitos Humanos",
    "eleitoral": "Eleitoral", "direito eleitoral": "Eleitoral",
    "institucional": "Institucional", "direito institucional": "Institucional",
}


def canon(nome):
    return ALIASES.get(_slug(nome), (nome or "").strip() or "Sem matéria")


def q_hash(q):
    base = _slug(q.get("enunciado") or "")[:120]
    return base or f"num-{q.get('numero')}"


def load_quiz_data(qdir):
    banks, exports, avisos = {}, [], []
    unicas = {}  # materia -> set de hashes (dedup de bancos que se sobrepõem)
    for p in sorted(qdir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            avisos.append(f"{p.name}: JSON inválido ({e})")
            continue
        # bancos aparecem como dict único ou como lista de bancos
        if isinstance(data, dict) and isinstance(data.get("questoes"), list):
            bancos_no_arquivo = [data]
        elif (isinstance(data, list) and data
              and all(isinstance(x, dict) and isinstance(x.get("questoes"), list)
                      for x in data)):
            bancos_no_arquivo = data
        else:
            bancos_no_arquivo = []
        if bancos_no_arquivo:
            for banco in bancos_no_arquivo:
                bid = banco.get("id") or p.stem
                qmap = {}
                for q in banco["questoes"]:
                    mat = canon(q.get("materia"))
                    if isinstance(q.get("numero"), int):
                        qmap[q["numero"]] = mat
                    unicas.setdefault(mat, set()).add(q_hash(q))
                banks[bid] = qmap
        elif (isinstance(data, list) and data
              and all(isinstance(x, dict) and "sim" in x and "numero" in x for x in data)):
            exports.append((p.name, data))
        else:
            avisos.append(f"{p.name}: formato não reconhecido — ignorado")
    return banks, unicas, exports, avisos


def cruza_erros(banks, exports):
    err = Counter()
    respondidos = set()  # ids de bancos citados em algum export
    sem_vinculo = 0
    for _nome, rows in exports:
        for row in rows:
            respondidos.add(row["sim"])
            mat = banks.get(row["sim"], {}).get(row.get("numero"))
            if mat:
                err[mat] += 1
            else:
                sem_vinculo += 1
    return err, respondidos, sem_vinculo


def classifica_motivo(texto):
    s = _slug(texto)
    if "distra" in s:
        return "Distração"
    if "pegadinha" in s or "inversao" in s or "requisito" in s or "simetric" in s:
        return "Pegadinha"
    if "jurisprud" in s or "desatualizad" in s or "overruling" in s:
        return "Jurisprudência"
    if "desconhec" in s:
        return "Desconhecimento"
    return "Outro"


def parse_erros_md(path):
    entradas, padroes = [], []
    if not path.exists():
        return entradas, padroes, [f"{path} não encontrado"]
    disc, entry, in_padroes, in_fence = None, None, False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            titulo = line[3:].strip()
            in_padroes = _slug(titulo).startswith("padroes recorrentes")
            c = canon(titulo)
            disc = c if c in DISCIPLINAS_CONHECIDAS else None
            entry = None
            continue
        if in_padroes:
            if line.strip():
                padroes.append(line.rstrip())
            continue
        if line.startswith("### ") and disc:
            entry = {"disciplina": disc, "titulo": line[4:].strip(),
                     "erro": "", "motivo": "", "fundamento": ""}
            entradas.append(entry)
            continue
        if entry:
            m = re.match(r"-\s+\*\*(Erro|Motivo|Fundamento correto):\*\*\s*(.*)", line.strip())
            if m:
                chave = {"Erro": "erro", "Motivo": "motivo",
                         "Fundamento correto": "fundamento"}[m.group(1)]
                entry[chave] = m.group(2).strip()
    return entradas, padroes, []


# ---------------------------------------------------------------- HTML/SVG --

E = html.escape


def md_inline(texto):
    """Converte só o **negrito** do markdown; o resto vira texto escapado."""
    out = E(texto)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def hbar_svg(rows, fmt):
    """Barras horizontais: rows = [(label, valor, tooltip)]. Uma série, azul."""
    if not rows:
        return "<p class='vazio'>Sem dados ainda.</p>"
    LBL, PADR, BH, GAP, TOP = 190, 84, 18, 12, 6
    W = 680
    Hn = TOP + len(rows) * (BH + GAP)
    maxv = max(v for _, v, _ in rows) or 1
    plot = W - LBL - PADR
    parts = [f'<svg viewBox="0 0 {W} {Hn}" role="img" '
             f'style="width:100%;height:auto;font:12px system-ui,sans-serif">']
    parts.append(f'<line x1="{LBL}" y1="0" x2="{LBL}" y2="{Hn - GAP + 4}" '
                 f'stroke="var(--baseline)" stroke-width="1"/>')
    for i, (label, val, tip) in enumerate(rows):
        y = TOP + i * (BH + GAP)
        w = max(plot * val / maxv, 2)
        r = min(4, w / 2)
        d = (f"M {LBL},{y} h {w - r:.1f} a {r},{r} 0 0 1 {r},{r} "
             f"v {BH - 2 * r:.1f} a {r},{r} 0 0 1 -{r},{r} h -{w - r:.1f} z")
        parts.append(
            f'<g class="bar"><title>{E(tip)}</title>'
            f'<path d="{d}" fill="var(--series-1)"/>'
            f'<text x="{LBL - 8}" y="{y + BH - 5}" text-anchor="end" '
            f'fill="var(--ink-2)">{E(label)}</text>'
            f'<text x="{LBL + w + 8:.1f}" y="{y + BH - 5}" '
            f'fill="var(--ink-1)">{E(fmt(val))}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


CSS = """
:root{color-scheme:dark;
 --page:#0d0d0d; --surface:#1a1a19; --ink-1:#ffffff; --ink-2:#c3c2b7;
 --muted:#898781; --grid:#2c2c2a; --baseline:#383835;
 --series-1:#3987e5; --border:rgba(255,255,255,.10)}
*{box-sizing:border-box;margin:0}
body{background:var(--page);color:var(--ink-1);
 font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:28px 16px}
main{max-width:960px;margin:0 auto;display:grid;gap:18px}
h1{font-size:22px} h2{font-size:15px;font-weight:600;margin-bottom:10px}
.sub{color:var(--muted);font-size:12px}
section{background:var(--surface);border:1px solid var(--border);
 border-radius:10px;padding:18px 20px;overflow-x:auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.kpi{background:var(--surface);border:1px solid var(--border);
 border-radius:10px;padding:14px 16px}
.kpi .v{font-size:26px;font-weight:650}
.kpi .l{color:var(--muted);font-size:12px;margin-top:2px}
.bar path{transition:opacity .1s} .bar:hover path{opacity:.8}
table{border-collapse:collapse;width:100%;font-size:13px}
th{color:var(--muted);text-align:left;font-weight:500;padding:6px 10px;
 border-bottom:1px solid var(--baseline)}
td{padding:8px 10px;border-bottom:1px solid var(--grid);vertical-align:top}
td.num{font-variant-numeric:tabular-nums}
.tag{display:inline-block;border:1px solid var(--border);border-radius:999px;
 padding:1px 9px;font-size:12px;color:var(--ink-2);white-space:nowrap}
.padroes p{margin:6px 0;color:var(--ink-2)} .padroes strong{color:var(--ink-1)}
.vazio{color:var(--muted)} footer{color:var(--muted);font-size:11px}
.caption{color:var(--muted);font-size:12px;margin-top:8px}
"""


def build_html(ctx):
    kpi = "".join(
        f'<div class="kpi"><div class="v">{E(str(v))}</div><div class="l">{E(l)}</div></div>'
        for v, l in ctx["kpis"])
    linhas = "".join(
        f'<tr><td><span class="tag">{E(e["disciplina"])}</span></td>'
        f'<td>{E(e["titulo"])}</td>'
        f'<td><span class="tag">{E(classifica_motivo(e["motivo"]))}</span></td>'
        f'<td>{md_inline(e["fundamento"] or e["motivo"] or "—")}</td></tr>'
        for e in ctx["entradas"])
    padroes = "".join(f"<p>{md_inline(l.lstrip('> #-').strip())}</p>"
                      for l in ctx["padroes"]) or "<p class='vazio'>Nada registrado.</p>"
    avisos = ("<footer>Avisos: " + " · ".join(E(a) for a in ctx["avisos"]) + "</footer>"
              if ctx["avisos"] else "")
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard — Desempenho MPSP</title><style>{CSS}</style></head>
<body><main>
<div><h1>Desempenho — MPSP 97º</h1>
<p class="sub">Gerado em {ctx["quando"]} · fontes: wiki/revisao/erros.md + quiz-data/</p></div>
<div class="kpis">{kpi}</div>
<section><h2>Taxa de erro por disciplina (quizzes com erros exportados)</h2>
{ctx["svg_taxa"]}
<p class="caption">Denominador: questões dos bancos citados em algum export de erros
({ctx["n_respondidas"]} questões). Quiz sem export não conta.</p></section>
<section><h2>Prioridade de revisão — erros × peso na prova</h2>
{ctx["svg_prio"]}
<p class="caption">Prioridade = (erros no erros.md + erros de quiz) × peso da disciplina
na prova objetiva (100 questões).</p></section>
<section><h2>Motivo dos erros registrados</h2>{ctx["svg_motivos"]}</section>
<section class="padroes"><h2>Padrões recorrentes (erros.md)</h2>{padroes}</section>
<section><h2>Erros registrados na wiki — fundamento para revisar</h2>
<table><thead><tr><th>Disciplina</th><th>Fonte</th><th>Motivo</th><th>Fundamento correto</th></tr></thead>
<tbody>{linhas or '<tr><td colspan="4" class="vazio">Nenhum erro registrado.</td></tr>'}</tbody></table></section>
{avisos}
</main></body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=".", help="pasta que contém wiki\\ e quiz-data\\")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    base = Path(args.base)
    qdir = base / "quiz-data"
    if not qdir.is_dir():
        sys.exit(f"ERRO: {qdir} não existe — confira --base.")

    banks, unicas, exports, avisos = load_quiz_data(qdir)
    err_quiz, respondidos, sem_vinculo = cruza_erros(banks, exports)
    entradas, padroes, avisos_md = parse_erros_md(base / "wiki" / "revisao" / "erros.md")
    avisos += avisos_md
    if sem_vinculo:
        avisos.append(f"{sem_vinculo} erro(s) de export sem banco correspondente")

    # denominador: questões (por matéria) dos bancos citados em exports
    denom = Counter()
    for bid in respondidos & set(banks):
        for mat in banks[bid].values():
            denom[mat] += 1

    err_md = Counter(e["disciplina"] for e in entradas)
    motivos = Counter(classifica_motivo(e["motivo"]) for e in entradas)

    taxa_rows = sorted(
        ((m, 100.0 * err_quiz[m] / denom[m],
          f"{m}: {err_quiz[m]} erro(s) em {denom[m]} questões")
         for m in denom if denom[m]),
        key=lambda r: -r[1])
    prio_rows = sorted(
        ((m, (err_md[m] + err_quiz[m]) * PESOS[m],
          f"{m}: {err_md[m] + err_quiz[m]} erro(s) × peso {PESOS[m]}")
         for m in PESOS if err_md[m] + err_quiz[m]),
        key=lambda r: -r[1])
    mot_rows = [(m, n, f"{m}: {n} erro(s)") for m, n in motivos.most_common()]

    acervo = sum(len(s) for s in unicas.values())
    n_respondidas = sum(denom.values())
    critica = prio_rows[0][0] if prio_rows else "—"

    ctx = {
        "quando": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "kpis": [
            (acervo, "questões únicas no acervo"),
            (n_respondidas, "questões em quizzes com export"),
            (sum(err_quiz.values()), "erros exportados dos quizzes"),
            (len(entradas), "erros documentados na wiki"),
            (critica, "disciplina prioritária"),
        ],
        "svg_taxa": hbar_svg(taxa_rows, lambda v: f"{v:.1f}%"),
        "svg_prio": hbar_svg(prio_rows, lambda v: f"{v:g}"),
        "svg_motivos": hbar_svg(mot_rows, lambda v: f"{v:g}"),
        "entradas": entradas,
        "padroes": padroes,
        "avisos": avisos,
        "n_respondidas": n_respondidas,
    }

    out = Path(args.out) if args.out else qdir / "Dashboard - Desempenho MPSP.html"
    out.write_text(build_html(ctx), encoding="utf-8")

    print(f"Bancos lidos: {len(banks)} | exports: {len(exports)} "
          f"| erros vinculados: {sum(err_quiz.values())} | sem vínculo: {sem_vinculo}")
    print(f"Entradas do erros.md: {len(entradas)} | disciplina prioritária: {critica}")
    for a in avisos:
        print(f"AVISO: {a}")
    print(f"OK → {out}")


if __name__ == "__main__":
    main()
