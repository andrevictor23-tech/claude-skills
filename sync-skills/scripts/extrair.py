#!/usr/bin/env python3
"""
extrair.py — Extrator universal de documentos com cache, para as skills do Claude.

Converte PDF (nativo ou escaneado), DOCX, XLSX, PPTX, HTML, imagens e outros
formatos para Markdown limpo, pronto para entrar no contexto sem desperdicio
de token. Roda 100% local: nenhum dado sai da maquina.

Estrategia (nesta ordem, para gastar o minimo de tempo e token):
  1. Cache — se ja extraimos este arquivo antes, devolve o cache.
  2. Texto nativo (PyMuPDF) — instantaneo, para PDFs que ja tem texto.
  3. Docling — OCR local + analise de layout, para escaneados e tabelas.

Uso:
    python extrair.py ARQUIVO [ARQUIVO...] [opcoes]

Opcoes:
    --out DIR        Onde salvar o .md (padrao: ao lado do cache)
    --force          Ignora o cache e reextrai
    --ocr            Forca Docling mesmo se houver texto nativo
    --no-ocr         Nunca usa Docling (so texto nativo)
    --stdout         Imprime o Markdown em vez de salvar
    --info           So diagnostica o arquivo, nao extrai
    --cache-dir DIR  Diretorio de cache (padrao: G:\\Meu Drive\\VS CODE TESTE\\extracao-cache
                     se existir, senao ~/.claude/cache/extracao)

Exemplos:
    python extrair.py autos.pdf
    python extrair.py *.pdf --out ./textos
    python extrair.py extrato.pdf --ocr --stdout
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------- constantes

VENV_PYTHON = Path.home() / ".claude" / "tools" / "docling-venv" / "Scripts" / "python.exe"

# O cache vai para o Google Drive quando disponivel, para sincronizar entre as
# maquinas do usuario — mesmo padrao ja adotado pela skill simulado-quiz.
#
# A letra do drive NAO e fixa: varia por maquina (G:, H:, ...), pode nao estar
# montada, e o nome da pasta muda com o idioma do Google Drive ("Meu Drive" x
# "My Drive"). Por isso procuramos, em vez de cravar um caminho.
CACHE_LOCAL = Path.home() / ".claude" / "cache" / "extracao"

# Permite fixar o cache por variavel de ambiente, acima de qualquer deteccao.
CACHE_ENV = "CLAUDE_EXTRACAO_CACHE"

_SUBPASTA_DRIVE = Path("VS CODE TESTE") / "extracao-cache"
_NOMES_DRIVE = ("Meu Drive", "My Drive")

# Um PDF cujo texto nativo renda menos que isto por pagina e, na pratica, um
# escaneado: o pouco texto costuma ser so carimbo/rodape do sistema.
MIN_CHARS_POR_PAGINA = 200

FORMATOS_DOCLING = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm", ".md", ".adoc",
    ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp",
    ".eml", ".msg", ".epub", ".csv", ".xhtml",
}

FORMATOS_TEXTO = {".txt", ".md", ".json", ".csv", ".log", ".xml", ".yaml", ".yml"}


# ------------------------------------------------------------------ utilidades

def log(msg):
    print(msg, file=sys.stderr, flush=True)


def aprox_tokens(texto):
    """Estimativa conservadora para portugues: ~4 caracteres por token."""
    return len(texto) // 4


def achar_google_drive():
    """Procura a raiz do Google Drive nesta maquina, varrendo as letras.

    Devolve None se nao houver — o chamador cai no cache local. Um cache local
    funciona igual; so nao e compartilhado com as outras maquinas.
    """
    for letra in "GHIJKLDEFNOPQRSTUVWXYZ":
        for nome in _NOMES_DRIVE:
            raiz = Path(f"{letra}:/") / nome
            try:
                if raiz.is_dir():
                    return raiz
            except OSError:
                continue  # drive listado mas indisponivel
    return None


def resolver_cache_dir(escolhido=None):
    if escolhido:
        d = Path(escolhido)
    elif os.environ.get(CACHE_ENV):
        d = Path(os.environ[CACHE_ENV])
    else:
        raiz = achar_google_drive()
        d = (raiz / _SUBPASTA_DRIVE) if raiz else CACHE_LOCAL

    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        # Drive montado mas sem escrita (offline, sem espaco): nao vale abortar
        # a extracao por causa do cache.
        log(f"aviso: nao consegui usar {d} ({e}); caindo no cache local")
        d = CACHE_LOCAL
        d.mkdir(parents=True, exist_ok=True)
    return d


def hash_arquivo(caminho):
    """Identidade do arquivo: conteudo + tamanho. Renomear nao invalida o cache."""
    h = hashlib.sha256()
    tam = caminho.stat().st_size
    h.update(str(tam).encode())
    with open(caminho, "rb") as fh:
        # Primeiros e ultimos 2 MB bastam para identificar sem ler tudo.
        h.update(fh.read(2 * 1024 * 1024))
        if tam > 4 * 1024 * 1024:
            fh.seek(-2 * 1024 * 1024, os.SEEK_END)
            h.update(fh.read())
    return h.hexdigest()[:16]


def limpar_ruido(texto):
    """Remove o lixo repetido que infla o contexto sem informar nada.

    O caso concreto que motivou isto: PDFs exportados dos autos digitais trazem
    em toda pagina um carimbo identico ("Copia extraida dos autos digitais do
    I.P. ... pelo DELEGADO ... as HHhMMmin do dia ..."). Em 41 paginas isso
    sozinho eram ~1.500 tokens de nada.
    """
    linhas = texto.split("\n")

    # Conta linhas nao triviais para achar as que se repetem pagina a pagina.
    contagem = {}
    for ln in linhas:
        s = ln.strip()
        if len(s) > 25:
            contagem[s] = contagem.get(s, 0) + 1

    # Repetiu 3+ vezes e nao parece conteudo? E cabecalho/rodape.
    repetidas = {s for s, n in contagem.items() if n >= 3}

    saida = []
    for ln in linhas:
        s = ln.strip()
        if s in repetidas:
            continue
        # Numero de pagina solto
        if re.fullmatch(r"\d{1,4}", s):
            continue
        if re.fullmatch(r"(?i)(pag(ina)?\.?\s*)?\d{1,4}(\s*(de|/)\s*\d{1,4})?", s):
            continue
        saida.append(ln)

    texto = "\n".join(saida)
    texto = re.sub(r"\n{4,}", "\n\n\n", texto)      # colapsa vazios excessivos
    texto = re.sub(r"[ \t]{3,}", "  ", texto)        # colapsa espacos
    return texto.strip()


# --------------------------------------------------------------- diagnostico

def diagnosticar_pdf(caminho):
    """Descobre se o PDF tem texto util ou se e imagem escaneada."""
    try:
        import fitz
    except ImportError:
        return None

    try:
        doc = fitz.open(caminho)
    except Exception as e:
        return {"erro": str(e)}

    n = len(doc)
    chars = 0
    imgs = 0
    por_pagina = []
    for p in doc:
        t = p.get_text().strip()
        chars += len(t)
        imgs += len(p.get_images())
        por_pagina.append(len(t))
    doc.close()

    media = chars / n if n else 0
    return {
        "paginas": n,
        "chars_nativos": chars,
        "chars_por_pagina": round(media, 1),
        "imagens": imgs,
        "escaneado": media < MIN_CHARS_POR_PAGINA,
    }


# ---------------------------------------------------------------- extratores

def extrair_nativo_pdf(caminho):
    """Texto ja embutido no PDF. Instantaneo e sem custo."""
    import fitz

    doc = fitz.open(caminho)
    partes = []
    for i, p in enumerate(doc):
        t = p.get_text()
        if t.strip():
            partes.append(t)
    doc.close()
    return "\n\n".join(partes)


def extrair_docling(caminho, com_ocr=True):
    """Docling: OCR local + analise de layout + estrutura de tabelas.

    OCR via EasyOCR com lang=['pt']. Isto NAO e detalhe de configuracao: o
    motor padrao do Docling (RapidOCR, modelo ch_PP-OCRv4) foi medido neste
    acervo e devolveu ZERO acentos — "MINISTERIOPUBLICO", "JUSTICA",
    "Falsificacao", palavras coladas e ate caractere chines no meio do texto.
    Inutilizavel para citacao literal em peca. O EasyOCR em portugues devolveu
    "MINISTERIO PUBLICO", "JUSTICA", "Noticia de Fato" corretamente acentuados.
    """
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import (
        PdfPipelineOptions,
        EasyOcrOptions,
    )

    opts = PdfPipelineOptions()
    opts.do_ocr = com_ocr
    opts.do_table_structure = True
    opts.generate_page_images = False
    if com_ocr:
        opts.ocr_options = EasyOcrOptions(lang=["pt"], force_full_page_ocr=True)

    conv = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
    )
    res = conv.convert(str(caminho))
    return res.document.export_to_markdown()


def extrair(caminho, forcar_ocr=False, sem_ocr=False):
    """Escolhe a estrategia mais barata que resolve, e devolve (markdown, meta)."""
    ext = caminho.suffix.lower()
    meta = {"arquivo": caminho.name, "extensao": ext}

    if ext in FORMATOS_TEXTO and ext not in {".csv"}:
        txt = caminho.read_text(encoding="utf-8", errors="replace")
        meta["metodo"] = "leitura direta"
        return txt, meta

    if ext == ".pdf":
        diag = diagnosticar_pdf(caminho)
        if diag and "erro" not in diag:
            meta["diagnostico"] = diag

            if not forcar_ocr and not diag["escaneado"]:
                log(f"  texto nativo ({diag['chars_por_pagina']} chars/pag) — sem OCR")
                txt = extrair_nativo_pdf(caminho)
                meta["metodo"] = "texto nativo (PyMuPDF)"
                return txt, meta

            if sem_ocr:
                log("  escaneado, mas --no-ocr: extraindo so o texto nativo")
                txt = extrair_nativo_pdf(caminho)
                meta["metodo"] = "texto nativo (forcado por --no-ocr)"
                return txt, meta

            log(f"  escaneado ({diag['chars_por_pagina']} chars/pag, "
                f"{diag['imagens']} imagens) — usando Docling com OCR")

    if sem_ocr and ext == ".pdf":
        txt = extrair_nativo_pdf(caminho)
        meta["metodo"] = "texto nativo"
        return txt, meta

    if ext in FORMATOS_DOCLING:
        t0 = time.time()
        txt = extrair_docling(caminho, com_ocr=not sem_ocr)
        meta["metodo"] = "Docling" + (" + OCR" if not sem_ocr else "")
        meta["segundos"] = round(time.time() - t0, 1)
        return txt, meta

    raise ValueError(f"formato nao suportado: {ext}")


# --------------------------------------------------------------------- fluxo

def processar(caminho, cache_dir, args):
    caminho = Path(caminho).resolve()
    if not caminho.exists():
        log(f"ERRO: nao encontrado: {caminho}")
        return None

    log(f"\n> {caminho.name}")

    if args.info:
        if caminho.suffix.lower() == ".pdf":
            d = diagnosticar_pdf(caminho)
            print(json.dumps(d, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"extensao": caminho.suffix,
                              "bytes": caminho.stat().st_size}, indent=2))
        return None

    h = hash_arquivo(caminho)
    slug = re.sub(r"[^\w\-]+", "_", caminho.stem)[:60]
    cache_md = cache_dir / f"{slug}.{h}.md"
    cache_meta = cache_dir / f"{slug}.{h}.json"

    if cache_md.exists() and not args.force:
        texto = cache_md.read_text(encoding="utf-8")
        log(f"  cache: {cache_md.name} ({aprox_tokens(texto):,} tokens aprox)")
    else:
        try:
            texto, meta = extrair(caminho, forcar_ocr=args.ocr, sem_ocr=args.no_ocr)
        except Exception as e:
            log(f"  ERRO na extracao: {e}")
            return None

        bruto = len(texto)
        texto = limpar_ruido(texto)
        economia = bruto - len(texto)

        meta["chars_brutos"] = bruto
        meta["chars_limpos"] = len(texto)
        meta["tokens_aprox"] = aprox_tokens(texto)
        meta["ruido_removido_chars"] = economia

        cache_md.write_text(texto, encoding="utf-8")
        cache_meta.write_text(json.dumps(meta, indent=2, ensure_ascii=False),
                              encoding="utf-8")

        log(f"  metodo: {meta['metodo']}")
        if economia > 0:
            log(f"  ruido removido: {economia:,} chars (~{economia//4:,} tokens)")
        log(f"  resultado: {len(texto):,} chars (~{aprox_tokens(texto):,} tokens)")
        log(f"  cache: {cache_md}")

    if args.stdout:
        print(texto)
    elif args.out:
        destino = Path(args.out)
        destino.mkdir(parents=True, exist_ok=True)
        alvo = destino / f"{caminho.stem}.md"
        alvo.write_text(texto, encoding="utf-8")
        log(f"  salvo: {alvo}")

    return cache_md


def main():
    ap = argparse.ArgumentParser(
        description="Extrator universal de documentos com cache (local, sem rede).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("arquivos", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--ocr", action="store_true")
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--info", action="store_true")
    ap.add_argument("--cache-dir")
    args = ap.parse_args()

    cache_dir = resolver_cache_dir(args.cache_dir)
    if not args.info:
        log(f"cache em: {cache_dir}")
        if cache_dir == CACHE_LOCAL:
            log("  (cache LOCAL — Google Drive nao encontrado; as outras "
                "maquinas vao reprocessar estes arquivos)")

    gerados = []
    for a in args.arquivos:
        r = processar(a, cache_dir, args)
        if r:
            gerados.append(r)

    if gerados and not args.stdout:
        log(f"\n{len(gerados)} arquivo(s) prontos. Leia os .md acima — nao o PDF.")


if __name__ == "__main__":
    main()
