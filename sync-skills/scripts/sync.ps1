# Sincroniza os repos do usuario com o GitHub:
#   1. ~/.claude/skills            (claude-skills)
#   2. ~/Documents/DELEGACIA       (delegacia-claude-workspace, privado)
#   3. ~/.claude/skills/osint-investigacao  (osint-investigacao)
# Seguro por padrao: commit local -> pull --rebase --autostash -> push.
# Em conflito, aborta o rebase e reporta, sem perder nada.

param([switch]$AllowNew)

# 'Continue', nao 'Stop': o git escreve avisos normais no stderr (ex.: "LF will be
# replaced by CRLF") e, sob 'Stop', o PowerShell 5.1 os promove a NativeCommandError
# e aborta o sync no meio. A corretude vem da checagem de $LASTEXITCODE apos cada
# chamada, que ja existe abaixo.
$ErrorActionPreference = 'Continue'
$global:exitCode = 0

# Padroes de alto sinal para dado sensivel. Usados apenas no repo PUBLICO.
# Deliberadamente estreitos: falso positivo trava o sync do usuario.
$global:sensivel = @(
    @{ nome = 'CPF';            re = '\d{3}\.\d{3}\.\d{3}-\d{2}' },
    @{ nome = 'CNPJ';           re = '\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}' },
    @{ nome = 'processo CNJ';   re = '\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}' },
    @{ nome = 'telefone';       re = '\(\d{2}\)\s?9?\d{4}-\d{4}' },
    @{ nome = 'valor em reais'; re = 'R\$\s?\d{1,3}(\.\d{3})+' },
    @{ nome = 'chave/API key';  re = '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{20,})' },
    @{ nome = 'chave privada';  re = '-----BEGIN [A-Z ]*PRIVATE KEY-----' }
)

# Nao escaneia a si mesmo: os regex acima viveriam como "achados" literais.
$global:isentos = @('sync-skills/scripts/sync.ps1')

# Portao de auditoria do repo PUBLICO. Roda ANTES do `git add -A`, porque
# depois de publicado o estrago nao se desfaz (o GitHub indexa e cacheia).
# Criado em 21/07/2026, depois que estado-carteira.md (perfil financeiro do
# usuario + nome, cargo e comarca) quase foi publicado por um `git add -A`.
# ATENCAO ao mexer aqui: nao use Write-Output dentro desta funcao. No PowerShell
# tudo que vai para o pipeline compoe o valor de retorno, entao as mensagens
# fariam a funcao devolver um array (sempre "verdadeiro") e o portao NUNCA
# bloquearia. Bug real, pego em teste no dia em que o portao foi escrito.
# As mensagens sao acumuladas em $global:auditMsgs e impressas pelo chamador.
function Test-Publicavel {
    param([string]$repo)

    $global:auditMsgs = @()
    $novos = @(git ls-files --others --exclude-standard)
    $modificados = @(git diff --name-only)
    $candidatos = @($novos + $modificados | Where-Object { $_ -and ($global:isentos -notcontains $_) } | Select-Object -Unique)

    $bloqueios = @()

    # (a) Arquivo novo nunca visto: exige decisao consciente.
    if ($novos.Count -gt 0 -and -not $AllowNew) {
        $global:auditMsgs += ""
        $global:auditMsgs += "!!! ARQUIVOS NOVOS (nao rastreados) no repo PUBLICO:"
        foreach ($n in $novos) { $global:auditMsgs += "      + $n" }
        $bloqueios += "arquivos novos sem classificacao"
    }

    # (b) Varredura de conteudo do que seria publicado.
    foreach ($f in $candidatos) {
        if (-not (Test-Path $f -PathType Leaf)) { continue }
        $info = Get-Item $f
        if ($info.Length -gt 2MB) { continue }
        $txt = Get-Content $f -Raw -ErrorAction SilentlyContinue
        if (-not $txt) { continue }
        foreach ($p in $global:sensivel) {
            if ($txt -match $p.re) {
                $global:auditMsgs += ""
                $global:auditMsgs += "!!! POSSIVEL DADO SENSIVEL: $f  [$($p.nome)]"
                $global:auditMsgs += "      trecho: $($Matches[0])"
                $bloqueios += "$f ($($p.nome))"
            }
        }
    }

    if ($bloqueios.Count -gt 0) {
        $global:auditMsgs += ""
        $global:auditMsgs += "=== SYNC BLOQUEADO: claude-skills e um repo PUBLICO ==="
        $global:auditMsgs += "Antes de sincronizar, para CADA item acima decida:"
        $global:auditMsgs += "  - e sigiloso?   -> mova para o repo privado e liste no .gitignore da skill"
        $global:auditMsgs += "  - e publicavel? -> rode de novo com -AllowNew (so libera o item (a))"
        $global:auditMsgs += "Nao basta olhar o nome do arquivo: leia o conteudo."
        return $false
    }
    return $true
}

function Sync-Repo {
    param([string]$repo, [string]$label, [switch]$Public)

    Write-Output ""
    Write-Output "########## $label ##########"

    if (-not (Test-Path (Join-Path $repo '.git'))) {
        Write-Output "ERRO: $repo nao e um repositorio git."
        $global:exitCode = 1
        return
    }

    Set-Location $repo

    if ($Public) {
        $ok = Test-Publicavel -repo $repo
        foreach ($m in $global:auditMsgs) { Write-Output $m }
        if (-not $ok) {
            $global:exitCode = 4
            return
        }
    }

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

# --- Repo 1: skills (PUBLICO: passa pelo portao de auditoria) ---
Sync-Repo -repo (Join-Path $env:USERPROFILE '.claude\skills') -label 'claude-skills' -Public

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
# Mora dentro de ~/.claude/skills para o Claude enxergar a skill. O .gitignore
# do claude-skills exclui esta pasta, entao o `git add -A` do Repo 1 nao a engole.
$osint = Join-Path $env:USERPROFILE '.claude\skills\osint-investigacao'
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
