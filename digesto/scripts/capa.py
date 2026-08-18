#!/usr/bin/env python3
"""
Desenha a capa da edição, no mesmo vocabulário visual dos diagramas.

Uso:  python capa.py capa.json capa.png

capa.json:
{
  "titulo": "Digesto",
  "subtitulo": "Claude Code, agentes e o que fazer com isso",
  "data": "15 de agosto de 2026",
  "fontes": ["Claude Code Masterclass", "All Agents Considered", "GitHub"],
  "selo": "6 fontes · 3 usos imediatos"
}
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

L, A = 1400, 2100
FUNDO = (255, 255, 255)
TINTA = (20, 20, 20)
SUAVE = (120, 120, 120)
REGUA = (200, 200, 200)
DESTAQUE = (200, 74, 20)


def fonte(nome, tam):
    for cand in (nome, "georgia.ttf", "segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{cand}", tam)
        except OSError:
            continue
    return ImageFont.load_default()


def quebrar(d, texto, fnt, largura):
    linhas, atual = [], []
    for palavra in texto.split():
        teste = " ".join(atual + [palavra])
        if d.textlength(teste, font=fnt) <= largura or not atual:
            atual.append(palavra)
        else:
            linhas.append(" ".join(atual))
            atual = [palavra]
    if atual:
        linhas.append(" ".join(atual))
    return linhas


def motivo(d, cx, base):
    """Pequeno caixa-e-seta, a assinatura visual da edição."""
    lc, ac, vao = 150, 58, 82
    largura_total = 3 * lc + 2 * vao
    xs = [cx - largura_total / 2 + i * (lc + vao) for i in range(3)]
    for i, x in enumerate(xs):
        d.rounded_rectangle([x, base, x + lc, base + ac], radius=9,
                            outline=TINTA, width=3 if i == 2 else 2)
    y = base + ac / 2
    for i in range(2):
        x0, x1 = xs[i] + lc, xs[i + 1]
        d.line([(x0, y), (x1 - 10, y)], fill=TINTA, width=2)
        d.polygon([(x1, y), (x1 - 12, y - 6), (x1 - 12, y + 6)], fill=TINTA)


def main():
    if len(sys.argv) < 3:
        raise SystemExit("uso: python capa.py <capa.json> <saida.png>")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    im = Image.new("RGB", (L, A), FUNDO)
    d = ImageDraw.Draw(im)

    f_titulo = fonte("georgiab.ttf", 150)
    f_sub = fonte("georgiai.ttf", 54)
    f_texto = fonte("georgia.ttf", 40)
    f_selo = fonte("seguisb.ttf", 36)

    m = 120
    d.line([(m, 300), (m + 190, 300)], fill=DESTAQUE, width=10)

    y = 380
    for linha in quebrar(d, spec["titulo"], f_titulo, L - 2 * m):
        d.text((m, y), linha, font=f_titulo, fill=TINTA)
        y += 172

    y += 24
    for linha in quebrar(d, spec.get("subtitulo", ""), f_sub, L - 2 * m):
        d.text((m, y), linha, font=f_sub, fill=SUAVE)
        y += 76

    if spec.get("selo"):
        y += 40
        d.text((m, y), spec["selo"], font=f_selo, fill=DESTAQUE)
        y += 70

    y += 40
    d.line([(m, y), (L - m, y)], fill=REGUA, width=3)
    y += 46
    for f in spec.get("fontes", []):
        d.text((m, y), f"· {f}", font=f_texto, fill=SUAVE)
        y += 60

    motivo(d, L / 2, A - 560)

    if spec.get("data"):
        d.text((m, A - 190), spec["data"], font=f_texto, fill=SUAVE)

    im.save(sys.argv[2], "PNG", optimize=True)
    print(f"{Path(sys.argv[2]).name}  {L}x{A}")


if __name__ == "__main__":
    main()
