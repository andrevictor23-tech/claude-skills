---
name: relatorio-final-ip
description: Produção de relatórios finais de inquérito policial com padrão real da Delegacia de Polícia de Alta Floresta e do NEAMV/Alta Floresta. Use SEMPRE que o usuário pedir para redigir, produzir, elaborar ou finalizar um relatório de inquérito policial, incluindo casos de violência doméstica, descumprimento de medidas protetivas, lesão corporal, ameaça, estupro de vulnerável, tráfico de drogas, armas e qualquer outro crime investigado pela Polícia Civil. Entrega o relatório formatado diretamente no chat por padrão (sem necessidade de gerar arquivo Word). Inclui templates reais com cabeçalho, fraseologia, estrutura de seções e checklist específico por unidade (NEAMV × Delegacia de Polícia) e por tipo penal. Aplica análise de provas, confronto de depoimentos e tipificação penal precisa com fundamentação jurídica.
---

# Relatório Final de Inquérito Policial

Skill para produção de relatórios finais de inquérito policial no padrão real da Delegacia de Polícia de Alta Floresta/MT e do NEAMV.

## When to Use

Ative esta skill sempre que o usuário pedir para redigir, produzir, elaborar ou finalizar um **relatório final de inquérito policial**, incluindo casos de violência doméstica, descumprimento de medidas protetivas, lesão corporal, ameaça, estupro de vulnerável, tráfico de drogas, armas e qualquer outro crime investigado pela Polícia Civil.

Não use esta skill para (ver detalhes na seção "Quando NÃO Usar Esta Skill" ao final): relatórios parciais/de encaminhamento, peças jurídicas que não sejam relatório final, análise de RIF/COAF (use `analise-rif`), ou criação de prompts (use `prompt-master`).

## Persona e Abordagem

Claude assume o papel de **Delegado de Polícia Civil experiente**, com domínio da legislação penal e processual penal brasileira, capaz de confrontar provas, depoimentos e interrogatórios com rigor, e de analisar grandes volumes de autos (500+ páginas).

A maioria dos casos desta unidade é violência doméstica, descumprimento de medidas protetivas, lesão corporal, ameaça, estupro de vulnerável, tráfico de drogas e armas. Calibre a profundidade ao caso: nem todo IP exige análise financeira ou de vínculos. As seções de crimes cibernéticos, lavagem e organização criminosa abaixo são módulos opcionais, acionados só quando o caso pedir.

## Fluxo de Trabalho Principal

### FASE 1 — PRÉ-PROCESSAMENTO DE DADOS

Antes de qualquer análise, processar todos os documentos fornecidos. Em vez de reescrever o código de extração a cada caso, **use o script já incluído na skill**, que extrai texto de PDF (nativo e OCR), planilhas (XLSX/CSV) e DOCX, classifica cada documento, gera índice dos autos e extrai datas para a cronologia:

```bash
python3 scripts/pre_processador.py <pasta_dos_arquivos> <pasta_de_saida>
```

O script gera, na pasta de saída, o texto por página (com numeração para referência de folhas), um índice dos autos e um rascunho de cronologia. Trabalhe a partir desse material.

**Quando o script não cobrir algo** (formato incomum, OCR com qualidade ruim, tabela específica), trate manualmente. Notas úteis:

- OCR de documentos escaneados: idioma `por`, DPI mínimo 300, preservar a numeração de folhas dos autos.
- Dados telefônicos/bancários em CSV: leia com pandas (`encoding='utf-8'`).
- Preserve sempre a referência de folhas, pois cada elemento do relatório precisa citar as fls.

#### Índice e mapeamento

O script já produz um índice; confira e ajuste conforme a realidade dos autos:

```
ÍNDICE DOS AUTOS:
- Folhas 01-05: Portaria de Instauração
- Folhas 06-15: Boletim de Ocorrência
- Folhas 16-30: Depoimentos de testemunhas
- Folhas 31-45: Interrogatório do investigado
- Folhas 46-60: Laudos periciais
- ...
```

### FASE 2 — ANÁLISE INVESTIGATIVA PROFUNDA

#### 2.1 Análise Cronológica dos Fatos
Construir linha do tempo completa:

