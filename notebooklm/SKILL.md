---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through document-only responses.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

## Idioma / Language

Formule as perguntas **sempre no mesmo idioma dos documentos** do notebook consultado. Para o usuário André (Delegado de Polícia Civil / PCMT), use **português do Brasil** em todas as queries. As respostas do NotebookLM espelharão o idioma da pergunta.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook", "consulta no notebook", "pesquisa no NotebookLM", "o que diz o notebook sobre"
- Needs source-grounded research for police reports, legal briefs, or concurso prep
- Needs content research for Instagram/social media posts

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "Qual é o conteúdo deste notebook? Quais temas são abordados? Forneça uma visão geral completa de forma breve e concisa." --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details missing, use Smart Add to discover them.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## ⚠️ CRITICAL: Custo de Tokens — Script Primeiro, Browser MCP por Último

**Regra:** para PERGUNTAR ao notebook, use SEMPRE `ask_question.py` via Bash. NUNCA dirija o
NotebookLM na mão com as ferramentas de browser MCP (`mcp__claude-in-chrome__*`).

Motivo, medido em sessão real (21/07/2026, revisão MPSP): extrair 3 respostas do notebook
via automação MCP custou **~14k tokens e 15 minutos**. As mesmas 3 respostas via
`ask_question.py` seriam ~3 chamadas Bash com texto puro no stdout.

O que queima tokens na automação MCP:

| Ferramenta | Custo aprox. | Observação |
|---|---|---|
| `computer{action:"screenshot"}` | ~1.500 tokens cada | O maior vilão — evitar |
| `read_page` / `get_page_text` | centenas | Aceitável |
| `javascript_tool` | dezenas | Barato, MAS trunca o retorno em ~1000 caracteres |

O truncamento do `javascript_tool` é a armadilha: uma resposta de 9.000 caracteres do
NotebookLM exige ~10 chamadas fatiadas (`.slice(0,950)`, `.slice(950,1900)`, ...). Foi isso
que estourou o custo.

### Quando o browser MCP é inevitável

O `ask_question.py` só PERGUNTA. Gerenciar fontes exige o browser MCP (a sessão Google logada):
adicionar/re-subir vídeos do YouTube, ver quais fontes falharam, marcar/desmarcar fontes,
usar recursos do Estúdio.

Nesses casos:

1. **Não tire screenshot para ler conteúdo.** Use `javascript_tool` com seletores.
   Screenshot só para localizar coordenada de clique que você não consegue de outro jeito.
2. **Para extrair texto longo, baixe em arquivo em vez de fatiar.** O usuário André autorizou
   downloads para esse fim (21/07/2026). Padrão:

```javascript
// no javascript_tool: dispara download do texto para a pasta de Downloads
const m=[...document.querySelectorAll('chat-message,[class*="message-text"]')];
const t=m[m.length-1].innerText;
const a=document.createElement('a');
a.href=URL.createObjectURL(new Blob([t],{type:'text/plain'}));
a.download='notebooklm-resposta.txt'; a.click();
'ok: '+t.length+' chars'
```

   Depois leia com uma única chamada `Read` em `E:\Users\andre\Downloads\notebooklm-resposta.txt`.
   Troca ~10 idas ao browser por 2.
3. **Listar fontes e detectar falhas** — uma chamada, sem screenshot:

```javascript
const it=[...document.querySelectorAll('.single-source-container')];
const r=it.map(e=>{const b=e.querySelector('button[aria-label]');return b?b.getAttribute('aria-label'):''});
// fontes que falharam aparecem com a URL crua como aria-label, não com o título do vídeo
JSON.stringify({ok:r.filter(x=>!/youtube\.com/i.test(x)), falhas:r.filter(x=>/youtube\.com/i.test(x))})
```

4. **Não brigue com a UI de seleção de fontes.** Os checkboxes do NotebookLM perdem estado ao
   rolar a lista ou filtrar. Em vez de isolar fontes, ancore a pergunta no título:
   *"Baseie-se EXCLUSIVAMENTE na fonte intitulada '[título exato]'. Ignore todas as demais."*
   Funciona de forma confiável e custa zero cliques.

