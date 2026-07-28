# desempenho

> Painel HTML autocontido dos estudos: taxa de erro por disciplina, motivos de erro e prioridade de revisão ponderada pelo peso de cada matéria na prova.

**English summary:** A self-contained HTML dashboard for exam preparation. It cross-references the mistakes logged by hand in the review wiki with the ones exported from the interactive quizzes, then charts error rate by subject, error causes and a revision priority weighted by each subject's share of the actual exam.

## O que faz

Não pede nenhum dado novo: o painel é montado a partir do que o fluxo de estudo
já produz — `wiki/revisao/erros.md` (erros documentados à mão) e os bancos e
exports de erros em `quiz-data/` (gerados pela `simulado-quiz` e pela
`treino-wiki`).

O `build_dashboard.py` cruza as duas fontes e gera um HTML offline, tema escuro,
com:

- **KPIs**: questões únicas no acervo, questões respondidas em quizzes com
  export, erros exportados, erros documentados na wiki e a disciplina prioritária;
- **Taxa de erro por disciplina**, considerando como respondidas as questões dos
  quizzes cujo resultado foi exportado;
- **Prioridade de revisão** = (erros da wiki + erros de quiz) × **peso da
  disciplina na prova objetiva** — é o gráfico que responde "por onde eu começo";
- **Motivo dos erros** classificado em distração, pegadinha, jurisprudência,
  desconhecimento e outro;
- **Padrões recorrentes** e a tabela de erros da wiki com o fundamento correto
  para revisar.

O valor da skill não é o HTML: é a **leitura**. Depois de gerar, o Claude entrega
no chat um diagnóstico curto — disciplina mais crítica pela prioridade ponderada,
motivo de erro dominante e a ação concreta (qual nota revisar, ou disparar um
`treino-wiki` na disciplina crítica).

## Quando usar

- "Dashboard", "painel de estudos", "como estou indo"
- "Análise de desempenho", "estatísticas dos simulados", "taxa de acerto"
- "Onde estou errando mais", "prioridade de revisão"

Não é esta skill: responder questões (`simulado-quiz`, `treino-wiki`) nem
registrar um erro novo (edite o `erros.md` direto).

## Como usar

1. "Gera o dashboard dos estudos"
2. "Como estou indo nos simulados?"
3. "Onde estou errando mais, considerando o peso da prova?"
4. "Painel de estudos e me diz por onde começar a revisão"

## O que a skill entrega

- **`Dashboard - Desempenho MPSP.html`** em `quiz-data/` (fica no Drive,
  sincroniza entre as máquinas): autocontido, abre offline no navegador, sem
  dependência externa. Use `--out` para outro caminho.
- **Diagnóstico no chat**, em 3–5 frases, com a ação sugerida.

## Estrutura da pasta

```
desempenho/
├── SKILL.md                       # instruções da skill (fluxo, leitura, manutenção)
└── scripts/
    └── build_dashboard.py         # erros.md + quiz-data/ → HTML autocontido
```

## Requisitos

- Python 3 (só biblioteca padrão).
- Pasta de estudos com `quiz-data/` (bancos e exports) e, idealmente,
  `wiki/revisao/erros.md`.

## Avisos

- A taxa de erro só considera respondidos os bancos citados em algum export de
  erros: **quiz feito sem exportar o resultado não conta**.
- Erros anotados só no `erros.md`, sem export correspondente, contam para
  prioridade e motivos, mas não para a taxa por banco.
- Export que cita uma questão inexistente nos bancos de `quiz-data/` entra como
  "não vinculado" e o script avisa quantos foram — costuma ser banco faltando,
  não erro de conta.
- Os pesos por disciplina são constante (`PESOS`) no `build_dashboard.py`,
  calibrados para a prova objetiva do MPSP 97º (100 questões). Mudou o alvo
  (MP-MT, outro edital)? Atualize a constante — não invente peso no chat.
