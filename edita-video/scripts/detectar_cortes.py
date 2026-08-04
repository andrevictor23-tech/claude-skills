# -*- coding: utf-8 -*-
"""Detecta muletas verbais ("né", "hã", "hum"...) na transcrição e gera a lista de cortes.

Gera dois arquivos: cortes.json (para aplicar_cortes.py) e cortes.txt (revisão humana).

Uso:
    python detectar_cortes.py transcricao.json [--muletas "né,hã,hum"] [--pad 0.04]
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Muletas cortadas por padrão quando aparecem como palavra isolada.
MULETAS_PADRAO = ["né", "hã", "ham", "hum", "uhm", "ãh", "ãhn", "ãã", "hem", "hein"]
# Padrões de hesitação alongada (é..., aa..., ee...) — sempre cortados.
PADROES_HESITACAO = [
    re.compile(r"^é{2,}$"),
    re.compile(r"^a{2,}$"),
    re.compile(r"^e{2,}$"),
    re.compile(r"^h[ãaâ]+m*$"),
    re.compile(r"^hu+m+$"),   # hum, humm ("um" sozinho é artigo — não cortar)
    re.compile(r"^u+h?m{2,}$"),  # umm, uhmm
    re.compile(r"^ã+h?n?$"),
    re.compile(r"^né+$"),
]

PONTUACAO = re.compile(r"[.,;:!?…—\-\"'()\[\]]+")


def normalizar(palavra: str) -> str:
    return PONTUACAO.sub("", palavra).strip().lower()


def eh_muleta(norm: str, muletas: set) -> bool:
    if not norm:
        return False
    if norm in muletas:
        return True
    return any(p.match(norm) for p in PADROES_HESITACAO)


def fmt_ts(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("transcricao", help="JSON gerado por transcrever.py")
    ap.add_argument("--muletas", default=None, help="lista separada por vírgula (substitui a padrão)")
    ap.add_argument("--pad", type=float, default=0.04, help="folga em segundos de cada lado do corte")
    args = ap.parse_args()

    caminho = Path(args.transcricao)
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    palavras = dados["palavras"]
    if args.muletas is not None:
        muletas = {m.strip().lower() for m in args.muletas.split(",") if m.strip()}
    else:
        muletas = set(MULETAS_PADRAO)

    cortes = []
    linhas = []
    for i, p in enumerate(palavras):
        norm = normalizar(p["w"])
        if not eh_muleta(norm, muletas):
            continue
        ini = max(0.0, p["ini"] - args.pad)
        fim = min(dados["duracao"], p["fim"] + args.pad)
        contexto_antes = " ".join(x["w"] for x in palavras[max(0, i - 3):i])
        contexto_depois = " ".join(x["w"] for x in palavras[i + 1:i + 4])
        cortes.append({"ini": round(ini, 3), "fim": round(fim, 3), "palavra": p["w"]})
        linhas.append(f"{fmt_ts(p['ini'])}  [{p['w']}]  ...{contexto_antes} (({p['w']})) {contexto_depois}...")

    # Funde cortes sobrepostos ou quase colados (<120 ms de distância).
    cortes.sort(key=lambda c: c["ini"])
    fundidos = []
    for c in cortes:
        if fundidos and c["ini"] - fundidos[-1]["fim"] < 0.12:
            fundidos[-1]["fim"] = max(fundidos[-1]["fim"], c["fim"])
            fundidos[-1]["palavra"] += " + " + c["palavra"]
        else:
            fundidos.append(dict(c))

    total = sum(c["fim"] - c["ini"] for c in fundidos)
    saida_json = caminho.with_name(caminho.stem + ".cortes.json")
    saida_txt = caminho.with_name(caminho.stem + ".cortes.txt")
    saida_json.write_text(
        json.dumps({"origem": dados["arquivo"], "duracao": dados["duracao"], "cortes": fundidos},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    cabecalho = [
        f"Arquivo: {dados['arquivo']}",
        f"Muletas detectadas: {len(cortes)} ({len(fundidos)} cortes após fusão) — {total:.1f}s removidos",
        "Revise abaixo; para ignorar um corte, apague a entrada correspondente no .cortes.json.",
        "",
    ]
    saida_txt.write_text("\n".join(cabecalho + linhas) + "\n", encoding="utf-8")

    print("\n".join(cabecalho + linhas))
    print(f"\nOK -> {saida_json}\n      {saida_txt}")


if __name__ == "__main__":
    main()
