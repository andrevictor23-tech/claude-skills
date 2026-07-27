# -*- coding: utf-8 -*-
"""Transforma um export do quiz em rascunho de entradas para wiki/revisao/erros.md.

Aceita o formato novo (-resultado.json, dict com "erros") e o antigo
(-erros.json, lista). Cruza cada erro com os bancos de quiz-data/ para
recuperar matéria, enunciado e comentário do espelho.

O rascunho sai com Motivo = [VERIFICAR]: quem classifica o motivo é o
usuário (ou o Claude na revisão) — nunca o parser.

Uso:
  python importar_erros.py --export <resultado.json> --quiz-data <dir> [--out rascunho.md]
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

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


ALIASES = {_slug(k): k for k in WIKI_NOTAS}
ALIASES.update({
    "direito penal": "Penal",
    "tutela de interesses difusos e coletivos": "Tutela Coletiva",
    "direito constitucional": "Constitucional",
    "direito processual penal": "Processo Penal",
    "direito civil": "Civil",
    "direito processual civil": "Processo Civil",
    "direito administrativo": "Administrativo",
    "direito da infancia e juventude": "Infância e Juventude",
    "eca": "Infância e Juventude",
    "direito comercial/empresarial": "Empresarial",
    "direito empresarial": "Empresarial",
    "dh": "Direitos Humanos",
    "direito eleitoral": "Eleitoral",
})


def canon(nome):
    return ALIASES.get(_slug(nome), (nome or "").strip() or "Sem matéria")


def carrega_bancos(qdir):
    """id do banco -> {numero -> questão completa}."""
    bancos = {}
    for p in sorted(Path(qdir).glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and isinstance(data.get("questoes"), list):
            lote = [data]
        elif (isinstance(data, list) and data
              and all(isinstance(x, dict) and isinstance(x.get("questoes"), list)
                      for x in data)):
            lote = data
        else:
            continue
        for banco in lote:
            bid = banco.get("id") or p.stem
            bancos[bid] = {q["numero"]: q for q in banco["questoes"]
                           if isinstance(q.get("numero"), int)}
    return bancos


def resumo_fundamento(q, limite=500):
    """Ponto-chave se houver; senão o trecho inicial do comentário do espelho."""
    texto = (q.get("ponto_chave") or q.get("comentario") or "").strip()
    texto = re.sub(r"\s+", " ", texto)
    if len(texto) > limite:
        texto = texto[:limite].rsplit(" ", 1)[0] + " […]"
    return texto or "[VERIFICAR — espelho sem comentário]"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--export", required=True, help="JSON exportado pelo quiz")
    ap.add_argument("--quiz-data", required=True, help="pasta quiz-data com os bancos")
    ap.add_argument("--fonte", default=None,
                    help='rótulo da fonte (padrão: nome do quiz no export ou do arquivo)')
    ap.add_argument("--out", default=None, help="arquivo de saída (padrão: stdout)")
    args = ap.parse_args()

    exp_path = Path(args.export)
    data = json.loads(exp_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("erros"), list):
        erros, fonte_padrao = data["erros"], data.get("quiz", exp_path.stem)
    elif isinstance(data, list):
        erros, fonte_padrao = data, exp_path.stem
    else:
        sys.exit("ERRO: formato de export não reconhecido.")

    fonte = args.fonte or fonte_padrao
    bancos = carrega_bancos(args.quiz_data)

    blocos, sem_vinculo = {}, []
    for row in erros:
        q = bancos.get(row.get("sim"), {}).get(row.get("numero"))
        if not q:
            sem_vinculo.append(f'{row.get("sim")}#{row.get("numero")}')
            continue
        disc = canon(q.get("materia"))
        nota = WIKI_NOTAS.get(disc)
        link = (f"[{nota}](../disciplinas/{nota})" if nota
                else "[VERIFICAR — nota da disciplina]")
        entrada = (
            f"### {disc} — {fonte}, Questão {row['numero']}\n\n"
            f"- **Erro:** marcou {row.get('marcada', '?')}; "
            f"gabarito {row.get('gabarito', '?')}\n"
            f"- **Motivo:** [VERIFICAR — pegadinha / desconhecimento / distração?]\n"
            f"- **Fundamento correto:** {resumo_fundamento(q)}\n"
            f"- **Revisar em:** {link}\n")
        blocos.setdefault(disc, []).append(entrada)

    partes = ["<!-- RASCUNHO gerado por importar_erros.py — revise Motivo e "
              "Fundamento antes de mover para wiki/revisao/erros.md -->\n"]
    for disc in sorted(blocos):
        partes.append(f"\n## {disc}\n")
        partes.extend("\n" + e for e in blocos[disc])
    saida = "\n".join(partes)

    if args.out:
        Path(args.out).write_text(saida, encoding="utf-8")
        print(f"OK: {sum(len(v) for v in blocos.values())} entrada(s) → {args.out}")
    else:
        print(saida)
    if sem_vinculo:
        print(f"\nAVISO: sem banco correspondente: {', '.join(sem_vinculo)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