### Vídeos do YouTube recém-enviados

O NotebookLM recusa vídeo cuja transcrição automática ainda não foi gerada pelo YouTube
("Não é possível importar este vídeo. A transcrição está indisponível"). Não é erro do
usuário nem da skill — é o YouTube ainda processando. **Não delete a fonte com falha:**
re-tente no dia seguinte. Re-submeter a URL cria uma entrada nova; se falhar de novo,
o notebook fica com linhas vermelhas duplicadas (limpar só depois que o vídeo entrar).

## Core Workflow

### Step 1: Check Authentication Status
```bash
python scripts/run.py auth_manager.py status
```

If not authenticated, proceed to setup.

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```

**Important:**
- Browser is VISIBLE for authentication
- Browser window opens automatically
- User must manually log in to Google
- Tell user: "Uma janela do navegador será aberta para login no Google"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Nome Descritivo" \
  --description "O que este notebook contém" \
  --topics "topico1,topico2,topico3"

# Search notebooks by topic
python scripts/run.py notebook_manager.py search --query "palavra-chave"

# Set active notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook if set)
python scripts/run.py ask_question.py --question "Sua pergunta aqui"

# Query specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required Claude Behavior:**
1. **STOP** - Do not immediately respond to user
2. **ANALYZE** - Compare answer to user's original request
3. **IDENTIFY GAPS** - Determine if more information needed
4. **ASK FOLLOW-UP** - If gaps exist, immediately ask:
   ```bash
   python scripts/run.py ask_question.py --question "Pergunta de acompanhamento com contexto..."
   ```
5. **REPEAT** - Continue until information is complete
6. **SYNTHESIZE** - Combine all answers before responding to user

## Domain-Specific Query Templates

### Domínio Jurídico-Policial (Delegacia de Alta Floresta/PCMT)

```bash
# Pesquisar jurisprudência sobre tipificação penal
python scripts/run.py ask_question.py \
  --question "Qual é o entendimento do STJ e STF sobre [tipo penal]? Inclua súmulas aplicáveis e teses fixadas em recursos repetitivos." \
  --notebook-id juridico

# Verificar procedimento para tipo de caso
python scripts/run.py ask_question.py \
  --question "Qual o procedimento correto para [flagrante/APF/TCO/IP] em caso de [situação]? Fundamente no CPP." \
  --notebook-id juridico

# Consultar Lei Maria da Penha / Lei Henry Borel
python scripts/run.py ask_question.py \
  --question "Quais os requisitos legais e procedimentos para [medida protetiva/APF/representação] em caso de violência doméstica contra [mulher/criança]?" \
  --notebook-id violencia-domestica

# Pesquisar tráfico/drogas
python scripts/run.py ask_question.py \
  --question "Qual a distinção entre tráfico e uso pessoal segundo a Lei 11.343/2006 e a jurisprudência atual? Quais os critérios objetivos utilizados?" \
  --notebook-id drogas
```

### Domínio Concurso Público

```bash
# Gerar flashcards de estudo
python scripts/run.py ask_question.py \
  --question "Gere 10 questões de múltipla escolha no estilo CESPE sobre [tema], com gabarito e justificativa de cada alternativa." \
  --notebook-id concurso

# Resumo de ponto do edital
python scripts/run.py ask_question.py \
  --question "Faça um resumo esquemático e didático do tema [X] para concurso de Delegado, destacando os pontos mais cobrados em provas." \
  --notebook-id concurso

# Distinções e pegadinhas
python scripts/run.py ask_question.py \
  --question "Quais são as principais distinções e 'pegadinhas' de prova sobre [tema]? Liste em formato comparativo." \
  --notebook-id concurso
