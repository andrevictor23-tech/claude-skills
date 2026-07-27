#!/usr/bin/env bash
# scan-sigilo.sh — barreira anti-vazamento do repositório PÚBLICO delta-skills.
#
# Procura, nos arquivos alterados, padrões de dado sensível de caso real:
#   - CPF formatado            (000.000.000-00)
#   - CNPJ formatado           (00.000.000/0000-00)
#   - número de processo CNJ   (0000000-00.0000.0.00.0000)
#   - número de IP da PJC/MT   (55.4.AAAA.N / 392.4.AAAA.N)
#   - número de ocorrência     (AAAA.NNNNNN)
#   - telefone celular BR      (DD 9XXXX-XXXX)
#
# Arquivos com exemplos FICTÍCIOS revisados pelo Delegado são liberados pela
# allowlist (.claude/sigilo-allowlist.txt). Qualquer ocorrência fora dela
# BLOQUEIA o commit do auto-sync: a persuasão falha; o bloqueio não.
#
# Desempenho: allowlist resolvida em bash puro e UM único grep para todos os
# arquivos (no Windows, spawn de processo é caro e o hook tem timeout de 60s).
#
# Uso:  scan-sigilo.sh arquivo [arquivo...]
# Sai com 0 se limpo; 1 se houver violação (lista em stdout, uma por linha).

set -u
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

ALLOWLIST=".claude/sigilo-allowlist.txt"

PADROES='[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}|[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}|[0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}|(^|[^0-9])(55|392)\.4\.20[0-9]{2}\.[0-9]+|(^|[^0-9])20[0-9]{2}\.[0-9]{6}([^0-9]|$)|\(?[0-9]{2}\)?[ .]?9[0-9]{4}-[0-9]{4}'

# Carrega a allowlist uma vez (prefixos de caminho; comentários e vazios fora).
prefixos=()
if [ -f "$ALLOWLIST" ]; then
  while IFS= read -r linha; do
    linha="${linha%%#*}"
    # trim de espaços em bash puro (sem tr: spawn por linha mata o desempenho)
    linha="${linha#"${linha%%[![:space:]]*}"}"
    linha="${linha%"${linha##*[![:space:]]}"}"
    [ -n "$linha" ] && prefixos+=("$linha")
  done < "$ALLOWLIST"
fi

# Filtra: só escaneia arquivo existente e fora da allowlist.
candidatos=()
for arq in "$@"; do
  [ -f "$arq" ] || continue                      # apagados/renomeados: nada a escanear
  arq="${arq#./}"
  liberado=0
  for p in ${prefixos[@]+"${prefixos[@]}"}; do
    case "$arq" in "$p"*) liberado=1; break ;; esac
  done
  [ "$liberado" -eq 1 ] && continue
  candidatos+=("$arq")
done

[ "${#candidatos[@]}" -eq 0 ] && exit 0

# Um único grep para todos os candidatos: -l lista os arquivos com ocorrência,
# -I ignora binários. Sai 1 (violação) se qualquer arquivo casar.
suspeitos="$(grep -lIE "$PADROES" -- "${candidatos[@]}" 2>/dev/null)"
if [ -n "$suspeitos" ]; then
  printf '%s\n' "$suspeitos"
  exit 1
fi
exit 0
