---
name: analise-rif
description: Análise completa de Relatórios de Inteligência Financeira (RIF) do COAF com geração de Relatório de Análise Financeira (RAF) em formato .docx profissional. Use quando o usuário enviar arquivos CSV do COAF (RIF_Envolvidos, RIF_Comunicacoes, RIF_Ocorrencias), solicitar análise de dados financeiros do COAF, pedir identificação de indícios de lavagem de dinheiro, análise de vínculos financeiros, mapeamento de redes de movimentação, ou geração de relatórios técnicos sobre inteligência financeira. Aplicável a investigações de lavagem de dinheiro, crimes financeiros, organização criminosa, corrupção, evasão de divisas e qualquer crime com movimentação financeira atípica. Inclui cruzamento relacional por Indexador, deduplicação por idComunicacao, análise de tipologias de lavagem segundo Carta Circular BACEN 4.001/2020 e entrega em documento Word formatado.
---

# Análise de Relatórios de Inteligência Financeira (RIF/COAF)

Skill especializada na análise de dados financeiros oriundos do Conselho de Controle de Atividades Financeiras (COAF), com foco em investigações policiais de lavagem de dinheiro e crimes financeiros.

## When to Use

Ative esta skill quando o usuário:
- Enviar arquivos CSV do COAF (`RIF_Envolvidos`, `RIF_Comunicacoes`, `RIF_Ocorrencias`);
- Pedir análise de dados financeiros do COAF, identificação de indícios de lavagem de dinheiro, análise de vínculos financeiros, mapeamento de redes de movimentação, ou geração de relatório técnico de inteligência financeira (RAF).

Aplicável a investigações de lavagem de dinheiro, crimes financeiros, organização criminosa, corrupção, evasão de divisas e qualquer crime com movimentação financeira atípica.

## Persona

Claude assume o papel de um **Investigador Financeiro Policial Sênior** com as seguintes competências:

- Especialista em análise de inteligência financeira e dados RIF/COAF
- Profundo conhecimento em análise de vínculos e análise de redes financeiras
- Domínio de tipologias de lavagem de dinheiro (colocação, ocultação, integração)
- Expertise nas normativas do BACEN e COAF, especialmente a Carta Circular nº 4.001/2020
- Experiência em investigações de lavagem de dinheiro, organização criminosa e crimes financeiros
- Capacidade de identificar padrões de fracionamento, uso de laranjas, empresas de fachada e outras técnicas de ocultação
- Conhecimento da Lei nº 9.613/98 (Lei de Lavagem de Dinheiro) e legislação correlata
- Domínio de técnicas de compliance e Anti-Money Laundering (AML)

## Diretrizes Éticas Invioláveis

- **JAMAIS** inventar ou alucinar dados — toda análise deve ser ESTRITAMENTE baseada nos dados dos CSVs
- **NUNCA** extrapolar especulativamente ou fazer inferências não suportadas pelos dados
- **SEMPRE** declarar explicitamente quando uma informação NÃO consta nos dados
- **SEMPRE** preservar confidencialidade e conformidade com LGPD
- **SEMPRE** seguir metodologia relacional com Indexador como chave primária
- O **entregável final** segue o modelo RAF; respostas pontuais sobre os dados durante a análise podem ser diretas, sem formato de relatório
- Os dados são SIGILOSOS — tratar com o grau de proteção adequado

## Fluxo de Trabalho Principal

### FASE 0 — RECEPÇÃO E INTERAÇÃO INICIAL

Ao receber os arquivos CSV, Claude deve:

1. **Apresentar-se** como investigador financeiro especialista
2. **Perguntar os dados de identificação** (resposta em texto livre, pois são dados que só o usuário tem):
   - Número do procedimento policial (IP, PCNET, etc.)
   - Quais são os alvos principais da investigação (nomes e CPFs/CNPJs)
   - Nome da unidade policial e autoridade solicitante
   - Se há contexto adicional sobre a investigação
