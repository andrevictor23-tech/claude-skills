# simulado-quiz

> Transforma PDFs de simulado de concurso (MPSP/VadeFocus) em quiz HTML interativo ou caderno de revisão de erros, com cache das questões extraídas para nunca reprocessar o mesmo PDF.

**English summary:** Converts Brazilian public-exam mock test PDFs (question booklet + answer key) into an interactive HTML quiz or an error-review notebook, caching extracted questions so the same PDF is never reprocessed.

## O que faz

A partir do par de PDFs de um simulado — `Enunciado.pdf` e `Espelho.pdf` (o
espelho contém gabarito e comentários por questão) — a skill:

1. **Extrai** as questões para JSON com `scripts/extract_simulado.py`, usando
   `pdftotext` (nunca lê o PDF como imagem, o que já estourou sessões no
   passado).
2. **Valida** a extração (contagem de questões, amostragem, gabaritos nulos),
   corrigindo manualmente o JSON quando o parser best-effort falhar em algum
   item.
3. **Gera** o quiz HTML autocontido com `scripts/generate_quiz.py`, a partir de
   um ou mais JSONs, com filtro opcional por matéria (`--materia`).

O ponto central é o **cache de extração**: os JSONs ficam em
`quiz-data/simulado-NN.json` no Google Drive do usuário. Se o cache existir, a
skill o usa direto e nunca reprocessa o PDF — e, por estar no Drive, o cache
sincroniza entre as máquinas do usuário.

## Quando usar

- "Monta um quiz do simulado 03"
- "Simulado interativo", "artefato para responder questões"
- "Caderno de revisão", "questões que eu errei"
- "Extrai as questões desse PDF de simulado"
- Qualquer menção a simulados do MPSP, VadeFocus, enunciado/espelho
- "Faça igual aquele quiz", "monta as questões de [matéria] dos simulados"

## Como usar

1. "Monta o quiz do Simulado 02 do MPSP" (com os PDFs de enunciado e espelho na
   pasta do Drive)
2. "Junta os simulados 1 a 3 num quiz só de Tutela Coletiva"
3. "Gera o caderno de revisão com as questões que errei" (usando o JSON
   exportado pelo botão "Exportar erros" do próprio quiz)
4. "Extrai as questões do Simulado 05 para o cache"

## O que a skill entrega

- **Quiz HTML** (`--modo quiz`, padrão): arquivo único e autocontido, salvo em
  `quiz-data/`, em português, tema escuro, funciona offline em qualquer
  máquina. Responde questão a questão com feedback e salva o progresso em
  localStorage por id do simulado. Tem botão "Exportar erros" (JSON).
- **Caderno de revisão** (`--modo revisao`): HTML de estudo com tudo revelado,
  em 3 camadas por questão — enunciado + alternativas, ★ ponto-chave e análise
  alternativa por alternativa (a partir do comentário do espelho). Nunca
  entrega só "gabarito: X".
- **Cache JSON** (`quiz-data/simulado-NN.json`): questões estruturadas,
  reutilizáveis em quizzes futuros sem reprocessar o PDF.

## Estrutura da pasta

```
simulado-quiz/
├── SKILL.md                       # instruções da skill (regras, passo a passo)
├── assets/
│   └── template.html              # template do quiz/caderno HTML autocontido
└── scripts/
    ├── extract_simulado.py        # PDF (enunciado + espelho) → JSON, via pdftotext
    └── generate_quiz.py           # JSON(s) → quiz ou caderno HTML (usa template.html)
```

## Requisitos

- Python 3 (somente biblioteca padrão).
- `pdftotext` (Poppler) instalado — usado pelo extrator.
- PDFs do simulado: `Simulado NN - MPSP (VadeFocus) - Enunciado.pdf` e o
  respectivo `- Espelho.pdf`, na pasta do Drive do usuário
  (`G:\Meu Drive\VS CODE TESTE\`).

## Avisos

- O parser de extração é **best-effort**: a validação pós-extração é
  obrigatória (total de questões ~81 no padrão MPSP, amostragem de 2-3
  questões, correção de gabaritos `null` no JSON).
- Nunca leia o PDF do simulado como imagem no contexto; sempre `pdftotext`.
  Para PDF escaneado (texto vazio/truncado), a skill recorre ao extrator
  universal referenciado em `sync-skills/references/extracao-documentos.md`.
- Confira as questões e gabaritos gerados com o espelho original antes de
  confiar neles para o estudo.
