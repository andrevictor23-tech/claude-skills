---
name: sync-skills
description: Sincroniza as skills do Claude entre as máquinas do usuário via git (repo andrevictor23-tech/claude-skills em ~/.claude/skills). Use SEMPRE que o usuário pedir para sincronizar, atualizar, puxar ou enviar skills entre computadores, mencionar "git pull das skills", "sync das skills", "atualiza minhas skills", "manda pro git", "as skills estão atualizadas?", ou quando ele digitar comandos git relacionados a ~/.claude/skills no chat. Também use ao final de qualquer sessão em que skills foram criadas ou editadas, para oferecer o envio das mudanças às outras máquinas.
---

# Sync de skills entre máquinas

O usuário mantém `~/.claude/skills` como clone de `https://github.com/andrevictor23-tech/claude-skills.git` em 3 máquinas. A pasta `ecc/` é subpasta rastreada do mesmo repo (não é repo separado).

O script também sincroniza um segundo repo: `~/Documents/DELEGACIA`, clone de `https://github.com/andrevictor23-tech/delegacia-claude-workspace.git` (**privado** — workspace institucional com CLAUDE.md aninhados). Se a pasta ainda não existir na máquina, o script clona automaticamente. O `.gitignore` desse repo é lista branca (só `.md` sobe), então arquivos de casos reais na pasta nunca são enviados.

## Procedimento

Execute o script pronto:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
```

O script faz, nesta ordem:
1. `git add -A` + commit automático das mudanças locais (mensagem `sync: <hostname> <data>`), se houver.
2. `git pull --rebase --autostash`.
3. `git push`.
4. Imprime resumo (commits enviados/recebidos, skills novas ou alteradas).

## Se der conflito

O script aborta o rebase automaticamente e deixa o repo como estava, imprimindo `CONFLITO` e os arquivos envolvidos. Nesse caso:
1. Mostre ao usuário quais arquivos conflitaram.
2. Pergunte qual versão ele quer manter (a desta máquina ou a do GitHub) — normalmente ele sabe qual máquina tem a versão mais nova.
3. Resolva com `git checkout --ours`/`--theirs` no arquivo, conclua o rebase e faça o push.

## Regras

- NUNCA usar `push --force`.
- `.venv/` e caches não entram no repo (já cobertos por .gitignore das skills que os têm). Se `git status` mostrar `.venv` de alguma skill, adicione ao `.gitignore` dela antes de commitar.
- Depois do sync, lembrar o usuário de rodar o sync nas outras máquinas para receber as mudanças.