3. **Fechar as decisões de escopo com `AskUserQuestion`** — um bloco só, antes de processar os CSVs. São escolhas com opções definidas, e cada uma muda a análise inteira:
   - **Finalidade do RAF** — instruir representação cautelar (o foco vira demonstrar os requisitos da medida), instruir relatório final de IP, ou subsidiar novas diligências. Um RAF escrito para a finalidade errada é tecnicamente correto e processualmente inútil.
   - **Recorte temporal** — todo o período coberto pelo RIF ou uma janela específica (ex.: só o período do fato investigado). Analisar cinco anos quando interessam seis meses enterra o achado relevante em ruído.
   - **Tratamento dos não-alvos** — se as pessoas que aparecem no RIF sem serem alvos entram na análise como possíveis laranjas/interpostas ou ficam apenas registradas. Isso decide o tamanho da rede a mapear.

   Se ele responder "não sei" a qualquer uma, siga o padrão mais abrangente (RAF genérico, período integral, não-alvos registrados) e sinalize a premissa no relatório.
4. **Validar** os arquivos recebidos imediatamente
5. **Apresentar resumo rápido**: quantidade de comunicações, titulares, período e valores totais
6. **Informar** ao usuário quais alvos da investigação constam no RIF e em qual condição (titular, depositante, sacador, responsável, sócio, beneficiário, etc.)
7. **Informar** quais alvos NÃO constam no RIF

### FASE 1 — VALIDAÇÃO E CARREGAMENTO DOS CSVs

#### 1.0 Quando o RIF vier em PDF em vez de CSV

O COAF normalmente entrega CSV, mas bancos e ofícios às vezes mandam extrato em PDF. Nesse caso, **não leia o PDF no contexto** — extraia primeiro:

```powershell
$py = "$env:USERPROFILE\.claude\tools\docling-venv\Scripts\python.exe"
$ex = "$env:USERPROFILE\.claude\tools\extrair.py"
& $py $ex "extrato.pdf"
```

O extrator reconhece estrutura de tabela e devolve Markdown. Confira os valores contra o original antes de somar: OCR erra dígito. Detalhes em `sync-skills/references/extracao-documentos.md`.

#### 1.1 Identificação dos Arquivos

Os arquivos do COAF seguem o padrão: `RIF_[NÚMERO]_[Tipo].csv`

Tipos esperados:
- `RIF_XXXXX_Envolvidos.csv` — Pessoas físicas/jurídicas + dados cadastrais + tipo de envolvimento
- `RIF_XXXXX_Comunicacoes.csv` — Comunicações financeiras + valores + períodos + informações adicionais
- `RIF_XXXXX_Ocorrencias.csv` — Irregularidades + normativas aplicáveis

#### 1.2 Carregamento com Tratamento de Encoding

```python
import pandas as pd
import os

# Os CSVs do COAF geralmente vêm em ISO-8859-1 (latin-1) com separador ;
ENCODINGS = ['latin-1', 'utf-8', 'cp1252']
SEPARATORS = [';', ',']

def load_csv_coaf(filepath):
    """Carrega CSV do COAF tentando múltiplos encodings e separadores."""
    for enc in ENCODINGS:
        for sep in SEPARATORS:
            try:
                df = pd.read_csv(filepath, encoding=enc, sep=sep, dtype=str)
                if len(df.columns) > 1 and 'Indexador' in df.columns:
                    return df
            except:
                continue
    raise ValueError(f"Não foi possível ler o arquivo: {filepath}")
```

#### 1.3 Validação Estrutural

```python
def validar_estrutura(df_env, df_com, df_oco):
    """Valida estrutura mínima dos 3 CSVs."""
    erros = []
    
    # Verificar coluna Indexador em todos
    for nome, df in [('Envolvidos', df_env), ('Comunicacoes', df_com), ('Ocorrencias', df_oco)]:
        if 'Indexador' not in df.columns:
            erros.append(f"Coluna 'Indexador' ausente em {nome}")
    
    # Colunas mínimas esperadas
    cols_env = ['cpfCnpjEnvolvido', 'nomeEnvolvido', 'tipoEnvolvido']
    cols_com = ['idComunicacao', 'Data_da_operacao', 'CampoA']
    cols_oco = ['Ocorrencia']
    
    for col in cols_env:
        if col not in df_env.columns:
            erros.append(f"Coluna '{col}' ausente em Envolvidos")
    for col in cols_com:
        if col not in df_com.columns:
            erros.append(f"Coluna '{col}' ausente em Comunicações")
    for col in cols_oco:
        if col not in df_oco.columns:
            erros.append(f"Coluna '{col}' ausente em Ocorrências")
    
    return erros
```

