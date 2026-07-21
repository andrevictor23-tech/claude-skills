# setup-extracao.ps1 - Prepara o ambiente de extracao de documentos nesta maquina.
#
# O venv do Docling tem ~1,3 GB e NAO vai para o git. Este script o recria
# localmente. Rode uma vez por maquina, depois do primeiro sync.
#
# Uso:
#   & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\setup-extracao.ps1"
#   ... -Force     (recria do zero, mesmo se ja existir)
#
# NOTA: mantenha este arquivo em ASCII puro. Travessao e outros caracteres
# nao-ASCII corrompem o parser do PowerShell 5.1 quando o arquivo e salvo
# em UTF-8 com BOM.

param([switch]$Force)

$ErrorActionPreference = "Stop"

$venv    = "$env:USERPROFILE\.claude\tools\docling-venv"
$py      = "$venv\Scripts\python.exe"
$tools   = "$env:USERPROFILE\.claude\tools"
$origem  = "$env:USERPROFILE\.claude\skills\sync-skills\scripts\extrair.py"
$destino = "$tools\extrair.py"

Write-Host "=== Setup do ambiente de extracao de documentos ===" -ForegroundColor Cyan

# 1. Python do sistema
$sysPy = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $sysPy) {
    Write-Host "ERRO: Python nao encontrado no PATH." -ForegroundColor Red
    Write-Host "Instale o Python 3.10+ em https://www.python.org/downloads/"
    Write-Host "(marque 'Add python.exe to PATH' no instalador)"
    exit 1
}
$ver = & python --version
Write-Host "Python do sistema: $ver"

# 2. Copiar o extrator para ~/.claude/tools
if (-not (Test-Path $tools)) {
    New-Item -ItemType Directory -Path $tools -Force | Out-Null
}
if (Test-Path $origem) {
    Copy-Item $origem $destino -Force
    Write-Host "extrair.py instalado em $destino" -ForegroundColor Green
} else {
    Write-Host "AVISO: extrair.py nao encontrado em $origem" -ForegroundColor Yellow
}

# 3. venv
if ((Test-Path $py) -and -not $Force) {
    & $py -c "import docling" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "venv ja existe e o Docling importa. Nada a fazer." -ForegroundColor Green
        Write-Host "(use -Force para recriar do zero)"
        exit 0
    }
    Write-Host "venv existe mas o Docling nao importa; reinstalando..." -ForegroundColor Yellow
}

if ($Force -and (Test-Path $venv)) {
    Write-Host "Removendo venv anterior..."
    Remove-Item $venv -Recurse -Force
}

if (-not (Test-Path $py)) {
    Write-Host "Criando venv em $venv ..."
    & python -m venv $venv
}

Write-Host "Instalando Docling. Sao ~1,3 GB, pode levar varios minutos..." -ForegroundColor Yellow
& $py -m pip install --upgrade pip --quiet
& $py -m pip install docling easyocr pymupdf pillow

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: falha ao instalar as dependencias." -ForegroundColor Red
    exit 1
}

& $py -c "import docling, easyocr, fitz; print('Docling + EasyOCR + PyMuPDF OK')"
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Pronto ===" -ForegroundColor Green
    Write-Host "Teste com:"
    Write-Host "  `$py = `"$py`""
    Write-Host "  `$ex = `"$destino`""
    Write-Host "  `& `$py `$ex ARQUIVO.pdf --info"
    Write-Host ""
    Write-Host "Na primeira conversao com OCR ele baixa ~500 MB de modelos."
} else {
    Write-Host "ERRO: pacotes instalados mas nao importam." -ForegroundColor Red
    exit 1
}
