# Prompt pronto — atualizar as outras máquinas (21/07/2026)

Copie o bloco abaixo e cole no Claude Code da outra máquina. É autocontido: não
depende do histórico da conversa em que as mudanças foram feitas.

---

```
Preciso atualizar esta máquina com as mudanças de skills feitas em 21/07/2026 em outra
máquina. Faça na ordem e me mostre o resultado de cada etapa:

1. SINCRONIZAR
   Rode: & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"

   O sync.ps1 agora tem um portão de auditoria no repo claude-skills (que é PÚBLICO).
   Se ele bloquear com "ARQUIVOS NOVOS (nao rastreados)", NÃO use -AllowNew às cegas:
   me mostre a lista e o conteúdo de cada arquivo primeiro. Só depois de eu confirmar
   que nenhum é sigiloso é que você roda de novo com -AllowNew.

2. ESPELHAR O ESTADO DA CARTEIRA
   O arquivo references/estado-carteira.md da skill analise-carteira deixou de ser
   versionado no claude-skills (repo público) porque reúne meu perfil financeiro com
   meu nome, cargo e comarca. A fonte de verdade passou para o repo privado. Copie:

   Copy-Item "$env:USERPROFILE\Documents\DELEGACIA\PESSOAL\estado-carteira.md" "$env:USERPROFILE\.claude\skills\analise-carteira\references\" -Force

   Se o arquivo de origem não existir, o repo privado não sincronizou — verifique o
   passo 1 antes de seguir.

3. CONFERIR A PROTEÇÃO
   Confirme que o arquivo existe localmente MAS não está rastreado pelo git:

   cd "$env:USERPROFILE\.claude\skills"
   Test-Path "analise-carteira\references\estado-carteira.md"   # deve dar True
   git ls-files --error-unmatch analise-carteira/references/estado-carteira.md

   O último comando DEVE falhar ("did not match any file"). Se ele ENCONTRAR o
   arquivo, o .gitignore da skill não veio no sync: me avise antes de sincronizar
   qualquer coisa, porque o próximo `git add -A` publicaria meus dados.

4. ME AVISAR
   Resuma o que mudou nas skills (git log --oneline -5) e confirme os passos 2 e 3.

Contexto das mudanças que você vai receber:
- notebooklm/SKILL.md: nova seção sobre custo de tokens. Regra: para PERGUNTAR ao
  notebook, usar sempre o script ask_question.py via Bash, nunca automação de browser
  MCP (que custou ~14k tokens numa sessão real). Browser MCP só para gerenciar fontes.
- analise-carteira/.gitignore (novo): bloqueia o estado-carteira.md.
- sync-skills/scripts/sync.ps1: portão de auditoria do repo público (bloqueia arquivo
  novo não classificado e varre CPF, CNPJ, processo CNJ, telefone, valores em reais,
  chaves de API e chaves privadas). Também troquei $ErrorActionPreference de 'Stop'
  para 'Continue', porque avisos normais do git no stderr abortavam o sync no meio.
```

---

## Observações para quem for manter este arquivo

- Use sempre `$env:USERPROFILE`, nunca caminho absoluto: o nome de usuário difere
  entre as máquinas do André (`andre`, `PJC`).
- O passo 3 é o que realmente importa. Se o `.gitignore` da skill `analise-carteira`
  não tiver chegado, a máquina volta a correr o risco de publicar o arquivo no
  próximo `git add -A`.
- Depois de rodar em todas as máquinas, este arquivo pode ser apagado — descreve uma
  migração pontual, não um procedimento recorrente.
