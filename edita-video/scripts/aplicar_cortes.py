# -*- coding: utf-8 -*-
"""Aplica a lista de cortes ao vídeo, removendo os trechos marcados.

Usa o ffmpeg embutido do imageio-ffmpeg (sem depender de ffmpeg no PATH).

Uso:
    python aplicar_cortes.py video.mp4 video.transcricao.cortes.json [--saida video_cortado.mp4]
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("cortes", help="JSON gerado por detectar_cortes.py")
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()

    video = Path(args.video)
    dados = json.loads(Path(args.cortes).read_text(encoding="utf-8"))
    cortes = dados["cortes"]
    saida = Path(args.saida) if args.saida else video.with_name(video.stem + "_sem-muletas" + video.suffix)

    if not cortes:
        print("Nenhum corte a aplicar; nada foi feito.")
        return

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    expr = "+".join(f"between(t,{c['ini']},{c['fim']})" for c in cortes)
    filtro = (
        f"[0:v]select='not({expr})',setpts=N/FRAME_RATE/TB[v];"
        f"[0:a]aselect='not({expr})',asetpts=N/SR/TB[a]"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(filtro)
        script = f.name

    cmd = [
        ffmpeg, "-y", "-i", str(video),
        "-filter_complex_script", script,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        str(saida),
    ]
    print(f"Removendo {len(cortes)} trechos ({sum(c['fim']-c['ini'] for c in cortes):.1f}s)...")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"ERRO ffmpeg:\n{r.stderr[-2000:]}")
    print(f"OK -> {saida}")


if __name__ == "__main__":
    main()
