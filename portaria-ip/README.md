# portaria-ip

> Corpo da portaria de instauração de inquérito policial e de ofícios requisitórios no padrão da Delegacia de Alta Floresta/MT, para colar no sistema da PJC.

**English summary:** Drafts the body text of Brazilian police inquiry opening orders (portarias) and direct-request letters (ofícios requisitórios) in the house style of a Civil Police unit in Mato Grosso. The official system adds header, numbering and digital signature, so the skill outputs only the text. It separates what the police authority may request directly (subscriber data, log preservation) from what requires a court order, and routes the latter to `representacao-cautelar`.

## Modos

1. **Portaria de instauração** — dois modelos reais sanitizados: notícia de crime (denúncia anônima, BO, relatório) e derivada de outro procedimento (traslado, RIF, inteligência). A portaria abre e determina providências cartorárias; diligências investigativas vêm em despacho posterior.
2. **Ofício requisitório** — dados cadastrais e preservação de registros, com fundamento por hipótese, campos por destinatário e advertência correta.

## Estrutura

- `SKILL.md` — fluxo dos dois modos e autoverificação.
- `references/modelos-portaria.md` — modelos A e B com a fraseologia da casa.
- `references/oficios-requisitorios.md` — corpo do ofício, fundamentos, preservação, campos por destinatário, canal e prazo.
- `evals/evals.json` — quatro casos fictícios.

## Sigilo

Modelos sanitizados: sem nomes, CPFs, números de procedimento ou contatos reais. Este repositório é público. Processamento sempre local.