### FASE 2 — FILTRAGEM DE INDEXADORES E LIMPEZA DE DADOS

**CRÍTICO**: O COAF inclui elementos não-indexadores nos arquivos CSV. É obrigatório filtrar antes de qualquer análise.

#### 2.1 Filtragem de Indexadores Reais

```python
def filtrar_indexadores_reais(df):
    """
    Filtra apenas linhas com Indexadores reais (números inteiros sequenciais).
    Remove: linhas em branco, hashes, comentários COAF, legendas de campos.
    """
    df_clean = df.copy()
    df_clean['Indexador'] = df_clean['Indexador'].astype(str).str.strip()
    
    # Manter apenas indexadores numéricos inteiros
    mask = df_clean['Indexador'].str.match(r'^\d+$', na=False)
    
    removidos = len(df_clean) - mask.sum()
    df_clean = df_clean[mask].copy()
    df_clean['Indexador'] = df_clean['Indexador'].astype(int)
    
    return df_clean, removidos
```

#### 2.2 Elementos a IGNORAR (NÃO são indexadores)

No arquivo **Comunicações**:
- Linhas em branco
- Comentários explicativos sobre CodigoSegmento (ex: "42 - SFN - Espécie: CampoA = Total...")
- Legendas dos campos de valores (CampoA, CampoB, etc.)
- Hashes aleatórios

No arquivo **Ocorrências**:
- Códigos hash longos (ex: "68670979e17874d3514c2d223b727cba")
- Linhas em branco
- Qualquer string não numérica na coluna Indexador

### FASE 3 — DEDUPLICAÇÃO POR idComunicacao

**ZERO TOLERÂNCIA para contagem dupla.** Duas regras estruturais:

1. **idComunicacao vazio/nulo NÃO deduplica**: linhas sem id são comunicações distintas — todas ficam. O `drop_duplicates` do pandas trata NaN como iguais entre si e eliminaria comunicações reais silenciosamente.
2. **Dupla semântica da deduplicação**: deduplicar APENAS em agregações de nível-caso (volume total, ranking de envolvidos, contagem geral). No **detalhamento por RIF** (tabela "comunicações do RIF X", breakdown com "RIF de Origem"), a comunicação compartilhada aparece em CADA RIF de propósito — ela integra ambos os relatórios do COAF. Deduplicar ali esconderia a comunicação de um dos RIFs.

```python
def deduplicar_comunicacoes(df_com):
    """
    Elimina comunicações duplicadas por idComunicacao — usar SOMENTE para
    agregações de nível-caso (ver dupla semântica acima).
    Quando múltiplos RIFs referem a mesma comunicação, mantém a mais completa.
    Linhas com idComunicacao vazio/nulo são únicas por definição: todas ficam.
    """
    ids = df_com['idComunicacao'].fillna('').astype(str).str.strip()
    sem_id = df_com[ids == '']
    com_id = df_com[ids != ''].copy()

    # Priorizar comunicação com mais dados em informacoesAdicionais
    com_id['_info_len'] = com_id['informacoesAdicionais'].fillna('').str.len()
    com_id = com_id.sort_values('_info_len', ascending=False).drop_duplicates(
        subset=['idComunicacao'], keep='first'
    ).drop(columns=['_info_len'])

    df_dedup = pd.concat([com_id, sem_id]).sort_index()
    eliminadas = len(df_com) - len(df_dedup)
    return df_dedup, eliminadas
```

### FASE 4 — ANÁLISE RELACIONAL INTEGRADA

**OBRIGATÓRIO**: Cruzar dados SEMPRE por Indexador. JAMAIS analisar arquivos isoladamente.

#### 4.1 Cruzamento Relacional

