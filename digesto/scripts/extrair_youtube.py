#!/usr/bin/env python3
"""
Extrai a transcrição de vídeos do YouTube para arquivos .txt.

Uso:  python extrair_youtube.py <pasta_de_saida> <url_ou_id> [url_ou_id ...]

Grava um .txt por vídeo, com carimbo de tempo a cada parágrafo, e imprime uma
linha de status por vídeo. O texto NÃO deve ser lido pelo agente: serve de
entrada para o delegado (Gemini ou Hermes).

Depende de youtube-transcript-api, presente no venv do Hermes:
%LOCALAPPDATA%/hermes/hermes-agent/venv/Scripts/python.exe
"""
import re
import sys
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

PREF = ["pt-BR", "pt", "en", "en-US"]
BLOCO = 55.0


def identificar(entrada):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", entrada)
    return m.group(1) if m else entrada.strip()


def carimbo(seg):
    seg = int(seg)
    h, resto = divmod(seg, 3600)
    m, s = divmod(resto, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def paragrafar(trechos):
    saida, atual, inicio = [], [], None
    for t, texto in trechos:
        if not texto:
            continue
        if inicio is None:
            inicio = t
        atual.append(texto)
        if ((t - inicio >= BLOCO and texto.endswith((".", "!", "?", ":")))
                or t - inicio >= BLOCO * 2.5):
            saida.append((inicio, " ".join(atual)))
            atual, inicio = [], None
    if atual:
        saida.append((inicio, " ".join(atual)))
    return saida


def main():
    if len(sys.argv) < 3:
        raise SystemExit("uso: python extrair_youtube.py <pasta> <url|id> [...]")
    pasta = Path(sys.argv[1])
    pasta.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()

    for entrada in sys.argv[2:]:
        vid = identificar(entrada)
        destino = pasta / f"youtube-{vid}.txt"
        try:
            dados = api.fetch(vid, languages=PREF)
            trechos = [(s.start, re.sub(r"\s+", " ", re.sub(r"^>>\s*", "", s.text)).strip())
                       for s in dados if s.text.strip()]
            paras = paragrafar(trechos)
            linhas = [f"FONTE: https://www.youtube.com/watch?v={vid}",
                      f"IDIOMA DA LEGENDA: {dados.language_code}",
                      "TIPO: transcrição automática do YouTube, pontuação aproximada",
                      ""]
            linhas += [f"[{carimbo(t)}] {texto}" for t, texto in paras]
            destino.write_text("\n\n".join(linhas), encoding="utf-8")
            palavras = sum(len(p[1].split()) for p in paras)
            print(f"OK    {vid}  {dados.language_code}  {palavras} palavras  -> {destino.name}")
        except Exception as e:
            print(f"FALHA {vid}  {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
