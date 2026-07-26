# Contribuindo

Obrigado pelo interesse em contribuir. Este é um projeto pessoal de skills de Claude Code para Polícia Judiciária e estudo jurídico, e contribuições de colegas delegados, servidores, advogados, estudantes e desenvolvedores são bem-vindas.

## Formas de contribuir

- **Correções**: erros de fundamentação jurídica, legislação desatualizada, typos, links quebrados.
- **Adaptações**: variantes de templates para outras unidades, comarcas ou estados (mantendo o template original intacto).
- **Novas skills**: fluxos jurídicos ou de estudo que sigam a estrutura do repositório.
- **Melhorias em skills existentes**: novos exemplos, referências, scripts auxiliares.
- **Ideias e dúvidas**: abra uma [issue](../../issues) ou inicie uma [discussion](../../discussions) — não precisa de código.

## Antes de começar

1. Leia o [README.md](README.md) e o [CLAUDE.md](CLAUDE.md) (convenções do repositório).
2. Procure nas [issues](../../issues) se alguém já propôs algo parecido.
3. Para mudanças grandes (nova skill, refatoração de template), abra uma issue antes de escrever código — evita trabalho perdido.

## Regra inegociável: dados sensíveis

Este repositório é **público**. Pull requests que contenham dados de casos reais, nomes de investigados ou vítimas, números de procedimento, documentos operacionais ou qualquer informação coberta por sigilo funcional ou pela LGPD **serão fechados sem merge**. Use sempre dados fictícios ou anonimizados em exemplos. Veja [SECURITY.md](SECURITY.md).

## Passo a passo

1. Faça um fork e crie uma branch descritiva (`feat/skill-habeas-corpus`, `fix/analise-rif-encoding`).
2. Faça as mudanças seguindo as convenções abaixo.
3. Abra o pull request preenchendo o template. Descreva **o que** mudou e **por quê**.

### Convenções

- **Idioma**: skills autorais e documentação em português brasileiro.
- **Estrutura de skill**: pasta na raiz com `SKILL.md` (frontmatter YAML com `name` e `description` listando gatilhos de ativação) e, se necessário, `references/`, `scripts/`, `templates/`, `assets/`. Skills autorais devem ter um `README.md` de guia de uso — use os existentes como modelo.
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/pt-br/) — `feat(nome-da-skill): ...`, `fix: ...`, `docs: ...`.
- **Encoding**: UTF-8 sem BOM.
- **Skills de terceiros** (`canvas-design`, `doc-coauthoring`, `find-skills`, `internal-comms`, `notebooklm`, `prompt-master`, `skill-creator`): contribuições devem ir para o projeto de origem; aqui só entram atualizações de sincronização com licenças preservadas.

### Checklist do pull request

- [ ] Nenhum dado sensível ou de caso real
- [ ] `SKILL.md` com frontmatter válido (se a mudança toca uma skill)
- [ ] `README.md` da skill atualizado (se o comportamento mudou)
- [ ] Tabela de skills do `README.md` da raiz atualizada (se skill nova ou renomeada)
- [ ] Testado localmente com o Claude Code

## Conduta

Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, você concorda em respeitá-lo.

## Licença

Ao contribuir, você concorda que sua contribuição será licenciada sob a [licença MIT](LICENSE) do projeto.
