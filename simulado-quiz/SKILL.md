---
name: simulado-quiz
description: Transforma PDFs de simulado de concurso (MPSP/VadeFocus e similares) em quiz HTML interativo ou caderno de revisão de erros, com cache das questões extraídas para nunca reprocessar o mesmo PDF. Use SEMPRE que o usuário pedir quiz, simulado interativo, artefato para responder questões, caderno de revisão, "questões que eu errei", revisão de simulado, extrair questões de PDF de simulado, ou mencionar simulados do MPSP, VadeFocus, enunciado/espelho. Ative também para "faça igual aquele quiz", "monta as questões de [matéria] dos simulados", ou qualquer pedido de estudar questões a partir de PDFs.
---

# Simulado → Quiz HTML com cache

Fluxo do usuário (estudo MP-SP): PDFs `Simulado NN - MPSP (VadeFocus) - Enunciado.pdf` + `... - Espelho.pdf` na **pasta de estudos** — a pasta que contém `wiki\` e `quiz-data\`. O Drive monta em caminho diferente por máquina (`G:\Meu Drive\VS CODE TESTE\` ou `C:\Users\<user>\Meu Drive\VS CODE TESTE\`): descubra o caminho real antes de montar comandos; nos exemplos abaixo ele aparece como `<pasta de estudos>`. O espelho tem gabarito e comentários por questão.

## REGRAS INEGOCIÁVEIS

1. **NUNCA leia PDF de simulado como imagem/página no contexto** (Read em PDF grande já estourou uma sessão de 100 MB). Sempre `pdftotext` primeiro. Se o `pdftotext` vier vazio ou truncado (PDF escaneado), use o extrator universal — ver `sync-skills/references/extracao-documentos.md`.
2. **Cache primeiro**: antes de extrair, verifique `<pasta de estudos>\quiz-data\simulado-NN.json`. Se existir, use-o direto — não reprocesse o PDF. O cache fica no Drive de propósito: sincroniza entre as 3 máquinas do usuário.
3. O HTML gerado é **autocontido** (um arquivo, sem dependências externas) e salvo em `<pasta de estudos>\quiz-data\` — abre em qualquer máquina.

## Passo a passo

### 1. Extrair (só se não houver cache)
```powershell
python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\extract_simulado.py" `
  --enunciado "<pasta de estudos>\Simulado NN - MPSP (VadeFocus) - Enunciado.pdf" `
  --espelho   "<pasta de estudos>\Simulado NN - MPSP (VadeFocus) - Espelho.pdf" `
  --out       "<pasta de estudos>\quiz-data\simulado-NN.json"
```

### 2. VALIDAR a extração (obrigatório)
O parser é best-effort. Após extrair:
- Confira o total de questões no relatório do script (simulado MPSP tem ~81).
- Abra 2-3 questões aleatórias do JSON e compare com o texto do `pdftotext`.
- Questões com `"gabarito": null` ou alternativas faltando: corrija manualmente no JSON (consultando o texto extraído, nunca a imagem do PDF).

### 3. Gerar o quiz
```powershell
python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\generate_quiz.py" `
  --data "<pasta de estudos>\quiz-data\simulado-01.json" [mais arquivos .json...] `
  --out  "<pasta de estudos>\quiz-data\Quiz - <título>.html" `
  --title "Simulados 1-3 MPSP - Tutela Coletiva"
```
Aceita múltiplos JSONs (para juntar vários simulados) e filtro opcional `--materia "Tutela Coletiva"` (filtra pelo campo `materia` das questões).

### 4. Export de resultado (botão "Exportar resultado")
O quiz exporta `<id>-resultado.json`: `{quiz, data, bancos, total, respondidas, acertos, por_materia: {materia: {respondidas, acertos}}, erros: [{sim, numero, marcada, gabarito}]}`. Exports antigos `-erros.json` (só a lista de erros) continuam válidos em todos os fluxos abaixo. Esses exports alimentam o dashboard da skill `desempenho` — incentive o usuário a exportar ao fim de cada quiz.

### 5. Caderno de revisão de erros
Se o usuário pedir "caderno de revisão" / "questões que errei": use a lista `erros` do export para montar um banco filtrado e gere o caderno com `generate_quiz.py --modo revisao`, que produz HTML de estudo com 3 camadas por questão: enunciado + alternativas, ★ ponto-chave, análise alternativa por alternativa (do comentário do espelho). Esse formato de 3 camadas foi validado pelo usuário — não entregue só "gabarito: X".

### 6. Registrar erros na wiki (fecha o ciclo)
Depois de um quiz com erros, gere o rascunho das entradas para `wiki/revisao/erros.md`:
```powershell
python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\importar_erros.py" `
  --export    "<pasta de estudos>\quiz-data\<id>-resultado.json" `
  --quiz-data "<pasta de estudos>\quiz-data"
```
O rascunho sai com `Motivo: [VERIFICAR]` de propósito — **pergunte ao usuário o motivo de cada erro** (pegadinha / desconhecimento / distração), refine o fundamento com base no espelho e só então insira as entradas na seção certa do `erros.md`. Nunca registre motivo por inferência.

## Estilo
Interface em português, tema escuro, funciona offline. O usuário estuda ~3-4h/dia; o quiz salva progresso em localStorage por id do simulado.
