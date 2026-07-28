# -*- coding: utf-8 -*-
"""Aplica os cartoes escritos pelo Claude no anki-master.json — skill `anki`.

Recebe um JSON no formato:

  { "<id da lacuna>": {"pergunta": "...", "resposta": "...", "extra": "..."}, ... }

`extra` e' opcional. Por padrao NUNCA sobrescreve cartao ja existente (so preenche
os nulos), para nao apagar um cartao que o usuario ja ajustou a mao.

Uso:
  python apply_cards.py --base "<pasta de estudos>" --file <cartoes.json> [--forcar]
  python apply_cards.py --base "<pasta>" --descartar <id> [<id> ...]
"""

import argparse
import json
import re
import sys
from pathlib import Path


def limpar(texto, limite=None):
    t = re.sub(r"[ \t]+", " ", (texto or "")).strip()
    if limite and len(t) > limite:
        t = t[:limite].rsplit(" ", 1)[0] + " […]"
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=".", help="pasta que contém quiz-data\\")
    ap.add_argument("--file", help="JSON com os cartões escritos pelo Claude")
    ap.add_argument("--descartar", nargs="+", default=[],
                    help="ids de lacunas que não devem virar cartão")
    ap.add_argument("--forcar", action="store_true",
                    help="sobrescreve cartões já existentes")
    args = ap.parse_args()

    if not args.file and not args.descartar:
        sys.exit("ERRO: informe --file e/ou --descartar.")

    master_path = Path(args.base) / "quiz-data" / "anki-master.json"
    if not master_path.exists():
        sys.exit(f"ERRO: {master_path} não existe — rode coletar_lacunas.py antes.")
    master = json.loads(master_path.read_text(encoding="utf-8"))
    lacunas = master.setdefault("lacunas", {})

    aplicados, pulados, desconhecidos, incompletos = 0, 0, [], []

    if args.file:
        cartoes = json.loads(Path(args.file).read_text(encoding="utf-8"))
        if not isinstance(cartoes, dict):
            sys.exit("ERRO: o JSON de cartões deve ser um objeto {id: {...}}.")
        for lid, campos in cartoes.items():
            entry = lacunas.get(lid)
            if entry is None:
                desconhecidos.append(lid)
                continue
            pergunta = limpar((campos or {}).get("pergunta"), 400)
            resposta = limpar((campos or {}).get("resposta"), 600)
            if not pergunta or not resposta:
                incompletos.append(lid)
                continue
            if entry.get("pergunta") and not args.forcar:
                pulados += 1
                continue
            entry["pergunta"] = pergunta
            entry["resposta"] = resposta
            extra = limpar((campos or {}).get("extra"), 600)
            if extra:
                entry["extra"] = extra
            aplicados += 1

    descartados = 0
    for lid in args.descartar:
        entry = lacunas.get(lid)
        if entry is None:
            desconhecidos.append(lid)
            continue
        entry["status"] = "descartado"
        descartados += 1

    master_path.write_text(json.dumps(master, ensure_ascii=False, indent=1),
                           encoding="utf-8")

    print(f"Cartões aplicados: {aplicados}")
    if pulados:
        print(f"Pulados (já tinham cartão; use --forcar para sobrescrever): {pulados}")
    if descartados:
        print(f"Lacunas descartadas: {descartados}")
    if incompletos:
        print(f"AVISO: sem pergunta/resposta, ignorados: {', '.join(incompletos[:10])}")
    if desconhecidos:
        print(f"AVISO: ids inexistentes no master: {', '.join(desconhecidos[:10])}")

    faltam = sum(1 for e in lacunas.values()
                 if e.get("status") == "ativo" and not e.get("pergunta"))
    print(f"Ainda pendentes de cartão: {faltam}")


if __name__ == "__main__":
    main()
