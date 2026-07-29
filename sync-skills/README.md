# sync-skills

> Sincroniza as skills do Claude entre as máquinas do usuário via git, mantendo `~/.claude/skills` como clone do repo `andrevictor23-tech/claude-skills`, junto com dois repos auxiliares.

**English summary:** Keeps the user's Claude skills synchronized across three machines via git, managing ~/.claude/skills as a clone of the claude-skills repository plus two auxiliary repos.

## O que faz

Mantém três repositórios sincronizados entre as 3 máquinas do usuário por meio do script `sync.ps1`:

1. `~/.claude/skills` — clone de `andrevictor23-tech/claude-skills` (**público**, este repositório).
2. `~/Documents/DELEGACIA` — clone de `andrevictor23-tech/delegacia-claude-workspace` (**privado**, workspace institucional). O `.gitignore` é lista branca (só `.md` e o léxico), então arquivos de casos reais nunca sobem.
3. `~/Documents/OSINT` — clone de `andrevictor23-tech/osint-investigacao`.

Se um repo auxiliar ainda não existir na máquina, o script clona automaticamente. Para cada repo, o fluxo é: commit automático das mudanças locais (`sync: <data>`) → `git pull --rebase --autostash` → `git push` → resumo do que chegou e mudou. Em conflito, o rebase é abortado sem perder nada e os arquivos conflitantes são reportados para o usuário decidir qual versão manter.

A skill também documenta o **extrator comum de documentos** (Docling) usado pelas skills que leem PDF/DOCX/imagem, e o espelhamento de arquivos sensíveis que vivem apenas no repo privado (acervo da `representacao-cautelar` e `estado-carteira.md` da `analise-carteira`).

## Quando usar

A skill ativa quando o usuário:

- Pedir para sincronizar, atualizar, puxar ou enviar skills entre computadores.
- Disser "git pull das skills", "sync das skills", "atualiza minhas skills", "manda pro git", "as skills estão atualizadas?".
- Digitar comandos git relacionados a `~/.claude/skills` no chat.
- Ao final de qualquer sessão em que skills foram criadas ou editadas (para oferecer o envio às outras máquinas).

## Como usar

Exemplos de prompts:

1. "Sincroniza minhas skills."
2. "Manda essas mudanças pro git pra eu pegar na outra máquina."
3. "As skills estão atualizadas nesta máquina?"
4. "Acabei de clonar numa máquina nova, prepara o ambiente de extração de documentos."
5. "Deu conflito no sync, me ajuda a resolver."

Comando principal executado pela skill:

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
```

(Sem `-ExecutionPolicy Bypass`: a política `RemoteSigned` já permite o script local, e a flag faz o classificador de permissões bloquear a execução.)

## O que a skill entrega

- Os três repos commitados, rebased e enviados ao GitHub, com resumo de commits recebidos e skills novas/alteradas.
- Em máquina nova: clone automático dos repos auxiliares, espelhamento do acervo privado para dentro das skills e setup do extrator via `setup-extracao.ps1`.
- Em caso de conflito: diagnóstico dos arquivos, escolha guiada da versão (`--ours`/`--theirs`) e conclusão do rebase.
- Prompt autocontido (`references/prompt-outras-maquinas.md`) para colar no Claude Code das outras máquinas após uma rodada de mudanças.

## Estrutura da pasta

- `SKILL.md` — instruções completas: repos, procedimento, resolução de conflitos, espelhamento de arquivos sensíveis e regras de segurança.
- `scripts/sync.ps1` — script de sincronização dos três repos, com varredura de padrões sensíveis (CPF etc.) no repo público antes do push.
- `scripts/extrair.py` — extrator universal de documentos (PDF nativo ou escaneado, DOCX, XLSX, PPTX, HTML, imagens) para Markdown, com cache; usa PyMuPDF para texto nativo e Docling/EasyOCR para OCR local. Nenhum dado sai da máquina.
- `scripts/setup-extracao.ps1` — prepara o ambiente de extração na máquina (copia o `extrair.py` para `~/.claude/tools/`, cria o venv e instala o Docling, ~1,3 GB; o venv não vai para o git).
- `references/extracao-documentos.md` — referência compartilhada de extração usada pelas demais skills.
- `references/prompt-outras-maquinas.md` — bloco pronto para atualizar as outras máquinas.

## Requisitos

- **git** configurado com acesso aos repos `andrevictor23-tech` no GitHub.
- **PowerShell** (Windows) para `sync.ps1` e `setup-extracao.ps1`.
- **Python** para o extrator (`extrair.py`), com venv do Docling criado pelo `setup-extracao.ps1` (~1,3 GB; primeira conversão com OCR baixa ~500 MB de modelos).

## Avisos

- **`claude-skills` é público: nada sigiloso pode entrar nele.** O acervo da skill `representacao-cautelar` (modelos reais, catálogo, léxico) e o `estado-carteira.md` da `analise-carteira` vivem apenas no repo privado, que é a fonte de verdade; nas skills, esses caminhos são ignorados pelo git e apenas espelhados por cópia.
- Antes de rodar o sync, conferir `git status --porcelain --untracked-files=all`: se algo sob `representacao-cautelar/assets/modelos/`, `references/catalogo-modelos.md` ou `scripts/lexico-semente.txt` aparecer, o `.gitignore` foi quebrado — consertar antes de sincronizar.
- Auditar o **conteúdo**, não só os nomes: um comentário ou resumo pode expor tática tanto quanto a peça inteira.
- **Nunca** usar `push --force`. `.venv/` e caches não entram no repo.
- Após o sync, lembrar de rodar o script nas outras máquinas para receber as mudanças.