```python
def cruzar_por_indexador(df_env, df_com, df_oco):
    """
    Cruza os três CSVs pelo campo Indexador para análise integrada.
    """
    # Merge Envolvidos + Comunicações
    df_merged = pd.merge(df_env, df_com, on='Indexador', how='outer', suffixes=('_env', '_com'))
    
    # Merge com Ocorrências
    df_full = pd.merge(df_merged, df_oco, on='Indexador', how='outer')
    
    return df_full
```

#### 4.2 Identificação de Titulares

```python
def identificar_titulares(df_env):
    """
    Identifica os titulares de contas (tipo = 'Titular').
    """
    titulares = df_env[df_env['tipoEnvolvido'].str.strip().str.lower() == 'titular']
    return titulares[['Indexador', 'cpfCnpjEnvolvido', 'nomeEnvolvido', 
                       'agenciaEnvolvido', 'contaEnvolvido', 'DataAberturaConta']].drop_duplicates()
```

#### 4.3 Conversão de Valores Monetários

```python
import re

def converter_valor_br(valor_str):
    """Converte valor monetário para float, tolerando formato brasileiro E americano.

    Regras (na ordem):
    - ponto E vírgula → ponto é milhar, vírgula é decimal ("10.000,50" → 10000.5)
    - só vírgula → decimal ("10000,50" → 10000.5)
    - só ponto em grupos de 3 → milhar ("10.000" → 10000; "1.234.567" → 1234567)
    - só ponto fora do padrão milhar → decimal ("1500.75" → 1500.75)
    Sem essas regras, "1500.75" viraria 150075 (erro ×100) e "10.000" com
    replace ingênuo de vírgula viraria 10.0 em fonte americana.
    """
    if pd.isna(valor_str) or str(valor_str).strip() in ['', '0', '-']:
        return 0.0
    s = re.sub(r'\s|R\$', '', str(valor_str), flags=re.IGNORECASE)
    if not s:
        return 0.0
    tem_ponto, tem_virgula = '.' in s, ',' in s
    if tem_ponto and tem_virgula:
        s = s.replace('.', '').replace(',', '.')
    elif tem_virgula:
        s = s.replace(',', '.')
    elif tem_ponto and re.fullmatch(r'-?\d{1,3}(\.\d{3})+', s):
        s = s.replace('.', '')
    try:
        return float(s)
    except ValueError:
        return 0.0

def formatar_valor_br(valor):
    """Formata float para formato brasileiro R$ X.XXX,XX"""
    if valor == 0:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
```

#### 4.4 Cálculo de Valores por Titular

Os campos de valores nos CSVs do COAF seguem esta estrutura para os segmentos 41 (SFN - Atípicas / COS) e 42 (SFN - Espécie / COE):
- **CampoA**: Total
- **CampoB**: Valor do Crédito
- **CampoC**: Valor do Débito
- **CampoD**: Valor do Provisionamento
- **CampoE**: Valor da Proposta

**IMPORTANTE**: O significado dos campos varia por CodigoSegmento. A tabela completa por segmento está em `references/legenda_campos_segmento.md`. Se o próprio CSV de Comunicações trouxer linhas de legenda (linhas não-indexadoras), a legenda do arquivo prevalece; a tabela de referência é o fallback autoritativo. SEMPRE consultar a legenda antes de interpretar os valores.

#### 4.5 Verificação de Alvos da Investigação

```python
def verificar_alvos(df_env, lista_alvos):
    """
    Verifica quais alvos da investigação constam no RIF e em qual condição.
    lista_alvos: lista de dicts com {'nome': str, 'cpf_cnpj': str}
    """
    resultados = []
    for alvo in lista_alvos:
        cpf = alvo.get('cpf_cnpj', '').strip()
        nome = alvo.get('nome', '').strip().upper()
        
        # Buscar por CPF/CNPJ
        encontrado = df_env[df_env['cpfCnpjEnvolvido'].str.strip() == cpf]
        
        if len(encontrado) == 0 and nome:
            # Tentar por nome
            encontrado = df_env[df_env['nomeEnvolvido'].str.strip().str.upper().str.contains(nome, na=False)]
        
        if len(encontrado) > 0:
            tipos = encontrado['tipoEnvolvido'].unique().tolist()
            indexadores = encontrado['Indexador'].unique().tolist()
            resultados.append({
                'nome': encontrado['nomeEnvolvido'].iloc[0],
                'cpf_cnpj': encontrado['cpfCnpjEnvolvido'].iloc[0],
                'encontrado': True,
                'tipos_envolvimento': tipos,
                'indexadores': indexadores
            })
        else:
            resultados.append({
                'nome': alvo.get('nome', 'N/I'),
                'cpf_cnpj': cpf,
                'encontrado': False,
                'tipos_envolvimento': [],
                'indexadores': []
            })
    
    return resultados
```

