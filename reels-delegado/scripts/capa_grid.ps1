# Gera candidatos a capa de reels: frames com timestamp queimado + grade mosaico.
# Uso: capa_grid.ps1 -Video video.mp4 -OutDir capas [-Intervalo 3]
param(
    [Parameter(Mandatory=$true)][string]$Video,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [int]$Intervalo = 3
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path $Video)) { Write-Output "ERRO: video nao encontrado: $Video"; exit 1 }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# 1. Extrai 1 frame a cada $Intervalo segundos, com timestamp queimado no canto
$vf = "fps=1/$Intervalo,drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':text='%{pts\:hms}':fontsize=64:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=12:x=20:y=20"
ffmpeg -y -v error -i $Video -vf $vf -fps_mode vfr "$OutDir\ts_%03d.png"
if ($LASTEXITCODE -ne 0) { Write-Output "ERRO no ffmpeg (extracao de frames)"; exit 1 }

$frames = Get-ChildItem "$OutDir\ts_*.png" | Sort-Object Name
$n = $frames.Count
if ($n -eq 0) { Write-Output "ERRO: nenhum frame extraido"; exit 1 }

# 2. Renomeia cada frame individual para o timestamp real (frame k => (k-1)*Intervalo s)
$k = 0
foreach ($f in $frames) {
    $t = [TimeSpan]::FromSeconds($k * $Intervalo)
    $name = "frame_{0:hh\-mm\-ss}.png" -f $t
    Move-Item -Force $f.FullName (Join-Path $OutDir $name)
    $k++
}

# 3. Monta a grade (4 colunas) — copias temporarias com nome numerico sequencial
$cols = 4
$rows = [math]::Ceiling($n / $cols)
$i = 0
Get-ChildItem "$OutDir\frame_*.png" | Sort-Object Name | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $OutDir "grade_tmp_$i.png"); $i++
}
ffmpeg -y -v error -framerate 1 -start_number 0 -i "$OutDir\grade_tmp_%d.png" -vf "scale=480:-2,tile=${cols}x${rows}" -frames:v 1 "$OutDir\grade.png"
$ok = $LASTEXITCODE -eq 0
Remove-Item "$OutDir\grade_tmp_*.png" -Force

if ($ok -and (Test-Path "$OutDir\grade.png")) {
    Write-Output "OK: $n frames em $OutDir (frame_HH-MM-SS.png) + grade.png (${cols}x${rows})"
} else {
    Write-Output "Frames individuais OK ($n), mas a grade falhou. Mostre os frames individuais."
    exit 1
}
