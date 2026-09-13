# Prompt pronto — catálogo OSINT Brazuca na skill osint-investigacao (13/09/2026)

Copie o bloco abaixo e cole no Claude Code das **outras máquinas**. É
autocontido: não depende do histórico da conversa em que a mudança foi feita.

Contexto desta migração: em 13/09/2026 a skill `osint-investigacao` passou a
integrar o catálogo OSINT Brazuca (commit `eea0e79`), com o script
`scripts/busca_brazuca.py` e a referência `references/osint-brazuca.md`. O
catálogo em si **não vem pelo git**: é clonado em `OSINT-tools/osint-brazuca/`
por máquina, e o `.gitignore` da skill ganhou `/OSINT-tools/` para o auto-sync
não engolir o repositório aninhado.

(A versão anterior deste arquivo, de 11/09/2026, publicava skills e o sub-agente
revisor presos numa máquina; já aplicada nas três máquinas.)

---

```
Atualizei a skill osint-investigacao em outra máquina: ela agora integra o
catálogo OSINT Brazuca (commit eea0e79 no repo osint-investigacao). Traga a
atualização e instale o catálogo aqui. Siga na ordem, me mostre o resultado de
cada etapa e pare se algo divergir.

1. SINCRONIZAR
   & "$env:USERPROFILE\.claude\skills\sync-skills\scripts\sync.ps1"
   Não use -ExecutionPolicy Bypass. Se barrar por arquivo novo ou conflito, me
   avise antes de qualquer outra ação.

2. CONFERIR QUE A VERSÃO CHEGOU
   git -C "$env:USERPROFILE\.claude\skills\osint-investigacao" log --oneline -1
   Tem que mostrar eea0e79 (ou commit posterior). Confira também que existem
   scripts\busca_brazuca.py e references\osint-brazuca.md, e que o .gitignore
   da skill termina com a linha  /OSINT-tools/

3. INSTALAR O CATÁLOGO (não vem pelo git, é clonado por máquina)
   cd "$env:USERPROFILE\.claude\skills\osint-investigacao"
   python scripts\busca_brazuca.py --instalar
   Se "python" não existir, tente "py".

4. TESTAR
   python scripts\busca_brazuca.py --busca imei
      -> deve trazer 1 fonte 🟢 (aparelho impedido, ABR Telecom)
   python scripts\busca_brazuca.py --busca desaparecidos --uf MT
      -> deve trazer o portal da PJC-MT
   python scripts\busca_brazuca.py --input cpf --incluir-vedadas
      -> deve listar 4 fontes 🔴 (força bruta de CPF, CPF Validador TRT3,
         e-CAC, Meu INSS); sem a flag, nenhuma 🔴 pode aparecer

5. CONFIRMAR QUE O CATÁLOGO NÃO VAZA PARA O REPO PÚBLICO
   git -C "$env:USERPROFILE\.claude\skills\osint-investigacao" status --porcelain --untracked-files=all
   Tem que sair vazio. Se aparecer qualquer coisa sob OSINT-tools/, pare e me
   avise: o repositório é público e tem auto-sync.
```

---

## Observações para quem mantiver este arquivo

- Use `$env:USERPROFILE` no corpo dos comandos, nunca caminho absoluto: o nome de
  usuário difere entre as máquinas do André (`andre`, `PJC`).
- As contagens da etapa 4 dependem do catálogo: se o OSINT Brazuca incluir ou
  remover fontes, os números podem mudar sem que haja erro. Divergência só na
  presença de 🔴 sem `--incluir-vedadas` é defeito real.
- Espelho automático de `~/.claude/agents` no `sync.ps1` segue pendente: agente
  novo ainda exige cópia à mão para `CONFIG-CLAUDE/agents/` no repo privado.
- Reescreva este arquivo na próxima migração — ele descreve sempre a mais recente.
