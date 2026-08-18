#!/usr/bin/env python3
"""
Desenha diagramas conceituais no estilo caixa-e-seta, direto em PNG.

Uso:  python diagrama.py spec.json saida.png
      python diagrama.py pasta_de_specs/ pasta_de_saida/

Formato do spec (JSON):
{
  "titulo": "Prompt engineering: voce roda o laco",
  "legenda": ["Voce e o operador do laco.", "Voce decide cada passo."],
  "moldura": true,
  "grade": {"col": 250, "lin": 150},
  "caixas": [
    {"id": "voce", "texto": "VOCE",  "col": 0, "lin": 0},
    {"id": "llm",  "texto": "LLM",   "col": 1, "lin": 0},
    {"id": "erro", "texto": "nao serviu?", "col": 1, "lin": 1},
    {"id": "fim",  "texto": "PRONTO", "col": 1, "lin": 2, "enfase": true}
  ],
  "setas": [
    {"de": "voce", "para": "llm",  "rotulo": "prompt"},
    {"de": "llm",  "para": "erro", "rotulo": "saida"},
    {"de": "erro", "para": "voce", "rotulo": "ajusta", "rota": "h"},
    {"de": "erro", "para": "fim"}
  ]
}

Campos opcionais da caixa: "largura", "altura", "enfase" (borda grossa),
"suave" (cinza claro), "x"/"y" para posicao livre em pixels.
Campos opcionais da seta: "rota" ("h" = anda na horizontal primeiro,
"v" = vertical primeiro), "tracejada", "rotulo_lado" ("acima"/"abaixo"/
"esquerda"/"direita").
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# paleta sobria, pensada para tinta eletronica: preto sobre branco
FUNDO = (255, 255, 255)
TRACO = (26, 26, 26)
TRACO_SUAVE = (140, 140, 140)
TEXTO = (17, 17, 17)
TEXTO_SUAVE = (95, 95, 95)
MOLDURA = (190, 190, 190)
PREENCHE_SUAVE = (244, 244, 244)

ESCALA = 2  # desenha no dobro e reduz no fim, para a borda sair limpa
MARGEM = 30
CAIXA_L, CAIXA_A = 155, 62
RAIO = 9


def fonte(tam, negrito=False):
    nomes = ["seguisb.ttf", "segoeui.ttf"] if negrito else ["segoeui.ttf", "arial.ttf"]
    for nome in nomes + ["arial.ttf", "arialbd.ttf"]:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{nome}", tam * ESCALA)
        except OSError:
            continue
    return ImageFont.load_default()


def medir(d, texto, fnt):
    caixa = d.textbbox((0, 0), texto, font=fnt)
    return caixa[2] - caixa[0], caixa[3] - caixa[1]


def centrar(d, texto, fnt, cx, cy, cor=TEXTO):
    l, a = medir(d, texto, fnt)
    d.text((cx - l / 2, cy - a / 2 - 2 * ESCALA), texto, font=fnt, fill=cor)


def quebrar(d, texto, fnt, largura):
    linhas, atual = [], []
    for palavra in texto.split():
        teste = " ".join(atual + [palavra])
        if medir(d, teste, fnt)[0] <= largura or not atual:
            atual.append(palavra)
        else:
            linhas.append(" ".join(atual))
            atual = [palavra]
    if atual:
        linhas.append(" ".join(atual))
    return linhas


def ancoras(cx):
    """Pontos de encaixe de uma caixa ja posicionada."""
    x, y, l, a = cx["_x"], cx["_y"], cx["_l"], cx["_a"]
    return {
        "esq": (x, y + a / 2), "dir": (x + l, y + a / 2),
        "cima": (x + l / 2, y), "baixo": (x + l / 2, y + a),
        "centro": (x + l / 2, y + a / 2),
    }


def seta_cabeca(d, ponta, direcao, cor, tam=9):
    """Triangulo cheio na ponta da seta."""
    t = tam * ESCALA
    x, y = ponta
    if direcao == "dir":
        pts = [(x, y), (x - t, y - t * 0.55), (x - t, y + t * 0.55)]
    elif direcao == "esq":
        pts = [(x, y), (x + t, y - t * 0.55), (x + t, y + t * 0.55)]
    elif direcao == "baixo":
        pts = [(x, y), (x - t * 0.55, y - t), (x + t * 0.55, y - t)]
    else:
        pts = [(x, y), (x - t * 0.55, y + t), (x + t * 0.55, y + t)]
    d.polygon(pts, fill=cor)


def rota_entre(origem, destino, preferencia):
    """Escolhe ancora de saida, ancora de chegada e o cotovelo entre elas."""
    ao, ad = ancoras(origem), ancoras(destino)
    ox, oy = ao["centro"]
    dx, dy = ad["centro"]
    horizontal = abs(dx - ox) > 1
    vertical = abs(dy - oy) > 1

    if horizontal and not vertical:
        lado_o = "dir" if dx > ox else "esq"
        lado_d = "esq" if dx > ox else "dir"
        return ao[lado_o], ad[lado_d], [], ("dir" if dx > ox else "esq")

    if vertical and not horizontal:
        lado_o = "baixo" if dy > oy else "cima"
        lado_d = "cima" if dy > oy else "baixo"
        return ao[lado_o], ad[lado_d], [], ("baixo" if dy > oy else "cima")

    # diagonal: cotovelo em L
    if preferencia == "h":
        p0 = ao["dir" if dx > ox else "esq"]
        p1 = ad["cima" if dy > oy else "baixo"]
        return p0, p1, [(p1[0], p0[1])], ("baixo" if dy > oy else "cima")
    p0 = ao["baixo" if dy > oy else "cima"]
    p1 = ad["esq" if dx > ox else "dir"]
    return p0, p1, [(p0[0], p1[1])], ("dir" if dx > ox else "esq")


def tracejar(d, a, b, cor, largura, passo=9):
    """Linha tracejada entre dois pontos (PIL nao tem dash nativo)."""
    passo *= ESCALA
    (x0, y0), (x1, y1) = a, b
    dist = max(abs(x1 - x0), abs(y1 - y0))
    if dist == 0:
        return
    n = max(1, int(dist / passo))
    for i in range(n):
        if i % 2:
            continue
        t0, t1 = i / n, min(1, (i + 1) / n)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=cor, width=largura)


def desenhar(spec, destino):
    grade = spec.get("grade", {})
    passo_col = grade.get("col", 250)
    passo_lin = grade.get("lin", 150)
    caixas = {c["id"]: dict(c) for c in spec["caixas"]}

    # posiciona
    for c in caixas.values():
        c["_l"] = c.get("largura", CAIXA_L) * ESCALA
        c["_a"] = c.get("altura", CAIXA_A) * ESCALA
        if "x" in c:
            c["_x"], c["_y"] = c["x"] * ESCALA, c["y"] * ESCALA
        else:
            centro_x = (c.get("col", 0) + 0.5) * passo_col * ESCALA
            centro_y = (c.get("lin", 0) + 0.5) * passo_lin * ESCALA
            c["_x"] = centro_x - c["_l"] / 2
            c["_y"] = centro_y - c["_a"] / 2

    # dimensoes da tela, com folga para rotulos de seta
    folga = 62 * ESCALA
    minx = min(c["_x"] for c in caixas.values()) - folga
    maxx = max(c["_x"] + c["_l"] for c in caixas.values()) + folga
    miny = min(c["_y"] for c in caixas.values()) - folga
    maxy = max(c["_y"] + c["_a"] for c in caixas.values()) + folga

    f_titulo = fonte(15)
    f_caixa = fonte(14, negrito=True)
    f_rotulo = fonte(11)
    f_legenda = fonte(12)

    topo = 52 * ESCALA if spec.get("titulo") else 18 * ESCALA
    legendas = spec.get("legenda") or []
    rodape = (26 * len(legendas) + 24) * ESCALA if legendas else 18 * ESCALA

    larg = int(maxx - minx) + 2 * MARGEM * ESCALA
    alt = int(maxy - miny) + topo + rodape + 2 * MARGEM * ESCALA

    im = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(im)

    desloc_x = MARGEM * ESCALA - minx
    desloc_y = MARGEM * ESCALA + topo - miny
    for c in caixas.values():
        c["_x"] += desloc_x
        c["_y"] += desloc_y

    if spec.get("moldura", True):
        m = 8 * ESCALA
        cantos = [(m, m), (larg - m, m), (larg - m, alt - m), (m, alt - m)]
        for i in range(4):
            tracejar(d, cantos[i], cantos[(i + 1) % 4], MOLDURA, 2 * ESCALA, passo=11)

    if spec.get("titulo"):
        centrar(d, spec["titulo"], f_titulo, larg / 2, MARGEM * ESCALA + 14 * ESCALA)

    # setas primeiro, para a caixa cobrir a ponta que encostar
    for s in spec.get("setas", []):
        cx_de, cx_para = caixas[s["de"]], caixas[s["para"]]
        p0, p1, meio, direcao = rota_entre(cx_de, cx_para, s.get("rota", "v"))
        pontos = [p0] + meio + [p1]
        cor = TRACO_SUAVE if s.get("suave") else TRACO
        for i in range(len(pontos) - 1):
            if s.get("tracejada"):
                tracejar(d, pontos[i], pontos[i + 1], cor, 2 * ESCALA)
            else:
                d.line([pontos[i], pontos[i + 1]], fill=cor, width=2 * ESCALA)
        seta_cabeca(d, p1, direcao, cor)

        if s.get("rotulo"):
            a, b = pontos[0], pontos[1]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            l, _ = medir(d, s["rotulo"], f_rotulo)
            lado = s.get("rotulo_lado")
            if abs(b[1] - a[1]) < 1:  # segmento horizontal
                pos = (mx, my - 13 * ESCALA) if lado != "abaixo" else (mx, my + 13 * ESCALA)
            else:  # segmento vertical
                dx = l / 2 + 10 * ESCALA
                pos = (mx - dx, my) if lado == "esquerda" else (mx + dx, my)
            d.rectangle([pos[0] - l / 2 - 3 * ESCALA, pos[1] - 9 * ESCALA,
                         pos[0] + l / 2 + 3 * ESCALA, pos[1] + 9 * ESCALA], fill=FUNDO)
            centrar(d, s["rotulo"], f_rotulo, pos[0], pos[1], TEXTO_SUAVE)

    for c in caixas.values():
        x, y, l, a = c["_x"], c["_y"], c["_l"], c["_a"]
        d.rounded_rectangle(
            [x, y, x + l, y + a], radius=RAIO * ESCALA,
            fill=PREENCHE_SUAVE if c.get("suave") else FUNDO,
            outline=TRACO, width=(3 if c.get("enfase") else 2) * ESCALA,
        )
        linhas = quebrar(d, c["texto"], f_caixa, l - 16 * ESCALA)
        alt_linha = 19 * ESCALA
        y0 = y + a / 2 - (len(linhas) - 1) * alt_linha / 2
        for i, linha in enumerate(linhas):
            centrar(d, linha, f_caixa, x + l / 2, y0 + i * alt_linha)

    if legendas:
        y = alt - MARGEM * ESCALA - rodape + 16 * ESCALA
        for linha in legendas:
            centrar(d, linha, f_legenda, larg / 2, y, TEXTO_SUAVE)
            y += 26 * ESCALA

    im = im.resize((larg // ESCALA, alt // ESCALA), Image.LANCZOS)
    im.save(destino, "PNG", optimize=True)
    return im.size


def main():
    if len(sys.argv) < 3:
        raise SystemExit("uso: python diagrama.py <spec.json|pasta> <saida.png|pasta>")
    origem, saida = Path(sys.argv[1]), Path(sys.argv[2])

    if origem.is_dir():
        saida.mkdir(parents=True, exist_ok=True)
        for spec in sorted(origem.glob("*.json")):
            tam = desenhar(json.loads(spec.read_text(encoding="utf-8")),
                           saida / f"{spec.stem}.png")
            print(f"{spec.stem}.png  {tam[0]}x{tam[1]}")
    else:
        tam = desenhar(json.loads(origem.read_text(encoding="utf-8")), saida)
        print(f"{saida.name}  {tam[0]}x{tam[1]}")


if __name__ == "__main__":
    main()
