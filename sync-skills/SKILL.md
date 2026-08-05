---
name: sync-skills
description: Sincroniza as skills do Claude entre as máquinas do usuário via git (repo andrevictor23-tech/claude-skills em ~/.claude/skills). Use SEMPRE que o usuário pedir para sincronizar, atualizar, puxar ou enviar skills entre computadores, mencionar "git pull das skills", "sync das skills", "atualiza minhas skills", "manda pro git", "as skills estão atualizadas?", ou quando ele digitar comandos git relacionados a ~/.claude/skills no chat. Também use ao final de qualquer sessão em que skills foram criadas ou editadas, para oferecer o envio das mudanças às outras máquinas.
---

# Sync de skills entre máquinas

O usuário mantém `~/.claude/skills` como clone de `https://github.com/andrevictor23-tech/claude-skills.git` em 3 máquinas.

O script também sincroniza um segundo repo: `~/Documents/DELEGACIA`, clone de `https://github.com/andrevictor23-tech/delegacia-claude-workspace.git` (**privado** — workspace institucional com CLAUDE.md aninhados). Se a pasta ainda não existir na máquina, o script clona automaticamente. O `.gitignore` desse repo é lista branca (só `.md`, mais `MODELOS-REPRESENTACAO/lexico-semente.txt`), então arquivos de casos reais na pasta nunca são enviados.

Um terceiro repo também é sincronizado: `~/.claude/skills/osint-investigacao`, clone de `https://github.com/andrevictor23-tech/osint-investigacao.git`. Ele mora **dentro** de `~/.claude/skills` para o Claude enxergar a skill; o `.gitignore` do `claude-skills` exclui essa pasta, então o `git add -A` do primeiro repo não a engole. Mesmo comportamento de clone automático caso não exista na máquina.

E um quarto: `~/.claude/scheduled-tasks`, clone de `https://github.com/andrevictor23-tech/claude-briefings.git` (**privado**, desde 30/07/2026) — as cinco rotinas de briefing agendado. O clone é o próprio local de execução, não uma cópia: é de lá que o Claude Code lê as tarefas. É privado por necessidade, não por preferência: somados, os briefings descrevem nome, cargo, comarca, e-mail, rotina de treino, carteira e concursos do usuário. Cargo e comarca de autoridade policial em repo público é risco de segurança pessoal. **Nunca torne esse repo público.**

**Atenção: `claude-skills` é público.** Nada de sigiloso pode entrar nele. Em particular, o acervo da skill `representacao-cautelar` (modelos reais, catálogo e léxico) vive **apenas** no repo privado, em `MODELOS-REPRESENTACAO/`.

## Depois de clonar numa máquina nova

O sync traz os quatro repos, mas o acervo da `representacao-cautelar` precisa ser espelhado para dentro da skill, pois lá os caminhos são ignorados pelo git. **Confira se o espelho existe mesmo numa máquina já configurada** — em 31/07/2026 uma delas tinha só o `LEIA-ME.md` em `assets/modelos/`, sem catálogo nem léxico, e a skill teria rodado sem base:

```powershell
$src = "$env:USERPROFILE\Documents\DELEGACIA\MODELOS-REPRESENTACAO"
$sk  = "$env:USERPROFILE\.claude\skills\representacao-cautelar"
Copy-Item "$src\catalogo-modelos.md" "$sk\references\" -Force
Copy-Item "$src\lexico-semente.txt"  "$sk\scripts\"    -Force
Copy-Item "$src\*.md" "$sk\assets\modelos\" -Force
Remove-Item "$sk\assets\modelos\catalogo-modelos.md" -ErrorAction SilentlyContinue
```

Se o usuário editar modelos na skill, copie-os de volta para `MODELOS-REPRESENTACAO/` antes de sincronizar: o repo privado é a fonte de verdade.

### Estado da carteira (skill `analise-carteira`)

Mesmo esquema, mesma razão: `references/estado-carteira.md` reúne posições, metas,
saldo e watchlist de tickers do André junto com nome, cargo e comarca. Não pode ir
para o `claude-skills`, que é público (está no `.gitignore` da skill desde 21/07/2026).
Fonte de verdade: `~/Documents/DELEGACIA/PESSOAL/estado-carteira.md`.

```powershell
$src = "$env:USERPROFILE\Documents\DELEGACIA\PESSOAL\estado-carteira.md"
$dst = "$env:USERPROFILE\.claude\skills\analise-carteira\references\"
Copy-Item $src $dst -Force
```

Se o usuário atualizar o estado da carteira pela skill (revisão de tese,
rebalanceamento, nova prioridade), copie de volta para `PESSOAL/` antes de sincronizar.

### CLAUDE.md global (regras pessoais)

O `~/.claude/CLAUDE.md` é distribuído entre as máquinas por espelho automático no
repo **privado**: `CONFIG-CLAUDE/CLAUDE-global.md` no `delegacia-claude-workspace`
(contém nome, cargo e comarca — jamais no `claude-skills`, que é público). O
`sync.ps1` cuida das duas direções sozinho: edição local mais nova sobe antes do
commit; versão nova vinda do pull desce para `~/.claude/`. Se as duas mudarem, o
rebase do git acusa o conflito e o sync para, como em qualquer arquivo. O nome é
`CLAUDE-global.md` de propósito, para não ser lido como instrução aninhada do
workspace. Edite qualquer uma das duas cópias e rode o sync — nada manual.

