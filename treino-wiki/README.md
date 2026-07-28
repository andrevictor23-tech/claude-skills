# treino-wiki

> Revisão relâmpago com perguntas inéditas geradas a partir das suas próprias notas de estudo, com correção imediata, placar e registro automático dos erros.

**English summary:** Rapid-fire revision drills built from the user's own study notes (not from exam PDFs): fresh true/false questions in the chat, one at a time, with immediate correction, running score and automatic logging of every miss back into the review wiki.

## O que faz

Gera perguntas objetivas **inéditas** a partir das notas de `wiki/disciplinas/*.md`
da pasta de estudos. A fonte é sempre a wiki — nunca PDFs de simulado (para isso
existe a `simulado-quiz`).

O formato padrão é **certo/errado**, difícil, no estilo VadeFocus: afirmações
plausíveis com um defeito preciso, para serem respondidas em segundos. A mira é
calibrada pelos seus erros já documentados em `wiki/revisao/erros.md`:

- ~40% no padrão de erro dominante (ex.: requisito acrescido, pares simétricos
  com atributos trocados);
- ~30% jurisprudência de véspera da nota (Informativos, Temas, Súmulas com
  citação exata);
- ~30% lei seca da disciplina.

Toda pergunta precisa ter **fundamento citável vindo da nota**. Se a nota não dá
o fundamento, a pergunta é trocada — a skill não inventa questão sobre fato não
verificável na wiki.

Dois modos:

- **Chat** (padrão): uma pergunta por vez, correção imediata com ✅/❌ e o
  fundamento em 1–3 linhas, placar parcial a cada 5 perguntas e diagnóstico final
  de qual pegadinha te derrubou.
- **HTML**: monta o banco em `quiz-data/treino-wiki-<tema>.json` e gera um quiz
  interativo com o gerador da `simulado-quiz`.

Em qualquer modo, **os erros viram registro**: cada um é gravado em
`wiki/revisao/erros.md`, na seção da disciplina, com a fonte `Treino Wiki DD/MM`.
Padrão novo que se repita entra em "Padrões recorrentes".

## Quando usar

- "Treino intensivo", "revisão relâmpago", "perguntas rápidas"
- "Me testa em Penal", "gera questões novas de Tutela Coletiva"
- "Quiz da wiki", "treino de véspera"
- Qualquer pedido de questões inéditas sobre conteúdo que você já estudou

Não é esta skill: questões extraídas de PDF de simulado (`simulado-quiz`),
arguição aprofundada de banca (`prova-oral`).

## Como usar

1. "Treino intensivo de Processo Penal, 15 perguntas"
2. "Revisão relâmpago, mix geral"
3. "Me testa no que eu mais erro"
4. "Gera um quiz HTML de Infância e Juventude a partir da wiki"

A skill pergunta em uma única mensagem a disciplina (ou "mix geral"), a
quantidade (padrão: 10) e o modo (chat ou HTML) — e já começa.

## O que a skill entrega

- **No modo chat**: a bateria de perguntas, o placar final com taxa de acerto e
  um diagnóstico curto do padrão de erro dominante.
- **No modo HTML**: `Quiz - Treino Wiki - <tema>.html` autocontido em
  `quiz-data/` (fica no Drive, sincroniza entre as máquinas), mais o banco
  `treino-wiki-<tema>.json` no mesmo esquema dos bancos C/E existentes.
- **Sempre**: as entradas novas em `wiki/revisao/erros.md` — que alimentam o
  dashboard da `desempenho` e o baralho da `anki`.

## Estrutura da pasta

```
treino-wiki/
└── SKILL.md                       # instruções da skill (fontes, calibragem, modos)
```

Sem scripts próprios: o modo HTML reaproveita o `generate_quiz.py` da
`simulado-quiz`.

## Requisitos

- Pasta de estudos com `wiki/disciplinas/*.md` preenchida — a qualidade das
  perguntas é a qualidade das suas notas.
- Para o modo HTML: Python 3 e a skill `simulado-quiz` instalada (o gerador de
  quiz vem dela).

## Avisos

- A skill nunca abre PDFs. Se o conteúdo não está na wiki, ele não vira pergunta.
- Perguntas sem fundamento citável na nota são descartadas, não "aproximadas" —
  se a bateria vier mais curta que o pedido, é sinal de nota incompleta.
- O registro em `erros.md` é feito ao final da sessão; se você abandonar o treino
  no meio, os erros daquela rodada não são gravados.
