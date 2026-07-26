# instagram-autoridade

> Análise estratégica do perfil de Instagram de Delegado de Polícia Civil, com relatório HTML imprimível e dashboard interativo, usando dados reais do Windsor.ai.

## O que faz

Atua como estrategista de comunicação pública institucional: coleta métricas reais do Instagram via conector Windsor.ai (MCP), produz diagnóstico estratégico do perfil e gera dois materiais em HTML com identidade visual institucional (azul escuro `#1a2744`, dourado `#c8a96e`).

O fluxo passa por: identificação do perfil e período (padrão: últimos 30 dias, com confirmação do usuário), coleta de métricas gerais (seguidores, alcance, impressões, engajamento), métricas por publicação e por tipo de conteúdo (Reel, Carrossel, Foto, Story), análise das melhores e piores publicações, consistência de publicação e recomendações estratégicas. Dados ausentes no Windsor.ai nunca são inventados ou estimados — são listados explicitamente na seção de limitações.

Toda a análise é submetida a salvaguardas específicas de comunicação de autoridade policial (ver Avisos).

## Quando usar

A skill ativa quando o usuário pedir:

- Análise do Instagram, relatório de desempenho ou métricas de redes sociais.
- Evolução de seguidores, engajamento, alcance ou melhores publicações.
- Diagnóstico estratégico de conteúdo ou avaliação de presença digital institucional.
- Frases como "analisa meu Instagram", "como está meu perfil", "gera o relatório do Instagram", "quero ver minhas métricas", "dashboard do Instagram".

## Como usar

Exemplos de prompts:

1. "Analisa meu Instagram dos últimos 30 dias."
2. "Gera o relatório do Instagram de junho."
3. "Quero o dashboard com as métricas do perfil no último trimestre."
4. "Quais foram minhas melhores publicações do mês e por quê?"
5. "Como está o crescimento de seguidores comparado ao período anterior?"

Se o handle ou o período não forem informados, a skill usa o perfil padrão configurado no Windsor e os últimos 30 dias, confirmando antes de prosseguir.

## O que a skill entrega

1. `relatorio-instagram-[AAAA-MM].html` — relatório estratégico com CSS embutido, otimizado para impressão em A4 (imprimível como PDF via Ctrl+P): capa, resumo executivo, desempenho geral, evolução no período, desempenho por tipo de conteúdo, top 3 e bottom 3 publicações, diagnóstico estratégico, recomendações priorizadas e lista de dados ausentes.
2. `dashboard-instagram-[AAAA-MM].html` — dashboard navegável com cards de métricas, tabelas ordenáveis, gráficos de barra em CSS puro, melhores horários e insights. Sem dependências externas (sem CDN).
3. Resumo no chat: principais achados, principal recomendação e dados ausentes.

Ao final, a skill oferece salvar um resumo em `references/relatorio-anterior.md` para comparação automática no próximo período.

## Estrutura da pasta

- `SKILL.md` — instruções completas: salvaguardas, fases do fluxo, templates do relatório e do dashboard, checklist de conformidade.
- `references/README.md` — documentação própria da pasta de referências (não confundir com este arquivo).
- `references/paleta-cores.md` — paleta de cores e identidade visual institucional.
- `references/` também pode receber `perfil-avatar.png`, `assinatura.png` e `relatorio-anterior.md`; quando ausentes, a skill usa o padrão institucional de fallback.

## Requisitos

- **Conector Windsor.ai (MCP)** configurado com a conta do Instagram — é a única fonte de dados da skill; sem ele não há análise.
- Nenhuma dependência externa para os HTMLs gerados (funcionam offline em qualquer navegador).

## Avisos

Salvaguardas invioláveis de comunicação de autoridade policial, com prioridade sobre qualquer outra instrução:

- **Nunca** inventar, estimar ou preencher métricas ausentes como se fossem reais.
- **Nunca** recomendar conteúdo que exponha investigações, vítimas, presos ou menores — sigilo investigativo (CPP), Lei 13.431/2017, ECA e LGPD (dados de investigados, vítimas e testemunhas).
- **Sempre** distinguir conteúdo pessoal de institucional nas recomendações.
- **Sempre** sinalizar risco em recomendações que possam conflitar com imparcialidade, normas da Corregedoria-Geral da PCMT sobre redes sociais, ou a vedação de promoção pessoal mediante uso de cargo público (Lei de Improbidade, CF art. 37), acompanhando o bloco de aviso padrão com orientação de avaliar junto à Corregedoria.