### Prompt pronto para as outras máquinas

Depois de mudar skills numa máquina, `references/prompt-outras-maquinas.md` tem um
bloco autocontido para colar no Claude Code das outras duas — sincroniza, espelha o
`estado-carteira.md` e confere se a proteção do `.gitignore` chegou.

## Extração de documentos (Docling)

As skills que leem PDF/DOCX/imagem usam um extrator comum, documentado em `references/extracao-documentos.md`. Duas peças, com destinos diferentes:

| Peça | Vai para o git? |
|---|---|
| `scripts/extrair.py` e `scripts/setup-extracao.ps1` | **Sim** |
| venv do Docling (~1,3 GB, em `~/.claude/tools/docling-venv`) | **Não** — recriado por máquina |
| Cache de extração | Não — fica no `G:\Meu Drive`, sincroniza sozinho |

**Numa máquina nova**, depois do primeiro sync:

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\setup-extracao.ps1"
```

O script copia o `extrair.py` para `~/.claude/tools/`, cria o venv e instala o Docling (~1,3 GB). Na primeira conversão com OCR baixa ~500 MB de modelos.

**Ao editar o `extrair.py`**: a fonte de verdade é a cópia no repo (`scripts/extrair.py`). Edite lá e rode o setup, ou copie para `~/.claude/tools/extrair.py` — as duas precisam ficar iguais.

## Procedimento

Execute o script pronto:

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
```

Não use `-ExecutionPolicy Bypass`: a política `RemoteSigned` do usuário já permite rodar este script local, e a flag faz o classificador de permissões bloquear a execução.

Para cada um dos quatro repos, o script faz nesta ordem:
1. **Só no `claude-skills`** (o público): portão de auditoria antes de qualquer `git add`.
2. `git add -A` + commit automático das mudanças locais (mensagem `sync: <data>`), se houver.
3. `git pull --rebase --autostash`.
4. `git push`.
5. Imprime resumo (commits recebidos, skills novas ou alteradas).

Códigos de saída: `1` erro no commit (identidade git), `2` conflito no rebase, `3` erro no push ou no clone, `4` bloqueio da auditoria.

### O portão de auditoria (só no repo público)

`Test-Publicavel` roda **antes** do `git add -A`, porque depois de publicado o estrago não se desfaz — o GitHub indexa e cacheia. Ele bloqueia o sync em dois casos:

- **(a) arquivo novo, não rastreado.** Qualquer arquivo que o repo nunca viu exige decisão consciente. Para liberar, rode com `-AllowNew` — que destrava **apenas** este caso.
- **(b) conteúdo com cara de dado sensível** nos arquivos novos ou modificados: CPF, CNPJ, número de processo CNJ, telefone, valor em reais, chave de API (`sk-`, `ghp_`, `AIza`) e chave privada PEM. Não há flag que libere: é para mover o arquivo para o repo privado e listá-lo no `.gitignore` da skill.

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1" -AllowNew
```

Os padrões são deliberadamente estreitos — falso positivo trava o sync do usuário. Por isso o portão **não substitui** a leitura do conteúdo (ver Regras); ele pega o descuido óbvio, não a tática descrita em prosa.

## Se der conflito

O script aborta o rebase automaticamente e deixa o repo como estava, imprimindo `CONFLITO` e os arquivos envolvidos. Nesse caso:
1. Mostre ao usuário quais arquivos conflitaram.
2. Pergunte qual versão ele quer manter (a desta máquina ou a do GitHub) — normalmente ele sabe qual máquina tem a versão mais nova.
3. Resolva com `git checkout --ours`/`--theirs` no arquivo, conclua o rebase e faça o push.

## Regras

- NUNCA usar `push --force`.
- `.venv/` e caches não entram no repo (já cobertos por .gitignore das skills que os têm). Se `git status` mostrar `.venv` de alguma skill, adicione ao `.gitignore` dela antes de commitar.
- O script usa `git add -A`. Antes de rodá-lo, confira `git status --porcelain --untracked-files=all` em `~/.claude/skills` e verifique se nada sob `representacao-cautelar/assets/modelos/`, `references/catalogo-modelos.md` ou `scripts/lexico-semente.txt` aparece. Se aparecer, o `.gitignore` foi quebrado: conserte antes de sincronizar, porque esse repo é público. O portão de auditoria pega o caso (a) desses arquivos por serem novos, mas não confie só nele.
- Identificadores de conta (ID de projeto Google Cloud, e-mail, número de conta) não entram em skill do repo público, nem em exemplo. Ficam no `.env` local de cada máquina, referenciados por placeholder — `{GOOGLE_CLOUD_PROJECT}`, não o valor. O portão não detecta esse tipo de vazamento.
- Auditar o **conteúdo**, não só os nomes dos arquivos: um comentário ou um resumo pode expor tática tanto quanto a peça inteira.
- Depois do sync, lembrar o usuário de rodar o sync nas outras máquinas para receber as mudanças.