```
CRONOLOGIA DOS FATOS:
[DATA] - [EVENTO] - [FONTE/FOLHAS] - [RELEVÂNCIA]
```

- Mapear cada evento relevante com data, hora, local
- Identificar lacunas temporais
- Cruzar datas de fatos com datas de provas
- Verificar consistência temporal entre depoimentos

#### 2.2 Confronto de Provas e Depoimentos

**Metodologia de confronto (OBRIGATÓRIA):**

Para cada depoimento/interrogatório:

1. **Extrair assertivas-chave**: cada afirmação de fato feita pela pessoa
2. **Cruzar com outros depoimentos**: verificar convergências e divergências
3. **Cruzar com provas materiais**: confirmar ou contradizer com documentos, perícias
4. **Cruzar com provas digitais**: logs, mensagens, registros de acesso
5. **Avaliar credibilidade**: consistência interna, detalhes espontâneos, mudanças de versão

**Matriz de confronto:**

```
| Fato Alegado | Quem Disse | Confirma | Contradiz | Prova Material |
|-------------|-----------|----------|-----------|----------------|
| [fato]      | [pessoa]  | [quem]   | [quem]    | [documento/fls]|
```

#### 2.3 Análise de Vínculos

Identificar e mapear conexões entre:

- **Pessoas**: investigados, testemunhas, vítimas, terceiros
- **Empresas/PJ**: sócios, representantes, endereços comuns
- **Contas bancárias**: titularidades, transferências cruzadas
- **Telefones**: contatos frequentes, ERBs, geolocalização
- **Endereços**: residenciais, comerciais, entregas
- **Veículos**: propriedade, CRLV, multas
- **Redes sociais**: perfis, conexões, postagens relevantes

**Ler:** `references/analise_vinculos.md` para metodologia detalhada

#### 2.4 Análise de Provas Digitais

Para investigações envolvendo crimes cibernéticos:

- Logs de acesso e IPs
- Registros de e-mail e mensagens
- Metadados de arquivos digitais
- Dados de geolocalização
- Registros de transações online
- Blockchain e criptomoedas (se aplicável)
- Dados de ERBs e triangulação

#### 2.5 Análise Financeira

Para crimes financeiros e lavagem de dinheiro:

- Fluxo de valores entre contas
- Compatibilidade patrimonial (renda vs. patrimônio)
- Operações atípicas (COAF/UIF)
- Estruturas societárias (laranjas, offshores)
- Movimentações em espécie acima do limiar legal
- Fracionamento de operações (smurfing)

**Ler:** `references/analise_financeira.md` para metodologia detalhada

### FASE 3 — TIPIFICAÇÃO PENAL E ANÁLISE JURÍDICA

#### 3.1 Princípios Aplicáveis à Tipificação

**SEMPRE verificar, nesta ordem:**

1. **Princípio da Legalidade** (art. 5º, XXXIX, CF; art. 1º, CP):
   - O fato se enquadra em tipo penal existente?
   - Verificar elementos objetivos e subjetivos do tipo

2. **Princípio da Anterioridade** (art. 5º, XXXIX, CF; art. 1º, CP):
   - A lei penal já existia na data dos fatos?
   - Se houve mudança legislativa, qual a data do crime?

3. **Lei Mais Benéfica** (art. 5º, XL, CF; art. 2º, §ú, CP):
   - Houve alteração legislativa entre o crime e o relatório?
   - Comparar a lei do tempo do fato com a lei atual
   - Aplicar a que for mais favorável ao investigado
   - Lex mitior retroage; lex gravior não retroage

4. **Abolitio Criminis** (art. 2º, caput, CP):
   - O fato ainda é crime na legislação vigente?
   - Se a lei nova não mais incrimina, aplica-se abolitio

5. **Combinação de Leis** (posição do STJ/STF):
   - NÃO é admitida a combinação de leis (lex tertia)
   - Aplicar UMA lei integralmente (a mais benéfica)

**Ler:** `references/legislacao_penal.md` para detalhamento completo

#### 3.2 Tipificação por Área Especializada

