#!/usr/bin/env python3
"""
Monta o EPUB de uma edição do digesto a partir de edicao.json.

Uso:  python montar_epub.py edicao.json
Saída: o .epub indicado em "arquivo", ao lado do JSON.

Cada capítulo herda o conteúdo do JSON que o delegado produziu em digestao/, e
só precisa declarar o que muda. Não copie resumo, pontos nem ações para cá: eles
já estão digeridos, e reescrevê-los custa token à toa.

edicao.json:
{
  "titulo": "...", "subtitulo": "...", "data": "2026-08-15",
  "arquivo": "Digesto-2026-08-15.epub",
  "img": "img",                      // pasta das imagens, relativa ao JSON
  "digestao": "digestao",            // pasta dos JSON do delegado
  "capa": "capa.png",                // opcional
  "abertura": "markdown",
  "fechamento": "markdown",
  "capitulos": [
    {
      "fonte": "<nome do arquivo em digestao/, sem .json>",
      "url": "...", "tipo": "artigo|repositório|vídeo|fonte",
      "imagens": [{"arquivo": "diag-01.png", "legenda": "..."}]
      // qualquer outro campo aqui SOBRESCREVE o do delegado. Use só quando a
      // redação dele não servir: "titulo", "veredito_frase", "resumo",
      // "pontos", "acoes", "ressalva".
    }
  ]
}

Capítulo sem "fonte" continua funcionando com todos os campos escritos à mão.
"""
import html
import json
import sys
import zipfile
from pathlib import Path

import markdown

CORES = {
    "USO IMEDIATO": ("#1b5e20", "#e8f5e9"),
    "IDEIA NOVA": ("#e65100", "#fff3e0"),
    "DESCARTE": ("#616161", "#f0f0f0"),
}

CSS = """
body { font-family: serif; line-height: 1.55; margin: 0 4%; text-align: justify; }
h1 { font-size: 1.45em; margin: 1em 0 .2em; text-align: left; line-height: 1.28; }
h2 { font-size: 1.16em; margin: 1.5em 0 .5em; text-align: left;
     border-bottom: 1px solid #bbb; padding-bottom: .18em; }
p { margin: 0 0 .7em; }
ul, ol { margin: .5em 0 .9em 1.1em; }
li { margin-bottom: .45em; }
hr { border: 0; border-top: 1px solid #ccc; margin: 1.4em 0; }
img { max-width: 100%; height: auto; }
.capa { margin: 0; padding: 0; text-align: center; }
.figura { text-align: center; margin: 1.3em 0; page-break-inside: avoid; }
.legenda { font-size: .78em; color: #666; font-style: italic; text-align: center;
           margin: .3em 0 0; }
.ficha { font-size: .85em; color: #444; margin: .2em 0 1em; text-align: left; }
.marca { font-size: .82em; color: #777; }
.veredito { border-left: 5px solid #888; padding: .5em .8em; margin: 1em 0 1.2em; }
.veredito .rotulo { font-weight: bold; font-size: .8em; letter-spacing: .06em;
                    display: block; margin-bottom: .25em; }
.ressalva { font-size: .9em; background: #f2f2f2; border-left: 4px solid #999;
            padding: .55em .8em; margin: 1.2em 0; }
.painel { margin: 1em 0; }
.painel li { margin-bottom: .7em; }
.painel .sel { font-weight: bold; font-size: .82em; letter-spacing: .05em; }
"""

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf"
    media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""


def md(texto):
    return markdown.markdown(texto or "", extensions=["tables", "sane_lists"])


def solto(texto):
    """Markdown de uma linha, sem o <p> em volta."""
    saida = md(texto)
    return saida[3:-4] if saida.startswith("<p>") and saida.endswith("</p>") else saida


