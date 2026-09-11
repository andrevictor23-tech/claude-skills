# Prompt pronto — publicar trabalho preso numa máquina (11/09/2026)

Copie o bloco abaixo e cole no Claude Code da máquina **onde o trabalho foi
feito**. É autocontido: não depende do histórico da conversa em que o problema
foi diagnosticado.

Contexto desta migração: em 11/09/2026 constatou-se que skills editadas numa
máquina (`despacho-plantao`, `representacao-cautelar`) nunca chegaram ao GitHub,
e que **sub-agente nenhum jamais atravessou máquina** — `~/.claude/agents` é
pasta irmã de `~/.claude/skills` e não era coberta por repositório algum. O
espelho `CONFIG-CLAUDE/agents/` no repositório privado passou a existir nesta
data para fechar o buraco.

(A versão anterior deste arquivo descrevia a instalação do hook `SessionStart`,
de 07/08/2026, já aplicada nas três máquinas.)

---

```
Tenho trabalho não publicado nesta máquina: editei as skills despacho-plantao e
representacao-cautelar (talvez outras) e criei um sub-agente revisor. Nada disso
chegou ao GitHub — conferi da outra máquina e TODAS as branches remotas do
claude-skills estão paradas em 17/08/2026. Publique daqui.

Siga na ordem e me mostre o resultado de cada etapa. Não pule etapa e não
prossiga se algo divergir do descrito.

1. LEVANTAR ANTES DE MEXER
   git -C "$env:USERPROFILE\.claude\skills" status --porcelain --untracked-files=all
   git -C "$env:USERPROFILE\.claude\skills" log --oneline -5
   Get-ChildItem "$env:USERPROFILE\.claude\agents" -ErrorAction SilentlyContinue
   Quero ver o tamanho do estrago antes de qualquer commit.

2. AUDITAR O CONTEÚDO — o claude-skills é PÚBLICO
   Antes de commitar, me mostre o `git diff` completo das skills modificadas e o
   conteúdo integral de cada arquivo novo. Procure especificamente: nome de
   investigado, CPF, número de processo, nome de operação, endereço, telefone e
   fraseologia que revele tática operacional (canais de cooperação com
   provedores, sistemas internos de inteligência, medidas de bloqueio de dados).
   Achando qualquer uma dessas coisas, PARE e me diga: aquilo vai para o
   repositório privado, não para o público.

3. PUBLICAR AS SKILLS
   & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
   Não use -ExecutionPolicy Bypass (faz o classificador de permissões bloquear).

   O portão de auditoria deve barrar com código 4 e a mensagem "ARQUIVOS NOVOS
   (nao rastreados)" — é o comportamento correto quando criei arquivo. Só rode de
   novo com -AllowNew depois que eu tiver aprovado a etapa 2. Se o bloqueio for
   por conteúdo suspeito (CPF, processo, chave), NÃO existe flag: me avise.

   Este sync também traz o conserto do caminho do workspace privado: o script
   agora procura o clone em Documents\DELEGACIA, Meu Drive\DELEGACIA e
   My Drive\DELEGACIA, em vez de assumir o primeiro.

4. O SUB-AGENTE — ele NÃO sobe sozinho
   Sub-agente mora em ~/.claude/agents/, pasta IRMÃ de ~/.claude/skills. Nenhum
   dos quatro repositórios do sync cobre esse caminho, então a etapa 3 não o
   levou. Faça à mão:

   a) Me mostre o conteúdo integral de cada .md em ~/.claude/agents/.
   b) Descubra qual caminho do workspace privado existe aqui (Documents\DELEGACIA
      ou Meu Drive\DELEGACIA). Se já existir CONFIG-CLAUDE\agents\ lá, siga em
      frente. Se NÃO existir, crie você mesmo: a pasta CONFIG-CLAUDE\agents e,
      no .gitignore do workspace — que é lista branca, ignora tudo e libera item
      a item —, a linha  !CONFIG-CLAUDE/agents/*.md  logo depois da linha
      !CONFIG-CLAUDE/CLAUDE-global.md. Sem essa linha o git ignora os agentes em
      silêncio e você vai achar que publicou.
   c) Copy-Item "$env:USERPROFILE\.claude\agents\*.md" "<workspace>\CONFIG-CLAUDE\agents\" -Force
   d) git -C "<workspace>" status --porcelain --untracked-files=all
      Os agentes TÊM que aparecer na lista. O .gitignore de lá é lista branca: se
      não aparecerem, estão sendo ignorados em silêncio — pare e me avise.
   e) Rode o sync de novo para publicar.

5. CONFIRMAR QUE SAIU MESMO
   Para cada um dos quatro repositórios (~/.claude/skills, o workspace privado,
   ~/.claude/skills/osint-investigacao, ~/.claude/scheduled-tasks):
   git -C "<repo>" fetch --quiet origin
   git -C "<repo>" rev-list --left-right --count origin/main...HEAD
   Tem que dar "0   0" em todos. Qualquer número à direita significa commit que
   não foi empurrado — o problema que originou tudo isto.
```

---

## Observações para quem mantiver este arquivo

- Use `$env:USERPROFILE` no corpo dos comandos, nunca caminho absoluto: o nome de
  usuário difere entre as máquinas do André (`andre`, `PJC`).
- A etapa 4 é manual de propósito. Um espelho automático de `~/.claude/agents`
  dentro do `sync.ps1` (nos moldes do `CLAUDE-global.md`) é o próximo passo
  natural, mas ainda não foi escrito — enquanto não for, agente novo exige a
  cópia à mão, nas duas direções.
- A ordem das etapas 3 e 4 importa: é o sync da etapa 3 que traz do repositório
  privado a pasta `CONFIG-CLAUDE/agents/` e a liberação correspondente no
  `.gitignore`. Copiar o agente antes disso faz o git ignorá-lo sem avisar.
- Reescreva este arquivo na próxima migração — ele descreve sempre a mais recente.