```

### Domínio Conteúdo Digital (Instagram/TikTok/YouTube)

```bash
# Pesquisar ideias de conteúdo viral
python scripts/run.py ask_question.py \
  --question "Quais formatos e ganchos de conteúdo sobre [tema] têm maior potencial viral no Instagram Reels e TikTok segundo as fontes?" \
  --notebook-id conteudo

# Script para Reels
python scripts/run.py ask_question.py \
  --question "Crie um roteiro de 60 segundos para Reels sobre [tema], com gancho inicial impactante, desenvolvimento e CTA final." \
  --notebook-id conteudo

# Estratégia de autoridade institucional
python scripts/run.py ask_question.py \
  --question "Quais estratégias de conteúdo são recomendadas para construir autoridade digital como Delegado de Polícia no Instagram?" \
  --notebook-id conteudo
```

### Domínio IA e Produtividade (Claude/Skills/ECC)

```bash
# Pesquisar como usar Skills do Claude Code
python scripts/run.py ask_question.py \
  --question "Como criar e estruturar uma skill para o Claude Code? Quais são os componentes obrigatórios do SKILL.md?" \
  --notebook-id claude-skills

# Pesquisar loops e automações
python scripts/run.py ask_question.py \
  --question "O que são loops no contexto de agentes IA? Como projetar um loop eficiente para [tarefa]?" \
  --notebook-id claude-skills

# ECC e configuração avançada
python scripts/run.py ask_question.py \
  --question "O que o ECC (Everything Claude Code) oferece além das funcionalidades padrão? Quais são os principais harnesses disponíveis?" \
  --notebook-id claude-skills
```

## Integration Patterns with Other Skills

### Pipeline: NotebookLM → relatorio-final-ip

Use NotebookLM para pesquisa jurídica antes de redigir um relatório de inquérito:

```bash
# 1. Pesquisar tipificação e jurisprudência
python scripts/run.py ask_question.py \
  --question "Qual a tipificação correta e os requisitos probatórios para [crime] segundo CP, jurisprudência STJ e STF?" \
  --notebook-id juridico

# 2. Com as referências obtidas, acionar a skill relatorio-final-ip
# A pesquisa do NotebookLM fornece fundamento jurídico sólido para o relatório
```

### Pipeline: NotebookLM → instagram-autoridade

```bash
# 1. Pesquisar tendências e melhores práticas
python scripts/run.py ask_question.py \
  --question "Quais tipos de conteúdo sobre segurança pública e direito têm maior engajamento no Instagram segundo as fontes?" \
  --notebook-id conteudo

# 2. Com os insights, acionar instagram-autoridade para análise do perfil
```

### Pipeline: NotebookLM → mapa-mental

```bash
# 1. Extrair estrutura do tema
python scripts/run.py ask_question.py \
  --question "Liste todos os tópicos, subtópicos e conceitos-chave sobre [tema] de forma hierárquica." \
  --notebook-id concurso

