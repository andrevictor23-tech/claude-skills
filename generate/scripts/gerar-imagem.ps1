<#
.SYNOPSIS
  Gera imagem pela linha Nano Banana (Gemini Image), rota Vertex AI ou AI Studio.

.DESCRIPTION
  Existe porque o PowerShell 5.1 tem duas armadilhas fatais com payload de imagem
  (ver "Armadilhas do PowerShell 5.1" no SKILL.md). Este script contorna as duas:
  monta o JSON em streaming e usa curl.exe no lugar de Invoke-RestMethod.

  Projeto, chave e pasta de saida saem do ~\.claude\.env -- nunca ficam aqui,
  porque esta skill vive em repo publico.

.EXAMPLE
  .\gerar-imagem.ps1 -PromptFile prompt.txt -Refs a.jpg,b.jpg -OutName teste_1785600000

.EXAMPLE
  .\gerar-imagem.ps1 -PromptFile p.txt -Refs foto.jpg -OutName final -Model gemini-3.1-flash-image -ImageSize 2K
#>
param(
  [Parameter(Mandatory=$true)][string]$PromptFile,
  [string[]]$Refs = @(),
  [Parameter(Mandatory=$true)][string]$OutName,
  [string]$Model     = "gemini-3.1-flash-lite-image",
  [string]$Aspect    = "1:1",
  [string]$ImageSize = "",
  [ValidateSet("vertex","aistudio")][string]$Route = "vertex",
  [string]$OutDir    = "",
  [int]$MaxSide      = 1280
)

$ErrorActionPreference = "Stop"
[System.Net.ServicePointManager]::Expect100Continue = $false
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
Add-Type -AssemblyName System.Drawing

# --- .env -------------------------------------------------------------------
$envFile = Join-Path $env:USERPROFILE ".claude\.env"
$cfg = @{}
if (Test-Path -LiteralPath $envFile) {
  foreach ($line in (Get-Content -LiteralPath $envFile)) {
    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
      $cfg[$matches[1]] = $matches[2].Trim().Trim('"').Trim("'")
    }
  }
}
if (-not $OutDir) {
  $OutDir = if ($cfg.GENERATE_OUT) { $cfg.GENERATE_OUT } else { Join-Path $env:USERPROFILE "Documents\PROJETOS\LEFRAN\generations" }
}
if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$scratch = Join-Path $env:TEMP "generate-skill"
if (-not (Test-Path $scratch)) { New-Item -ItemType Directory -Path $scratch -Force | Out-Null }

# --- helpers ----------------------------------------------------------------

# ARMADILHA 1: ConvertTo-Json escapa string caractere a caractere. Com base64 de
# alguns MB o processo passa de 12 GB de RAM e nunca termina. Nada de base64
# passa por ConvertTo-Json aqui.
function Get-B64Resized([string]$path, [int]$maxSide) {
  $img = [System.Drawing.Image]::FromFile($path)
  try {
    $scale = [Math]::Min(1.0, $maxSide / [Math]::Max($img.Width, $img.Height))
    $w = [int]($img.Width * $scale); $h = [int]($img.Height * $scale)
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($img, 0, 0, $w, $h)
    $g.Dispose()
    $ms = New-Object System.IO.MemoryStream
    $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
    $p = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $p.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 90L)
    $bmp.Save($ms, $enc, $p); $bmp.Dispose()
    $b64 = [Convert]::ToBase64String($ms.ToArray()); $ms.Dispose()
    return $b64
  } finally { $img.Dispose() }
}

# ARMADILHA 2: ConvertTo-Json sobre string com mais de ~1 KB devolve o objeto
# {"value":...,"Count":...} em vez de uma string JSON, e o Vertex responde 400
# "Starting an object on a scalar field". Prompt longo exige escape manual.
function ConvertTo-JsonString([string]$s) {
  $sb = New-Object System.Text.StringBuilder
  [void]$sb.Append('"')
  foreach ($c in $s.ToCharArray()) {
    switch ($c) {
      '"'     { [void]$sb.Append('\"') }
      '\'     { [void]$sb.Append('\\') }
      "`n"    { [void]$sb.Append('\n') }
      "`r"    { [void]$sb.Append('\r') }
      "`t"    { [void]$sb.Append('\t') }
      default {
        if ([int]$c -lt 32 -or [int]$c -gt 126) { [void]$sb.AppendFormat('\u{0:x4}', [int]$c) }
        else { [void]$sb.Append($c) }
      }
    }
  }
  [void]$sb.Append('"')
  return $sb.ToString()
}

