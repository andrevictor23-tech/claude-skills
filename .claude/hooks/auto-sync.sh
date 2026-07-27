#!/usr/bin/env bash
# auto-sync.sh — salva e envia automaticamente as mudanças da skill para o GitHub.
#
# Chamado pelo "Stop hook" do Claude Code (ver .claude/settings.json): sempre que o
# Claude termina de responder, se houver mudanças no repositório, faz commit e push.
# Objetivo: nunca perder trabalho ao editar a skill, em qualquer computador.
#
# Seguro por design:
#   - só age dentro de um repositório git;
#   - o .gitignore deste repo já bloqueia dados sigilosos;
#   - scan-sigilo.sh escaneia os arquivos alterados ANTES do commit: padrão de
#     CPF, CNPJ, processo, IP ou telefone fora da allowlist BLOQUEIA o envio;
#   - nunca interrompe a sessão: falhas são silenciosas e o commit local persiste
#     mesmo que o push falhe (ex.: sem rede ou sem login) — vai no próximo envio.

set -u
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

# Só continua se estivermos dentro de um repositório git.
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Nada mudou? Não faz nada (silencioso).
[ -z "$(git status --porcelain)" ] && exit 0

ramo="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"

# --- Barreira anti-vazamento -------------------------------------------------
# Escaneia todos os arquivos alterados/novos. Se houver padrão de dado sensível
# fora da allowlist, NÃO comita nada: avisa o Delegado e deixa a árvore intacta
# para revisão (anonimizar, mover ao acervo privado, ou liberar na allowlist).
# -uall: lista arquivos individuais dentro de pastas novas (sem isso, pasta nao
# rastreada chega como diretorio e escaparia do scanner, que so le arquivos).
mapfile -t alterados < <(git status --porcelain -uall | sed -E 's/^.{3}//; s/^"(.*)"$/\1/; s/^.* -> //')
if [ -x .claude/hooks/scan-sigilo.sh ] || [ -f .claude/hooks/scan-sigilo.sh ]; then
  suspeitos="$(bash .claude/hooks/scan-sigilo.sh "${alterados[@]}")" || {
    lista="$(echo "$suspeitos" | head -5 | tr '\n' ' ')"
    printf '{"systemMessage":"SIGILO: commit BLOQUEADO. Padrao de dado sensivel (CPF/CNPJ/processo/IP/telefone) fora da allowlist em: %s. Revise: anonimize, mova ao acervo privado, ou (se ficticio) adicione a .claude/sigilo-allowlist.txt e rode o sync de novo."}\n' "$lista"
    exit 0
  }
fi
# -----------------------------------------------------------------------------

git add -A
git commit -q -m "auto: backup automatico da skill ($(date '+%Y-%m-%d %H:%M'))" >/dev/null 2>&1 || exit 0

if git push -q >/dev/null 2>&1; then
  printf '{"systemMessage":"Skill salva e enviada ao GitHub (ramo %s)."}\n' "$ramo"
else
  printf '{"systemMessage":"Skill salva localmente (commit feito). O envio ao GitHub falhou (verifique rede/login) e sera reenviado no proximo."}\n'
fi
exit 0