def pagina(titulo, corpo):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pt-BR" lang="pt-BR">
<head><meta charset="utf-8"/><title>{html.escape(titulo)}</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>{corpo}</body></html>
"""


def figura(arquivo, legenda):
    alt = html.escape(legenda or "")
    return (f'<div class="figura"><img src="img/{arquivo}" alt="{alt}"/>'
            + (f'<p class="legenda">{alt}</p>' if legenda else "") + "</div>")


def bloco_veredito(cap):
    cor, fundo = CORES.get(cap.get("veredito", ""), ("#888", "#f0f0f0"))
    return (f'<div class="veredito" style="border-color:{cor};background:{fundo}">'
            f'<span class="rotulo" style="color:{cor}">'
            f'{html.escape(cap.get("veredito", ""))}</span>'
            f'{solto(cap.get("veredito_frase", ""))}</div>')


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python montar_epub.py <edicao.json>")
    fonte = Path(sys.argv[1]).resolve()
    ed = json.loads(fonte.read_text(encoding="utf-8"))
    base = fonte.parent
    pasta_img = base / ed.get("img", "img")
    pasta_dig = base / ed.get("digestao", "digestao")
    destino = base / ed.get("arquivo", "digesto.epub")

    # cada capítulo herda a digestão do delegado; o que estiver no edicao.json manda
    capitulos = []
    for cap in ed["capitulos"]:
        if cap.get("fonte"):
            origem = pasta_dig / f"{cap['fonte']}.json"
            if not origem.exists():
                raise SystemExit(f"digestão não encontrada: {origem}")
            base_cap = json.loads(origem.read_text(encoding="utf-8"))
            base_cap = {k: v for k, v in base_cap.items() if not k.startswith("_")}
            base_cap.pop("diagramas", None)  # é insumo do desenho, não vai para o texto
            base_cap.update({k: v for k, v in cap.items() if k != "fonte"})
            capitulos.append(base_cap)
        else:
            capitulos.append(cap)
    ed["capitulos"] = capitulos

    ident = f"urn:uuid:digesto-{ed.get('data', 'sem-data')}"
    arquivos, secoes = {}, []

    if ed.get("capa") and (pasta_img / ed["capa"]).exists():
        arquivos["capa.xhtml"] = pagina(
            "Capa", f'<div class="capa"><img src="img/{ed["capa"]}" alt="Capa"/></div>')

    # abertura, com o painel de triagem
    corpo = f'<h1>{html.escape(ed["titulo"])}</h1>'
    if ed.get("subtitulo"):
        corpo += f'<p class="marca">{html.escape(ed["subtitulo"])}</p>'
    corpo += "<hr/>" + md(ed.get("abertura", ""))
    corpo += "<h2>Painel de triagem</h2><ol class=\"painel\">"
    for i, cap in enumerate(ed["capitulos"], 1):
        cor = CORES.get(cap.get("veredito", ""), ("#888", ""))[0]
        corpo += (f'<li><span class="sel" style="color:{cor}">'
                  f'{html.escape(cap.get("veredito", ""))}</span><br/>'
                  f'<a href="cap{i:02d}.xhtml">{html.escape(cap["titulo"])}</a><br/>'
                  f'<span class="marca">{html.escape(cap.get("autor", ""))}'
                  f'{" · " + html.escape(cap["tipo"]) if cap.get("tipo") else ""}</span>'
                  f'<br/>{solto(cap.get("veredito_frase", ""))}</li>')
    corpo += "</ol>"
    arquivos["abertura.xhtml"] = pagina("Abertura", corpo)
    secoes.append(("abertura.xhtml", "Abertura e painel de triagem"))

    for i, cap in enumerate(ed["capitulos"], 1):
        nome = f"cap{i:02d}.xhtml"
        c = f'<h1>{i}. {html.escape(cap["titulo"])}</h1>'
        ficha = " · ".join(filter(None, [cap.get("autor"), cap.get("data"), cap.get("tipo")]))
        if ficha:
            c += f'<p class="ficha">{html.escape(ficha)}<br/>{html.escape(cap.get("url", ""))}</p>'
        c += bloco_veredito(cap)
        if cap.get("resumo"):
            c += "<h2>O que entrega</h2>" + md(cap["resumo"])

        imagens = list(cap.get("imagens", []))
        if imagens:
            im = imagens.pop(0)
            c += figura(im["arquivo"], im.get("legenda", ""))

        if cap.get("pontos"):
            c += "<h2>Pontos de atenção</h2><ul>"
            for p in cap["pontos"]:
                c += f"<li>{solto(p)}</li>"
            c += "</ul>"

        for im in imagens:
            c += figura(im["arquivo"], im.get("legenda", ""))

        if cap.get("acoes"):
            c += "<h2>O que dá para fazer com isso</h2><ul>"
            for a in cap["acoes"]:
                c += f"<li>{solto(a)}</li>"
            c += "</ul>"

        if cap.get("ressalva"):
            c += f'<div class="ressalva"><strong>Ressalva.</strong> {solto(cap["ressalva"])}</div>'

        arquivos[nome] = pagina(cap["titulo"], c)
        secoes.append((nome, f'{i}. {cap["titulo"]}'))

    if ed.get("fechamento"):
        arquivos["fechamento.xhtml"] = pagina("Notas finais", md(ed["fechamento"]))
        secoes.append(("fechamento.xhtml", "Notas finais"))

    itens = "".join(f'<li><a href="{a}">{html.escape(r)}</a></li>' for a, r in secoes)
    arquivos["nav.xhtml"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="pt-BR" lang="pt-BR">
<head><meta charset="utf-8"/><title>Sumário</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body><nav epub:type="toc" id="toc"><h1>Sumário</h1><ol>{itens}</ol></nav></body></html>
"""

    pontos = "".join(
        f'<navPoint id="np{n}" playOrder="{n}"><navLabel><text>{html.escape(r)}</text>'
        f'</navLabel><content src="{a}"/></navPoint>'
        for n, (a, r) in enumerate(secoes, 1))
    arquivos["toc.ncx"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{ident}"/></head>
<docTitle><text>{html.escape(ed["titulo"])}</text></docTitle>
<navMap>{pontos}</navMap></ncx>
"""

    imagens = sorted(p for p in pasta_img.iterdir()
                     if p.suffix.lower() in (".png", ".jpg", ".jpeg")) \
        if pasta_img.is_dir() else []
    man_img = ""
    for n, p in enumerate(imagens, 1):
        tipo = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        extra = ' properties="cover-image"' if p.name == ed.get("capa") else ""
        man_img += f'    <item id="img{n}" href="img/{p.name}" media-type="{tipo}"{extra}/>\n'

    man_sec = "".join(
        f'    <item id="s{n}" href="{a}" media-type="application/xhtml+xml"/>\n'
        for n, (a, _) in enumerate(secoes, 1))
    espinha = "".join(f'<itemref idref="s{n}"/>' for n in range(1, len(secoes) + 1))
    capa_item = ('    <item id="capa" href="capa.xhtml" media-type="application/xhtml+xml"/>\n'
                 if "capa.xhtml" in arquivos else "")
    capa_ref = '<itemref idref="capa"/>' if "capa.xhtml" in arquivos else ""

    arquivos["content.opf"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{ident}</dc:identifier>
    <dc:title>{html.escape(ed["titulo"])}</dc:title>
    <dc:creator>{html.escape(ed.get("autor", "Digesto"))}</dc:creator>
    <dc:language>pt-BR</dc:language>
    <dc:date>{ed.get("data", "")}</dc:date>
    <meta property="dcterms:modified">{ed.get("data", "2026-01-01")}T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="style.css" media-type="text/css"/>
{capa_item}{man_sec}{man_img}  </manifest>
  <spine toc="ncx">{capa_ref}<itemref idref="nav"/>{espinha}</spine>
</package>
"""

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", CONTAINER)
        z.writestr("OEBPS/style.css", CSS)
        for nome, conteudo in arquivos.items():
            z.writestr(f"OEBPS/{nome}", conteudo)
        for p in imagens:
            z.write(p, f"OEBPS/img/{p.name}")

    print(f"EPUB: {destino}")
    print(f"{destino.stat().st_size / 1024:.0f} KB · {len(secoes)} seções · "
          f"{len(imagens)} imagens")


if __name__ == "__main__":
    main()
