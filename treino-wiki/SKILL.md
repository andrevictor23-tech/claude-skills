---
name: treino-wiki
description: Treino intensivo de revisão relâmpago com perguntas geradas a partir das notas da wiki de estudos (não de PDFs de simulado). Perguntas rápidas e objetivas no chat, uma por vez, com correção imediata, placar e registro de erros na wiki; opcionalmente gera quiz HTML no padrão do simulado-quiz. Use SEMPRE que o usuário pedir "treino intensivo", "revisão relâmpago", "perguntas rápidas", "me testa em [disciplina]", "flashcards de [tema]", "quiz da wiki", "gera questões novas", "treino de véspera", ou pedir questões inéditas sobre o conteúdo já estudado. Não use quando ele quiser questões extraídas de PDF de simulado (use simulado-quiz) nem arguição aprofundada de banca (use prova-oral).
---

# Treino Wiki — Revisão Relâmpago

Gera perguntas objetivas inéditas a partir das notas de `wiki/disciplinas/*.md` da pasta de estudos (a pasta que contém `wiki/`). Nunca abra PDFs — a fonte é a wiki (e `converted_markdown/` apenas se a nota citar um trecho que precise de conferência).

## Configuração (uma pergunta só)

Pergunte em uma única mensagem: disciplina(s) ou "mix geral", quantidade (padrão: 10) e modo — **chat** (padrão, pergunta a pergunta aqui) ou **HTML** (gera quiz interativo).

## Geração das perguntas — o que importa

1. Leia a(s) nota(s) da disciplina em `wiki/disciplinas/` e a seção da disciplina em `wiki/revisao/erros.md`.
2. Formato **certo/errado** por padrão (respostas em segundos), difícil, estilo VadeFocus: afirmações plausíveis com um defeito preciso.
3. **Mire nos padrões de erro documentados** em `erros.md` ("Padrões recorrentes"). Distribua: ~40% no padrão dominante do usuário (ex.: requisito acrescido — enunciados que somam um pressuposto a mais; pares simétricos com atributos trocados), ~30% jurisprudência de véspera da nota (Infos/Temas/Súmulas com citação exata), ~30% lei seca cobrada da disciplina.
4. Toda pergunta precisa ter **fundamento citável** (artigo, súmula, tema, Info) vindo da nota. Se a nota não dá o fundamento, não invente — troque a pergunta. Nunca gere questão de fato não verificável na wiki.

## Modo chat (padrão)

- **Uma pergunta por vez**, numerada, e espere a resposta (C/E) antes de seguir.
- Correção **imediata e curta**: ✅/❌ + fundamento em 1–3 linhas + macete se existir na nota.
- Placar parcial a cada 5 perguntas; placar final com taxa de acerto e diagnóstico (qual padrão de pegadinha derrubou o usuário).
- **Erros viram registro**: ao final, grave cada erro em `wiki/revisao/erros.md` na seção da disciplina, formato do arquivo, fonte `Treino Wiki DD/MM`. Se um padrão novo se repetir, acrescente-o em "Padrões recorrentes".

## Modo HTML

1. Monte o banco em `quiz-data/treino-wiki-<tema>.json` no **mesmo esquema dos bancos C/E existentes** (confira `quiz-data/revisao-final-ce.json` como referência de esquema): `{simulado, id, questoes: [{numero, materia, tema, enunciado, alternativas: {"C": "Certo", "E": "Errado"}, gabarito, ponto_chave}]}`. O `ponto_chave` é obrigatório e explica o defeito da afirmação com o fundamento citável.
2. Gere o HTML com o gerador do simulado-quiz:
   ```powershell
   python "$env:USERPROFILE\.claude\skills\simulado-quiz\scripts\generate_quiz.py" `
     --data "<pasta de estudos>\quiz-data\treino-wiki-<tema>.json" `
     --out  "<pasta de estudos>\quiz-data\Quiz - Treino Wiki - <tema>.html" `
     --title "Treino Wiki - <tema>"
   ```
3. Vale a regra do simulado-quiz: HTML autocontido, salvo em `quiz-data/` (sincroniza entre as máquinas). Erros exportados pelo quiz seguem o fluxo normal de registro em `erros.md`.

## Estilo

Ritmo rápido, sem preâmbulos entre perguntas. Interface em português. O objetivo é volume com precisão cirúrgica no fundamento — 10 perguntas em 10 minutos, não uma aula.
