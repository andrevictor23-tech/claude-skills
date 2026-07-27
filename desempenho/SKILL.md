---
name: desempenho
description: Dashboard de desempenho nos estudos para concurso (MPSP/MP-MT) — cruza os erros registrados na wiki (wiki/revisao/erros.md) com os erros exportados dos quizzes (quiz-data/*-erros.json) e gera um painel HTML autocontido com taxa de erro por disciplina, motivos de erro, prioridade de revisão ponderada pelo peso da prova e lista detalhada de fundamentos. Use SEMPRE que o usuário pedir "dashboard", "como estou indo", "análise de desempenho", "estatísticas dos simulados", "taxa de acerto", "onde estou errando mais", "prioridade de revisão", "painel de estudos", ou quiser visão consolidada dos erros. Não use para responder questões (simulado-quiz/treino-wiki) nem para registrar um erro novo (edite erros.md direto).
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
