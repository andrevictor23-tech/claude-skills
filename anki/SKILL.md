---
name: anki
description: Transforma os erros comprovados dos estudos (exports de quiz em quiz-data/*-resultado.json + wiki/revisao/erros.md) em baralho Anki incremental com repetição espaçada, um subbaralho por disciplina. Use SEMPRE que o usuário pedir "gera meus flashcards", "manda os erros pro Anki", "cartões do Anki", "ankifica isso", "baralho de revisão", "flashcards do simulado", "quero revisar meus erros no Anki", ou mencionar Anki, .apkg, repetição espaçada e cartões de estudo para concurso. Ative também depois de um quiz ruim, quando o usuário perguntar como fixar o que errou. Não use para o vocabulário de inglês do Kindle (skill vocabulario-kindle) nem para responder questões (simulado-quiz/treino-wiki).
---

# Erros → Anki (concurso)

Fecha o ciclo do estudo: `simulado-quiz` e `treino-wiki` produzem os erros,
`desempenho` mostra onde eles doem mais — esta skill transforma esses mesmos
erros em memória de longo prazo.

Trabalha na **pasta de estudos** (a que contém `wiki\` e `quiz-data\`). O Drive
monta em caminho diferente por máquina (`G:\Meu Drive\VS CODE TESTE\` ou
`C:\Users\<user>\Meu Drive\VS CODE TESTE\`): descubra o caminho real antes de
montar comandos; abaixo ele aparece como `<pasta de estudos>`.

## Princípio (não mudar sem pedido do usuário)

**Só vira cartão o que ele comprovadamente errou.** Gerar cartão de material
inteiro ("ankifica esse PDF") produz baralho grande e inútil: o usuário revisa
o que a IA achou importante, não o que ele não sabe. A lista de erros já existe
e é o melhor filtro possível — use-a.

Decorre daí:

- **Um cartão por lacuna**, não por questão. Questão de prova tem 5 alternativas
  e 3 pegadinhas; o cartão cobra **o fundamento que teria evitado o erro**.
- **Nunca decore o gabarito** ("questão 37 é letra C" não serve para nada).
- O parser **não escreve cartão** — quem escreve é você (Claude), lendo o
  enunciado e o comentário do espelho. Cartão gerado por regex fica ruim.

## Fluxo (quando o usuário pedir)

### 1. Coletar as lacunas

```powershell
python "$env:USERPROFILE\.claude\skills\anki\scripts\coletar_lacunas.py" `
  --base "<pasta de estudos>" `
  --pendentes "<scratchpad>\pendentes.json"
```

Lê os exports de quiz (`*-resultado.json` e o formato antigo `*-erros.json`),
cruza com os bancos para recuperar enunciado/gabarito/comentário do espelho, lê
`wiki/revisao/erros.md` e atualiza `quiz-data/anki-master.json`. Idempotente:
rodar de novo não duplica nem apaga cartão já escrito.

O arquivo `pendentes.json` sai **ordenado por prioridade** (vezes errada × peso
da disciplina na prova) e limitado (`--limite-pendentes`, padrão 40) — leia ele,
não o master inteiro.

### 2. Escrever os cartões (trabalho do Claude)

Para cada lacuna pendente, escreva `pergunta` + `resposta` (e `extra` quando
houver fundamento legal a registrar). Regras de formulação:

- **Atômico**: uma ideia por cartão. Se o fundamento tem quatro requisitos,
  ou faça quatro cartões, ou pergunte pelo critério que distingue os casos.
- **Autossuficiente**: a pergunta tem de fazer sentido sozinha, meses depois,
  sem a questão do lado. Nada de "na alternativa C, por quê?".
- **Resposta curta**: uma linha. O que não couber vai em `extra`.
- **Cobre o que ele errou**, não o tema inteiro. Se ele confundiu prescrição da
  pretensão punitiva com a executória, o cartão é sobre a distinção.
- `extra`: artigo, súmula, tese de repetitivo, ou o porquê da pegadinha.

Salve no scratchpad e aplique:

```json
{ "simulado-12#37": {"pergunta": "...", "resposta": "...", "extra": "..."} }
```

```powershell
python "$env:USERPROFILE\.claude\skills\anki\scripts\apply_cards.py" `
  --base "<pasta de estudos>" --file "<scratchpad>\cartoes.json"
```

Nunca sobrescreve cartão existente (o usuário pode tê-lo ajustado à mão);
`--forcar` reverte. Lacuna que não merece cartão: `--descartar <id>`.

### 3. Gerar o baralho

```powershell
python "$env:USERPROFILE\.claude\skills\anki\scripts\generate_anki.py" `
  --base "<pasta de estudos>"
```

Gera `quiz-data/Concurso - Lacunas.apkg` com um subbaralho por disciplina
(`Concurso::Penal`, `Concurso::Processo Penal`, ...). Requer `genanki`
(`python -m pip install genanki` se faltar). `--disciplina Penal` gera só uma.

### 4. Instruir o usuário

Importar no Anki (duplo clique, ou AnkiDroid/AnkiMobile via AnkiWeb).
**Reimportar atualiza os cartões sem duplicar e sem perder o progresso de
revisão** (GUIDs estáveis por lacuna). Diga quantos cartões novos entraram e em
que disciplina se concentraram — se bater com a disciplina prioritária do
`desempenho`, vale mencionar.

## REGRAS INEGOCIÁVEIS

1. `MODEL_ID`, `DECK_BASE` e a ordem da tupla `DISCIPLINAS` em `generate_anki.py`
   NUNCA mudam — mexer duplica os baralhos no Anki do usuário. Disciplina nova
   entra **no fim** da tupla.
2. Não edite `anki-master.json` na mão fora dos scripts; ele é a fonte de verdade
   acumulada (os exports de quiz podem sumir, o master não).
3. Nada de cartão a partir de lacuna sem fundamento no espelho — sem base, o
   cartão ensina errado. Marque `--descartar` ou peça o fundamento ao usuário.
4. O campo `Fonte` é para voltar à origem, não para estudar: mantenha curto.

## Limitações honestas (não esconda do usuário)

- Erro de quiz sem banco correspondente em `quiz-data/` fica de fora (o script
  avisa quantos) — falta o banco, não é bug.
- `--link-local` põe link `file://` para a nota da wiki: funciona no Anki do PC,
  não no celular. Por isso é opt-in.
- O baralho só cresce com o que ele errou: se parar de exportar resultado dos
  quizzes, ele para de crescer.
