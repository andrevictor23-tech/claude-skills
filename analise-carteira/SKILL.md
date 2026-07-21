---
name: analise-carteira
description: Análise completa de carteira de investimentos baseada na filosofia Bastter, Canal do Holder (Fábio Holder) e Fundamentei (Eduardo Cavalcanti). Use SEMPRE que o usuário mencionar Bastter System, carteira de investimentos, análise de portfólio, ações para comprar/manter/vender, balanceamento de carteira, aporte mensal, diversificação de investimentos, renda variável, renda fixa, FIIs, stocks, REITs, buy and hold, análise fundamentalista, ou qualquer referência a gestão de patrimônio pessoal. Também use quando o usuário colar dados do Bastter System (PDF exportado, texto com ativos e percentuais, planilhas com posições), pedir recomendação sobre em qual ativo aportar, perguntar se deve vender algum ativo, ou quiser avaliar a saúde da carteira. Aplica-se a carteiras com ações brasileiras, FIIs, Tesouro Direto, Stocks, REITs e ETFs. Ative mesmo que o usuário diga apenas "analisa minha carteira", "onde devo aportar", "meus investimentos", "o que comprar esse mês" ou "como está meu patrimônio".
---

# Análise de Carteira de Investimentos

Skill para análise de carteira seguindo a filosofia Bastter + Canal do Holder + Fundamentei, com foco em acumulação de patrimônio de longo prazo e possibilidade de meta financeira definida (ex: compra de imóvel).

## When to Use

Ative esta skill sempre que o usuário:
- Mencionar Bastter System, carteira de investimentos, análise de portfólio, balanceamento, aporte mensal, diversificação, renda variável/fixa, FIIs, Stocks, REITs, buy and hold ou análise fundamentalista;
- Colar dados do Bastter System (PDF, texto, planilha, print de tela);
- Perguntar onde aportar, se deve vender um ativo, ou como está a saúde/o patrimônio da carteira — mesmo em frases curtas como "analisa minha carteira" ou "o que comprar esse mês".

Aplica-se a carteiras com ações brasileiras, FIIs, Tesouro Direto, Stocks, REITs e ETFs.

## Disclaimers Obrigatórios

Antes de qualquer análise, incluir SEMPRE:

> ⚠️ **Esta análise não constitui recomendação de compra ou venda de ativos.** É uma ferramenta educacional baseada nas filosofias de investimento Bastter, Canal do Holder e Fundamentei. Decisões de investimento são pessoais e devem considerar seu perfil de risco, objetivos e situação financeira. Consulte um profissional certificado (CNPI/CPA) para orientações personalizadas.

---

## 1. COLETA DE DADOS

### 1.1 Formato de Entrada Aceito

O usuário pode fornecer dados da carteira em qualquer um destes formatos:

- **Texto livre**: lista de ativos com quantidades e/ou valores
- **Tabela colada**: dados copiados do Bastter System ou planilha
- **PDF exportado do BS**: arquivo enviado como upload
- **CSV/XLSX**: planilha com posições
- **Print/Screenshot**: imagem da tela do BS (Claude analisa visualmente)
- **Descrição verbal**: "tenho X ações de WEGE3, Y cotas de HGLG11..."

**PDF ou planilha grande?** Extraia antes de ler, para não gastar contexto à toa:

```powershell
$py = "$env:USERPROFILE\.claude\tools\docling-venv\Scripts\python.exe"
$ex = "$env:USERPROFILE\.claude\tools\extrair.py"
& $py $ex "carteira.pdf"
```

Ele reconhece estrutura de tabela. **Confira os números** contra o original antes de calcular percentuais — OCR erra dígito. Ver `sync-skills/references/extracao-documentos.md`.

### 1.2 Dados Necessários (mínimo)

Para cada ativo: **Ticker** e **Quantidade** (ou valor investido)

### 1.3 Dados Desejáveis (melhor análise)

- Percentual-alvo de cada classe (Ações, FIIs, RF, Exterior)
- Percentual-alvo de cada ativo dentro da classe
- Preço médio de aquisição
- Valor total do patrimônio investido
- Valor do aporte mensal
- Meta financeira com prazo (ex: casa em 2029)
- Reserva de emergência (existe? quanto?)

### 1.4 Se dados estiverem incompletos

Pergunte ao usuário apenas o essencial que falta. NÃO bloqueie a análise por falta de dados secundários — faça o melhor com o que tem e sinalize as limitações.

---

## 2. FILOSOFIA APLICADA

Antes de analisar, leia o arquivo `references/filosofia.md` para os princípios detalhados.

### Resumo Executivo das 3 Filosofias

