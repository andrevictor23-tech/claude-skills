---
name: portaria-ip
description: 'Redige o corpo da portaria de instauração de inquérito policial e de ofícios requisitórios no padrão da Delegacia de Alta Floresta/MT, prontos para colar no sistema da PJC. Use ao pedir a portaria ("instaura o IP", "baixa a portaria") ou ofício de requisição direta (dados cadastrais, preservação de registros) a Google, Meta, operadora, banco ou órgão, e quando a despacho-plantao concluir pela instauração. Não use para o despacho de plantão (despacho-plantao) nem para pedido ao juiz (representacao-cautelar).'
---

# Portaria de IP e Ofícios Requisitórios

Skill que redige duas peças da rotina do Delegado:

1. **Portaria de instauração de inquérito policial**;
2. **Ofício requisitório**: o que a autoridade policial pede diretamente, sem ordem judicial.

O usuário é o Delegado Titular. A skill entrega o **corpo do texto** para colar no sistema da PJC, que gera cabeçalho, numeração, data de expedição e assinatura digital. Nunca reproduza esses elementos.

Fecha o ciclo com as irmãs: `despacho-plantao` decide instaurar, esta skill materializa a portaria e as requisições diretas, `representacao-cautelar` leva ao juiz o que tem reserva de jurisdição, `relatorio-final-ip` encerra.

## Princípio que rege tudo

**A portaria abre; não investiga.** Na prática da unidade, a portaria narra a notícia, capitula em tese, nomeia os investigados conhecidos e determina providências **cartorárias** iniciais (juntada, autuação, certificação, sigilo). As diligências investigativas vêm depois, em despacho, com os autos conclusos. Portaria com rol de diligências e ofícios embutidos é modelo de outra casa.

**O ofício pede só o que a lei deixa pedir, a quem pode responder.** Cada campo requisitado precisa existir no destinatário e caber na requisição direta. Campo copiado de modelo de outro provedor, ou dado com reserva de jurisdição, devolve resposta vazia ou recusa.

Fato ausente vira `[VERIFICAR]` ou pergunta. Nome, CPF, número de procedimento, data, IP, conta: só o que veio do usuário ou dos autos.

## Sigilo

Processamento local. Nenhum dado do procedimento vai a serviço externo, nem para "conferir" legislação. Dispositivo a conferir recebe `[CONFERIR EXTERNAMENTE]` e o usuário decide.

## Modo 1 — Portaria de instauração

### Passo 1 — Identificar origem e elementos

Leia o material (BO, despacho, denúncia anônima, relatório de investigação, RIF, peças de outro IP). PDF passa antes pelo extrator local (`~/.claude/tools/extrair.py`); leia o `.md`. Extraia:

| Elemento | Onde entra |
|---|---|
| Fonte da notícia (BO, denúncia anônima, relatório, RIF, traslado) | Parágrafo de origem |
| Fatos e indícios, com data e local | Narrativa |
| Capitulação em tese | Parágrafo "Considerando" |
| Investigados conhecidos, com CPF quando houver | Parágrafo "Considerando" |
| Bem jurídico atingido | Fecho do "Considerando" |
| Documentos a juntar | Providências |

Inciso do art. 5º do CPP: **I** quando de ofício (padrão da unidade); **II** quando por requisição do juiz ou do Ministério Público, ou a requerimento do ofendido. Na dúvida, pergunte.

### Passo 2 — Escolher o modelo

Os modelos estão em `references/modelos-portaria.md`:

- **A — Notícia de crime** (BO, denúncia anônima, relatório de investigação): narrativa curta, providência de juntada, autos conclusos.
- **B — Derivada de outro procedimento** (traslado de peças, RIF difundido em outro IP, relatórios de inteligência): ordem de autuação das peças, certificação de origem, tramitação restrita quando houver inteligência financeira.

### Passo 3 — Capitular

- Capitulação sempre **em tese**, com artigo e lei.
- Verifique se o dispositivo está vigente. Armadilha recorrente: fraude em licitação pelo art. 90 da Lei 8.666/93, revogado pela Lei 14.133/2021. Hoje são os arts. 337-E a 337-P do CP.
- Havendo duas capitulações defensáveis (ex.: organização criminosa x associação criminosa), apresente as duas ao usuário com uma linha de fundamento cada e recomende uma. Não escolha em silêncio.
- Autoria desconhecida: "praticado por pessoa(s) a apurar".

