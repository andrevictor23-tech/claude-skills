---
paths:
  - "*/assets/**"
  - "*/references/**"
  - "*/evals/**"
  - "*/templates/**"
---

# Sigilo — material de apoio das skills (assets, references, evals, templates)

Este repositório é PÚBLICO e faz push automático a cada sessão (Stop hook). As pastas cobertas por esta rule são as que carregam exemplos, modelos e casos de teste — o lugar mais provável de um vazamento acidental.

## Antes de criar ou editar qualquer arquivo aqui

1. **Nenhum dado de caso real.** Nomes de investigados, vítimas ou testemunhas, CPFs, CNPJs, contas, telefones, números de IP/ocorrência/processo reais são proibidos, mesmo "só de exemplo". Exemplo se inventa, nunca se copia de auto.
2. **Ficção se declara.** Todo arquivo com dados de aparência realista (CSVs de eval, casos de teste, modelos preenchidos) deve estar coberto por um LEIA-ME ou nota declarando que os dados são 100% fictícios.
3. **A barreira existe e não se contorna.** O `scan-sigilo.sh` bloqueia o commit quando encontra padrão de CPF/CNPJ/processo/IP/telefone fora da allowlist (`.claude/sigilo-allowlist.txt`). Se o bloqueio disparar sobre dado fictício legítimo, o caminho é o humano revisar e adicionar o arquivo à allowlist — nunca desabilitar o scanner, alterar seus padrões para "passar", ou fazer commit manual por fora do sync.
4. **Allowlist é ato do Delegado.** Não adicionar linhas à allowlist por iniciativa própria: apresentar o caso ao usuário e aguardar a decisão.
5. **Acervo real mora no repo privado** (`delegacia-claude-workspace`). Modelos brutos da `representacao-cautelar` e qualquer material derivado de caso real não entram aqui nem "temporariamente" — o push automático não perdoa rascunho esquecido.

Na dúvida entre agilidade e sigilo, o sigilo prevalece: pergunte antes de gravar.