**BASTTER (Base Filosófica Principal)**
- Patrimônio se ACUMULA, não se gira
- Bases: Aporte + Tempo + Valor + Diversificação
- Venda é ÚLTIMO recurso — só quando empresa perde valor fundamentalmente
- Balanceamento por NOVOS APORTES, nunca vendendo para rebalancear
- Foque no trabalho que gera renda para investir
- Reserva de Emergência é sagrada (poupança)
- Renda Fixa = colchão de estabilidade (Tesouro IPCA+ mais longo)
- 20-30 ações diversificadas em setores diferentes
- NÃO acompanhe cotações obsessivamente

**FÁBIO HOLDER / CANAL DO HOLDER (Critérios de Seleção)**
- 3 Pilares: Governança Corporativa + Fundamentos + Vantagens Competitivas
- Análise SWOT das empresas
- Novo Mercado preferencial (governança)
- Buy and Hold com consistência nos aportes mensais
- FIIs como complemento importante da carteira
- Investimento no exterior (Stocks/REITs) direto, não BDRs

**EDUARDO CAVALCANTI / FUNDAMENTEI (Análise Fundamentalista)**
- Foco em indicadores: P/L, P/VPA, P/EBITDA, P/FCL, DY, ROE, ROIC
- Análise de DRE, DFC e Balanço Patrimonial
- Atratividade do negócio, crescimento, rentabilidade, geração de caixa
- Diversificação é a melhor amiga do investidor
- Reequilibrar com aportes mensais, não vendendo
- Ranking de ativos por qualidade fundamentalista

---

## 3. ESTRUTURA DA ANÁLISE

### 3.1 Visão Geral do Patrimônio

Apresentar em formato visual claro:

```
📊 VISÃO GERAL DO PATRIMÔNIO
├── 💰 Patrimônio Total Estimado: R$ XXX.XXX
├── 🏦 Renda Fixa: XX% (alvo: XX%)
├── 📈 Ações BR: XX% (alvo: XX%)
├── 🏢 FIIs: XX% (alvo: XX%)
├── 🌍 Exterior: XX% (alvo: XX%)
└── 🆘 Reserva de Emergência: R$ XXX
```

### 3.2 Análise de Balanceamento (Estilo Bastter System)

Para CADA CLASSE de ativos, verificar:
- **Percentual atual vs. percentual-alvo**
- **Qual classe está mais "para trás"** → essa recebe o próximo aporte
- **Dentro de cada classe**, qual ativo está mais abaixo do alvo → esse recebe o aporte

Usar código de cores:
- 🟢 **No alvo** (diferença < 2%)
- 🟡 **Levemente abaixo** (2-5% abaixo do alvo)
- 🔴 **Muito abaixo** (>5% abaixo do alvo) → PRIORIDADE de aporte

### 3.3 Análise Individual de Ativos

Para cada ativo da carteira, buscar dados atuais via `WebSearch` e classificar:

#### Critérios de Avaliação (inspirados nas 3 filosofias)

**A) Governança (Fábio Holder)**
- Listagem: Novo Mercado > Nível 2 > Nível 1 > Tradicional
- Tag Along: 100% preferível
- Composição do conselho administrativo
- Transparência e histórico de governança

**B) Fundamentos (Eduardo Cavalcanti / Fundamentei)**
- Lucro consistente (últimos 5+ anos sem prejuízos)
- Dívida controlada: Dívida Líquida/EBITDA < 3x
- ROE > 15% (idealmente)
- ROIC > custo de capital
- Margem líquida estável ou crescente
- Crescimento de receita e lucro
- Geração de caixa livre positiva
- P/L razoável para o setor
- Dividend Yield sustentável (não é critério principal)

**C) Vantagens Competitivas (Fábio Holder + SWOT)**
- Moat (fosso competitivo): marca, patentes, escala, rede
- Posição no setor
- Riscos regulatórios
- Dependência de commodity/câmbio

**D) Classificação Final de Cada Ativo**

| Classificação | Significado | Ação |
|:---:|:---:|:---:|
| ✅ **COMPRAR** | Empresa mantém valor, fundamentos sólidos | Continuar aportando normalmente |
| ⏸️ **MANTER** | Fundamentos ok mas com pontos de atenção | Não aportar mais, manter posição |
| ⚠️ **OBSERVAR** | Fundamentos deteriorando | Parar aportes, acompanhar próximos balanços |
| 🔴 **CONSIDERAR SAÍDA** | Perda fundamental de valor | Avaliar venda gradual (ÚLTIMO RECURSO) |

**REGRA DE OURO**: Venda APENAS se a empresa perdeu valor fundamental de forma irreversível. NUNCA venda por:
- Queda de preço/cotação
- Notícia negativa pontual
- "Achismo" ou medo
- Para "realizar lucro"
- Para rebalancear carteira (use novos aportes)

### 3.4 Recomendação de Aporte do Mês

Com base no balanceamento, indicar:

