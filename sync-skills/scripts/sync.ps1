# Sincroniza os repos do usuario com o GitHub:
#   1. ~/.claude/skills            (claude-skills)
#   2. ~/Documents/DELEGACIA       (delegacia-claude-workspace, privado)
#   3. ~/Documents/OSINT           (osint-investigacao)
# Seguro por padrao: commit local -> pull --rebase --autostash -> push.
# Em conflito, aborta o rebase e reporta, sem perder nada.

$ErrorActionPreference = 'Stop'
$global:exitCode = 0

function Sync-Repo {
    param([string]$repo, [string]$label)

    Write-Output ""
    Write-Output "########## $label ##########"

    if (-not (Test-Path (Join-Path $repo '.git'))) {
        Write-Output "ERRO: $repo nao e um repositorio git."
        $global:exitCode = 1
        return
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
            $global:exitCode = 1
            return
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
        $global:exitCode = 2
        return
    }

    # 3. Push
    git push origin HEAD
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERRO no push. Verifique credenciais/conexao."
        $global:exitCode = 3
        return
    }

    # 4. Resumo
    $after = git rev-parse HEAD
    Write-Output ""
    Write-Output "=== SYNC CONCLUIDO: $label ==="
    $received = git log --oneline "$before..$after" 2>$null
    if ($received) {
        Write-Output "Novidades recebidas/aplicadas:"
        Write-Output ($received | Out-String)
    } else {
        Write-Output "Repo ja estava atualizado."
    }
    git status --short --branch | Select-Object -First 3
}

# --- Repo 1: skills ---
Sync-Repo -repo (Join-Path $env:USERPROFILE '.claude\skills') -label 'claude-skills'

# --- Repo 2: workspace DELEGACIA (clona se ainda nao existir nesta maquina) ---
$delegacia = Join-Path $env:USERPROFILE 'Documents\DELEGACIA'
if (-not (Test-Path (Join-Path $delegacia '.git'))) {
    Write-Output ""
    Write-Output "########## delegacia-claude-workspace ##########"
    Write-Output "Repo ainda nao existe nesta maquina. Clonando..."
    git clone https://github.com/andrevictor23-tech/delegacia-claude-workspace.git $delegacia
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERRO ao clonar delegacia-claude-workspace. Verifique credenciais (repo privado)."
        $global:exitCode = 3
    } else {
        Write-Output "Clonado em $delegacia"
    }
} else {
    Sync-Repo -repo $delegacia -label 'delegacia-claude-workspace'
}

# --- Repo 3: osint-investigacao (clona se ainda nao existir nesta maquina) ---
$osint = Join-Path $env:USERPROFILE 'Documents\OSINT'
if (-not (Test-Path (Join-Path $osint '.git'))) {
    Write-Output ""
    Write-Output "########## osint-investigacao ##########"
    Write-Output "Repo ainda nao existe nesta maquina. Clonando..."
    git clone https://github.com/andrevictor23-tech/osint-investigacao.git $osint
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERRO ao clonar osint-investigacao. Verifique credenciais (repo privado?)."
        $global:exitCode = 3
    } else {
        Write-Output "Clonado em $osint"
    }
} else {
    Sync-Repo -repo $osint -label 'osint-investigacao'
}

exit $global:exitCode