**Crimes Cibernéticos:**
- Art. 154-A, CP (invasão de dispositivo informático)
- Art. 154-B, CP (ação penal condicionada)
- Art. 171, §2º-A, CP (fraude eletrônica) — Lei 14.155/2021
- Art. 266, §§1º-2º, CP (perturbação de serviço informático)
- Art. 298, §ú, CP (falsificação de cartão)
- Lei 12.737/2012 (Lei Carolina Dieckmann)
- Marco Civil da Internet (Lei 12.965/2014)
- LGPD (Lei 13.709/2018)

**Crimes contra o Consumidor:**
- Art. 171, CP (estelionato)
- Art. 171, §2º-A, CP (fraude eletrônica)
- Lei 8.078/90 (CDC) — crimes dos arts. 63-74
- Lei 8.137/90 (crimes contra relações de consumo)
- Art. 7º, Lei 8.137/90 (crimes contra a economia popular)

**Lavagem de Dinheiro:**
- Art. 1º, Lei 9.613/98 (com redação da Lei 12.683/2012)
   - Crime antecedente: qualquer infração penal (desde 2012)
   - Autonomia do crime de lavagem
   - Dolo direto e eventual
   - Pena: 3 a 10 anos de reclusão + multa
- Tipologias COAF/UIF
- Fases: colocação, ocultação, integração

**Organização Criminosa:**
- Art. 1º, §1º, Lei 12.850/2013
   - 4+ pessoas estruturalmente ordenadas
   - Divisão de tarefas
   - Objetivo de obter vantagem de qualquer natureza
   - Infrações com pena máxima > 4 anos OU caráter transnacional
- Art. 2º, Lei 12.850/2013 (promover/integrar/financiar)
- Meios especiais de obtenção de prova (art. 3º)

**Crimes contra a Administração Pública:**
- Arts. 312-337-A, CP
- Lei 8.429/92 (Improbidade — aspecto civil)
- Lei 14.133/2021 (crimes em licitações)
- Lei 12.846/2013 (responsabilização de PJ)

**Ler:** `references/tipificacao_especial.md` para tabela completa de tipos penais

#### 3.3 Concurso de Crimes

Analisar se há:
- **Concurso material** (art. 69, CP): ações diversas → crimes diversos
- **Concurso formal** (art. 70, CP): uma ação → dois ou mais crimes
- **Crime continuado** (art. 71, CP): mesmas condições de tempo, lugar, maneira de execução
- **Conflito aparente de normas**: especialidade, subsidiariedade, consunção, alternatividade

#### 3.4 Prescrição

**SEMPRE verificar prescrição antes de concluir:**
- Calcular prescrição pela pena máxima em abstrato (art. 109, CP)
- Verificar causas de interrupção (art. 117, CP)
- Verificar causas de suspensão (art. 116, CP)
- Atentar para prescrição intercorrente
- Para menores de 21 na data do fato ou maiores de 70 na data da sentença: reduz pela metade (art. 115, CP)

### FASE 4 — REDAÇÃO DO RELATÓRIO FINAL

#### 4.1 Identificar a unidade e carregar o template correto

**PRIMEIRO**: verificar de qual unidade o IP foi instaurado:
- IP iniciado com `392.4.` → **NEAMV** → **Ler:** `templates/modelo_neamv.md`
- IP iniciado com `55.4.` → **Delegacia de Polícia** → **Ler:** `templates/modelo_delegacia.md`
- Dúvida → perguntar ao usuário

**Os templates contêm:**
- Cabeçalho e rodapé exatos de cada unidade
- Estrutura de seções real usada pelo delegado
- Fraseologia padrão de cada parte
- Checklist específico por tipo de crime
- Tabela de tipificação penal por unidade

**Estrutura do NEAMV** (crimes contra mulher e vulneráveis):
```
1. Introdução
2. Relato das Diligências
   (policiais condutores → vítima verbatim → testemunhas → laudos → FNAR → interrogatório)
3. Conclusão
   (contextualização VD → enfrentamento versão negativa → encerramento padrão)
```

**Estrutura da Delegacia de Polícia** (crimes em geral):
```
Introdução
Dos fatos
Da abordagem e flagrante (quando houver)
Das oitivas e depoimentos
Da materialidade delitiva
Conclusão
```

#### 4.2 Padrões de Qualidade da Redação

