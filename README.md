# claude-skills

Claude Code skills for Brazilian judicial police document production and legal study, written in Brazilian Portuguese.

**English summary.** I am a Civil Police Chief (Delegado de Polícia Civil) in Alta Floresta, Mato Grosso, Brazil. This repository contains skills I use in daily casework: on-duty arrest dispatches, final reports in criminal investigations, analysis of COAF financial intelligence reports, and study tooling for Brazilian legal exams. It is a new, personal project and reflects my unit's local conventions. Adaptations and contributions are welcome. The documentation below is in Portuguese, the language of the community it serves.

---

## O que é

Biblioteca de skills para o Claude Code voltada à produção de documentos de Polícia Judiciária e ao estudo jurídico. Nasceu do meu uso diário como Delegado de Polícia Civil. Publico como está, na expectativa de que sirva a colegas e a outros operadores do Direito.

## Skills

| Skill | O que faz |
|---|---|
| despacho-plantao | Despachos de plantão a partir do fato narrado: decide entre APF, TCO, BOC, instauração de IP ou não instauração, com fundamento no CPP, CP e leis extravagantes |
| relatorio-final-ip | Relatórios finais de inquérito policial, com templates por unidade e checklist por tipo penal, incluindo violência doméstica sob a Lei 14.994/2024 |
| analise-rif | Análise de Relatórios de Inteligência Financeira do COAF (CSVs de envolvidos, comunicações e ocorrências), com Relatório de Análise Financeira em .docx segundo as tipologias da Carta Circular BACEN 4.001/2020 |
| mapa-mental | Mapas mentais interativos em HTML/SVG para revisão de conteúdo jurídico |
| simulado-quiz | Simulados interativos em HTML gerados a partir de materiais de curso, para preparação de concursos |

## Instalação

Para skills pessoais, disponíveis em todos os projetos:

```bash
git clone https://github.com/andrevictor23-tech/claude-skills.git
cp -r claude-skills/nome-da-skill ~/.claude/skills/
```

Para uso restrito a um projeto, copie a pasta para `.claude/skills/` na raiz do projeto. Documentação oficial: https://code.claude.com/docs/en/skills

## Uso

Instaladas, as skills são acionadas pelo contexto da conversa ou por comando. Exemplos: "despacha esse flagrante", "redija o relatório final do IP", "analisa esses CSVs do COAF", "monta um mapa mental do art. 121-A do CP". Cada pasta contém um SKILL.md com as instruções completas.

## Avisos

1. Projeto pessoal. Não é produto oficial da Polícia Judiciária Civil de Mato Grosso nem de qualquer instituição.
2. Os templates carregam convenções da minha unidade (cabeçalhos, fraseologia). Adapte antes de usar em outra delegacia ou escritório.
3. Todo documento gerado é minuta e exige revisão da autoridade ou do profissional responsável antes de qualquer uso oficial.
4. Dados de casos reais estão sujeitos a sigilo funcional e à LGPD (Lei 13.709/2018). Este repositório não contém dados de casos. Fora de ambiente institucional controlado, use apenas dados anonimizados.

## Skills de terceiros

As pastas `ecc/` (Everything Claude Code, de Affaan Mustafa, MIT), `notebooklm/`, `canvas-design/`, `internal-comms/`, `skill-creator/`, `doc-coauthoring/`, `find-skills/` e `prompt-master/` contêm skills de terceiros que uso no dia a dia, mantidas aqui por conveniência de sincronização, com licenças e créditos preservados nas respectivas pastas. As skills autorais deste repositório são as listadas na tabela acima.

## Licença

MIT. Veja o arquivo LICENSE.