### Passo 4 — Redigir

Siga a fraseologia do modelo escolhido. Narrativa em terceira pessoa, impessoal, com "em tese" ao atribuir conduta ou qualificar fato. Providências numeradas, todas dirigidas ao Escrivão. Encerramento: autos conclusos e "CUMPRA-SE.".

### Passo 5 — Autoverificar

- [ ] Nenhum cabeçalho, número de portaria ou bloco de assinatura digital no texto.
- [ ] Inciso do art. 5º coerente com a origem.
- [ ] Toda capitulação com artigo e lei, vigente, e "em tese".
- [ ] Todo investigado nominado consta do material; CPF só se veio dos autos.
- [ ] Providências só cartorárias; diligência investigativa ficou para despacho posterior ou para as Notas.
- [ ] Datas e números de procedimento conferidos contra o material.
- [ ] Nenhum `[VERIFICAR]` esquecido sem menção nas Notas.

## Modo 2 — Ofício requisitório

### Passo 1 — Separar requisição direta de reserva de jurisdição

Antes de redigir, classifique cada dado pedido. A tabela de referência é a seção 0 de `representacao-cautelar/references/quebra-sigilo.md` (fonte única; leia lá). Em resumo: **dados cadastrais** (qualificação, filiação, endereço) e **pedido de preservação de registros** vão por ofício; **registros de conexão e de acesso, conteúdo, localização, extratos e movimentação** vão ao juiz.

Dado com reserva de jurisdição vira aviso ao usuário e encaminhamento para a `representacao-cautelar`, nunca linha do ofício.

### Passo 2 — Montar pelo destinatário

Use `references/oficios-requisitorios.md`: modelo de corpo, fundamento por hipótese, campos por tipo de destinatário e canal de resposta.

Pontos que mais derrubam ofício:

- **Fundamento específico.** Cite o dispositivo da hipótese do caso, não a lei inteira.
- **Advertência correta.** Pedido de não notificar o usuário se apoia no sigilo do inquérito (art. 20 do CPP). Ameaça penal só cabe em investigação de organização criminosa: recusa ou omissão de dados requisitados é o art. 21 da Lei 12.850/13; embaraço à investigação, o art. 2º, § 1º, da mesma lei. A Lei 12.830/13 não tipifica crime.
- **Identificação por IP.** Exige IP, **porta lógica de origem**, data, hora e fuso horário. Sem a porta, o IP compartilhado (CGNAT) não individualiza o assinante.
- **Campos do destinatário certo.** Operadora não tem "ID do roteador Starlink"; Google não tem "endereço de instalação".
- **Período sem colchetes.** Período, prazo e identificadores preenchidos; campo de modelo esquecido vira `[VERIFICAR]` nas Notas.

### Passo 3 — Autoverificar

- [ ] Cada dado pedido cabe em requisição direta.
- [ ] Fundamento específico e vigente para a hipótese.
- [ ] Advertência compatível com o crime investigado.
- [ ] Identificadores completos (IP com porta, data, hora e fuso; e-mail; número com DDD).
- [ ] Campos existentes no destinatário.
- [ ] Prazo e canal de resposta indicados.

## Formato de saída

1. **O texto**, em bloco limpo, pronto para colar no sistema.
2. **Notas ao Delegado**, fora do texto e curtas: premissas assumidas, `[VERIFICAR]` pendentes, capitulação alternativa, dados que exigem representação judicial e diligências sugeridas para o despacho seguinte.

Pedido com vários destinatários: um ofício por destinatário, em sequência.

## Limites

- Não decide se instaura: isso é a `despacho-plantao`. Se o pedido chegar sem decisão de instaurar e o caso for duvidoso (atipicidade, falta de representação), diga isso em uma linha antes de redigir.
- Não redige aditamento de portaria nem ofício a juízo: o primeiro ainda não tem modelo real da unidade; o segundo é `representacao-cautelar`.
- Não substitui a conferência do Delegado antes de assinar no sistema.
