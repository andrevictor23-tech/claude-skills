# -*- coding: utf-8 -*-
"""Transcreve um vídeo/áudio com timestamps por palavra usando faster-whisper.

Uso:
    python transcrever.py entrada.mp4 [--saida transcricao.json] [--modelo large-v3] [--device cpu]
"""
import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", help="arquivo de vídeo ou áudio")
    ap.add_argument("--saida", default=None, help="JSON de saída (padrão: <entrada>.transcricao.json)")
    ap.add_argument("--modelo", default="large-v3", help="small | medium | large-v3 (padrão large-v3)")
    ap.add_argument("--device", default="cpu", help="cpu | cuda | auto")
    ap.add_argument("--idioma", default="pt")
    args = ap.parse_args()

    entrada = Path(args.entrada)
    if not entrada.exists():
        sys.exit(f"ERRO: arquivo não encontrado: {entrada}")
    saida = Path(args.saida) if args.saida else entrada.with_suffix(entrada.suffix + ".transcricao.json")

    from faster_whisper import WhisperModel

    compute = "int8" if args.device == "cpu" else "auto"
    print(f"Carregando modelo {args.modelo} ({args.device}/{compute})...")
    model = WhisperModel(args.modelo, device=args.device, compute_type=compute)

    print(f"Transcrevendo {entrada.name}...")
    segments, info = model.transcribe(
        str(entrada),
        language=args.idioma,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 300},
    )

    palavras = []
    texto = []
    for seg in segments:
        texto.append(seg.text)
        for w in seg.words or []:
            palavras.append({"w": w.word.strip(), "ini": round(w.start, 3), "fim": round(w.end, 3)})
        print(f"  [{seg.start:7.2f}s] {seg.text.strip()}")

    dados = {
        "arquivo": str(entrada),
        "duracao": round(info.duration, 3),
        "idioma": info.language,
        "modelo": args.modelo,
        "texto": "".join(texto).strip(),
        "palavras": palavras,
    }
    saida.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nOK: {len(palavras)} palavras, {info.duration:.1f}s -> {saida}")


if __name__ == "__main__":
    main()
