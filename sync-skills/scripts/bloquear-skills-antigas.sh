#!/usr/bin/env bash
# bloquear-skills-antigas.sh — hook PreToolUse (matcher "Skill"), escopo usuario.
#
# O claude.ai sincroniza para o Claude Code copias de agosto/2026 de quatro skills
# autorais, com o prefixo "anthropic-skills:". A versao atual de cada uma mora
# neste repo. Este hook recusa a copia antiga e manda o Claude usar a local de
# mesmo nome. Registrado no ~/.claude/settings.json de cada maquina pelo
# sync.ps1 (instalar-hook-skills.py). Se as copias forem apagadas no claude.ai,
# o hook vira no-op e pode ser removido.

nome="$(grep -oE '"skill"[[:space:]]*:[[:space:]]*"anthropic-skills:(conciso|despacho-plantao|relatorio-final-ip|representacao-cautelar)"' \
        | grep -oE 'anthropic-skills:[a-z-]+')"

[ -z "$nome" ] && exit 0

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s é cópia antiga sincronizada do claude.ai. Use a skill local %s (mesmo nome, sem o prefixo anthropic-skills:)."}}\n' \
  "$nome" "${nome#anthropic-skills:}"
exit 0
