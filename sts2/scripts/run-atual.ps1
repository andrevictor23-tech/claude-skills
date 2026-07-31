# Le o save da run ativa de Slay the Spire 2 e imprime o estado em texto legivel.
# Uso: powershell -File run-atual.ps1  [-Historico]
# ASCII puro de proposito: PowerShell 5.1 quebra com acentos/travessao sem BOM.
param([switch]$Historico)

$ErrorActionPreference = 'Stop'

function Get-SaveRoot {
    $bases = @(
        "C:\Program Files (x86)\Steam\userdata",
        "$env:ProgramFiles\Steam\userdata"
    )
    foreach ($b in $bases) {
        if (-not (Test-Path $b)) { continue }
        $hit = Get-ChildItem $b -Directory -EA SilentlyContinue |
               ForEach-Object { Join-Path $_.FullName "2868840\remote" } |
               Where-Object { Test-Path $_ } | Select-Object -First 1
        if ($hit) { return $hit }
    }
    return $null
}

function Get-ProfileDir($root) {
    # profile.save aponta o perfil em uso; se faltar, usa o de saves mais recente
    $pf = Join-Path $root "profile.save"
    if (Test-Path $pf) {
        $id = (Get-Content $pf -Raw | ConvertFrom-Json).last_profile_id
        $d = Join-Path $root "profile$id\saves"
        if (Test-Path $d) { return $d }
    }
    Get-ChildItem $root -Directory -Filter "profile*" |
        ForEach-Object { Join-Path $_.FullName "saves" } |
        Where-Object { Test-Path (Join-Path $_ "current_run.save") } |
        Sort-Object { (Get-Item (Join-Path $_ "current_run.save")).LastWriteTime } -Descending |
        Select-Object -First 1
}

function Nice($id) {
    if (-not $id) { return "" }
    $t = ($id -replace '^[A-Z_]+\.', '') -replace '_', ' '
    (Get-Culture).TextInfo.ToTitleCase($t.ToLower())
}

$root = Get-SaveRoot
if (-not $root) { "ERRO: pasta de saves do Slay the Spire 2 nao encontrada."; exit 1 }

$dir = Get-ProfileDir $root
if (-not $dir) { "ERRO: nenhum perfil com save encontrado em $root"; exit 1 }

$runFile = Join-Path $dir "current_run.save"
if (-not (Test-Path $runFile)) { "SEM RUN ATIVA - o jogador esta no menu ou entre runs."; exit 0 }

$r = Get-Content $runFile -Raw | ConvertFrom-Json
$p = $r.players[0]
$age = [int]((Get-Date) - (Get-Item $runFile).LastWriteTime).TotalMinutes

# ---------- cabecalho ----------
# map_point_history e um array POR ATO: [ato][no]. Achata mantendo a ordem.
$hist = @()
foreach ($actHist in $r.map_point_history) { $hist += @($actHist) }
# Neow nao conta como andar
$andar = [Math]::Max(0, $hist.Count - 1)
$act   = $r.acts[$r.current_act_index]
$hpPct = if ($p.max_hp) { [math]::Round(100 * $p.current_hp / $p.max_hp) } else { 0 }

"=========== RUN ATIVA - Slay the Spire 2 ==========="
$aviso = ""
if ($age -gt 45) { $aviso = "   << ATENCAO: save antigo, pode nao ser a run em curso" }
"Salvo ha {0} min{1}" -f $age, $aviso
""
"Personagem : {0}   (Ascension {1})" -f (Nice $p.character_id), $r.ascension
"Ato        : {0}   [ato {1} de 3]" -f (Nice $act.id), ($r.current_act_index + 1)
"Andar      : {0}" -f $andar
"HP         : {0}/{1}  ({2} pct)" -f $p.current_hp, $p.max_hp, $hpPct
"Ouro       : {0}" -f $p.gold
"Energia    : {0}" -f $p.max_energy
if ($p.base_orb_slot_count) { "Slots orbe : {0}" -f $p.base_orb_slot_count }
$mods = @($r.modifiers) | Where-Object { $_ }
if ($mods.Count) { "Modificador: {0}" -f (($mods | ForEach-Object { Nice $_ }) -join ', ') }
"Tempo      : {0} min   |   Modo: {1}" -f [math]::Round($r.run_time / 60), $r.game_mode

# ---------- deck ----------
""
"--- DECK ({0} cartas) ---" -f $p.deck.Count
$p.deck | Group-Object id |
    Sort-Object @{Expression='Count';Descending=$true}, @{Expression='Name';Descending=$false} |
    ForEach-Object {
    "  {0,2}x  {1}" -f $_.Count, (Nice $_.Name)
}

