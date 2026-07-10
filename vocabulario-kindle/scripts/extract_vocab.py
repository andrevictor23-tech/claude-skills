"""Extrai vocabulario EN do vocab.db do Kindle e atualiza o master JSON (incremental).

Uso:
  python extract_vocab.py --db "C:/Users/andre/Downloads/vocab.db" [--data-dir <pasta>]

- Agrupa lookups por stem (raiz da palavra).
- Palavras ja presentes no master sao preservadas (com traducao/definicao ja feitas).
- Palavras novas entram com "traducao": null e "definicao": null, para o Claude preencher.
- Sempre atualiza frases de exemplo e contagem de lookups (novas leituras somam contexto).
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

DRIVE_CANDIDATES = [
    Path("G:/Meu Drive/vocabulario-kindle"),
    Path.home() / "Meu Drive" / "vocabulario-kindle",
]

KINDLE_DB_CANDIDATES = [
    Path.home() / "Downloads" / "vocab.db",
] + [Path(f"{d}:/system/vocabulary/vocab.db") for d in "DEFGHIJ"]

MAX_EXEMPLOS = 3


def achar_data_dir(cli_value):
    if cli_value:
        p = Path(cli_value)
        p.mkdir(parents=True, exist_ok=True)
        return p
    for cand in DRIVE_CANDIDATES:
        if cand.parent.exists():
            cand.mkdir(parents=True, exist_ok=True)
            return cand
    sys.exit("ERRO: nenhuma pasta 'Meu Drive' encontrada; passe --data-dir explicitamente.")


def achar_db(cli_value):
    if cli_value:
        p = Path(cli_value)
        if not p.exists():
            sys.exit(f"ERRO: vocab.db nao encontrado em {p}")
        return p
    for cand in KINDLE_DB_CANDIDATES:
        if cand.exists():
            return cand
    sys.exit("ERRO: vocab.db nao encontrado (Downloads nem Kindle plugado); passe --db.")


def limpar_titulo(titulo):
    """Titulos vindos de acervos externos tem lixo: corta em ' -- ' e normaliza."""
    if not titulo:
        return "Livro desconhecido"
    titulo = titulo.split(" -- ")[0]
    titulo = titulo.replace(" _ ", ": ")
    titulo = re.sub(r"\s+", " ", titulo).strip()
    return titulo[:90]


def limpar_frase(usage):
    if not usage:
        return None
    frase = re.sub(r"\s+", " ", usage).strip()
    # frases muito curtas ou muito longas dao cartoes ruins
    if len(frase) < 15:
        return None
    return frase[:280]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", help="caminho do vocab.db (default: Downloads ou Kindle plugado)")
    ap.add_argument("--data-dir", help="pasta de dados (default: <Meu Drive>/vocabulario-kindle)")
    args = ap.parse_args()

    db_path = achar_db(args.db)
    data_dir = achar_data_dir(args.data_dir)
    master_path = data_dir / "vocab-master.json"

    master = {"palavras": {}}
    if master_path.exists():
        master = json.loads(master_path.read_text(encoding="utf-8"))

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    rows = cur.execute(
        """SELECT w.stem, w.word, w.category, l.usage, b.title, l.timestamp
           FROM WORDS w
           LEFT JOIN LOOKUPS l ON l.word_key = w.id
           LEFT JOIN BOOK_INFO b ON l.book_key = b.id
           WHERE w.lang = 'en'
           ORDER BY l.timestamp ASC"""
    ).fetchall()
    con.close()

    palavras = master["palavras"]
    novas = []
    contagem_rodada = {}
    for stem, word, category, usage, title, ts in rows:
        stem = (stem or word or "").strip().lower()
        if not stem or not re.match(r"^[a-z][a-z' -]*$", stem):
            continue
        entry = palavras.get(stem)
        if entry is None:
            entry = {
                "stem": stem,
                "formas": [],
                "traducao": None,
                "definicao": None,
                "exemplos": [],
                "dominada_kindle": False,
                "lookups": 0,
                "primeiro_lookup": None,
                "ultimo_lookup": None,
            }
            palavras[stem] = entry
            novas.append(stem)

        if word and word.lower() not in entry["formas"]:
            entry["formas"].append(word.lower())
        if category == 100:
            entry["dominada_kindle"] = True

        frase = limpar_frase(usage)
        if frase:
            ja_tem = any(e["frase"] == frase for e in entry["exemplos"])
            if not ja_tem:
                entry["exemplos"].append({"frase": frase, "livro": limpar_titulo(title)})
                # mantem so os exemplos mais recentes
                entry["exemplos"] = entry["exemplos"][-MAX_EXEMPLOS:]

        if ts:
            contagem_rodada[stem] = contagem_rodada.get(stem, 0) + 1
            if not entry["primeiro_lookup"] or ts < entry["primeiro_lookup"]:
                entry["primeiro_lookup"] = ts
            if not entry["ultimo_lookup"] or ts > entry["ultimo_lookup"]:
                entry["ultimo_lookup"] = ts

    # o vocab.db do Kindle e cumulativo: recomputar evita inflar em re-execucoes
    for stem, n in contagem_rodada.items():
        palavras[stem]["lookups"] = max(palavras[stem].get("lookups", 0), n)

    master_path.write_text(
        json.dumps(master, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    pendentes = sorted(s for s, e in palavras.items() if not e["traducao"])
    print(f"vocab.db lido: {db_path}")
    print(f"Master: {master_path}")
    print(f"Total de palavras EN no master: {len(palavras)}")
    print(f"Novas nesta rodada: {len(novas)}")
    print(f"Pendentes de enriquecimento (traducao/definicao): {len(pendentes)}")
    if pendentes:
        print("LISTA_PENDENTES: " + ", ".join(pendentes))


if __name__ == "__main__":
    main()
