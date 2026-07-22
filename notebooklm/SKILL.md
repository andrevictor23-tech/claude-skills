---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through document-only responses.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

## Idioma / Language

Formule as perguntas **sempre no mesmo idioma dos documentos** do notebook consultado. Para o usuÃ¡rio AndrÃ© (Delegado de PolÃ­cia Civil / PCMT), use **portuguÃªs do Brasil** em todas as queries. As respostas do NotebookLM espelharÃ£o o idioma da pergunta.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook", "consulta no notebook", "pesquisa no NotebookLM", "o que diz o notebook sobre"
- Needs source-grounded research for police reports, legal briefs, or concurso prep
- Needs content research for Instagram/social media posts

## âš ï¸ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "Qual Ã© o conteÃºdo deste notebook? Quais temas sÃ£o abordados? ForneÃ§a uma visÃ£o geral completa de forma breve e concisa." --notebook-url "[URL]"

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
# âœ… CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# âŒ WRONG - Never call directly:
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
- Tell user: "Uma janela do navegador serÃ¡ aberta para login no Google"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Nome Descritivo" \
  --description "O que este notebook contÃ©m" \
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

### DomÃ­nio JurÃ­dico-Policial (Delegacia de Alta Floresta/PCMT)

```bash
# Pesquisar jurisprudÃªncia sobre tipificaÃ§Ã£o penal
python scripts/run.py ask_question.py \
  --question "Qual Ã© o entendimento do STJ e STF sobre [tipo penal]? Inclua sÃºmulas aplicÃ¡veis e teses fixadas em recursos repetitivos." \
  --notebook-id juridico

# Verificar procedimento para tipo de caso
python scripts/run.py ask_question.py \
  --question "Qual o procedimento correto para [flagrante/APF/TCO/IP] em caso de [situaÃ§Ã£o]? Fundamente no CPP." \
  --notebook-id juridico

# Consultar Lei Maria da Penha / Lei Henry Borel
python scripts/run.py ask_question.py \
  --question "Quais os requisitos legais e procedimentos para [medida protetiva/APF/representaÃ§Ã£o] em caso de violÃªncia domÃ©stica contra [mulher/crianÃ§a]?" \
  --notebook-id violencia-domestica

# Pesquisar trÃ¡fico/drogas
python scripts/run.py ask_question.py \
  --question "Qual a distinÃ§Ã£o entre trÃ¡fico e uso pessoal segundo a Lei 11.343/2006 e a jurisprudÃªncia atual? Quais os critÃ©rios objetivos utilizados?" \
  --notebook-id drogas
```

### DomÃ­nio Concurso PÃºblico

```bash
# Gerar flashcards de estudo
python scripts/run.py ask_question.py \
  --question "Gere 10 questÃµes de mÃºltipla escolha no estilo CESPE sobre [tema], com gabarito e justificativa de cada alternativa." \
  --notebook-id concurso

# Resumo de ponto do edital
python scripts/run.py ask_question.py \
  --question "FaÃ§a um resumo esquemÃ¡tico e didÃ¡tico do tema [X] para concurso de Delegado, destacando os pontos mais cobrados em provas." \
  --notebook-id concurso

# DistinÃ§Ãµes e pegadinhas
python scripts/run.py ask_question.py \
  --question "Quais sÃ£o as principais distinÃ§Ãµes e 'pegadinhas' de prova sobre [tema]? Liste em formato comparativo." \
  --notebook-id concurso
```

### DomÃ­nio ConteÃºdo Digital (Instagram/TikTok/YouTube)

```bash
# Pesquisar ideias de conteÃºdo viral
python scripts/run.py ask_question.py \
  --question "Quais formatos e ganchos de conteÃºdo sobre [tema] tÃªm maior potencial viral no Instagram Reels e TikTok segundo as fontes?" \
  --notebook-id conteudo

# Script para Reels
python scripts/run.py ask_question.py \
  --question "Crie um roteiro de 60 segundos para Reels sobre [tema], com gancho inicial impactante, desenvolvimento e CTA final." \
  --notebook-id conteudo

# EstratÃ©gia de autoridade institucional
python scripts/run.py ask_question.py \
  --question "Quais estratÃ©gias de conteÃºdo sÃ£o recomendadas para construir autoridade digital como Delegado de PolÃ­cia no Instagram?" \
  --notebook-id conteudo
```

### DomÃ­nio IA e Produtividade (Claude/Skills/ECC)

```bash
# Pesquisar como usar Skills do Claude Code
python scripts/run.py ask_question.py \
  --question "Como criar e estruturar uma skill para o Claude Code? Quais sÃ£o os componentes obrigatÃ³rios do SKILL.md?" \
  --notebook-id claude-skills

# Pesquisar loops e automaÃ§Ãµes
python scripts/run.py ask_question.py \
  --question "O que sÃ£o loops no contexto de agentes IA? Como projetar um loop eficiente para [tarefa]?" \
  --notebook-id claude-skills

# ECC e configuraÃ§Ã£o avanÃ§ada
python scripts/run.py ask_question.py \
  --question "O que o ECC (Everything Claude Code) oferece alÃ©m das funcionalidades padrÃ£o? Quais sÃ£o os principais harnesses disponÃ­veis?" \
  --notebook-id claude-skills
```

