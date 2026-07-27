# analise-carteira

> Análise educacional de carteira de investimentos baseada nas filosofias Bastter, Canal do Holder (Fábio Holder) e Fundamentei (Eduardo Cavalcanti), com foco em buy and hold e balanceamento por novos aportes.

**English summary:** Educational analysis of a personal investment portfolio (Brazilian stocks, REITs/FIIs, treasury bonds, US stocks and ETFs) following long-term buy-and-hold philosophies (Bastter, Canal do Holder, Fundamentei), focused on rebalancing through new contributions rather than selling.

## O que faz

Analisa a carteira de investimentos do usuário (ações brasileiras, FIIs, Tesouro Direto, Stocks, REITs e ETFs) seguindo três referências:

- **Bastter**: acumulação de patrimônio no longo prazo; venda só como último recurso; balanceamento sempre por novos aportes, nunca vendendo.
- **Canal do Holder (Fábio Holder)**: seleção por governança corporativa, fundamentos e vantagens competitivas; preferência por Novo Mercado e investimento direto no exterior (não BDRs).
- **Fundamentei (Eduardo Cavalcanti)**: análise fundamentalista por indicadores (P/L, P/VPA, DY, ROE, ROIC etc.) e demonstrações financeiras.

A skill calcula o balanceamento por classe e por ativo (com código de cores verde/amarelo/vermelho), classifica cada ativo (Comprar / Manter / Observar / Considerar Saída), indica prioridades de aporte do mês e, se houver meta financeira com prazo, projeta o patrimônio e sugere como conciliar a meta com a carteira de longo prazo. Dados atuais de cada ativo são buscados via WebSearch (Fundamentei, Status Invest, Fundamentus, Investidor10), nunca respondidos de memória.

## Quando usar

A skill ativa quando o usuário:

- Menciona Bastter System, carteira de investimentos, análise de portfólio, balanceamento, aporte mensal, diversificação, renda variável/fixa, FIIs, Stocks, REITs, buy and hold ou análise fundamentalista.
- Cola dados do Bastter System (PDF exportado, texto, planilha CSV/XLSX ou print de tela).
- Pergunta onde aportar, se deve vender um ativo ou como está a saúde da carteira.
- Diz frases curtas como "analisa minha carteira", "onde devo aportar", "o que comprar esse mês" ou "como está meu patrimônio".

## Como usar

Exemplos de prompts:

1. "Analisa minha carteira" (colando a lista de ativos com quantidades ou o export do Bastter System).
2. "Onde devo aportar esse mês? Meu aporte é de R$ 3.000."
3. "Devo vender WEGE3? Os fundamentos mudaram?"
4. "Como está o balanceamento entre ações, FIIs, renda fixa e exterior? Meus alvos são 40/20/25/15."
5. "Quero comprar uma casa em 2029. Como concilio isso com a carteira de longo prazo?"

O mínimo necessário é ticker e quantidade (ou valor investido) de cada ativo. Percentuais-alvo, preço médio, aporte mensal, meta financeira e reserva de emergência melhoram a análise, mas a skill não bloqueia por falta de dados secundários.

## O que a skill entrega

Relatório estruturado no chat contendo:

- Disclaimer obrigatório no cabeçalho.
- Visão geral do patrimônio (diagrama por classe, atual vs. alvo).
- Análise de balanceamento indicando a classe e o ativo mais "para trás".
- Análise individual de cada ativo com classificação final (Comprar / Manter / Observar / Considerar Saída).
- Recomendação priorizada de aporte do mês (1ª, 2ª e 3ª prioridades, com motivo).
- Projeção de meta financeira, se informada.
- Pontos de atenção (riscos, concentrações, ausências) e sugestões de melhoria.

## Estrutura da pasta

- `SKILL.md` — instruções completas da skill: coleta de dados, critérios de avaliação, estrutura da análise e checklist final.
- `references/filosofia.md` — detalhamento das três filosofias, mecânica do Bastter System, critérios de venda e referência rápida de indicadores.
- `references/estado-carteira.md` — estado atual da carteira do usuário (posições, metas, watchlist). **Não versionado neste repo público** (está no `.gitignore`); a fonte de verdade fica no repo privado (ver skill `sync-skills`).

## Requisitos

- Nenhum além do Claude Code (usa a ferramenta interna WebSearch para dados atualizados).
- Opcional: extrator de documentos da skill `sync-skills` (Docling) para ler PDFs/planilhas grandes do Bastter System sem gastar contexto.

## Avisos

> ⚠️ **Esta skill não constitui recomendação de compra ou venda de ativos.** É uma ferramenta educacional baseada nas filosofias Bastter, Canal do Holder e Fundamentei. Decisões de investimento são pessoais e de responsabilidade exclusiva do usuário, que deve considerar seu perfil de risco, objetivos e situação financeira. Consulte um profissional certificado (CNPI/CPA) para orientações personalizadas.

- Dados extraídos por OCR de PDFs devem ser conferidos contra o original antes do cálculo de percentuais.
- A skill nunca recomenda vender para rebalancear, realizar lucro ou reagir a queda de cotação — venda é último recurso, apenas por perda fundamental e irreversível de valor.