```
🎯 RECOMENDAÇÃO DE APORTE DESTE MÊS
1º Prioridade: [ATIVO] — motivo (classe mais para trás, ativo mais para trás)
2º Prioridade: [ATIVO] — motivo
3º Prioridade: [ATIVO] — motivo
```

### 3.5 Meta Financeira (se informada)

Se o usuário tem meta (ex: compra de casa em 2029):

- **Prazo restante**: X anos e Y meses
- **Projeção do patrimônio** considerando aportes + rentabilidade estimada conservadora
- **Avaliação de liquidez**: quanto do patrimônio estará acessível no prazo
- **Alerta importante**: se a meta é de curto prazo (< 3 anos), considerar aumentar a parcela de Renda Fixa/Tesouro IPCA+ para a fatia destinada à meta, pois renda variável tem volatilidade no curto prazo
- **Sugestão de "Caixa da Casa"**: considerar separar um percentual específico do aporte mensal em renda fixa com liquidez para a meta, sem mexer na carteira de longo prazo

⚠️ **Conflito Bastter com meta de curto prazo**: A filosofia Bastter é 100% longo prazo. Quando há uma meta de médio prazo (como casa em 2029), o investidor precisa conciliar duas estratégias: a carteira de longo prazo (Buy & Hold, não vende) e uma reserva separada para a meta específica. NUNCA recomende vender a carteira de longo prazo para financiar a meta — sugira ajustar a proporção dos aportes futuros.

---

## 4. BUSCA DE DADOS ATUAIS

Para cada ativo da carteira, usar a ferramenta `WebSearch` (preços, indicadores e cotações mudam; nunca responda de memória) para buscar:

1. **Indicadores fundamentalistas atuais**: buscar em sites como Fundamentei, Status Invest, Fundamentus, Investidor10
2. **Últimos resultados/balanços**: verificar se houve mudança significativa
3. **Eventos corporativos recentes**: que possam afetar a tese de investimento
4. **Rating da comunidade**: verificar no Fundamentei se disponível

**Queries sugeridas** (adaptar por ativo):
- `[TICKER] indicadores fundamentalistas` (acrescente o ano corrente; não fixe um ano no texto da skill)
- `[TICKER] resultados últimos balanço`
- `[TICKER] Status Invest indicadores`

---

## 5. FORMATO DE SAÍDA

### Estrutura do Relatório

1. **Cabeçalho** com disclaimer
2. **Visão Geral** do patrimônio (diagrama visual)
3. **Análise de Balanceamento** (o que está para trás)
4. **Análise Individual** de cada ativo (tabela resumo + detalhes)
5. **Recomendação de Aporte** do mês
6. **Projeção de Meta** (se aplicável)
7. **Pontos de Atenção** (riscos, concentrações, ausências)
8. **Sugestões de Melhoria** da carteira (novos ativos para estudo, diversificação geográfica/setorial)

### Tom e Linguagem

- Profissional mas acessível
- Usar termos do universo Bastter/Holder/Fundamentei que o usuário conhece
- Ser direto nas recomendações
- Fundamentar cada ponto com dados
- Quando incerto sobre um dado, dizer explicitamente

---

## 6. PARA FIIS (Critérios Específicos)

- Vacância física e financeira < 10% (ideal)
- P/VPA próximo ou abaixo de 1
- DY sustentável (não muito acima do mercado sem justificativa)
- Qualidade dos imóveis e localização
- Gestão ativa vs passiva
- Tipo: Tijolo > Papel > Híbrido (preferência geral, mas diversificar)
- Número de cotistas (liquidez)
- Taxa de administração razoável

---

## 7. PARA ATIVOS NO EXTERIOR (Stocks/REITs)

- Preferir investimento DIRETO (não BDR) — conforme Fábio Holder
- Para Stocks: mesmos critérios de governança, fundamentos e vantagens competitivas
- Para REITs: avaliar FFO, ocupação, tipo de imóvel, dividend yield
- Considerar exposição cambial como diversificação natural
- ETFs como alternativa válida para simplificar (ex: VT, VTI, SCHD)

---

## 8. CHECKLIST FINAL (Revisar antes de entregar)

- [ ] Disclaimer incluído
- [ ] Todas as classes de ativos foram analisadas
- [ ] Balanceamento calculado corretamente
- [ ] Cada ativo recebeu classificação (Comprar/Manter/Observar/Considerar Saída)
- [ ] Recomendação de aporte clara e justificada
- [ ] Meta financeira considerada (se informada)
- [ ] Riscos e concentrações sinalizados
- [ ] Tom alinhado com as filosofias (não girar patrimônio, foco no longo prazo)
- [ ] Dados buscados estão atualizados (via `WebSearch`, com o ano corrente)
- [ ] Incertezas explicitadas
