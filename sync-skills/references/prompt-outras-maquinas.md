# Prompt pronto — atualizar as outras máquinas (05/08/2026)

Copie o bloco abaixo e cole no Claude Code da outra máquina. É autocontido: não
depende do histórico da conversa em que as mudanças foram feitas.

(A versão anterior deste arquivo descrevia a migração de 21/07/2026 — portão de
auditoria e estado-carteira —, já aplicada nas três máquinas.)

---

```
Preciso atualizar esta máquina com mudanças feitas em 05/08/2026 em outra máquina
(skill nova, edições em skills existentes e um espelho novo do CLAUDE.md global).
Faça na ordem e me mostre o resultado de cada etapa:

1. SINCRONIZAR (primeira rodada)
   Rode: & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
   (sem -ExecutionPolicy Bypass). Se o portão de auditoria bloquear com "ARQUIVOS
   NOVOS (nao rastreados)" no repo público, NÃO use -AllowNew às cegas: me mostre
   a lista e o conteúdo de cada arquivo, e só rode de novo com -AllowNew depois
   que eu confirmar que nada é sigiloso.

2. CONFERIR O CLAUDE.md LOCAL ANTES DA SEGUNDA RODADA
   A partir de agora o ~/.claude/CLAUDE.md é espelhado entre as máquinas via repo
   privado (Documents\DELEGACIA\CONFIG-CLAUDE\CLAUDE-global.md). A segunda rodada
   do sync vai SOBRESCREVER o ~/.claude/CLAUDE.md desta máquina com a versão do
   repo. Antes disso, compare os dois arquivos: se o local tiver algum trecho que
   a versão do repo não tem, me mostre a diferença e PARE — decido eu.

3. SINCRONIZAR (segunda rodada)
   Rode o mesmo sync.ps1 de novo. A primeira rodada só trouxe o script novo; é
   esta que executa o espelho. Saída esperada: "CLAUDE.md global atualizado a
   partir do repo privado."

4. VERIFICAR
   - ~/.claude/CLAUDE.md deve ter a regra "4. Extensão sob medida" na seção Postura.
   - Deve existir a skill nova: ~/.claude/skills/conciso/SKILL.md
   - git log --oneline -5 em ~/.claude/skills, e me resuma o que chegou.

Contexto das mudanças que você vai receber:
- conciso (skill nova): modo de resposta direto e enxuto sob demanda (/conciso),
  porte auditado de ayghri/i-have-adhd (MIT). Não rege peças jurídicas — só a
  conversa em volta delas.
- relatorio-final-ip: nova seção "Modo análise" — "analisa esse IP" entrega
  parecer conciso em prosa, sem template nem revisão por subagente; a description
  ganhou esse gatilho.
- representacao-cautelar: no modo "vê o que cabe nesses autos", a lista de
  medidas com uma linha de justificativa é o produto inteiro do turno; peça só
  depois da confirmação.
- CLAUDE.md global: regra 4 de Postura (extensão sob medida: análise ≠ peça) e o
  espelho automático descrito no passo 2 (documentado na SKILL.md da sync-skills).
- notebooklm/scripts/auth_manager.py: passa a aceitar o domínio novo
  notebook.google.com no login (redirect recente do Google).
```

---

## Observações para quem for manter este arquivo

- Use sempre `$env:USERPROFILE`, nunca caminho absoluto: o nome de usuário difere
  entre as máquinas do André (`andre`, `PJC`).
- O passo 2 é o que realmente importa nesta migração: é a única rodada em que uma
  edição local divergente do CLAUDE.md poderia ser sobrescrita sem aviso, porque o
  script antigo (da primeira rodada) ainda não tinha o espelho. Das rodadas
  seguintes em diante, o próprio sync resolve as duas direções.
- Depois de rodar nas duas máquinas restantes, reescreva este arquivo na próxima
  migração — ele descreve sempre a migração pontual mais recente.
