# claude-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Skills](https://img.shields.io/badge/skills-20-8A2BE2.svg)](#skills)
[![Idioma](https://img.shields.io/badge/idioma-pt--BR-009c3b.svg)](#o-que-é)
[![Claude Code](https://img.shields.io/badge/feito%20para-Claude%20Code-d97757.svg)](https://code.claude.com/docs/en/skills)

Skills de Claude Code para produção de documentos de Polícia Judiciária, análise de inteligência financeira e estudo jurídico, escritas em português brasileiro.

**English summary.** I am a Civil Police Chief (Delegado de Polícia Civil) in Alta Floresta, Mato Grosso, Brazil. This repository contains the Claude Code skills I use in daily casework: on-duty arrest dispatches, final reports in criminal investigations, precautionary measure requests, analysis of COAF financial intelligence reports, and study tooling for Brazilian legal exams. It is a personal project and reflects my unit's local conventions. Adaptations and contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The documentation below is in Portuguese, the language of the community it serves.

---

## O que é

Biblioteca de skills para o [Claude Code](https://code.claude.com/docs/en/skills) voltada à produção de documentos de Polícia Judiciária e ao estudo jurídico. Nasceu do meu uso diário como Delegado de Polícia Civil. Publico como está, na expectativa de que sirva a colegas e a outros operadores do Direito.

Cada skill é uma pasta com um `SKILL.md` (instruções que o Claude carrega sob demanda) e, quando necessário, `references/`, `scripts/`, `templates/` e `assets/` de apoio. As skills autorais têm um `README.md` próprio com guia de uso detalhado — clique no nome da skill na tabela abaixo.

## Skills

### Polícia Judiciária

| Skill | O que faz |
|---|---|
| [despacho-plantao](despacho-plantao/) | Despachos de plantão a partir do fato narrado: decide entre APF, TCO, BOC, instauração de IP ou não instauração, com fundamento no CPP, CP e leis extravagantes |
| [relatorio-final-ip](relatorio-final-ip/) | Relatórios finais de inquérito policial, com templates por unidade (NEAMV × Delegacia) e checklist por tipo penal, incluindo violência doméstica sob a Lei 14.994/2024 |
| [representacao-cautelar](representacao-cautelar/) | Representações da Autoridade Policial ao Juízo: preventiva, temporária, busca e apreensão, quebras de sigilo, interceptação e medidas assecuratórias |
| [analise-rif](analise-rif/) | Análise de Relatórios de Inteligência Financeira do COAF (CSVs de envolvidos, comunicações e ocorrências), com Relatório de Análise Financeira em .docx segundo as tipologias da Carta Circular BACEN 4.001/2020 |
| [instagram-autoridade](instagram-autoridade/) | Relatório estratégico e dashboard do Instagram institucional, com salvaguardas de sigilo investigativo, LGPD e Corregedoria (dados via Windsor.ai) |
| [reels-delegado](reels-delegado/) | Fluxo de publicação de reels institucionais: edição com ffmpeg, capa por grade de frames, texto do post e respostas a comentários |

### Estudo jurídico e concursos

| Skill | O que faz |
|---|---|
| [mapa-mental](mapa-mental/) | Mapas mentais interativos em HTML/SVG (metodologia Buzan) para revisão de conteúdo jurídico |
| [simulado-quiz](simulado-quiz/) | Converte PDFs de simulado em quiz HTML interativo ou caderno de erros, com cache de extração |
| [revisao-espacada](revisao-espacada/) | Revisão espaçada com caderno de erros para concursos (intervalos 1/3/7/15/30 dias) |
| [sabatina](sabatina/) | Entrevista socrática pergunta a pergunta até haver entendimento compartilhado, antes de produzir qualquer peça |
| [vocabulario-kindle](vocabulario-kindle/) | Converte o `vocab.db` do Kindle Vocabulary Builder em baralho Anki com frases reais dos livros |

### Produtividade pessoal

| Skill | O que faz |
|---|---|
| [analise-carteira](analise-carteira/) | Análise de carteira de investimentos na filosofia Bastter/Canal do Holder/Fundamentei (não é recomendação de investimento) |
| [sync-skills](sync-skills/) | Sincroniza as skills entre máquinas via git; inclui extrator universal de documentos (Docling + EasyOCR) |

### Skills de terceiros

Mantidas aqui por conveniência de sincronização, com licenças e créditos preservados nas respectivas pastas:

| Skill | Origem / o que faz |
|---|---|
| [notebooklm](notebooklm/) | Consulta notebooks do Google NotebookLM via automação de browser, com respostas ancoradas nas fontes |
| [canvas-design](canvas-design/) | Arte visual em .png/.pdf (pôsteres e peças estáticas) |
| [internal-comms](internal-comms/) | Comunicações internas (status reports, newsletters, FAQs) |
| [skill-creator](skill-creator/) | Criação, edição e avaliação (evals) de skills |
| [doc-coauthoring](doc-coauthoring/) | Co-autoria estruturada de documentos, propostas e specs |
| [find-skills](find-skills/) | Descoberta e instalação de skills a partir de perguntas "how do I do X" |
| [prompt-master](prompt-master/) | Geração de prompts otimizados para ferramentas de IA |

## Instalação

Para skills pessoais, disponíveis em todos os projetos:

```bash
git clone https://github.com/andrevictor23-tech/claude-skills.git
cp -r claude-skills/nome-da-skill ~/.claude/skills/
```

Para uso restrito a um projeto, copie a pasta para `.claude/skills/` na raiz do projeto. Documentação oficial: https://code.claude.com/docs/en/skills

> **Atenção ao clonar o repositório inteiro:** o arquivo `.claude/settings.json` deste repo configura um hook de *Stop* (`.claude/hooks/auto-sync.sh`) que faz **commit e push automáticos** ao final de cada sessão do Claude Code aberta dentro da pasta. Isso é uma conveniência minha de sincronização entre máquinas. Se você clonou para explorar, remova o hook ou copie apenas as pastas de skill que interessam.

## Requisitos

O Claude Code é o único requisito comum. Algumas skills usam ferramentas adicionais, sempre documentadas no `README.md` da própria skill:

- **Python 3** — `analise-rif`, `relatorio-final-ip`, `simulado-quiz`, `vocabulario-kindle`, `revisao-espacada`, `representacao-cautelar` (scripts auxiliares) e `notebooklm` (ver `notebooklm/requirements.txt`)
- **ffmpeg** — `reels-delegado`
- **PowerShell** — `reels-delegado`, `sync-skills` (fluxos pensados para Windows)
- **Conector Windsor.ai (MCP)** — `instagram-autoridade`
- **Docling + EasyOCR** — extrator de documentos da `sync-skills`

## Uso

Instaladas, as skills são acionadas pelo contexto da conversa ou por comando. Exemplos: "despacha esse flagrante", "redija o relatório final do IP", "analisa esses CSVs do COAF", "monta um mapa mental do art. 121-A do CP". Cada pasta contém um `SKILL.md` com as instruções completas e um `README.md` com guia de uso e exemplos de prompt.

## Avisos

1. Projeto pessoal. Não é produto oficial da Polícia Judiciária Civil de Mato Grosso nem de qualquer instituição.
2. Os templates carregam convenções da minha unidade (cabeçalhos, fraseologia). Adapte antes de usar em outra delegacia ou escritório.
3. Todo documento gerado é minuta e exige revisão da autoridade ou do profissional responsável antes de qualquer uso oficial.
4. Dados de casos reais estão sujeitos a sigilo funcional e à LGPD (Lei 13.709/2018). Este repositório não contém dados de casos. Fora de ambiente institucional controlado, use apenas dados anonimizados. Veja também [SECURITY.md](SECURITY.md).

## Contribuindo

Contribuições são bem-vindas — correções, adaptações para outras unidades e comarcas, novas skills jurídicas. Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para o passo a passo e o [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) para as regras de convivência. Para dúvidas e ideias, abra uma [issue](../../issues) ou uma [discussion](../../discussions).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE). As skills de terceiros mantêm as licenças originais nas respectivas pastas.
