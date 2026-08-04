# -*- coding: utf-8 -*-
"""Melhora a voz do vídeo: remove graves de ambiente, de-esser, compressão,
realce de presença (clareza de dicção) e normalização de volume.

O vídeo não é reencodado (c:v copy); só o áudio é processado.

Uso:
    python melhorar_audio.py video.mp4 [--saida video_voz.mp4] [--presenca 3]
"""
import argparse
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--saida", default=None)
    ap.add_argument("--presenca", type=float, default=3.0,
                    help="ganho em dB na faixa de 2-4 kHz (clareza de consoantes); padrão 3")
    args = ap.parse_args()

    video = Path(args.video)
    saida = Path(args.saida) if args.saida else video.with_name(video.stem + "_voz" + video.suffix)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    cadeia = ",".join([
        "highpass=f=75",                                   # tira ronco de ambiente/mesa
        "deesser=i=0.3",                                   # suaviza sibilância ("s" estourado)
        f"equalizer=f=3000:t=q:w=1.2:g={args.presenca}",   # presença: consoantes mais nítidas
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=120:makeup=4dB",
        "loudnorm=I=-16:TP=-1.5:LRA=11",                   # volume padrão de redes sociais
    ])
    cmd = [
        ffmpeg, "-y", "-i", str(video),
        "-af", cadeia,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(saida),
    ]
    print("Processando áudio...")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"ERRO ffmpeg:\n{r.stderr[-2000:]}")
    print(f"OK -> {saida}")


if __name__ == "__main__":
    main()
