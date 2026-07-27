# vocabulario-kindle

> Transforma o Vocabulary Builder do Kindle (`vocab.db`) em um baralho Anki de inglês incremental, com repetição espaçada, recall ativo e as frases reais dos livros lidos.

**English summary:** Turns the Kindle Vocabulary Builder database (vocab.db) into an incremental English Anki deck with spaced repetition, active recall and the real sentences from the books the user actually read.

## O que faz

Quando você consulta uma palavra no dicionário do Kindle, o aparelho grava a
palavra e a frase exata do livro em `vocab.db`. Esta skill mantém, a partir
desse banco, um baralho Anki incremental:

1. **Extrai** as palavras novas do `vocab.db` para um `vocab-master.json`
   acumulado (idempotente: reprocessar o mesmo banco nunca duplica).
2. **Enriquece** as palavras pendentes: o Claude gera tradução PT-BR concisa e
   definição simples em inglês, sempre no sentido usado no livro (lê os
   exemplos do master antes de traduzir).
3. **Gera** o arquivo `.apkg` do Anki, com 2 cartões por palavra:
   **Reconhecimento** (palavra + frase do livro → tradução/definição) e
   **Produção** (frase com lacuna + dica em PT → palavra), aplicando *sentence
   mining* — o contexto pessoal da leitura fixa melhor que exemplo genérico.

Palavras marcadas como dominadas no próprio Kindle (category=100) ficam fora do
baralho (a flag `--incluir-dominadas` reverte). Só entram palavras em inglês
(`lang='en'`); o banco também guarda consultas em PT, que são ignoradas.

## Quando usar

- "Atualiza meu vocabulário do Kindle"
- "Novas palavras do Kindle", "puxa as palavras novas" (com o Kindle plugado)
- "Gera o baralho de inglês", "anki do kindle"
- Qualquer menção a `vocab.db`, Vocabulary Builder ou flashcards/cartões de
  inglês a partir das leituras

## Como usar

1. "Pluguei o Kindle, atualiza meu vocabulário"
2. "Gera o baralho de inglês com as palavras novas"
3. "Anki do Kindle: puxa o vocab.db dos Downloads e atualiza o baralho"
4. "Tem palavra pendente de tradução no meu vocabulário? Enriquece e regenera
   o baralho"

A skill procura o `vocab.db` no Kindle plugado via USB
(`<letra>:\system\vocabulary\vocab.db`) ou em uma cópia em
`Downloads\vocab.db`.

## O que a skill entrega

- **Baralho Anki**: `Kindle Vocabulario EN.apkg`, salvo em
  `<Meu Drive>/vocabulario-kindle/` (sincroniza entre as máquinas). Importar
  por duplo clique no Anki desktop, ou via AnkiWeb no AnkiDroid/AnkiMobile.
  Baralho: `Ingles::Kindle Vocabulario`. Reimportar **atualiza os cartões sem
  duplicar e sem perder o progresso de revisão** (GUIDs estáveis por palavra);
  a repetição espaçada em si fica a cargo do Anki (FSRS).
- **`vocab-master.json`**: fonte de verdade acumulada das palavras e
  enriquecimentos (sobrevive mesmo se o `vocab.db` do Kindle for resetado).

## Estrutura da pasta

```
vocabulario-kindle/
├── SKILL.md                       # instruções da skill (método, fluxo, regras)
└── scripts/
    ├── extract_vocab.py           # vocab.db → vocab-master.json (incremental) + lista de pendentes
    ├── apply_enrichment.py        # aplica traduções/definições geradas (só preenche os null)
    └── generate_anki.py           # vocab-master.json → .apkg (requer genanki)
```

## Requisitos

- Python 3 (extração e enriquecimento usam só a biblioteca padrão, incl.
  sqlite3).
- Biblioteca `genanki` para gerar o `.apkg` (`python -m pip install genanki`).
- Arquivo de entrada: `vocab.db` do Kindle (via USB ou cópia em Downloads).
- Anki (desktop ou mobile) para importar e revisar o baralho.

## Avisos

- `MODEL_ID` e `DECK_ID` em `generate_anki.py` nunca devem mudar — mudar
  duplica o baralho inteiro no seu Anki.
- Não edite `vocab-master.json` manualmente fora do fluxo da skill.
- Frases vindas de sumário/índice do livro geram cartões ruins: se um cartão
  estiver estranho, corrija o campo `exemplos` da palavra no master e regenere.
- Confira as traduções/definições geradas — elas são produzidas pelo Claude a
  partir do contexto do livro e podem precisar de ajuste fino.
