---
name: sync-skills
description: Sincroniza as skills do Claude entre as máquinas do usuário via git (repo andrevictor23-tech/claude-skills em ~/.claude/skills). Use SEMPRE que o usuário pedir para sincronizar, atualizar, puxar ou enviar skills entre computadores, mencionar "git pull das skills", "sync das skills", "atualiza minhas skills", "manda pro git", "as skills estão atualizadas?", ou quando ele digitar comandos git relacionados a ~/.claude/skills no chat. Também use ao final de qualquer sessão em que skills foram criadas ou editadas, para oferecer o envio das mudanças às outras máquinas.
---

# Sync de skills entre máquinas

O usuário mantém `~/.claude/skills` como clone de `https://github.com/andrevictor23-tech/claude-skills.git` em 3 máquinas. A pasta `ecc/` é subpasta rastreada do mesmo repo (não é repo separado).

O script também sincroniza um segundo repo: `~/Documents/DELEGACIA`, clone de `https://github.com/andrevictor23-tech/delegacia-claude-workspace.git` (**privado** — workspace institucional com CLAUDE.md aninhados). Se a pasta ainda não existir na máquina, o script clona automaticamente. O `.gitignore` desse repo é lista branca (só `.md`, mais `MODELOS-REPRESENTACAO/lexico-semente.txt`), então arquivos de casos reais na pasta nunca são enviados.

Um terceiro repo também é sincronizado: `~/Documents/OSINT`, clone de `https://github.com/andrevictor23-tech/osint-investigacao.git`. Mesmo comportamento de clone automático caso a pasta ainda não exista na máquina.

**Atenção: `claude-skills` é público.** Nada de sigiloso pode entrar nele. Em particular, o acervo da skill `representacao-cautelar` (modelos reais, catálogo e léxico) vive **apenas** no repo privado, em `MODELOS-REPRESENTACAO/`.

## Depois de clonar numa máquina nova

O sync traz os dois repos, mas o acervo da `representacao-cautelar` precisa ser espelhado para dentro da skill, pois lá os caminhos são ignorados pelo git:

```powershell
$src = "$env:USERPROFILE\Documents\DELEGACIA\MODELOS-REPRESENTACAO"
$sk  = "$env:USERPROFILE\.claude\skills\representacao-cautelar"
Copy-Item "$src\catalogo-modelos.md" "$sk\references\" -Force
Copy-Item "$src\lexico-semente.txt"  "$sk\scripts\"    -Force
Copy-Item "$src\*.md" "$sk\assets\modelos\" -Force
Remove-Item "$sk\assets\modelos\catalogo-modelos.md" -ErrorAction SilentlyContinue
```

Se o usuário editar modelos na skill, copie-os de volta para `MODELOS-REPRESENTACAO/` antes de sincronizar: o repo privado é a fonte de verdade.

## Procedimento

Execute o script pronto:

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
```

Não use `-ExecutionPolicy Bypass`: a política `RemoteSigned` do usuário já permite rodar este script local, e a flag faz o classificador de permissões bloquear a execução.

Para cada um dos três repos, o script faz nesta ordem:
1. `git add -A` + commit automático das mudanças locais (mensagem `sync: <data>`), se houver.
2. `git pull --rebase --autostash`.
3. `git push`.
4. Imprime resumo (commits recebidos, skills novas ou alteradas).

## Se der conflito

O script aborta o rebase automaticamente e deixa o repo como estava, imprimindo `CONFLITO` e os arquivos envolvidos. Nesse caso:
1. Mostre ao usuário quais arquivos conflitaram.
2. Pergunte qual versão ele quer manter (a desta máquina ou a do GitHub) — normalmente ele sabe qual máquina tem a versão mais nova.
3. Resolva com `git checkout --ours`/`--theirs` no arquivo, conclua o rebase e faça o push.

## Regras

- NUNCA usar `push --force`.
- `.venv/` e caches não entram no repo (já cobertos por .gitignore das skills que os têm). Se `git status` mostrar `.venv` de alguma skill, adicione ao `.gitignore` dela antes de commitar.
- O script usa `git add -A`. Antes de rodá-lo, confira `git status --porcelain --untracked-files=all` em `~/.claude/skills` e verifique se nada sob `representacao-cautelar/assets/modelos/`, `references/catalogo-modelos.md` ou `scripts/lexico-semente.txt` aparece. Se aparecer, o `.gitignore` foi quebrado: conserte antes de sincronizar, porque esse repo é público.
- Auditar o **conteúdo**, não só os nomes dos arquivos: um comentário ou um resumo pode expor tática tanto quanto a peça inteira.
- Depois do sync, lembrar o usuário de rodar o sync nas outras máquinas para receber as mudanças.
