# Sync automatico, chamado pelo hook SessionStart do ~/.claude/settings.json.
#
# Roda o sync.ps1 em modo somente-recebe (-PullOnly): nunca commita, nunca
# empurra e nunca toca em repo com mudanca pendente. Enviar continua sendo ato
# deliberado do usuario (skill sync-skills), porque o claude-skills e publico.
#
# Trava de tempo: o usuario abre varias sessoes por dia, em varias pastas. Sem
# ela, cada abertura dispararia fetch nos quatro repos, e duas sessoes abertas
# ao mesmo tempo correriam uma sobre a outra. O carimbo e tocado ANTES do sync,
# de modo que uma segunda sessao iniciada no mesmo instante ja o encontra novo
# e desiste.

param(
    [int]$IntervaloHoras = 4,
    [switch]$Force
)

$carimbo = Join-Path $env:USERPROFILE '.claude\.last-auto-sync'
$log     = Join-Path $env:USERPROFILE '.claude\auto-sync.log'
$sync    = Join-Path $env:USERPROFILE '.claude\skills\sync-skills\scripts\sync.ps1'

if (-not (Test-Path $sync)) { exit 0 }

if (-not $Force -and (Test-Path $carimbo)) {
    $decorrido = (Get-Date) - (Get-Item $carimbo).LastWriteTime
    if ($decorrido -lt [TimeSpan]::FromHours($IntervaloHoras)) { exit 0 }
}

# Toca o carimbo primeiro (ver comentario acima sobre sessoes simultaneas).
if (Test-Path $carimbo) {
    (Get-Item $carimbo).LastWriteTime = Get-Date
} else {
    New-Item -ItemType File -Path $carimbo -Force | Out-Null
}

# Log rotativo simples: acima de 200 KB, mantem so a metade final.
if ((Test-Path $log) -and ((Get-Item $log).Length -gt 200KB)) {
    $linhas = Get-Content $log
    $linhas | Select-Object -Last ([int]($linhas.Count / 2)) | Set-Content $log -Encoding utf8
}

$saida = & $sync -PullOnly 2>&1 | Out-String
$codigo = $LASTEXITCODE

$cabecalho = "===== $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | auto-sync (PullOnly) | exit $codigo ====="
Add-Content $log -Value $cabecalho -Encoding utf8
Add-Content $log -Value $saida -Encoding utf8

# Exit 2 (conflito no rebase) e o unico caso que exige decisao humana: com
# asyncRewake no hook, ele acorda a sessao com o texto abaixo. Os demais erros
# (credencial, rede) ficam so no log — nao vale interromper o usuario por isso.
if ($codigo -eq 2) {
    Write-Output "Sync automatico das skills parou em CONFLITO de rebase. Veja $log e resolva antes de continuar."
    exit 2
}

exit 0