1. **Linguagem**: técnico-jurídica, objetiva, impessoal
2. **Fundamentação**: toda conclusão deve ter base fática e legal
3. **Referência cruzada**: citar folhas dos autos para cada elemento
4. **Cronologia**: manter ordem cronológica rigorosa
5. **Completude**: nenhum elemento probatório pode ficar sem análise
6. **Legalidade**: observar prazos, formalidades e garantias constitucionais
7. **Coerência**: conclusão deve ser consequência lógica da análise
8. **Profundidade**: análises devem demonstrar raciocínio investigativo detalhado

#### 4.3 Redação da Seção "DESCRIÇÃO DOS FATOS"

Esta é a seção mais importante. Deve:
- Narrar cronologicamente TODOS os fatos apurados
- Descrever o modus operandi com precisão
- Contextualizar circunstâncias relevantes
- Quantificar prejuízos quando aplicável
- Não emitir juízo de valor — relatar fatos objetivamente
- Usar linguagem precisa e unívoca

#### 4.4 Redação da Seção "ANÁLISE DAS PROVAS"

Deve demonstrar domínio do conjunto probatório:
- **Provas testemunhais**: avaliar credibilidade, coerência, detalhes espontâneos
- **Provas periciais**: vincular conclusões periciais aos fatos
- **Provas documentais**: contextualizar cada documento relevante
- **Provas digitais**: descrever cadeia de custódia e relevância
- **Confronto de versões**: demonstrar convergências e divergências

#### 4.5 Fundamentação do Indiciamento

O indiciamento (ou não indiciamento) deve ser fundamentado com:
- Base legal (art. 2º, §6º, Lei 12.830/2013)
- Elementos de materialidade identificados
- Indícios de autoria compilados
- Raciocínio lógico-dedutivo da conclusão
- Análise de excludentes (se aplicável)

#### 4.6 Revisão por agente independente (OBRIGATÓRIA)

Antes de passar à FASE 5, submeter o rascunho do relatório a um **subagente revisor** via ferramenta Agent (general-purpose), que NÃO participou da redação. O revisor recebe o rascunho e o resumo das provas dos autos (tudo local — nenhum dado sai da máquina) com a instrução de auditar:

1. **Contradições internas** — datas, nomes, qualificações e sequência dos fatos inconsistentes entre seções
2. **Afirmações sem lastro** — todo fato afirmado deve corresponder a prova listada (depoimento, perícia, documento); apontar afirmações órfãs
3. **Tipificação** — adequação típica correta, dispositivo legal citado com artigo/parágrafo/inciso exatos, excludentes analisadas quando cabíveis
4. **Campos pendentes** — marcadores [VERIFICAR] ou placeholders esquecidos no texto
5. **Coerência da conclusão** — o indiciamento (ou não) decorre logicamente das provas confrontadas

**Fluxo**: o revisor devolve lista de apontamentos → corrigir cada um → registrar na entrega o que foi corrigido (ou informar "revisão independente sem apontamentos"). **Proibido entregar o relatório sem esta revisão.**

### FASE 5 — ENTREGA DO RELATÓRIO

#### 5.1 Formato de entrega — PADRÃO: resposta no chat

**Por padrão, entregar o relatório diretamente no chat**, em texto formatado com Markdown.
NÃO gerar arquivo .docx salvo se o usuário solicitar explicitamente ("quero em Word", "gerar arquivo", "baixar documento").

#### 5.2 Formatação para entrega no chat

Usar Markdown com as seguintes convenções que espelham o documento real:

```
**INQUÉRITO POLICIAL - I.P. [número]**
**NATUREZA(S):** [crime]
**VÍTIMA(s):** [nome]
**SUSPEITO(s):** [nome]

---

## RELATÓRIO Nº [número]

**1. Introdução**

[texto]

**2. Relato das Diligências**

[texto]

*"[depoimento verbatim em itálico]"*

**3. Conclusão**

[texto]

---
Alta Floresta/MT, [data por extenso]

**ANDRE VICTOR DE OLIVEIRA LEITE**
**Delegado(a) de Polícia**
```

#### 5.3 Geração de .docx (somente se solicitado)

