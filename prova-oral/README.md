# prova-oral

> Simulador de banca examinadora de prova oral: sorteio de ponto, arguição pergunta a pergunta, follow-up de pressão, espelho de resposta e nota por questão.

**English summary:** An oral-exam board simulator for Brazilian public prosecutor and legal career exams. It draws a topic, questions the candidate one question at a time in real board style, applies pressure follow-ups, and only then delivers the model answer, a score per question and a written record of every weakness.

## O que faz

Simula a arguição oral dos concursos do Ministério Público (foco: MPSP 97º e
MP-MT). Durante a sessão você é tratado como **candidato**, e a postura é de
banca real: formal, sóbria, sem elogio fácil e sem hostilidade.

O conteúdo sai da sua pasta de estudos — começa pelo `wiki/indice.md` (disciplinas,
pesos e notas disponíveis), tira os temas de `wiki/disciplinas/*.md` e, quando
existe, do edital em `converted_markdown/`. Cerca de **1/3 das perguntas é
calibrado pelos seus pontos fracos** documentados em `wiki/revisao/erros.md`: a
banca real explora hesitação, e aqui se explora a fraqueza já registrada.

A sessão segue o rito:

1. **Configuração** numa única pergunta: disciplina (ou sorteio livre), duração
   (padrão: bloco de 5 perguntas) e nível de pressão (padrão: banca real).
2. **Sorteio do ponto**, anunciado como banca.
3. **Arguição**: uma pergunta por vez, encadeada do geral ao específico
   ("O que é X?" → "E a posição do STF?" → "Mas e se [variação fática]?"), com
   **follow-up de pressão** — que vem inclusive quando a resposta está certa,
   porque a banca testa firmeza. Sem correção no meio do bloco.
4. **Espelho e nota**: ao fim do bloco, a resposta esperada com citação exata
   (artigo, súmula, tema, Informativo), o que você disse, e nota 0–10 por
   pergunta com critério explícito, mais o diagnóstico de conteúdo × postura.
5. **Registro de fraquezas**: toda pergunta com nota menor que 7 vira entrada em
   `wiki/revisao/erros.md`, com o motivo real — desconhecimento, imprecisão ou
   insegurança sob pressão.

## Quando usar

- "Prova oral", "simula a banca", "me argui", "arguição oral"
- "Sorteia um ponto", "me toma o ponto", "treino para a oral"
- Preparação para a fase oral de concurso jurídico

Não é esta skill: planejamento de peças e decisões (`sabatina`), questões
objetivas rápidas (`treino-wiki`).

## Como usar

1. "Simula a banca em Tutela Coletiva"
2. "Prova oral, sorteio livre, bloco de 10 perguntas"
3. "Me toma o ponto de improbidade, pressão máxima"
4. "Treino para a oral no que eu mais erro"

Dica que a própria skill sugere: use o ditado do Windows (`Win+H`) para responder
falando, como na prova real — a oral se perde tanto por postura quanto por
conteúdo.

## O que a skill entrega

- **A arguição em si**, no chat, em ritmo de banca.
- **Espelho de resposta** por pergunta, com fundamento citável no padrão das
  notas da wiki.
- **Nota 0–10 por questão**, média do bloco e diagnóstico curto.
- **Entradas novas em `wiki/revisao/erros.md`** — que alimentam o dashboard da
  `desempenho` e o baralho da `anki`.

## Estrutura da pasta

```
prova-oral/
└── SKILL.md                       # instruções da skill (fontes, rito, postura de banca)
```

Sem scripts: a sessão inteira acontece no chat, sobre as notas da wiki.

## Requisitos

- Pasta de estudos com `wiki/indice.md` e `wiki/disciplinas/*.md` preenchidos —
  a banca só cobra o que está nas suas notas.
- `wiki/revisao/erros.md` (opcional, mas é o que calibra a mira nas fraquezas).

## Avisos

- A skill não corrige durante o bloco, de propósito. O feedback vem no espelho,
  como na prova real — não estranhe o silêncio avaliativo.
- O follow-up de pressão sobre resposta certa é intencional: ceder a ele conta
  como falha de postura no diagnóstico.
- "Não sei" é registrado e a banca segue adiante, sem entregar a resposta na
  hora; ela aparece no espelho ao fim do bloco.
- As notas 0–10 são estimativas de treino, calibradas pelas suas anotações — não
  são régua oficial de banca nenhuma.
