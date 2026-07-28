# -*- coding: utf-8 -*-
"""Coleta lacunas (erros comprovados) e atualiza o anki-master.json — skill `anki`.

Fontes:
  - quiz-data/*-resultado.json (e o formato antigo *-erros.json), cruzados com os
    bancos de questoes para recuperar enunciado, gabarito e comentario do espelho;
  - wiki/revisao/erros.md, com os erros que o usuario documentou a mao.

O master e' incremental e idempotente: rodar de novo NUNCA apaga cartao ja escrito
(pergunta/resposta) nem duplica lacuna — so atualiza o contexto vindo da fonte e
acrescenta as lacunas novas.

Uso:
  python coletar_lacunas.py --base "<pasta de estudos>" [--pendentes <arquivo.json>]
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Pesos da prova objetiva MPSP 97o (mesma constante de desempenho/build_dashboard.py).
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

WIKI_NOTAS = {
    "Penal": "penal.md",
    "Tutela Coletiva": "tutela-coletiva.md",
    "Constitucional": "constitucional.md",
    "Processo Penal": "processo-penal.md",
    "Civil": "civil.md",
    "Processo Civil": "processo-civil.md",
    "Administrativo": "administrativo.md",
    "Infância e Juventude": "infancia-juventude.md",
    "Empresarial": "empresarial.md",
    "Direitos Humanos": "direitos-humanos.md",
    "Eleitoral": "eleitoral.md",
}


def _slug(texto):
    s = unicodedata.normalize("NFKD", texto or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


ALIASES = {_slug(k): k for k in DISCIPLINAS_CONHECIDAS}
ALIASES.update({
    "direito penal": "Penal",
    "tutela de interesses difusos e coletivos": "Tutela Coletiva",
    "difusos e coletivos": "Tutela Coletiva",
    "direito constitucional": "Constitucional",
    "direito processual penal": "Processo Penal",
    "direito civil": "Civil",
    "direito processual civil": "Processo Civil",
    "direito administrativo": "Administrativo",
    "direito da infancia e juventude": "Infância e Juventude",
    "infancia": "Infância e Juventude",
    "eca": "Infância e Juventude",
    "comercial": "Empresarial",
    "direito comercial/empresarial": "Empresarial",
    "direito empresarial": "Empresarial",
    "dh": "Direitos Humanos",
    "direito eleitoral": "Eleitoral",
    "direito institucional": "Institucional",
})


def _slug_id(texto):
    """Slug estrito, para virar id de lacuna (sem acento, espaco ou pontuacao)."""
    return re.sub(r"[^a-z0-9]+", "-", _slug(texto)).strip("-")


def canon(nome):
    return ALIASES.get(_slug(nome), (nome or "").strip() or "Sem matéria")


def limpar(texto, limite=None):
    t = re.sub(r"\s+", " ", (texto or "")).strip()
    if limite and len(t) > limite:
        t = t[:limite].rsplit(" ", 1)[0] + " […]"
    return t


# ------------------------------------------------------------------ fontes --

def carrega_quiz_data(qdir):
    """Retorna (bancos, exports, avisos). bancos: id -> {numero -> questao}."""
    bancos, exports, avisos = {}, [], []
    for p in sorted(qdir.glob("*.json")):
        if p.name == "anki-master.json":
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            avisos.append(f"{p.name}: JSON inválido ({e})")
            continue
        if isinstance(data, dict) and isinstance(data.get("questoes"), list):
            lote = [data]
        elif (isinstance(data, list) and data
              and all(isinstance(x, dict) and isinstance(x.get("questoes"), list)
                      for x in data)):
            lote = data
        else:
            lote = []
        if lote:
            for banco in lote:
                bid = banco.get("id") or p.stem
                bancos[bid] = {q["numero"]: q for q in banco["questoes"]
                               if isinstance(q.get("numero"), int)}
        elif isinstance(data, dict) and isinstance(data.get("erros"), list):
            exports.append((data.get("quiz") or p.stem, data["erros"]))
        elif (isinstance(data, list) and data
              and all(isinstance(x, dict) and "sim" in x and "numero" in x for x in data)):
            exports.append((p.stem, data))
        else:
            avisos.append(f"{p.name}: formato não reconhecido — ignorado")
    return bancos, exports, avisos


def parse_erros_md(path):
    """Entradas do erros.md: ## Disciplina / ### Titulo / - **Campo:** valor."""
    entradas = []
    if not path.exists():
        return entradas, [f"{path.name} não encontrado — só os quizzes entraram"]
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
            continue
        if line.startswith("### ") and disc:
            entry = {"disciplina": disc, "titulo": line[4:].strip(),
                     "erro": "", "motivo": "", "fundamento": ""}
            entradas.append(entry)
            continue
        if entry:
            m = re.match(r"-\s+\*\*(Erro|Motivo|Fundamento correto):\*\*\s*(.*)",
                         line.strip())
            if m:
                chave = {"Erro": "erro", "Motivo": "motivo",
                         "Fundamento correto": "fundamento"}[m.group(1)]
                entry[chave] = m.group(2).strip()
    return entradas, []