## Integration Patterns with Other Skills

### Pipeline: NotebookLM â†’ relatorio-final-ip

Use NotebookLM para pesquisa jurÃ­dica antes de redigir um relatÃ³rio de inquÃ©rito:

```bash
# 1. Pesquisar tipificaÃ§Ã£o e jurisprudÃªncia
python scripts/run.py ask_question.py \
  --question "Qual a tipificaÃ§Ã£o correta e os requisitos probatÃ³rios para [crime] segundo CP, jurisprudÃªncia STJ e STF?" \
  --notebook-id juridico

# 2. Com as referÃªncias obtidas, acionar a skill relatorio-final-ip
# A pesquisa do NotebookLM fornece fundamento jurÃ­dico sÃ³lido para o relatÃ³rio
```

### Pipeline: NotebookLM â†’ instagram-autoridade

```bash
# 1. Pesquisar tendÃªncias e melhores prÃ¡ticas
python scripts/run.py ask_question.py \
  --question "Quais tipos de conteÃºdo sobre seguranÃ§a pÃºblica e direito tÃªm maior engajamento no Instagram segundo as fontes?" \
  --notebook-id conteudo

# 2. Com os insights, acionar instagram-autoridade para anÃ¡lise do perfil
```

### Pipeline: NotebookLM â†’ mapa-mental

```bash
# 1. Extrair estrutura do tema
python scripts/run.py ask_question.py \
  --question "Liste todos os tÃ³picos, subtÃ³picos e conceitos-chave sobre [tema] de forma hierÃ¡rquica." \
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

## Recommended Notebook Library Structure (AndrÃ© - PCMT)

| ID sugerido | Nome | TÃ³picos | ConteÃºdo |
|---|---|---|---|
| `juridico` | Direito Penal e Processual | cp,cpp,stj,stf,jurisprudencia | CP, CPP, sÃºmulas, jurisprudÃªncia |
| `violencia-domestica` | ViolÃªncia DomÃ©stica e Familiar | lmp,henry-borel,vitimas | Lei 11.340, Lei 14.344, Lei 13.431 |
| `drogas` | Lei de Drogas | trafico,uso,11343 | Lei 11.343/2006, jurisprudÃªncia |
| `concurso` | Concurso Delegado | edital,questoes,cespe | Material de estudo, editais, provas anteriores |
| `conteudo` | ConteÃºdo Digital | instagram,reels,tiktok,viral | EstratÃ©gias de criaÃ§Ã£o de conteÃºdo |
| `claude-skills` | Claude Code e IA | ecc,skills,loops,agentes | DocumentaÃ§Ã£o Claude, ECC, skills |
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
UsuÃ¡rio menciona NotebookLM / compartilha URL / pergunta sobre documentos
    â†“
Verificar auth â†’ python scripts/run.py auth_manager.py status
    â†“
Se nÃ£o autenticado â†’ python scripts/run.py auth_manager.py setup
    â†“
Verificar/Adicionar notebook â†’ python scripts/run.py notebook_manager.py list/add
    â†“
Identificar domÃ­nio â†’ jurÃ­dico? concurso? conteÃºdo? IA/skills?
    â†“
Usar template de query do domÃ­nio correspondente
    â†“
Perguntar â†’ python scripts/run.py ask_question.py --question "..."
    â†“
Ver "Is that ALL you need?" â†’ Fazer follow-ups atÃ© completar
    â†“
Sintetizar em portuguÃªs â†’ Responder ao usuÃ¡rio
    â†“
Integrar com outra skill se necessÃ¡rio (relatorio-final-ip, mapa-mental, etc.)
```

## Troubleshooting

| Problema | SoluÃ§Ã£o |
|---------|----------|
| ModuleNotFoundError | Use o wrapper `run.py` |
| Falha de autenticaÃ§Ã£o | Browser deve estar visÃ­vel no setup! --show-browser |
| Rate limit (50/dia) | Aguardar ou trocar conta Google |
| Browser trava | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook nÃ£o encontrado | Verificar com `notebook_manager.py list` |
| Resposta em inglÃªs | Formular a pergunta em portuguÃªs |

## Best Practices

1. **Sempre use run.py** - Gerencia o ambiente automaticamente
2. **Verifique auth primeiro** - Antes de qualquer operaÃ§Ã£o
3. **Perguntas de acompanhamento** - NÃ£o pare na primeira resposta
4. **Browser visÃ­vel para auth** - ObrigatÃ³rio no login manual
5. **Inclua contexto** - Cada pergunta Ã© independente; inclua contexto relevante
6. **Sintetize respostas** - Combine mÃºltiplas respostas antes de responder
7. **Use templates de domÃ­nio** - Queries especÃ­ficas dÃ£o respostas mais precisas
8. **Organize por domÃ­nio** - Separe jurÃ­dico, concurso, conteÃºdo e IA em notebooks distintos
9. **Integre com outras skills** - NotebookLM Ã© a fase de pesquisa; outras skills produzem o output

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
