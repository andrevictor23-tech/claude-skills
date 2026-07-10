"""Aplica traducoes/definicoes (geradas pelo Claude) ao vocab-master.json.

Uso:
  python apply_enrichment.py --file <enriquecimento.json> [--data-dir <pasta>]

Formato do arquivo de entrada:
  { "stem": {"traducao": "...", "definicao": "..."}, ... }
"""
import argparse
import json
import sys
from pathlib import Path

DRIVE_CANDIDATES = [
    Path("G:/Meu Drive/vocabulario-kindle"),
    Path.home() / "Meu Drive" / "vocabulario-kindle",
]


def achar_data_dir(cli_value):
    if cli_value:
        return Path(cli_value)
    for cand in DRIVE_CANDIDATES:
        if cand.exists():
            return cand
    sys.exit("ERRO: pasta de dados nao encontrada; passe --data-dir.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--data-dir")
    args = ap.parse_args()

    data_dir = achar_data_dir(args.data_dir)
    master_path = data_dir / "vocab-master.json"
    master = json.loads(master_path.read_text(encoding="utf-8"))
    enriquecimento = json.loads(Path(args.file).read_text(encoding="utf-8"))

    aplicadas, desconhecidas = 0, []
    for stem, info in enriquecimento.items():
        entry = master["palavras"].get(stem)
        if not entry:
            desconhecidas.append(stem)
            continue
        entry["traducao"] = info["traducao"]
        entry["definicao"] = info["definicao"]
        aplicadas += 1

    master_path.write_text(
        json.dumps(master, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    pendentes = [s for s, e in master["palavras"].items() if not e["traducao"]]
    print(f"Enriquecimento aplicado: {aplicadas} palavras")
    if desconhecidas:
        print(f"Ignoradas (nao estao no master): {', '.join(desconhecidas)}")
    print(f"Ainda pendentes: {len(pendentes)}")
    if pendentes:
        print("LISTA_PENDENTES: " + ", ".join(sorted(pendentes)))


if __name__ == "__main__":
    main()
