# sabatina

> Entrevista socrática pergunta a pergunta: sabatina você sobre um plano, peça, decisão ou funcionalidade até haver entendimento compartilhado — e só então parte para a execução.

**English summary:** A relentless Socratic interviewer: before anything is produced (a legal draft, code, a plan), it questions the user one question at a time until there is genuine shared understanding, and only then hands off to execution.

## O que faz

Antes de produzir qualquer coisa (peça jurídica, código, plano), a skill
conduz uma entrevista sem pressa e sem complacência, guiada por um princípio:
**o erro mais caro não é executar mal, é executar bem a coisa errada.**

O método:

- **Uma pergunta por vez** — nada de rajada de perguntas; cada resposta
  determina a próxima.
- **Toda pergunta vem com recomendação** — a skill apresenta a opção que
  adotaria e por quê, para você confirmar, corrigir ou refinar.
- **Fato é dela, decisão é sua** — o que dá para descobrir sozinha (autos,
  arquivos, repositório, lei, jurisprudência) ela pesquisa antes de perguntar;
  tese, estratégia, escopo e risco ficam com você.
- **Desce a árvore de decisões** — resolve primeiro as decisões que
  condicionam as outras, persegue respostas vagas e confronta premissas
  frágeis (registra a discordância uma vez, com motivo, e depois acata).
- **Nada é produzido antes da confirmação** — a sabatina termina com uma
  síntese do entendimento compartilhado, e só após o seu "ok" explícito começa
  a execução (ou a skill propõe qual outra skill assume, ex.:
  `relatorio-final-ip`, `despacho-plantao`).

Detecta sozinha se o assunto é **jurídico/investigativo** (fato, autoria,
tipificação, medida cabível, objetivo real, riscos, sigilo e limites) ou
**técnico/código** (problema real, escopo, comportamento observável, casos de
borda, integração, persistência, critério de pronto) e adapta os ramos de
perguntas.

## Quando usar

- "Me sabatina", "me questiona", "me interroga", "grill me"
- "Pergunta tudo que precisar antes de escrever"
- "Quero pensar melhor nisso", "me ajuda a fechar essa ideia"
- "Estressa esse plano", "me faz as perguntas"
- Antes de peça jurídica complexa (representação cautelar, relatório final de
  inquérito, despacho difícil) ou de funcionalidade não trivial em código
- Sempre que a ideia estiver crua, ambígua ou com decisões em aberto

Não é para pedidos já completos e sem ambiguidade, nem para tarefas mecânicas
de execução direta.

## Como usar

1. "Me sabatina antes de eu escrever essa representação de prisão preventiva"
2. "Quero criar uma automação para os relatórios da delegacia. Estressa esse
   plano antes de codar."
3. "Tenho uma ideia crua de funcionalidade, me faz as perguntas até fecharmos
   o escopo"
4. "Antes de redigir o relatório final desse IP, pergunta tudo que precisar"

## O que a skill entrega

Tudo acontece **no chat**: a sequência de perguntas (cada uma com
recomendação), o fechamento dos ramos de decisão e, ao final, a **síntese do
entendimento compartilhado** — o que foi decidido, com que fundamento, e o que
ficou deliberadamente de fora. A execução em si (peça, código) só vem depois
da sua confirmação, nesta skill ou na skill especializada indicada.

## Estrutura da pasta

```
sabatina/
└── SKILL.md    # instruções completas da skill (não há arquivos auxiliares)
```

## Requisitos

Nenhum além do Claude Code.

## Avisos

- A skill não encerra a sabatina sozinha: só você declara que houve
  entendimento compartilhado.
- Adaptada do `/grilling` de Matt Pocock (mattpocock/skills, MIT), apoiado na
  ideia de *design tree* de Frederick Brooks (*The Design of Design*),
  reescrita para o contexto jurídico/investigativo e técnico do usuário.
