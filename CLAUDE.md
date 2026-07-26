# CLAUDE.md

Orientações para o Claude Code ao trabalhar neste repositório.

## O que é este repositório

Biblioteca pessoal de skills de Claude Code do André (Delegado de Polícia Civil em Alta Floresta/MT), sincronizada entre máquinas via `~/.claude/skills`. Contém skills autorais em português brasileiro (documentos de Polícia Judiciária, estudo jurídico, produtividade) e skills de terceiros mantidas por conveniência.

## Estrutura

- Cada skill é uma pasta na raiz com um `SKILL.md` (obrigatório, com frontmatter YAML `name` + `description`).
- Pastas auxiliares opcionais por skill: `references/` (material que o Claude lê sob demanda), `scripts/` (Python/PowerShell), `templates/`, `assets/`, `evals/`.
- Skills autorais têm um `README.md` com guia de uso (o que faz, quando usar, exemplos de prompt, requisitos, avisos). Ao criar ou alterar uma skill autoral, mantenha o `README.md` dela em dia.
- Skills de terceiros (`canvas-design`, `doc-coauthoring`, `find-skills`, `internal-comms`, `notebooklm`, `prompt-master`, `skill-creator`): não altere o conteúdo além do mínimo necessário e preserve `LICENSE`/`LICENSE.txt` e créditos.

## Convenções

- **Idioma**: skills autorais, documentação e mensagens ao usuário em português brasileiro. Termos jurídicos por extenso na primeira ocorrência (ex.: "Auto de Prisão em Flagrante (APF)").
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), escopo = nome da skill quando aplicável (ex.: `docs(analise-rif): ...`). O hook de auto-sync gera commits `sync: <data>` automaticamente — não os imite em commits manuais.
- **Encoding**: UTF-8 sem BOM. Cuidado com mojibake ao editar arquivos com acentuação.
- **Novas skills**: use a skill `skill-creator` deste repo como referência de estrutura; descrições de frontmatter devem listar gatilhos de ativação concretos.

## Sigilo e dados sensíveis — regra inegociável

- **Nunca** versione dados de casos reais, nomes de investigados, números de procedimento ou documentos operacionais neste repositório — ele é **público**.
- O acervo sigiloso (modelos reais de peças, documentos da unidade) mora no repositório **privado** `delegacia-claude-workspace`. Aqui ficam apenas os `LEIA-ME` explicativos (ex.: `representacao-cautelar/assets/modelos/`).
- O `.gitignore` da raiz documenta essa política em comentários — leia antes de adicionar arquivos novos em `assets/` ou `references/`.
- Exemplos em documentação devem usar dados fictícios ou anonimizados.

## Hook de auto-sync

`.claude/settings.json` registra um hook de *Stop* que executa `.claude/hooks/auto-sync.sh`: `git add -A` + commit `sync: <data>` + push ao final de cada sessão. Consequências práticas:

- Arquivos deixados na árvore de trabalho serão commitados e publicados automaticamente. Não deixe rascunhos, dados de teste ou arquivos temporários na pasta do repo.
- Prefira commits manuais descritivos para mudanças substantivas; o auto-sync é rede de segurança, não substituto.

## Testes e verificação

- Não há CI. Verifique skills manualmente: frontmatter YAML válido, links internos do README funcionando, scripts Python executam com `python3 <script> --help` (quando aplicável).
- `representacao-cautelar/evals/evals.json` é o único conjunto de evals; a infra de execução está em `skill-creator/`.