# ------------------------------------------------------------------- merge --

CAMPOS_DO_CLAUDE = ("pergunta", "resposta", "extra")


def nova_lacuna(lid, origem, disciplina):
    return {
        "id": lid,
        "origem": origem,
        "disciplina": disciplina,
        "tema": None,
        "fonte": "",
        "enunciado": "",
        "alternativas": {},
        "marcada": None,
        "gabarito": None,
        "fundamento": "",
        "vezes_errada": 0,
        "exports_contados": [],
        "pergunta": None,
        "resposta": None,
        "extra": None,
        "status": "ativo",
    }


def merge_contexto(entry, novos):
    """Atualiza o contexto vindo da fonte sem tocar no que o Claude escreveu."""
    for k, v in novos.items():
        if k in CAMPOS_DO_CLAUDE or k == "status":
            continue
        if v not in (None, "", {}, []):
            entry[k] = v


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=".", help="pasta que contém wiki\\ e quiz-data\\")
    ap.add_argument("--pendentes", default=None,
                    help="grava as lacunas sem cartão num JSON enxuto (para o Claude ler)")
    ap.add_argument("--limite-pendentes", type=int, default=40,
                    help="quantas pendentes gravar no arquivo acima (padrão: 40)")
    args = ap.parse_args()

    base = Path(args.base)
    qdir = base / "quiz-data"
    if not qdir.is_dir():
        sys.exit(f"ERRO: {qdir} não existe — confira --base.")

    master_path = qdir / "anki-master.json"
    master = {"versao": 1, "lacunas": {}}
    if master_path.exists():
        master = json.loads(master_path.read_text(encoding="utf-8"))
    master.setdefault("lacunas", {})
    lacunas = master["lacunas"]

    bancos, exports, avisos = carrega_quiz_data(qdir)
    entradas_md, avisos_md = parse_erros_md(base / "wiki" / "revisao" / "erros.md")
    avisos += avisos_md

    novas, sem_vinculo = [], []

    # --- 1. erros exportados dos quizzes -------------------------------------
    for nome_quiz, rows in exports:
        for row in rows:
            sim, numero = row.get("sim"), row.get("numero")
            q = bancos.get(sim, {}).get(numero)
            if not q:
                sem_vinculo.append(f"{sim}#{numero}")
                continue
            lid = f"{sim}#{numero}"
            entry = lacunas.get(lid)
            if entry is None:
                entry = nova_lacuna(lid, "quiz", canon(q.get("materia")))
                lacunas[lid] = entry
                novas.append(lid)
            merge_contexto(entry, {
                "disciplina": canon(q.get("materia")),
                "tema": limpar(q.get("tema"), 80) or None,
                "fonte": f"{sim} · Q{numero}",
                "quiz": nome_quiz,
                "enunciado": limpar(q.get("enunciado"), 900),
                "alternativas": {k: limpar(v, 300)
                                 for k, v in (q.get("alternativas") or {}).items()},
                "marcada": row.get("marcada"),
                "gabarito": row.get("gabarito") or q.get("gabarito"),
                "fundamento": limpar(q.get("ponto_chave") or q.get("comentario"), 900),
            })
            # o mesmo erro pode aparecer em varios exports; conta uma vez por export.
            # a lista fica no master para que reprocessar nao infle o contador.
            contados = entry.setdefault("exports_contados", [])
            if nome_quiz not in contados:
                contados.append(nome_quiz)
                entry["vezes_errada"] = entry.get("vezes_errada", 0) + 1

    # --- 2. erros documentados na wiki --------------------------------------
    # indice para nao duplicar o que ja veio do quiz (o importar_erros.py escreve
    # titulos no formato "<disciplina> — <quiz>, Questão <n>")
    por_disc_numero = {}
    for lid, e in lacunas.items():
        if e.get("origem") != "quiz":
            continue
        m = re.search(r"#(\d+)$", lid)
        if m:
            por_disc_numero.setdefault((e["disciplina"], int(m.group(1))), []).append(lid)

    for ent in entradas_md:
        m = re.search(r"quest[ãa]o\s*(\d+)", _slug(ent["titulo"]))
        alvo = None
        if m:
            candidatos = por_disc_numero.get((ent["disciplina"], int(m.group(1))), [])
            if len(candidatos) == 1:
                alvo = candidatos[0]
        if alvo:
            # mesma questao: a anotacao da wiki enriquece a lacuna do quiz
            entry = lacunas[alvo]
            if ent["fundamento"] and len(ent["fundamento"]) > len(entry.get("fundamento") or ""):
                entry["fundamento"] = limpar(ent["fundamento"], 900)
            if ent["motivo"]:
                entry["motivo"] = limpar(ent["motivo"], 200)
            continue

        lid = "wiki::" + _slug_id(ent["titulo"])[:80]
        entry = lacunas.get(lid)
        if entry is None:
            entry = nova_lacuna(lid, "wiki", ent["disciplina"])
            entry["vezes_errada"] = 1
            lacunas[lid] = entry
            novas.append(lid)
        merge_contexto(entry, {
            "disciplina": ent["disciplina"],
            "fonte": limpar(ent["titulo"], 120),
            "enunciado": limpar(ent["erro"], 600),
            "motivo": limpar(ent["motivo"], 200),
            "fundamento": limpar(ent["fundamento"], 900),
        })

    for lid, e in lacunas.items():
        e["nota_wiki"] = WIKI_NOTAS.get(e.get("disciplina"), "")

    master_path.write_text(json.dumps(master, ensure_ascii=False, indent=1),
                           encoding="utf-8")

    # --- 3. relatorio + pendentes -------------------------------------------
    def prioridade(e):
        return (e.get("vezes_errada", 1) or 1) * PESOS.get(e.get("disciplina"), 1)

    pendentes = sorted(
        (e for e in lacunas.values()
         if e.get("status") == "ativo" and not e.get("pergunta")),
        key=lambda e: (-prioridade(e), e["id"]))

    print(f"Master: {master_path}")
    print(f"Bancos: {len(bancos)} | exports: {len(exports)} | "
          f"entradas do erros.md: {len(entradas_md)}")
    print(f"Lacunas no master: {len(lacunas)} | novas nesta rodada: {len(novas)}")
    print(f"Pendentes de cartão: {len(pendentes)}")
    for a in avisos:
        print(f"AVISO: {a}")
    if sem_vinculo:
        print(f"AVISO: {len(sem_vinculo)} erro(s) de export sem banco correspondente: "
              f"{', '.join(sem_vinculo[:10])}")

    if pendentes:
        recorte = pendentes[:args.limite_pendentes]
        print("LISTA_PENDENTES: " + ", ".join(e["id"] for e in recorte))
        if args.pendentes:
            enxuto = [{k: v for k, v in e.items()
                       if k in ("id", "disciplina", "tema", "fonte", "enunciado",
                                "alternativas", "marcada", "gabarito", "fundamento",
                                "motivo", "vezes_errada")}
                      for e in recorte]
            Path(args.pendentes).write_text(
                json.dumps(enxuto, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"Pendentes gravadas em: {args.pendentes} ({len(enxuto)} de "
                  f"{len(pendentes)})")


if __name__ == "__main__":
    main()
