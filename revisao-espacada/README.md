# revisao-espacada

Skill de revisão espaçada e caderno de erros para concursos.

## O que faz
Registra cada questão que você erra, agenda revisões em intervalos crescentes
(1, 3, 7, 15 e 30 dias) e, na hora de revisar, explica o ponto que você errou e
gera questões novas sobre o tema.

## Instalação no Claude Code
1. Copie a pasta `revisao-espacada/` para o diretório de skills do seu projeto
   (ex.: `.claude/skills/revisao-espacada/`) ou para `~/.claude/skills/`.
2. Crie um arquivo `caderno-erros.md` na pasta do seu projeto de estudo
   (use o `caderno-erros-exemplo.md` como base; pode apagar o erro de exemplo).
3. Pronto. É só conversar normalmente.

## Como usar (linguagem natural)
- "Errei essa questão: [cola a questão e o gabarito]" → registra no caderno.
- "O que tenho para revisar hoje?" → roda a revisão do dia.
- "Quais matérias eu mais erro?" → estatística por matéria.

## Requisitos
- Python 3 (já vem no ambiente do Claude Code). Sem bibliotecas externas.

## Estrutura
```
revisao-espacada/
├── SKILL.md                    # instruções da skill
├── README.md                   # este arquivo
├── caderno-erros-exemplo.md    # modelo do banco de dados
└── scripts/
    └── revisao.py              # motor de datas e intervalos
```