# ---------- reliquias / pocoes ----------
""
"--- RELIQUIAS ({0}) ---" -f $p.relics.Count
if ($p.relics.Count) {
    $p.relics | Sort-Object floor_added_to_deck | ForEach-Object {
        "  {0,-30} (andar {1})" -f (Nice $_.id), $_.floor_added_to_deck
    }
} else { "  (nenhuma)" }

""
"--- POCOES ({0} de {1}) ---" -f $p.potions.Count, $p.max_potion_slot_count
if ($p.potions.Count) { $p.potions | ForEach-Object { "  " + (Nice $_.id) } } else { "  (vazio)" }

# ---------- caminho percorrido ----------
""
"--- ESTE ATO ---"
# ancient/boss/pool ficam dentro de acts[i].rooms
$rooms = $act.rooms
$nd = "(ainda nao revelado)"
$anc = if ($rooms.ancient_id) { Nice $rooms.ancient_id } else { $nd }
$bss = if ($rooms.boss_id)    { Nice $rooms.boss_id }    else { $nd }
"  Ancient        : {0}" -f $anc
"  Boss do ato    : {0}" -f $bss

# elites contadas do historico real, que nao depende do campo do ato atual
$elRun = @($hist | Where-Object { $_.map_point_type -eq 'elite' }).Count
$elAto = @(@($r.map_point_history[$r.current_act_index]) | Where-Object { $_.map_point_type -eq 'elite' }).Count
"  Elites vencidas: {0} neste ato   |   {1} na run inteira" -f $elAto, $elRun
$pool = @($rooms.elite_encounter_ids) | Select-Object -Unique | ForEach-Object { Nice $_ }
if ($pool) { "  Pool de elites : {0}" -f ($pool -join ', ') }

if ($hist.Count) {
    ""
    "--- ULTIMOS 6 NOS ---"
    $hist | Select-Object -Last 6 | ForEach-Object {
        $st = $_.player_stats[0]
        $rm = $_.rooms[0]
        $lbl = if ($rm.model_id) { Nice $rm.model_id } else { Nice $_.map_point_type }
        "  [{0,-10}] {1,-34} HP {2,-4} dano {3,-4} ouro {4}" -f `
            $_.map_point_type, $lbl, $st.current_hp, $st.damage_taken, $st.current_gold
    }
}

# ---------- alertas ----------
$al = @()
if ($hpPct -lt 35) {
    $al += "HP CRITICO ($hpPct pct) - nao entre em elite; priorize fogueira ou cura."
} elseif ($hpPct -lt 60) {
    $al += "HP baixo ($hpPct pct) - elite so com plano claro."
}
if ($p.potions.Count -ge $p.max_potion_slot_count) {
    $al += "Pocoes cheias - a proxima e perdida. Use uma no proximo combate."
}
if ($p.gold -ge 300) {
    $al += "Ouro alto ($($p.gold)) - parado nao vale nada; force uma loja."
}
$act1Relics = ($p.relics | Where-Object { $_.floor_added_to_deck -le 17 }).Count
if ($r.current_act_index -ge 1 -and $act1Relics -lt 5) {
    $al += "So $act1Relics reliquias no Ato 1 (media nas suas vitorias: 6.5) - compense com elites agora."
}
if ($r.current_act_index -ge 1 -and $p.relics.Count -lt 8 -and $andar -gt 25) {
    $al += "Ritmo de reliquias abaixo do padrao das suas vitorias (14 ao fim do Ato 2)."
}
if ($al.Count) {
    ""
    "--- ALERTAS ---"
    $al | ForEach-Object { "  ! $_" }
}

# ---------- historico opcional ----------
if ($Historico) {
    ""
    "--- ULTIMAS 10 RUNS ---"
    Get-ChildItem (Join-Path $dir "history") -Filter *.run |
        Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
        try {
            $h = Get-Content $_.FullName -Raw | ConvertFrom-Json
            $res = if ($h.win) { "VITORIA" }
                   elseif ($h.was_abandoned) { "abandonada" }
                   else { "morreu p/ " + (Nice $h.killed_by_encounter) }
            # nos arquivos de historico o campo chama "character" (no save ativo e "character_id")
            $ch = $h.players[0].character
            if (-not $ch) { $ch = $h.players[0].character_id }
            "  {0:dd/MM}  {1,-12} A{2}  {3}" -f (Get-Date $_.LastWriteTime), (Nice $ch), $h.ascension, $res
        } catch {}
    }
}
""