# 2. Passar o resultado para a skill mapa-mental para gerar o mapa visual
```

## Script Reference

### Authentication Management (`auth_manager.py`)
```bash
python scripts/run.py auth_manager.py setup    # Initial setup (browser visible)
python scripts/run.py auth_manager.py status   # Check authentication
python scripts/run.py auth_manager.py reauth   # Re-authenticate (browser visible)
python scripts/run.py auth_manager.py clear    # Clear authentication
```

### Notebook Management (`notebook_manager.py`)
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### Question Interface (`ask_question.py`)
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Data Cleanup (`cleanup_manager.py`)
```bash
python scripts/run.py cleanup_manager.py                    # Preview cleanup
python scripts/run.py cleanup_manager.py --confirm          # Execute cleanup
python scripts/run.py cleanup_manager.py --preserve-library # Keep notebooks
```

## Recommended Notebook Library Structure (André - PCMT)

| ID sugerido | Nome | Tópicos | Conteúdo |
|---|---|---|---|
| `juridico` | Direito Penal e Processual | cp,cpp,stj,stf,jurisprudencia | CP, CPP, súmulas, jurisprudência |
| `violencia-domestica` | Violência Doméstica e Familiar | lmp,henry-borel,vitimas | Lei 11.340, Lei 14.344, Lei 13.431 |
| `drogas` | Lei de Drogas | trafico,uso,11343 | Lei 11.343/2006, jurisprudência |
| `concurso` | Concurso Delegado | edital,questoes,cespe | Material de estudo, editais, provas anteriores |
| `conteudo` | Conteúdo Digital | instagram,reels,tiktok,viral | Estratégias de criação de conteúdo |
| `claude-skills` | Claude Code e IA | ecc,skills,loops,agentes | Documentação Claude, ECC, skills |
| `financeiro` | Lavagem e Crime Financeiro | coaf,rif,bacen,lavagem | Carta BACEN 4001, tipologias COAF |

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Chromium browser installs automatically
- Everything isolated in skill directory

Manual setup (only if automatic fails):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Data Storage

All data stored in `~/.claude/skills/notebooklm/data/`:
- `library.json` - Notebook metadata
- `auth_info.json` - Authentication status
- `browser_state/` - Browser cookies and session

**Security:** Protected by `.gitignore`, never commit to git.

## Configuration

Optional `.env` file in skill directory:
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Decision Flow

```
Usuário menciona NotebookLM / compartilha URL / pergunta sobre documentos
    ↓
Verificar auth → python scripts/run.py auth_manager.py status
    ↓
Se não autenticado → python scripts/run.py auth_manager.py setup
    ↓
Verificar/Adicionar notebook → python scripts/run.py notebook_manager.py list/add
    ↓
Identificar domínio → jurídico? concurso? conteúdo? IA/skills?
    ↓
Usar template de query do domínio correspondente
    ↓
Perguntar → python scripts/run.py ask_question.py --question "..."
    ↓
Ver "Is that ALL you need?" → Fazer follow-ups até completar
    ↓
Sintetizar em português → Responder ao usuário
    ↓
Integrar com outra skill se necessário (relatorio-final-ip, mapa-mental, etc.)
```

## Troubleshooting

| Problema | Solução |
|---------|----------|
| ModuleNotFoundError | Use o wrapper `run.py` |
| Falha de autenticação | Browser deve estar visível no setup! --show-browser |
| Rate limit (50/dia) | Aguardar ou trocar conta Google |
| Browser trava | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook não encontrado | Verificar com `notebook_manager.py list` |
| Resposta em inglês | Formular a pergunta em português |

## Best Practices

1. **Sempre use run.py** - Gerencia o ambiente automaticamente
2. **Verifique auth primeiro** - Antes de qualquer operação
3. **Perguntas de acompanhamento** - Não pare na primeira resposta
4. **Browser visível para auth** - Obrigatório no login manual
5. **Inclua contexto** - Cada pergunta é independente; inclua contexto relevante
6. **Sintetize respostas** - Combine múltiplas respostas antes de responder
7. **Use templates de domínio** - Queries específicas dão respostas mais precisas
8. **Organize por domínio** - Separe jurídico, concurso, conteúdo e IA em notebooks distintos
9. **Integre com outras skills** - NotebookLM é a fase de pesquisa; outras skills produzem o output

## Limitations

- No session persistence (each question = new browser)
- Rate limits on free Google accounts (50 queries/day)
- Manual upload required (user must add docs to NotebookLM)
- Browser overhead (few seconds per question)
- NotebookLM Studio features (flashcards, mind maps, audio) not yet automatable via script

## Resources (Skill Structure)

- `scripts/` - All automation scripts (ask_question.py, notebook_manager.py, etc.)
- `data/` - Local storage for authentication and notebook library
- `references/` - Extended documentation:
  - `api_reference.md` - Detailed API documentation for all scripts
  - `troubleshooting.md` - Common issues and solutions
  - `usage_patterns.md` - Best practices and workflow examples
- `.venv/` - Isolated Python environment (auto-created on first run)
- `.gitignore` - Protects sensitive data from being committed
