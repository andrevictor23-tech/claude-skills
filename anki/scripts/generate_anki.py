# -*- coding: utf-8 -*-
"""Gera o baralho Anki (.apkg) a partir do anki-master.json — skill `anki`.

Um cartao por lacuna (pergunta -> resposta + fundamento + fonte), em subbaralhos
por disciplina: `Concurso::Penal`, `Concurso::Processo Penal`, ...

GUIDs estaveis por id da lacuna: reimportar o .apkg ATUALIZA os cartoes existentes
sem duplicar e sem perder o agendamento da repeticao espacada.

Uso:
  python generate_anki.py --base "<pasta de estudos>" [--out <arquivo.apkg>]
                          [--disciplina Penal] [--link-local]

Requer: pip install genanki
"""

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import genanki
except ImportError:
    sys.exit("ERRO: rode 'python -m pip install genanki' primeiro.")

# IDs fixos: NUNCA mudar, senao o Anki duplica o baralho inteiro.
MODEL_ID = 1748392051

# Ordem congelada — o id de cada subbaralho e' DECK_BASE + indice nesta tupla.
# So acrescente disciplinas NO FIM; reordenar troca os ids e duplica baralhos.
DECK_BASE = 1892740150
DISCIPLINAS = (
    "Penal",
    "Tutela Coletiva",
    "Constitucional",
    "Processo Penal",
    "Civil",
    "Processo Civil",
    "Administrativo",
    "Infância e Juventude",
    "Empresarial",
    "Direitos Humanos",
    "Eleitoral",
    "Institucional",
    "Outras",
)

CSS = """
.card { font-family: 'Segoe UI', sans-serif; font-size: 19px; text-align: left;
        color: #1a2332; background-color: #f7f4ee; padding: 14px; }
.disciplina { font-size: 12px; letter-spacing: 1px; text-transform: uppercase;
              color: #8a6d1f; margin-bottom: 10px; }
.pergunta { font-size: 21px; line-height: 1.45; font-weight: 600; }
.resposta { font-size: 20px; line-height: 1.45; color: #2d6a4f; font-weight: 600;
            margin-top: 12px; }
.extra { font-size: 16px; line-height: 1.5; color: #444; margin-top: 10px; }
.fonte { font-size: 12px; color: #6b7280; margin-top: 18px;
         font-family: Consolas, monospace; }
.fonte a { color: #6b7280; }
hr#answer { border: none; border-top: 2px solid #d9d2c4; margin: 14px 0; }
.nightMode .card { color: #e8e4da; background-color: #1a2332; }
.nightMode .resposta { color: #7fc8a4; }
.nightMode .extra { color: #b8b2a4; }
.nightMode .disciplina { color: #d4b458; }
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Concurso — Lacunas (anki)",
    fields=[
        {"name": "Pergunta"},
        {"name": "Resposta"},
        {"name": "Extra"},
        {"name": "Disciplina"},
        {"name": "Fonte"},
    ],
    templates=[
        {
            "name": "Recall (pergunta -> fundamento)",
            "qfmt": '<div class="disciplina">{{Disciplina}}</div>'
                    '<div class="pergunta">{{Pergunta}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">'
                    '<div class="resposta">{{Resposta}}</div>'
                    '{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}'
                    '<div class="fonte">{{Fonte}}</div>',
        },
    ],
    css=CSS,
)


class LacunaNote(genanki.Note):
    def __init__(self, *a, lacuna_id="", **kw):
        super().__init__(*a, **kw)
        self._lacuna_id = lacuna_id

    @property
    def guid(self):
        # estavel por lacuna: reimportar atualiza em vez de duplicar
        return genanki.guid_for("anki-estudos::" + self._lacuna_id)


def _slug(texto):
    s = unicodedata.normalize("NFKD", texto or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def monta_fonte(e, base, link_local):
    """Rodape do cartao: origem do erro + nota da wiki para revisar."""
    partes = []
    if e.get("fonte"):
        partes.append(html.escape(e["fonte"]))
    nota = e.get("nota_wiki")
    if nota:
        if link_local:
            caminho = (base / "wiki" / "disciplinas" / nota).resolve()
            href = caminho.as_uri()
            partes.append(f'<a href="{html.escape(href)}">{html.escape(nota)}</a>')
        else:
            partes.append(f"revisar em wiki/disciplinas/{html.escape(nota)}")
    return " · ".join(partes)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=".", help="pasta que contém quiz-data\\")
    ap.add_argument("--out", default=None, help="arquivo .apkg de saída")
    ap.add_argument("--disciplina", default=None,
                    help="gera só uma disciplina (padrão: todas)")
    ap.add_argument("--link-local", action="store_true",
                    help="põe link file:// para a nota da wiki (só funciona no PC)")
    args = ap.parse_args()

    base = Path(args.base)
    master_path = base / "quiz-data" / "anki-master.json"
    if not master_path.exists():
        sys.exit(f"ERRO: {master_path} não existe — rode coletar_lacunas.py antes.")
    master = json.loads(master_path.read_text(encoding="utf-8"))

    decks = {nome: genanki.Deck(DECK_BASE + i, f"Concurso::{nome}")
             for i, nome in enumerate(DISCIPLINAS)}

    total, sem_cartao, descartadas, por_disc = 0, 0, 0, {}
    for lid, e in sorted(master.get("lacunas", {}).items()):
        if e.get("status") != "ativo":
            descartadas += 1
            continue
        disc = e.get("disciplina") or "Outras"
        if args.disciplina and _slug(disc) != _slug(args.disciplina):
            continue
        if not e.get("pergunta") or not e.get("resposta"):
            sem_cartao += 1
            continue
        deck = decks.get(disc) or decks["Outras"]
        tags = [_slug(disc), e.get("origem") or "quiz"]
        if e.get("quiz"):
            tags.append("quiz::" + _slug(e["quiz"]))
        deck.add_note(LacunaNote(
            model=MODEL,
            lacuna_id=lid,
            fields=[
                e["pergunta"],
                e["resposta"],
                e.get("extra") or "",
                disc,
                monta_fonte(e, base, args.link_local),
            ],
            tags=[t for t in tags if t],
        ))
        total += 1
        por_disc[disc] = por_disc.get(disc, 0) + 1

    if not total:
        sys.exit("ERRO: nenhuma lacuna com cartão escrito — rode o passo 2 "
                 "(Claude escreve pergunta/resposta) antes de gerar.")

    out = Path(args.out) if args.out else base / "quiz-data" / "Concurso - Lacunas.apkg"
    genanki.Package([d for d in decks.values() if d.notes]).write_to_file(str(out))

    print(f"Baralho gerado: {out}")
    print(f"Cartões: {total}")
    for disc in sorted(por_disc, key=lambda d: -por_disc[d]):
        print(f"  Concurso::{disc}: {por_disc[disc]}")
    if sem_cartao:
        print(f"Lacunas sem cartão escrito (ficaram de fora): {sem_cartao}")
    if descartadas:
        print(f"Lacunas descartadas pelo usuário: {descartadas}")


if __name__ == "__main__":
    main()
