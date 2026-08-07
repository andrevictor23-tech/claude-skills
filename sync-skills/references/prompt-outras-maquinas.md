# Prompt pronto — atualizar as outras máquinas (07/08/2026)

Copie o bloco abaixo e cole no Claude Code da outra máquina. É autocontido: não
depende do histórico da conversa em que as mudanças foram feitas.

(A versão anterior deste arquivo descrevia a migração de 05/08/2026 — skill
`conciso` e espelho do CLAUDE.md global —, já aplicada nas três máquinas.)

---

```
Preciso aplicar nesta máquina as mudanças feitas em 07/08/2026 em outra máquina:
o sync das skills passou a rodar sozinho na abertura do Claude Code, via hook
SessionStart. Faça na ordem e me mostre o resultado de cada etapa:

1. SINCRONIZAR
   Rode: & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
   (sem -ExecutionPolicy Bypass). Se o portão de auditoria bloquear com "ARQUIVOS
   NOVOS (nao rastreados)" no repo público, NÃO use -AllowNew às cegas: me mostre
   a lista e o conteúdo de cada arquivo, e só rode de novo com -AllowNew depois
   que eu confirmar que nada é sigiloso.

   Isso traz: scripts/auto-sync.ps1 (novo), sync.ps1 com o modo -PullOnly, e a
   SKILL.md da sync-skills documentando o hook.

2. CONFERIR O CLAUDE.md GLOBAL
   O ~/.claude/CLAUDE.md é espelhado entre as máquinas pelo repo privado. A regra
   5 da seção Postura (modo conciso) tinha duas redações divergentes e foi fundida
   em 07/08/2026. Depois do sync, o ~/.claude/CLAUDE.md desta máquina deve conter,
   na regra 5: "resposta primeiro, prosa enxuta, zero preâmbulo e zero fecho, sem
   tabelas nem seções salvo pedido expresso". Se estiver diferente, me mostre a
   diferença e PARE — decido eu.

3. INSTALAR O HOOK
   Edite ~/.claude/settings.json (não substitua o arquivo: preserve tudo que já
   existe) acrescentando a chave "hooks" no nível raiz:

   "hooks": {
     "SessionStart": [
       {
         "hooks": [
           {
             "type": "command",
             "command": "powershell.exe",
             "args": ["-NoProfile", "-File", "<CAMINHO>"],
             "asyncRewake": true,
             "timeout": 300,
             "rewakeSummary": "Conflito no sync das skills",
             "statusMessage": "Sincronizando skills..."
           }
         ]
       }
     ]
   }

   <CAMINHO> é absoluto e com barras normais — o nome de usuário do Windows muda
   de máquina para máquina, então descubra o valor real desta antes de escrever:
   rode `$env:USERPROFILE` e monte
   <USERPROFILE com barras normais>/.claude/skills/sync-skills/scripts/auto-sync.ps1

   NÃO use "shell": "powershell" — essa opção aponta para o pwsh (PowerShell 7),
   que pode não existir aqui; o hook silenciosamente nunca rodaria.

4. TESTAR
   - Valide o JSON:
     Get-Content "$env:USERPROFILE\.claude\settings.json" -Raw | ConvertFrom-Json |
       Select-Object -ExpandProperty hooks | ConvertTo-Json -Depth 6
   - Rode a invocação exata do hook, forçando fora da trava de tempo:
     powershell.exe -NoProfile -File "<CAMINHO>" -Force
   - Mostre o fim de ~/.claude/auto-sync.log e me diga o que cada repo reportou.
     Repo com mudança local não commitada aparece como "PULADO" — é o esperado.
   - Rode a invocação de novo SEM -Force e confirme que o log não cresceu (prova
     de que a trava de 4h funciona).

O hook só entra em vigor na próxima abertura do Claude Code.

Contexto do que muda:
- O automático SÓ RECEBE (sync.ps1 -PullOnly): nunca commita, nunca empurra e
  pula repo com mudança pendente. Enviar continua ato deliberado meu, porque o
  claude-skills é público.
- Trava de 4h por carimbo em ~/.claude/.last-auto-sync, tocado antes do sync —
  também evita corrida entre sessões abertas ao mesmo tempo.
- Conflito de rebase sai com código 2 e acorda a sessão (asyncRewake); erro de
  rede ou credencial fica só no log.
```

---

## Observações para quem for manter este arquivo

- Use sempre `$env:USERPROFILE` no corpo dos comandos, nunca caminho absoluto: o
  nome de usuário difere entre as máquinas do André (`andre`, `PJC`). A única
  exceção é o `args` do hook, que não passa por shell e por isso não expande
  variável — daí o passo 3 mandar descobrir o valor real antes de escrever.
- O passo 2 existe porque a regra 5 do CLAUDE.md nasceu com duas redações em
  máquinas diferentes e conflitou no rebase de 07/08/2026. Se a máquina em que o
  prompt for colado tiver a redação perdedora e um `LastWriteTime` mais novo,
  o espelho pode tentar subir a versão errada — daí conferir antes.
- Depois de rodar nas duas máquinas restantes, reescreva este arquivo na próxima
  migração — ele descreve sempre a migração pontual mais recente.