# --- payload ----------------------------------------------------------------
$prompt = Get-Content -LiteralPath $PromptFile -Raw -Encoding UTF8
$imgCfg = "{`"aspectRatio`":`"$Aspect`""
if ($ImageSize) { $imgCfg += ",`"imageSize`":`"$ImageSize`"" }
$imgCfg += "}"

$reqFile = Join-Path $scratch "req.json"
$sw = New-Object System.IO.StreamWriter($reqFile, $false, (New-Object System.Text.UTF8Encoding($false)))
try {
  # "role":"user" e obrigatorio no Vertex; inofensivo no AI Studio.
  $sw.Write('{"contents":[{"role":"user","parts":[{"text":')
  $sw.Write((ConvertTo-JsonString $prompt))
  $sw.Write('}')
  foreach ($r in $Refs) {
    if (-not (Test-Path -LiteralPath $r)) { throw "referencia nao encontrada: $r" }
    $sw.Write(',{"inline_data":{"mime_type":"image/jpeg","data":"')
    $sw.Write((Get-B64Resized $r $MaxSide))
    $sw.Write('"}}')
  }
  $sw.Write(']}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":')
  $sw.Write($imgCfg)
  $sw.Write('}}')
} finally { $sw.Close(); $sw.Dispose() }
Write-Host ("payload: " + [math]::Round((Get-Item $reqFile).Length/1KB) + " KB, " + $Refs.Count + " referencia(s)")

# --- chamada ----------------------------------------------------------------
$respFile = Join-Path $scratch "resp.json"
$hdrFile  = Join-Path $scratch "hdr.txt"
$curlArgs = @("-s","-S","--max-time","600","-o",$respFile,"-X","POST")

if ($Route -eq "vertex") {
  $project = $cfg.GOOGLE_CLOUD_PROJECT
  if (-not $project) { throw "GOOGLE_CLOUD_PROJECT ausente em $envFile" }
  $tok = gcloud auth print-access-token
  if (-not $tok) { throw "gcloud sem token -- rodar: gcloud auth login" }
  $hw = New-Object System.IO.StreamWriter($hdrFile, $false, (New-Object System.Text.UTF8Encoding($false)))
  $hw.Write("Authorization: Bearer $tok"); $hw.Close(); $hw.Dispose()
  $uri = "https://aiplatform.googleapis.com/v1/projects/$project/locations/global/publishers/google/models/${Model}:generateContent"
  $curlArgs += @($uri, "-H", "@$hdrFile")
} else {
  $key = $cfg.GOOGLE_AI_STUDIO_KEY
  if (-not $key) { throw "GOOGLE_AI_STUDIO_KEY ausente em $envFile" }
  $uri = "https://generativelanguage.googleapis.com/v1beta/models/${Model}:generateContent?key=$key"
  $curlArgs += @($uri)
}
$curlArgs += @("-H","Content-Type: application/json","--data-binary","@$reqFile")

# ARMADILHA 3: Invoke-RestMethod tambem sufoca ao parsear a RESPOSTA (imagem em
# base64). curl.exe grava direto no disco; a extracao abaixo e por regex.
$sw2 = [System.Diagnostics.Stopwatch]::StartNew()
& curl.exe @curlArgs
$sw2.Stop()
if (Test-Path $hdrFile) { Remove-Item $hdrFile -Force }
Write-Host ("HTTP: " + [math]::Round($sw2.Elapsed.TotalSeconds,1) + "s, resposta " + [math]::Round((Get-Item $respFile).Length/1KB) + " KB")

# --- resposta ---------------------------------------------------------------
$raw = [System.IO.File]::ReadAllText($respFile)
if ($raw -notmatch '"inlineData"') {
  Write-Host "SEM IMAGEM na resposta:" -ForegroundColor Red
  Write-Host $raw.Substring(0, [Math]::Min(2000, $raw.Length))
  exit 1
}
# Salvar com a extensao do mimeType da resposta -- ela varia por rota e modelo.
$mime = ([regex]'"mimeType"\s*:\s*"([^"]+)"').Match($raw).Groups[1].Value
$data = ([regex]'"data"\s*:\s*"([^"]+)"').Match($raw).Groups[1].Value
$ext  = switch ($mime) { "image/png" { "png" } "image/jpeg" { "jpg" } "image/webp" { "webp" } default { "bin" } }
$file = Join-Path $OutDir "$OutName.$ext"
[System.IO.File]::WriteAllBytes($file, [Convert]::FromBase64String($data))

$sidecar = [ordered]@{
  model   = $Model
  route   = $Route
  prompt  = $prompt
  refs    = $Refs
  params  = [ordered]@{ aspectRatio = $Aspect; imageSize = $ImageSize }
  created = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
} | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText((Join-Path $OutDir "$OutName.json"), $sidecar, (New-Object System.Text.UTF8Encoding($false)))

$chk = [System.Drawing.Image]::FromFile($file)
Write-Host ("OK -> $file | $($chk.Width)x$($chk.Height) | $([math]::Round((Get-Item $file).Length/1KB)) KB | $mime") -ForegroundColor Green
$chk.Dispose()
Remove-Item $reqFile, $respFile -Force -ErrorAction SilentlyContinue
