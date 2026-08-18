#!/usr/bin/env python3
"""
Baixa páginas e grava o texto em .txt, sem passar o conteúdo pelo agente.

Uso:  python extrair_web.py <pasta_de_saida> <url> [url ...]

Imprime uma linha de status por URL (palavras colhidas e arquivo gerado). Se a
contagem vier baixa demais para o tipo de página, suspeite de paywall ou de
conteúdo montado por javascript e caia para a extração pelo Chrome logado.

Trata github.com/<user>/<repo> como caso especial: busca o README pelo raw.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"}
IGNORAR = {"script", "style", "noscript", "svg", "head", "nav", "footer", "form"}
BLOCO = {"p", "div", "section", "article", "li", "tr", "br", "h1", "h2", "h3",
         "h4", "h5", "h6", "pre", "blockquote", "figcaption"}


class Texto(HTMLParser):
    def __init__(self):
        super().__init__()
        self.partes = []
        self.pular = 0

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self.pular += 1
        elif tag in BLOCO:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORAR and self.pular:
            self.pular -= 1
        elif tag in BLOCO:
            self.partes.append("\n")

    def handle_data(self, dado):
        if not self.pular:
            self.partes.append(dado)

    def resultado(self):
        bruto = "".join(self.partes)
        bruto = re.sub(r"[ \t ]+", " ", bruto)
        linhas = [l.strip() for l in bruto.split("\n")]
        return "\n".join(l for l in linhas if l)


def apelido(url):
    corte = re.sub(r"^https?://", "", url).rstrip("/")
    corte = re.sub(r"\?.*$", "", corte)
    return re.sub(r"[^a-z0-9]+", "-", corte.lower()).strip("-")[:70]


def github(url):
    """Para repositórios, o README costuma valer mais que a página renderizada."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/?#]+)", url)
    if not m:
        return None
    usuario, repo = m.group(1), m.group(2)
    for ramo in ("main", "master"):
        for nome in ("README.md", "readme.md", "README.MD"):
            bruto = f"https://raw.githubusercontent.com/{usuario}/{repo}/{ramo}/{nome}"
            r = requests.get(bruto, headers=UA, timeout=30)
            if r.status_code == 200 and r.text.strip():
                return f"FONTE: {url}\nARQUIVO: {nome} (ramo {ramo})\n\n{r.text}"
    return None


def main():
    if len(sys.argv) < 3:
        raise SystemExit("uso: python extrair_web.py <pasta> <url> [...]")
    pasta = Path(sys.argv[1])
    pasta.mkdir(parents=True, exist_ok=True)

    for url in sys.argv[2:]:
        destino = pasta / f"{apelido(url)}.txt"
        try:
            conteudo = github(url) if "github.com/" in url else None
            if conteudo is None:
                r = requests.get(url, headers=UA, timeout=45)
                r.raise_for_status()
                p = Texto()
                p.feed(r.text)
                conteudo = f"FONTE: {url}\n\n{p.resultado()}"
            destino.write_text(conteudo, encoding="utf-8")
            print(f"OK    {len(conteudo.split()):>6} palavras  -> {destino.name}")
        except Exception as e:
            print(f"FALHA {type(e).__name__}: {e}  ({url})")


if __name__ == "__main__":
    main()