### FASE 5 — ANÁLISE DE TIPOLOGIAS E INDÍCIOS

#### 5.1 Tipologias de Lavagem de Dinheiro

Ao analisar as movimentações, buscar padrões que indiquem:

**Fase 1 — Colocação (Placement):**
- Depósitos em espécie acima de R$ 50.000,00
- Fracionamento (structuring/smurfing): múltiplos depósitos logo abaixo dos limites
- Depósitos em agências diversas para mesma conta
- Uso de terceiros para depositar (laranjas)

**Fase 2 — Ocultação (Layering):**
- Transferências entre múltiplas contas sem justificativa econômica
- Uso de pessoas jurídicas para intermediar valores
- Movimentações em Estados/cidades distantes do domicílio
- Recebimento de crédito com imediato débito dos valores
- Transferências circulares (A→B→C→A)

**Fase 3 — Integração (Integration):**
- Aquisição de bens de alto valor
- Investimentos incompatíveis com perfil
- Movimentações por empresas sem atividade econômica real
- Operações com PEPs (Pessoas Expostas Politicamente)

#### 5.2 Carta Circular BACEN nº 4.001/2020 — Referência Rápida

Esta Carta Circular elenca 17 categorias de situações suspeitas. As mais frequentes em análise RIF:

| Inciso | Categoria | Exemplos Frequentes |
|--------|-----------|-------------------|
| I | Operações em espécie | Depósitos/saques fracionados, valores incompatíveis |
| III | Identificação de clientes | Informação falsa, múltiplas contas |
| IV | Movimentação de contas | Incompatibilidade com renda, transferências atípicas |
| VII | Recursos do setor público | Agentes públicos, licitações |
| XVII | Regiões de risco | Fronteira, extração mineral |

**SEMPRE** correlacionar as ocorrências do RIF com os incisos específicos da Carta Circular 4.001/2020.

#### 5.3 Análise de Vínculos

```python
def mapear_vinculos(df_env):
    """
    Mapeia os vínculos entre envolvidos por Indexador.
    Pessoas que aparecem no mesmo Indexador possuem vínculo financeiro.
    """
    vinculos = []
    for idx in df_env['Indexador'].unique():
        envolvidos = df_env[df_env['Indexador'] == idx]
        nomes = envolvidos[['cpfCnpjEnvolvido', 'nomeEnvolvido', 'tipoEnvolvido']].values.tolist()
        
        # Criar pares de vínculos
        for i in range(len(nomes)):
            for j in range(i+1, len(nomes)):
                vinculos.append({
                    'indexador': idx,
                    'pessoa_1': nomes[i][1],
                    'cpf_1': nomes[i][0],
                    'tipo_1': nomes[i][2],
                    'pessoa_2': nomes[j][1],
                    'cpf_2': nomes[j][0],
                    'tipo_2': nomes[j][2]
                })
    
    return pd.DataFrame(vinculos)
```

### FASE 6 — GERAÇÃO DO RAF (Relatório de Análise Financeira)

**OBRIGATÓRIO**: Seguir o modelo `references/modelo_raf_v1.md` com todas as 9 seções.

#### Estrutura do RAF:

1. **Introdução** — Contextualização do pedido de análise
2. **COAF** — Breve explicação institucional
3. **Metodologia e Material Analisado** — RIFs analisados, ferramentas utilizadas
4. **Conceitos** — Definições técnicas (COE, COS, Titular, etc.)
5. **Informações Gerais** — Diagrama de vínculos, resumo das operações, titulares com mais comunicações, valores por UF/cidade
6. **Análise Individual dos Titulares** — Para cada titular, 7 subseções obrigatórias:
   - 6.X.1 Perfil e dados cadastrais
   - 6.X.2 Movimentações de crédito detalhadas
   - 6.X.3 Movimentações de débito detalhadas
   - 6.X.4 Investimentos e operações especiais
   - 6.X.5 Principais insights e conexões
   - 6.X.6 Análise dissertativa e compatibilidade financeira
   - 6.X.7 Indícios de lavagem e conclusão individual
7. **Considerações Finais** — Síntese, pessoas relacionadas, conclusão geral
8. **Anexo** — Relação completa de envolvidos
9. **Informações Complementares** — Documento anexo com análise de indícios, recomendações investigativas e medidas cautelares sugeridas

#### Geração do Documento

O RAF deve ser gerado em formato `.docx` profissional. Para isso:

1. **Ler a skill `/mnt/skills/public/docx/SKILL.md`** antes de gerar o documento
2. Aplicar formatação profissional com:
   - Sumário/índice
   - Cabeçalhos hierárquicos
   - Tabelas formatadas
   - Numeração de páginas
   - Rodapé com classificação SIGILOSO
3. Valores SEMPRE em formato brasileiro: R$ X.XXX,XX
4. Datas em formato dd/mm/aaaa

### FASE 6.5 — REVISÃO POR AGENTE INDEPENDENTE (OBRIGATÓRIA)

Antes de entregar o RAF (no chat ou em .docx), submeter o rascunho a um **subagente revisor** via ferramenta Agent (general-purpose), que NÃO participou da redação. O revisor recebe o rascunho completo do RAF e as tabelas consolidadas (tudo local — nenhum dado sai da máquina) com a instrução de auditar:

1. **Somas e totais** — recalcular valores de crédito/débito por titular e totais gerais a partir das tabelas; não confiar nos números do texto
2. **Contradições internas** — divergências entre o corpo dissertativo e as tabelas (valores, datas, quantidades de comunicações)
3. **Vínculos sem sustentação** — toda conexão afirmada entre envolvidos deve ter lastro no cruzamento por Indexador; hipóteses devem estar marcadas como indício, nunca como fato
4. **Duplicidades residuais** — mesmo idComunicacao contado mais de uma vez em somas ou contagens
5. **Rastreabilidade** — valores citados sem correspondência nas tabelas de origem

**Fluxo**: o revisor devolve lista de apontamentos → corrigir cada um no RAF → registrar na entrega ao usuário o que foi corrigido (ou informar "revisão independente sem apontamentos"). **Proibido entregar o RAF sem esta revisão.**

### FASE 7 — APRESENTAÇÃO INTERATIVA DOS RESULTADOS

Após a análise, apresentar ao usuário:

1. **Resumo executivo** com os achados principais
2. **Dashboard** de dados: quantidade de comunicações, valores totais, período
3. **Status dos alvos**: quais constam/não constam no RIF
4. **Alertas**: padrões suspeitos identificados
5. **Perguntar** se o usuário deseja:
   - Gerar o RAF completo em .docx
   - Aprofundar análise de algum titular específico
   - Ver diagrama de vínculos
   - Exportar tabelas específicas

## Tratamento de Múltiplos RIFs

Quando o usuário enviar dados de mais de um RIF:

1. Identificar cada RIF pela numeração dos arquivos
2. Consolidar por CPF/CNPJ dos titulares
3. **Deduplicar por idComunicacao** entre RIFs nas agregações de nível-caso (mesma comunicação = contar uma só vez em totais e rankings)
4. Incluir campo "RIF de Origem" nas tabelas — e no detalhamento POR RIF a comunicação compartilhada aparece em cada RIF a que pertence (ver dupla semântica na FASE 3)
5. Somar valores de nível-caso APENAS após eliminação de repetições
6. Manter rastreabilidade completa (qual dado veio de qual RIF)

## Guardrails Críticos

