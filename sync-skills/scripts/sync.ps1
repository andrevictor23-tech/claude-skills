# Sincroniza ~/.claude/skills com o GitHub (claude-skills).
# Seguro por padrao: commit local -> pull --rebase --autostash -> push.
# Em conflito, aborta o rebase e reporta, sem perder nada.

$ErrorActionPreference = 'Stop'
$repo = Join-Path $env:USERPROFILE '.claude\skills'

if (-not (Test-Path (Join-Path $repo '.git'))) {
    Write-Output "ERRO: $repo nao e um repositorio git."
    exit 1
}

Set-Location $repo

# 1. Commit local, se houver mudancas
$dirty = git status --porcelain
if ($dirty) {
    git add -A
    $msg = "sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $msg | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERRO no commit (identidade git configurada? git config --global user.name/email)."
        exit 1
    }
    Write-Output "Commit local criado: $msg"
    Write-Output ($dirty | Out-String)
} else {
    Write-Output "Nenhuma mudanca local para commitar."
}

$before = git rev-parse HEAD

# 2. Pull com rebase (autostash cobre sobras nao commitadas)
git fetch origin
git pull --rebase --autostash
if ($LASTEXITCODE -ne 0) {
    Write-Output "CONFLITO no rebase. Abortando para preservar o estado local."
    git rebase --abort
    Write-Output "Repo restaurado. Veja os arquivos em conflito acima e resolva manualmente (SKILL.md da sync-skills)."
    exit 2
}

# 3. Push
git push origin HEAD
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERRO no push. Verifique credenciais/conexao."
    exit 3
}

# 4. Resumo
$after = git rev-parse HEAD
Write-Output ""
Write-Output "=== SYNC CONCLUIDO ==="
$received = git log --oneline "$before..$after" 2>$null
if ($received) {
    Write-Output "Novidades recebidas/aplicadas:"
    Write-Output ($received | Out-String)
} else {
    Write-Output "Repo ja estava atualizado."
}
git status --short --branch | Select-Object -First 3
