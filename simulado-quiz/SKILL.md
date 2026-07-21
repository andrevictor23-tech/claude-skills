---
name: simulado-quiz
description: Transforma PDFs de simulado de concurso (MPSP/VadeFocus e similares) em quiz HTML interativo ou caderno de revisão de erros, com cache das questões extraídas para nunca reprocessar o mesmo PDF. Use SEMPRE que o usuário pedir quiz, simulado interativo, artefato para responder questões, caderno de revisão, "questões que eu errei", revisão de simulado, extrair questões de PDF de simulado, ou mencionar simulados do MPSP, VadeFocus, enunciado/espelho. Ative também para "faça igual aquele quiz", "monta as questões de [matéria] dos simulados", ou qualquer pedido de estudar questões a partir de PDFs.
---

# Simulado → Quiz HTML com cache

Fluxo do usuário (estudo MP-SP): PDFs `Simulado NN - MPSP (VadeFocus) - Enunciado.pdf` + `... - Espelho.pdf` em `G:\Meu Drive\VS CODE TESTE\`. O espelho tem gabarito e comentários por questão.

## REGRAS INEGOCIÁVEIS

1. **NUNCA leia PDF de simulado como imagem/página no contexto** (Read em PDF grande já estourou uma sessão de 100 MB). Sempre `pdftotext` primeiro. Se o `pdftotext` vier vazio ou truncado (PDF escaneado), use o extrator universal — ver `sync-skills/references/extracao-documentos.md`.
2. **Cache primeiro**: antes de extrair, verifique `G:\Meu Drive\VS CODE TESTE\quiz-data\simulado-NN.json`. Se existir, use-o direto — não reprocesse o PDF. O cache fica no Drive de propósito: sincroniza entre as 3 máquinas do usuário.
3. O HTML gerado é **autocontido** (um arquivo, sem dependências externas) e salvo em `G:\Meu Drive\VS CODE TESTE\quiz-data\` — abre em qualquer máquina.

## Passo a passo

### 1. Extrair (só se não houver cache)
```powershell
python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\extract_simulado.py" `
  --enunciado "G:\Meu Drive\VS CODE TESTE\Simulado NN - MPSP (VadeFocus) - Enunciado.pdf" `
  --espelho   "G:\Meu Drive\VS CODE TESTE\Simulado NN - MPSP (VadeFocus) - Espelho.pdf" `
  --out       "G:\Meu Drive\VS CODE TESTE\quiz-data\simulado-NN.json"
```

### 2. VALIDAR a extração (obrigatório)
O parser é best-effort. Após extrair:
- Confira o total de questões no relatório do script (simulado MPSP tem ~81).
- Abra 2-3 questões aleatórias do JSON e compare com o texto do `pdftotext`.
- Questões com `"gabarito": null` ou alternativas faltando: corrija manualmente no JSON (consultando o texto extraído, nunca a imagem do PDF).

### 3. Gerar o quiz
```powershell
python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\generate_quiz.py" `
  --data "G:\Meu Drive\VS CODE TESTE\quiz-data\simulado-01.json" [mais arquivos .json...] `
  --out  "G:\Meu Drive\VS CODE TESTE\quiz-data\Quiz - <título>.html" `
  --title "Simulados 1-3 MPSP - Tutela Coletiva"
```
Aceita múltiplos JSONs (para juntar vários simulados) e filtro opcional `--materia "Tutela Coletiva"` (filtra pelo campo `materia` das questões).

### 4. Caderno de revisão de erros
Se o usuário pedir "caderno de revisão" / "questões que errei": o quiz gerado já exporta os erros (botão "Exportar erros" → JSON). Com esse JSON, gere o caderno com `generate_quiz.py --modo revisao`, que produz HTML de estudo com 3 camadas por questão: enunciado + alternativas, ★ ponto-chave, análise alternativa por alternativa (do comentário do espelho). Esse formato de 3 camadas foi validado pelo usuário — não entregue só "gabarito: X".

## Estilo
Interface em português, tema escuro, funciona offline. O usuário estuda ~3-4h/dia; o quiz salva progresso em localStorage por id do simulado.
