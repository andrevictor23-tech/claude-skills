# revisao-espacada

> Sistema de revisão espaçada e caderno de erros para estudo de concursos: registra cada questão errada, agenda revisões em intervalos crescentes e reforça o ponto fraco na hora certa.

## O que faz

Transforma os erros de questões e simulados em um sistema de estudo guiado por
dado. Cada questão errada vira um item rastreável em um caderno de erros em
Markdown; a skill agenda quando revisar e, na revisão, explica o ponto errado e
gera questões novas sobre o tema (no estilo da banca-alvo, ex.: FGV para MPMT,
CEBRASPE certo/errado para Cartório TJMT).

Os intervalos são fixos e crescentes, por nível (1 a 5): **1, 3, 7, 15 e 30
dias**. Acertar na revisão sobe um nível (espaça mais); errar reseta para o
nível 1 (revisa amanhã de novo). Após acertar no nível 5, o item é marcado como
dominado e sai da fila ativa. Toda a matemática de datas e a leitura/escrita do
caderno ficam a cargo de `scripts/revisao.py` (comandos `add`, `due`, `list`,
`revisar`, `stats`, sempre com saída em JSON que a skill traduz para linguagem
natural).

## Quando usar

- "Errei essa questão", "anota no caderno de erros", "registra esse erro"
- "O que tenho para revisar hoje?", "minha revisão de hoje", "bora revisar"
- "O que cai mais?", "quais matérias eu mais erro?", "como está meu caderno?"
- Colar uma questão com gabarito comentado para arquivar
- Pedir questões novas sobre temas que vem errando

## Como usar

1. "Errei essa questão: [cola a questão e o gabarito]" → registra no caderno,
   informando ID e data da primeira revisão.
2. "O que tenho para revisar hoje?" → roda a revisão do dia: para cada item
   vencido, explicação do ponto errado + 2-3 questões inéditas; depois da sua
   resposta, o resultado é registrado e o nível ajustado.
3. "Quais matérias eu mais erro?" → estatística por matéria, em tabela, com
   leitura estratégica de onde concentrar o estudo.
4. "Registra esses 3 erros do simulado de hoje" → registro em lote.

## O que a skill entrega

- **Conversa no chat**: explicações dos pontos errados (ancoradas no fundamento
  legal), questões novas com gabarito comentado após a sua resposta, e
  fechamento da sessão (quantos itens revisados, quantos subiram de nível).
- **Caderno de erros** (`caderno-erros.md`): arquivo Markdown que serve de
  banco de dados — cada erro é um bloco `<!-- ERRO id=NNNN -->`, com matéria,
  assunto, questão, "errei porque" e resposta correta. Por ser texto puro, pode
  ser versionado em Git, lido no celular ou usado como fonte no NotebookLM.

## Instalação no Claude Code

1. Copie a pasta `revisao-espacada/` para o diretório de skills do seu projeto
   (ex.: `.claude/skills/revisao-espacada/`) ou para `~/.claude/skills/`.
2. Crie um arquivo `caderno-erros.md` na pasta do seu projeto de estudo
   (use o `caderno-erros-exemplo.md` como base; pode apagar o erro de exemplo).
3. Pronto. É só conversar normalmente.

## Estrutura da pasta

```
revisao-espacada/
├── SKILL.md                    # instruções da skill (fluxos, regras, intervalos)
├── README.md                   # este arquivo
├── caderno-erros-exemplo.md    # modelo do banco de dados (caderno de erros)
└── scripts/
    └── revisao.py              # motor de datas e intervalos (add/due/list/revisar/stats)
```

## Requisitos

- Python 3 (já vem no ambiente do Claude Code). Sem bibliotecas externas.
- Um `caderno-erros.md` no seu projeto de estudo (criado na instalação acima).

## Avisos

- **Nunca edite datas ou níveis manualmente** no caderno — sempre pelo script
  `revisao.py`, para não corromper o agendamento.
- As explicações e questões geradas devem ser conferidas com a fonte original
  (lei, súmula, doutrina); a skill sinaliza quando estiver incerta sobre um
  fundamento em vez de inventar citação.
