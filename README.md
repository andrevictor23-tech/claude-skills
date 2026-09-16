# claude-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Skills](https://img.shields.io/badge/skills-24-8A2BE2.svg)](#skills)
[![Sigilo](https://img.shields.io/badge/sigilo-scan%20autom%C3%A1tico-critical.svg)](#sigilo-como-este-repositório-não-vaza-dado-de-caso)
[![Idioma](https://img.shields.io/badge/idioma-pt--BR-009c3b.svg)](#o-que-é)
[![Claude Code](https://img.shields.io/badge/feito%20para-Claude%20Code-d97757.svg)](https://code.claude.com/docs/en/skills)

Skills de Claude Code para produção de documentos de Polícia Judiciária, análise de inteligência financeira e estudo jurídico, escritas em português brasileiro.

**English summary.** I am a Civil Police Chief (Delegado de Polícia Civil) in Alta Floresta, Mato Grosso, Brazil. This repository contains the Claude Code skills I use in daily casework: on-duty arrest dispatches, final reports in criminal investigations, precautionary measure requests, analysis of COAF financial intelligence reports, and study tooling for Brazilian legal exams. Because the work is covered by investigative secrecy, the repository ships an automated leak barrier that blocks any commit containing case-data patterns — see [Sigilo](#sigilo-como-este-repositório-não-vaza-dado-de-caso) and [SECURITY.md](SECURITY.md). It is a personal project and reflects my unit's local conventions. Adaptations and contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The documentation below is in Portuguese, the language of the community it serves.

---

## O que é

Biblioteca de skills para o [Claude Code](https://code.claude.com/docs/en/skills) voltada à produção de documentos de Polícia Judiciária e ao estudo jurídico. Nasceu do meu uso diário como Delegado de Polícia Civil. Publico como está, na expectativa de que sirva a colegas e a outros operadores do Direito.

Cada skill é uma pasta com um `SKILL.md` (instruções que o Claude carrega sob demanda) e, quando necessário, `references/`, `scripts/`, `templates/` e `assets/` de apoio. Várias skills têm um `README.md` próprio com guia de uso detalhado — clique no nome da skill nas tabelas abaixo.

Todas seguem a [especificação oficial Agent Skills](https://github.com/anthropics/skills) da Anthropic: frontmatter com gatilhos de ativação concretos, corpo enxuto e material de referência carregado sob demanda.

## Sigilo: como este repositório não vaza dado de caso

Publicar fluxos de trabalho de Polícia Judiciária tem um risco óbvio: o dado de inquérito viajar junto. A separação aqui não depende da disciplina do autor — é mecânica, e está descrita por inteiro no [SECURITY.md](SECURITY.md):

- **Barreira automática antes de cada commit.** O hook [`.claude/hooks/scan-sigilo.sh`](.claude/hooks/scan-sigilo.sh) escaneia os arquivos alterados em busca de CPF, CNPJ, número de processo no padrão CNJ, número de IP e de ocorrência da PJC/MT e telefone celular. Qualquer ocorrência fora da allowlist **bloqueia o commit inteiro**.
- **Allowlist explícita para o que é fictício.** Arquivos com exemplos inventados e revisados por humano entram em `.claude/sigilo-allowlist.txt`. Nada é liberado por inferência.
- **Acervo real em repositório privado.** Os modelos de peça que serviram de base ficam fora daqui, bloqueados pelo [`.gitignore`](.gitignore); neste repo sobem apenas os arquivos `LEIA-ME` que explicam a separação.
- **Fixtures sintéticas.** Os casos de teste das skills — por exemplo, os CSVs de RIF em `analise-rif/evals/fixtures/` — usam pessoas, empresas e CPFs inventados.

A detecção é por padrão de texto e não é infalível: nome próprio, por exemplo, não é detectável. A barreira complementa, não substitui, a regra de nunca usar a árvore de trabalho como rascunho de caso real. Se você encontrar algo que pareça dado real, inclusive no histórico do git, **não abra issue pública** — escreva para andrevictor23@gmail.com.

## Skills

### Polícia Judiciária

| Skill | O que faz |
|---|---|
| [despacho-plantao](despacho-plantao/) | Despachos de plantão a partir do fato narrado: decide entre APF, TCO, BOC, instauração de IP ou não instauração, com fundamento no CPP, CP e leis extravagantes |
| [relatorio-final-ip](relatorio-final-ip/) | Relatórios finais de inquérito policial, com templates por unidade (NEAMV × Delegacia) e checklist por tipo penal, incluindo violência doméstica sob a Lei 14.994/2024 |
| [representacao-cautelar](representacao-cautelar/) | Representações da Autoridade Policial ao Juízo: preventiva, temporária, busca e apreensão, quebras de sigilo, interceptação e medidas assecuratórias |
| [analise-rif](analise-rif/) | Análise de Relatórios de Inteligência Financeira do COAF (CSVs de envolvidos, comunicações e ocorrências), com Relatório de Análise Financeira em .docx segundo as tipologias da Carta Circular BACEN 4.001/2020 |
| [revisao-contradicoes](revisao-contradicoes/) | Submete a peça pronta a um revisor independente que só aponta defeitos: contradição interna, afirmação sem lastro nos autos, fundamentação genérica, placeholder esquecido e conclusão que não decorre das provas |

### Estudo jurídico e concursos

| Skill | O que faz |
|---|---|
| [mapa-mental](mapa-mental/) | Mapas mentais interativos em HTML/SVG (metodologia Buzan) para revisão de conteúdo jurídico |
| [simulado-quiz](simulado-quiz/) | Converte PDFs de simulado em quiz HTML interativo ou caderno de erros, com cache de extração |
| [treino-wiki](treino-wiki/) | Revisão relâmpago com perguntas inéditas geradas a partir das notas da wiki de estudos, com correção imediata e registro dos erros |
| [prova-oral](prova-oral/) | Simulador de banca examinadora: arguição oral com sorteio de ponto, follow-ups de pressão, espelho de resposta e nota por questão |
| [registrar-erro](registrar-erro/) | Transforma questão errada colada crua (QConcursos, Decorando a Lei Seca, quiz local) em entrada do caderno de erros, inferindo disciplina, motivo e fundamento |
| [anki](anki/) | Converte os erros dos quizzes e da wiki de revisão em baralho Anki incremental, com um subbaralho por disciplina |
| [desempenho](desempenho/) | Dashboard HTML dos estudos: taxa de erro por disciplina, motivos de erro e prioridade de revisão ponderada pelo peso da prova |
| [guia-cartorio](guia-cartorio/) | Guia semanal de estudos com as novidades notariais e registrais dos últimos sete dias |
| [vocabulario-kindle](vocabulario-kindle/) | Converte o `vocab.db` do Kindle Vocabulary Builder em baralho Anki com frases reais dos livros |

### Trabalho com agentes

| Skill | O que faz |
|---|---|
| [sabatina](sabatina/) | Entrevista socrática pergunta a pergunta até haver entendimento compartilhado, antes de produzir peça ou implementar funcionalidade |
| [escrita-para-agentes](escrita-para-agentes/) | Referência de escrita de documentos consumidos por agente (`SKILL.md`, `CLAUDE.md`, `AGENTS.md`, memória), incluindo por que uma skill dispara errado ou deixa de disparar |
| [handoff](handoff/) | Comprime a sessão num documento de passagem para outra sessão ou agente continuar de onde parou |
| [conciso](conciso/) | Modo de resposta direto e enxuto para o restante da sessão |
| [sync-skills](sync-skills/) | Sincroniza as skills entre máquinas via git; inclui extrator universal de documentos (Docling + EasyOCR) |

### Mídia e uso pessoal

| Skill | O que faz |
|---|---|
| [generate](generate/) | Gera imagens e vídeos com modelos do Google via Vertex AI (Nano Banana e Veo) |
| [edita-video](edita-video/) | Trata vídeo falado (Reels, stories, institucional): remove muletas verbais e silêncios e melhora o áudio |
| [digesto](digesto/) | Transforma links acumulados em EPUB de curadoria para o Kindle, com veredito de utilidade por fonte |
| [analise-carteira](analise-carteira/) | Análise de carteira de investimentos na filosofia Bastter/Canal do Holder/Fundamentei (não é recomendação de investimento) |
| [sts2](sts2/) | Coach de Slay the Spire 2 em tempo real, lendo o save da run ativa |

## Instalação

Para skills pessoais, disponíveis em todos os projetos:

```bash
git clone https://github.com/andrevictor23-tech/claude-skills.git
cp -r claude-skills/nome-da-skill ~/.claude/skills/
```

Para uso restrito a um projeto, copie a pasta para `.claude/skills/` na raiz do projeto. Documentação oficial: https://code.claude.com/docs/en/skills

> **Atenção ao clonar o repositório inteiro:** o arquivo `.claude/settings.json` deste repo configura um hook de *Stop* (`.claude/hooks/auto-sync.sh`) que faz **commit e push automáticos** ao final de cada sessão do Claude Code aberta dentro da pasta. Isso é uma conveniência minha de sincronização entre máquinas. Se você clonou para explorar, remova o hook ou copie apenas as pastas de skill que interessam.

## Requisitos

O Claude Code é o único requisito comum. Algumas skills usam ferramentas adicionais, sempre documentadas na própria skill:

- **Python 3** — `analise-rif`, `relatorio-final-ip`, `simulado-quiz`, `anki`, `vocabulario-kindle` e `representacao-cautelar` (scripts auxiliares)
- **PowerShell** — `sync-skills`, `generate` e `sts2` (fluxo pensado para Windows)
- **Docling + EasyOCR** — extrator de documentos da `sync-skills`

## Uso

Instaladas, as skills são acionadas pelo contexto da conversa ou por comando. Exemplos: "despacha esse flagrante", "redija o relatório final do IP", "analisa esses CSVs do COAF", "monta um mapa mental do art. 121-A do CP". Cada pasta contém um `SKILL.md` com as instruções completas.

## Avisos

1. Projeto pessoal. Não é produto oficial da Polícia Judiciária Civil de Mato Grosso nem de qualquer instituição.
2. Os templates carregam convenções da minha unidade (cabeçalhos, fraseologia). Adapte antes de usar em outra delegacia ou escritório.
3. Todo documento gerado é minuta e exige revisão da autoridade ou do profissional responsável antes de qualquer uso oficial.
4. Dados de casos reais estão sujeitos a sigilo funcional e à LGPD (Lei 13.709/2018). Este repositório não contém dados de casos — veja [Sigilo](#sigilo-como-este-repositório-não-vaza-dado-de-caso). Fora de ambiente institucional controlado, use apenas dados anonimizados.

## Skills de terceiros que uso

Estas não são minhas e não são redistribuídas aqui — cada uma tem autoria e licença próprias. Instale direto na origem:

| Skill | Autoria | O que faz |
|---|---|---|
| [skill-creator](https://github.com/anthropics/skills) | Anthropic (Apache-2.0) | Criação, edição e avaliação (evals) de skills |
| [find-skills](https://github.com/vercel-labs/skills) | Vercel Labs | Descoberta e instalação de skills a partir de perguntas "how do I do X" |
| [calibrate](https://github.com/robonuggets/calibrate) | RoboNuggets | Revisa a conversa em busca de correções e sugere ajustes em skills e `CLAUDE.md` |
| [doctor-plus](https://github.com/robonuggets/doctor-plus) | RoboNuggets | Health check estendido do Claude Code, com auditoria de context engineering |
| [prompt-master](https://github.com/nidhinjs/prompt-master) | nidhinjs | Geração de prompts otimizados para ferramentas de IA |
| [notebooklm](https://github.com/PleasePrompto/notebooklm-skill) | Please Prompto! | Consulta notebooks do Google NotebookLM com respostas ancoradas nas fontes |

## Contribuindo

Contribuições são bem-vindas — correções, adaptações para outras unidades e comarcas, novas skills jurídicas. Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para o passo a passo e o [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) para as regras de convivência. Para dúvidas e ideias, abra uma [issue](../../issues) ou uma [discussion](../../discussions).

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
