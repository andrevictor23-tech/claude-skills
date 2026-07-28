# anki

> Transforma os erros comprovados dos estudos — exports de quiz e a wiki de revisão — em um baralho Anki incremental, com um subbaralho por disciplina.

**English summary:** Turns proven study mistakes (quiz result exports plus the hand-written review wiki) into an incremental Anki deck, one subdeck per subject, so spaced repetition works only on what the user actually got wrong.

## O que faz

O ciclo de estudo já produzia os dados certos e os deixava morrer num painel:
`simulado-quiz` e `treino-wiki` geram os erros, `desempenho` mostra onde eles
pesam mais na prova. Esta skill fecha o ciclo e leva esses erros para a memória
de longo prazo:

1. **Coleta** as lacunas: lê os exports de quiz (`quiz-data/*-resultado.json` e o
   formato antigo `*-erros.json`), cruza com os bancos de questões para
   recuperar enunciado, gabarito e comentário do espelho, lê
   `wiki/revisao/erros.md` e acumula tudo em `quiz-data/anki-master.json`
   (idempotente: rodar de novo nunca duplica).
2. **Escreve os cartões**: o Claude lê as lacunas pendentes — já ordenadas por
   prioridade (vezes errada × peso da disciplina na prova) — e redige
   pergunta/resposta atômicas, cobrando o fundamento que teria evitado o erro.
3. **Gera** o `.apkg` com um subbaralho por disciplina (`Concurso::Penal`,
   `Concurso::Processo Penal`, ...), com o rodapé de cada cartão apontando para a
   nota da wiki onde revisar o assunto.

O princípio é o filtro: **só vira cartão o que você comprovadamente errou**.
Ankificar material inteiro produz baralho grande e inútil — você acaba revisando
o que a IA achou importante, e não o que você não sabe.

## Quando usar

- "Gera meus flashcards", "manda os erros pro Anki", "ankifica isso"
- "Baralho de revisão", "flashcards do simulado", "cartões do Anki"
- "Quero revisar no Anki o que errei"
- Depois de um simulado ruim, quando a pergunta for como fixar o que errou

Não é esta skill: vocabulário de inglês do Kindle (`vocabulario-kindle`),
responder questões (`simulado-quiz`, `treino-wiki`), ver estatísticas
(`desempenho`).

## Como usar

1. "Fiz o simulado 12 e exportei o resultado — manda os erros pro Anki"
2. "Gera os flashcards só de Penal"
3. "Tem lacuna pendente de cartão? Escreve e regenera o baralho"
4. "Esse erro aqui não vale cartão, descarta"

## O que a skill entrega

- **Baralho Anki**: `Concurso - Lacunas.apkg`, salvo em `quiz-data/` (fica no
  Drive, sincroniza entre as máquinas). Importar por duplo clique no Anki
  desktop, ou via AnkiWeb no AnkiDroid/AnkiMobile. Reimportar **atualiza os
  cartões sem duplicar e sem perder o progresso de revisão** (GUIDs estáveis por
  lacuna); o agendamento da repetição espaçada fica a cargo do Anki (FSRS).
- **`anki-master.json`**: fonte de verdade acumulada das lacunas e dos cartões
  escritos (sobrevive mesmo se os exports de quiz forem apagados).

## Estrutura da pasta

```
anki/
├── SKILL.md                       # instruções da skill (princípio, fluxo, regras)
└── scripts/
    ├── coletar_lacunas.py         # quizzes + erros.md → anki-master.json + lista de pendentes
    ├── apply_cards.py             # aplica os cartões escritos pelo Claude (só preenche os null)
    └── generate_anki.py           # anki-master.json → .apkg por disciplina (requer genanki)
```

## Requisitos

- Python 3 (coleta e aplicação usam só a biblioteca padrão).
- Biblioteca `genanki` para gerar o `.apkg` (`python -m pip install genanki`).
- Pasta de estudos com `quiz-data/` (bancos + exports) e, opcionalmente,
  `wiki/revisao/erros.md`.
- Anki (desktop ou mobile) para importar e revisar o baralho.

## Avisos

- `MODEL_ID`, `DECK_BASE` e a **ordem** da tupla `DISCIPLINAS` em
  `generate_anki.py` nunca devem mudar — mexer duplica os baralhos no seu Anki.
  Disciplina nova entra no fim da tupla.
- Não edite `anki-master.json` manualmente fora do fluxo da skill.
- Erro de quiz cuja questão não está em nenhum banco de `quiz-data/` fica de
  fora; o script avisa quantos foram.
- `--link-local` põe link `file://` para a nota da wiki no rodapé do cartão:
  funciona no Anki do PC, não no celular. Por isso é opt-in.
- Confira os cartões gerados — a pergunta e a resposta são redigidas pelo Claude
  a partir do comentário do espelho e podem precisar de ajuste fino.
