"""Gera o baralho Anki (.apkg) a partir do vocab-master.json.

Uso:
  python generate_anki.py [--data-dir <pasta>] [--out <arquivo.apkg>]

Design dos cartoes (2 por palavra):
  1. Reconhecimento (leitura): frase real do livro com a palavra em destaque -> traducao + definicao.
  2. Producao (recall ativo / cloze): frase com lacuna + traducao como dica -> palavra.

GUIDs estaveis por stem: reimportar o .apkg ATUALIZA os cartoes existentes no Anki
sem duplicar e sem perder o agendamento da repeticao espacada.
Requer: pip install genanki
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import genanki
except ImportError:
    sys.exit("ERRO: rode 'python -m pip install genanki' primeiro.")

DRIVE_CANDIDATES = [
    Path("G:/Meu Drive/vocabulario-kindle"),
    Path.home() / "Meu Drive" / "vocabulario-kindle",
]

MODEL_ID = 1607392319  # fixos: nunca mudar, senao o Anki duplica tudo
DECK_ID = 2059400110

CSS = """
.card { font-family: 'Segoe UI', sans-serif; font-size: 20px; text-align: center;
        color: #1a2332; background-color: #f7f4ee; padding: 12px; }
.frase { font-size: 21px; line-height: 1.5; margin: 14px 8px; }
.frase b { color: #8a6d1f; }
.lacuna { color: #8a6d1f; font-weight: bold; letter-spacing: 2px; }
.palavra { font-size: 30px; font-weight: 700; color: #1a2332; margin: 10px 0 2px; }
.traducao { font-size: 22px; color: #2d6a4f; font-weight: 600; margin-top: 8px; }
.definicao { font-size: 16px; color: #444; margin-top: 8px; font-style: italic; }
.livro { font-size: 12px; color: #6b7280; margin-top: 16px;
         font-family: Consolas, monospace; }
.dica { font-size: 15px; color: #6b7280; margin-top: 10px; }
hr#answer { border: none; border-top: 2px solid #d9d2c4; margin: 14px 0; }
.nightMode .card { color: #e8e4da; background-color: #1a2332; }
.nightMode .palavra { color: #e8e4da; }
.nightMode .traducao { color: #7fc8a4; }
.nightMode .definicao { color: #b8b2a4; }
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Kindle Vocab EN (vocabulario-kindle)",
    fields=[
        {"name": "Word"},
        {"name": "Traducao"},
        {"name": "Definicao"},
        {"name": "Frase"},
        {"name": "FraseCloze"},
        {"name": "Livro"},
    ],
    templates=[
        {
            "name": "1 Reconhecimento (EN -> PT)",
            "qfmt": '<div class="palavra">{{Word}}</div>'
                    '<div class="frase">{{Frase}}</div>'
                    '<div class="livro">{{Livro}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">'
                    '<div class="traducao">{{Traducao}}</div>'
                    '<div class="definicao">{{Definicao}}</div>',
        },
        {
            "name": "2 Producao (cloze + dica PT)",
            "qfmt": '<div class="frase">{{FraseCloze}}</div>'
                    '<div class="dica">dica: {{Traducao}}</div>',
            "afmt": '<div class="palavra">{{Word}}</div>'
                    '<div class="frase">{{Frase}}</div>'
                    '<hr id="answer">'
                    '<div class="definicao">{{Definicao}}</div>'
                    '<div class="livro">{{Livro}}</div>',
        },
    ],
    css=CSS,
)


class VocabNote(genanki.Note):
    @property
    def guid(self):
        # estavel por stem: reimportacao atualiza em vez de duplicar
        return genanki.guid_for("vocabulario-kindle::" + self.fields[0].lower())


def achar_data_dir(cli_value):
    if cli_value:
        return Path(cli_value)
    for cand in DRIVE_CANDIDATES:
        if cand.exists():
            return cand
    sys.exit("ERRO: pasta de dados nao encontrada; passe --data-dir.")


def destacar(frase, formas, stem):
    """Retorna (frase com <b>palavra</b>, frase com lacuna) usando a forma presente na frase."""
    candidatos = sorted(set(formas + [stem]), key=len, reverse=True)
    for forma in candidatos:
        m = re.search(r"\b" + re.escape(forma) + r"\w*", frase, re.IGNORECASE)
        if m:
            achada = m.group(0)
            em_negrito = frase.replace(achada, f"<b>{achada}</b>", 1)
            com_lacuna = frase.replace(achada, '<span class="lacuna">_____</span>', 1)
            return em_negrito, com_lacuna
    return frase, frase


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", help="pasta com vocab-master.json")
    ap.add_argument("--out", help="arquivo .apkg de saida")
    ap.add_argument("--incluir-dominadas", action="store_true",
                    help="inclui palavras marcadas como dominadas no Kindle")
    args = ap.parse_args()

    data_dir = achar_data_dir(args.data_dir)
    master = json.loads((data_dir / "vocab-master.json").read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else data_dir / "Kindle Vocabulario EN.apkg"

    deck = genanki.Deck(DECK_ID, "Ingles::Kindle Vocabulario")
    total, sem_enriquecimento, puladas = 0, 0, 0

    for stem, e in sorted(master["palavras"].items()):
        if not e.get("traducao") or not e.get("definicao"):
            sem_enriquecimento += 1
            continue
        if e.get("dominada_kindle") and not args.incluir_dominadas:
            puladas += 1
            continue
        exemplo = e["exemplos"][-1] if e["exemplos"] else None
        if exemplo:
            frase, cloze = destacar(exemplo["frase"], e.get("formas", []), stem)
            livro = exemplo["livro"]
        else:
            frase, cloze, livro = "", "", ""
        deck.add_note(VocabNote(model=MODEL, fields=[
            stem, e["traducao"], e["definicao"], frase, cloze, livro,
        ]))
        total += 1

    genanki.Package(deck).write_to_file(str(out))
    print(f"Baralho gerado: {out}")
    print(f"Palavras no baralho: {total} ({total * 2} cartoes)")
    print(f"Puladas (dominadas no Kindle): {puladas}")
    if sem_enriquecimento:
        print(f"ATENCAO: {sem_enriquecimento} palavras sem traducao/definicao ficaram de fora "
              f"- rode o enriquecimento no Claude Code antes.")


if __name__ == "__main__":
    main()
