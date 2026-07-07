# -*- coding: utf-8 -*-
"""Gera quiz HTML autocontido a partir de JSONs de simulado extraidos.

--modo quiz    : responder questao a questao com feedback (padrao)
--modo revisao : caderno de revisao (tudo revelado, com espelho)
--materia X    : filtra questoes pelo campo 'materia'
"""
import argparse
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent.parent / "assets" / "template.html"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True, help="um ou mais JSONs de simulado")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--modo", choices=["quiz", "revisao"], default="quiz")
    ap.add_argument("--materia", help="filtra pelo campo materia")
    args = ap.parse_args()

    sims = []
    for f in args.data:
        sim = json.loads(Path(f).read_text(encoding="utf-8"))
        if args.materia:
            sim["questoes"] = [q for q in sim["questoes"]
                               if (q.get("materia") or "").lower() == args.materia.lower()]
        if sim["questoes"]:
            sims.append(sim)

    total = sum(len(s["questoes"]) for s in sims)
    if not total:
        print("ERRO: nenhuma questao apos o filtro. Confira o campo 'materia' nos JSONs.")
        return 1

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__TITLE__", args.title)
    html = html.replace("__MODE__", args.modo)
    html = html.replace("__QUIZ_DATA__", json.dumps(sims, ensure_ascii=False))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"OK: {total} questoes de {len(sims)} simulado(s) -> {out}")


if __name__ == "__main__":
    sys.exit(main() or 0)