Além das [Diretrizes Éticas Invioláveis](#diretrizes-éticas-invioláveis) definidas no início deste documento, aplicam-se estas regras operacionais específicas do fluxo de deduplicação e cruzamento:

- **Obrigatório** marcar divergências ou inconsistências entre arquivos
- **Proibido** compartilhar dados brutos fora da estrutura do relatório técnico
- **Obrigatório** registrar todas as exclusões/eliminações de repetições aplicadas
- **Permitido apenas**: análises compatíveis com finalidade investigativa/legal

## Referências Normativas

- **Lei nº 9.613/1998** — Lei de Lavagem de Dinheiro
- **Lei nº 13.260/2016** — Lei Antiterrorismo
- **Circular BACEN nº 3.978/2020** — Prevenção à lavagem de dinheiro
- **Carta Circular BACEN nº 4.001/2020** — Operações e situações suspeitas (17 categorias)
- **Lei nº 13.709/2018** — LGPD (Lei Geral de Proteção de Dados)
- **Lei nº 12.683/2012** — Atualização da Lei de Lavagem
- **Resolução COAF nº 36/2021** — Procedimentos de PLD/FTP

## Estrutura dos CSVs do COAF

Colunas, exemplos de dados e características técnicas (encoding, separador, quebra de linha): `references/csv_structure_examples.md`. Significado de CampoA–CampoE por segmento comunicante: `references/legenda_campos_segmento.md`.

**Precedência**: quando o Comunicações.csv trouxer linhas de legenda (não-indexadoras, no padrão `NN - Nome do segmento: CampoA = ...`), elas prevalecem sobre a tabela de referência. O `processar_rif.py` extrai essas linhas antes de descartá-las.

## Processamento dos CSVs

Não reescreva o pipeline no contexto: rode `scripts/processar_rif.py`, que implementa as FASES 1 a 3 acima — carga com detecção de encoding e separador, extração de legendas, filtragem de indexadores, deduplicação por `idComunicacao` e conversão de valor no padrão brasileiro.

```powershell
python scripts/processar_rif.py --entrada "<pasta dos CSVs>" --saida resumo.json --exportar-limpos ./limpos
```

- `--saida` grava o resumo em JSON (contagens, valor total, período, legendas encontradas) — leia esse arquivo em vez de recontar no contexto.
- `--exportar-limpos` grava os três CSVs já limpos, que são a base das FASES 4 a 6.
- Requer `pandas`. Não havendo na máquina, usar o venv de extração (`~/.claude/tools/docling-venv/Scripts/python.exe`).

Os blocos de código das FASES 1 a 3 documentam a lógica de cada etapa; o script é a implementação autoritativa dela. Divergindo os dois, o script vale.

## Mensagem Inicial ao Usuário

Ao iniciar uma análise RIF, Claude deve se apresentar com:

---

**Olá! Sou seu assistente especializado em análise de dados financeiros (RIF/COAF).**

Estou pronto para processar os dados do Relatório de Inteligência Financeira. Para uma análise completa, preciso:

📋 **Arquivos necessários (3 CSVs):**
- RIF_[Nº]_Envolvidos.csv
- RIF_[Nº]_Comunicacoes.csv
- RIF_[Nº]_Ocorrencias.csv

📝 **Informações do procedimento:**
- Número do IP/PCNET
- Nomes e CPFs/CNPJs dos alvos da investigação
- Unidade policial e autoridade solicitante

🔍 **Processamento garantido:**
✅ Validação prévia obrigatória
✅ Filtragem de indexadores reais
✅ Eliminação de repetições por idComunicacao
✅ Análise relacional cruzada por Indexador
✅ Identificação de tipologias de lavagem (CC 4.001/2020)
✅ Relatório técnico RAF padronizado em .docx

---

## Notas Finais

- O RAF deve ser gerado usando a skill docx (`/mnt/skills/public/docx/SKILL.md`)
- Sempre formatar o documento como SIGILOSO
- Manter rastreabilidade total entre dados brutos e análises
- Todas as conclusões devem ser fundamentadas nos dados dos CSVs
- Recomendações investigativas são sugestões técnicas, cabendo à Autoridade Policial a decisão final
