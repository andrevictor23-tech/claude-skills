---
name: desempenho
description: Painel HTML de desempenho nos estudos para concurso, cruzando o caderno de erros da wiki com os exports dos quizzes, com taxa de erro por disciplina, motivos e prioridade de revisão ponderada pelo peso da prova. Use quando o usuário pedir dashboard, estatísticas dos simulados, "como estou indo" ou "onde estou errando mais". Registrar erro novo é da skill registrar-erro.
---

# Desempenho — Dashboard de Estudos

Gera um painel HTML autocontido (tema escuro, offline) a partir dos dados que o usuário já produz: `wiki/revisao/erros.md` + bancos e exports de erros em `quiz-data/`.

## Passo a passo

### 1. Gerar o dashboard

```powershell
python "$env:USERPROFILE\.claude\skills\desempenho\scripts\build_dashboard.py" `
  --base "<pasta de estudos>"   # a pasta que contém wiki\ e quiz-data\
```

Saída padrão: `<pasta de estudos>\quiz-data\Dashboard - Desempenho MPSP.html` (fica no Drive, sincroniza entre as máquinas). Use `--out` para outro caminho.

### 2. Conferir o relatório do script

O script imprime um resumo: bancos lidos, exports vinculados, erros sem vínculo (export cita um `sim`/questão que não está em nenhum banco). Erros sem vínculo não somem — entram no painel como "não vinculado" — mas se forem muitos, avise o usuário que há banco faltando em `quiz-data/`.

### 3. Interpretar para o usuário (sempre)

Depois de gerar, entregue no chat um diagnóstico curto (3–5 frases): disciplina mais crítica pela **prioridade ponderada** (erros × peso da prova), motivo de erro dominante, e a ação concreta sugerida (qual nota da wiki revisar, ou treino-wiki na disciplina crítica). O HTML mostra números; o valor da skill é a leitura.

## Limitações honestas (não esconda do usuário)

- A taxa de erro considera **respondidos** os bancos citados em algum export de erros — quiz feito sem exportar erros não conta.
- Erros anotados só no `erros.md` (sem export) contam para prioridade e motivos, mas não para a taxa por banco.

## Manutenção

Os pesos por disciplina (prova objetiva MPSP 97º, 100 questões) estão em constante no `build_dashboard.py` — se o alvo mudar (MP-MT, outro edital), atualize a constante `PESOS` lá, não invente pesos no chat.
