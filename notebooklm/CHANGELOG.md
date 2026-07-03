
## [2026-07-03] - AtualizaÃ§Ã£o de contexto e templates de domÃ­nio

### Adicionado
- InstruÃ§Ã£o de idioma: queries devem ser formuladas em portuguÃªs do Brasil
- Templates de query por domÃ­nio: jurÃ­dico-policial, concurso pÃºblico, conteÃºdo digital (Instagram/TikTok/YouTube) e IA/produtividade (Claude/ECC/skills)
- Pipelines de integraÃ§Ã£o com outras skills: `relatorio-final-ip`, `instagram-autoridade`, `mapa-mental`
- Tabela de estrutura de biblioteca recomendada (7 notebooks por domÃ­nio de uso)
- Triggers em portuguÃªs adicionados Ã  seÃ§Ã£o "When to Use"
- Mensagem de browser em portuguÃªs no Step 2
- Entrada de troubleshooting para "Resposta em inglÃªs"
- Decision Flow reescrito em portuguÃªs com etapa de identificaÃ§Ã£o de domÃ­nio

### Modificado
- Best Practices ampliadas com orientaÃ§Ãµes de organizaÃ§Ã£o por domÃ­nio e integraÃ§Ã£o de skills
- SeÃ§Ã£o de recursos (Resources) simplificada

### Contexto
- AtualizaÃ§Ã£o baseada em anÃ¡lise do notebook NotebookLM do usuÃ¡rio
  (Claude Code + NotebookLM = HACK DESBLOQUEADO) e padrÃµes de uso diÃ¡rio
  identificados: trabalho policial/jurÃ­dico, preparo para concurso,
  criaÃ§Ã£o de conteÃºdo digital e pesquisa sobre IA/Claude Code.
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-11-21

### Added
- **Modular Architecture** - Refactored codebase for better maintainability
  - New `config.py` - Centralized configuration (paths, selectors, timeouts)
  - New `browser_utils.py` - BrowserFactory and StealthUtils classes
  - Cleaner separation of concerns across all scripts

### Changed
- **Timeout increased to 120 seconds** - Long queries no longer timeout prematurely
  - `ask_question.py`: 30s → 120s
  - `browser_session.py`: 30s → 120s
  - Resolves Issue #4

### Fixed
- **Thinking Message Detection** - Fixed incomplete answers showing placeholder text
  - Now waits for `div.thinking-message` element to disappear before reading answer
  - Answers like "Reviewing the content..." or "Looking for answers..." no longer returned prematurely
  - Works reliably across all languages and NotebookLM UI changes

- **Correct CSS Selectors** - Updated to match current NotebookLM UI
  - Changed from `.response-content, .message-content` to `.to-user-container .message-text-content`
  - Consistent selectors across all scripts

- **Stability Detection** - Improved answer completeness check
  - Now requires 3 consecutive stable polls instead of 1 second wait
  - Prevents truncated responses during streaming

## [1.2.0] - 2025-10-28

### Added
- Initial public release
- NotebookLM integration via browser automation
- Session-based conversations with Gemini 2.5
- Notebook library management
- Knowledge base preparation tools
- Google authentication with persistent sessions

