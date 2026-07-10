---
name: vocabulario-kindle
description: Transforma o Vocabulary Builder do Kindle (vocab.db) em baralho Anki de inglês com repetição espaçada, recall ativo e frases reais dos livros lidos. Use SEMPRE que o usuário pedir para atualizar o vocabulário do Kindle, "atualiza meu vocabulário", "novas palavras do Kindle", "gera o baralho de inglês", "anki do kindle", mencionar vocab.db, Vocabulary Builder, palavras que consultou no Kindle, ou pedir flashcards/cartões de inglês a partir das leituras. Ative também quando o usuário plugar o Kindle e pedir para puxar as palavras novas.
---

# Vocabulário do Kindle → Anki (inglês)

O usuário lê no Kindle e consulta palavras no dicionário; o Kindle grava tudo em
`vocab.db` (palavra + frase exata do livro). Esta skill mantém um baralho Anki
incremental a partir desse banco. Dados ficam em `<Meu Drive>/vocabulario-kindle/`
(sincroniza entre as máquinas; nesta máquina é `C:\Users\andre\Meu Drive`, em
outras pode ser `G:\Meu Drive` — os scripts detectam sozinhos).

## Método (não mudar sem pedido do usuário)

- **Repetição espaçada**: o Anki agenda as revisões (FSRS). Meta do plano de
  transição: 10 min/dia (item "Anki" da Fase 1; uso leve é permitido antes).
- **Recall ativo + cloze**: cada palavra gera 2 cartões — Reconhecimento
  (palavra + frase do livro → tradução/definição) e Produção (frase com lacuna
  + dica em PT → palavra).
- **Sentence mining**: a frase do cartão é a frase REAL do livro onde o usuário
  tropeçou na palavra — contexto pessoal fixa melhor que exemplo genérico.
- Palavras marcadas como **dominadas no próprio Kindle** (category=100) ficam
  fora do baralho (flag `--incluir-dominadas` reverte).

## Fluxo de atualização (quando o usuário pedir)

O `vocab.db` vem do Kindle plugado via USB (`<letra>:\system\vocabulary\vocab.db`)
ou de uma cópia em `Downloads\vocab.db`. Os scripts procuram nos dois lugares.

### 1. Extrair (incremental, nunca duplica)

```powershell
python "$env:USERPROFILE\.claude\skills\vocabulario-kindle\scripts\extract_vocab.py"
```

Atualiza `vocab-master.json` e imprime `LISTA_PENDENTES` (palavras novas sem
tradução). Reprocessar o mesmo vocab.db é seguro (idempotente).

### 2. Enriquecer as pendentes (trabalho do Claude)

Para cada stem em `LISTA_PENDENTES`, gere tradução PT-BR concisa e definição
simples em inglês (estilo learner's dictionary). **Leia os `exemplos` da palavra
no `vocab-master.json` e traduza no sentido usado no livro** (acepção do
contexto primeiro, outras depois). Salve como JSON no scratchpad:

```json
{ "stem": {"traducao": "...", "definicao": "..."}, ... }
```

Depois aplique (nunca sobrescreve enriquecimento existente, só preenche os null):

```powershell
python "$env:USERPROFILE\.claude\skills\vocabulario-kindle\scripts\apply_enrichment.py" --file <arquivo.json>
```

### 3. Gerar o baralho

```powershell
python "$env:USERPROFILE\.claude\skills\vocabulario-kindle\scripts\generate_anki.py"
```

Gera `<Meu Drive>/vocabulario-kindle/Kindle Vocabulario EN.apkg`. Requer
`genanki` (`python -m pip install genanki` se faltar).

### 4. Instruir o usuário

Importar o `.apkg` no Anki (duplo clique, ou AnkiDroid/AnkiMobile via AnkiWeb).
**Reimportar atualiza os cartões sem duplicar e sem perder o progresso de
revisão** (GUIDs estáveis por palavra). Baralho: `Ingles::Kindle Vocabulario`.

## REGRAS INEGOCIÁVEIS

1. `MODEL_ID` e `DECK_ID` em `generate_anki.py` NUNCA mudam — mudar duplica o
   baralho inteiro no Anki do usuário.
2. Só palavras `lang='en'` entram (o banco também tem centenas em PT — ignorar).
3. Não editar `vocab-master.json` na mão fora do fluxo acima; ele é a fonte de
   verdade acumulada (o vocab.db do Kindle pode ser resetado, o master não).
4. Frases de exemplo vindas de sumário/índice do livro geram cartões ruins —
   se o usuário reclamar de um cartão, corrija o campo `exemplos` da palavra no
   master e regenere.