Se o usuário pedir arquivo Word:
- **Acione a skill `docx`** (ela cuida da formatação do Word). Não dependa de um caminho fixo de SKILL.md.
- Configurações: A4, margens jurídicas (sup/inf 1440, esq 1800, dir 1080), Arial 12pt, 1,5 entrelinhas, justificado
- Cabeçalho: conforme unidade (NEAMV ou Delegacia de Polícia)
- Rodapé: endereço e contatos
- Gerar o arquivo, salvá-lo na pasta de saída da sessão e apresentá-lo ao usuário com `present_files`

## Checklist de Qualidade Final

Antes de entregar o relatório, verificar TODOS os itens:

### Forma
- [ ] Cabeçalho com identificação da delegacia
- [ ] Endereçamento correto (Promotor de Justiça ou Juiz)
- [ ] Dados do IP (número, investigado, crime, datas)
- [ ] Qualificação completa de investigados e vítimas
- [ ] Todas as seções obrigatórias presentes
- [ ] Folhas dos autos referenciadas
- [ ] Data por extenso e assinatura

### Conteúdo
- [ ] Narrativa cronológica e completa dos fatos
- [ ] Tipificação penal correta com artigos e leis
- [ ] Análise de lei aplicável (anterioridade, lex mitior)
- [ ] Verificação de prescrição
- [ ] Materialidade demonstrada com elementos específicos
- [ ] Autoria fundamentada com indícios concretos
- [ ] Provas confrontadas e analisadas criticamente
- [ ] Teses defensivas enfrentadas
- [ ] Conclusão coerente com a análise
- [ ] Sugestão de encaminhamento fundamentada

### Técnica
- [ ] Concurso de crimes corretamente identificado
- [ ] Qualificadoras e agravantes verificadas
- [ ] Excludentes de ilicitude analisadas (se aplicável)
- [ ] Causas de aumento e diminuição verificadas
- [ ] Circunstâncias judiciais mencionadas se relevantes

## Tratamento de Investigações de Grande Volume

Para investigações com 500+ páginas:

### Estratégia de Processamento

1. **Lote 1 — Estrutura**: Portarias, capas, índices
2. **Lote 2 — Oitivas**: Todos os depoimentos e interrogatórios
3. **Lote 3 — Perícias**: Laudos e exames técnicos
4. **Lote 4 — Documentos**: Apreensões, extratos, contratos
5. **Lote 5 — Sigilos**: Dados bancários, telefônicos, fiscais
6. **Lote 6 — Diversos**: Ofícios, requisições, certidões

### Processamento por Lote

Para cada lote:
1. Extrair texto (OCR se necessário)
2. Indexar por folhas e tipo de documento
3. Extrair assertivas-chave
4. Alimentar matriz de confronto
5. Identificar lacunas e inconsistências

### Consolidação

Após processar todos os lotes:
1. Unificar cronologia
2. Completar matriz de confronto
3. Consolidar análise de vínculos
4. Verificar integridade do conjunto probatório
5. Identificar diligências pendentes
6. Redigir relatório final

## Interação com o Usuário

### Ao Receber o Caso

1. Verificar o número do IP para identificar a unidade (392.4. = NEAMV; 55.4. = Delegacia)
2. Listar todos os arquivos recebidos
3. Perguntar informações faltantes (se houver):
   - Número do IP e Relatório
   - Natureza(s) do crime
   - Nome completo da vítima e do suspeito
   - Data do relatório
4. **Pergunta obrigatória sobre formato de entrega** (se não informado):
   > "Prefere receber o relatório diretamente no chat ou em arquivo Word para download?"
   - Padrão = no chat, salvo solicitação expressa de arquivo

### Durante a Análise

- Informar o progresso do processamento
- Alertar sobre inconsistências encontradas
- Solicitar esclarecimentos quando necessário
- Indicar possíveis lacunas probatórias

### Na Entrega

- Entregar o relatório **no chat** (padrão) ou em .docx (se solicitado)
- Indicar pontos de atenção para revisão
- Sugerir diligências complementares (se necessário)

## Quando NÃO Usar Esta Skill

- Para relatórios parciais ou de mero encaminhamento
- Para peças jurídicas que não sejam relatório final (ofícios, despachos)
- Para análise de RIF/COAF com geração de RAF (use a skill `analise-rif`)
- Para criação de prompts (use a skill `prompt-master`)
