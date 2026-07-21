---
name: revisao-espacada
description: Sistema de revisão espaçada e caderno de erros para estudo de concursos públicos (MPMT, MPSP, Cartório TJMT e outros). Use SEMPRE que o usuário registrar um erro de questão ou simulado, disser "errei essa questão", "anota no caderno de erros", "registra esse erro", "o que tenho para revisar hoje", "minha revisão de hoje", "revisão espaçada", "o que cai mais", "quais matérias erro mais", ou quiser estudar/revisar pontos que já errou. Também use quando o usuário colar uma questão com gabarito comentado para arquivar, pedir questões novas sobre temas que vem errando, ou quiser ver estatística de erros por matéria. Mantém um caderno de erros em Markdown, agenda revisões em intervalos fixos (1, 3, 7, 15, 30 dias), entrega a explicação do ponto errado e gera questões novas sobre os temas fracos.
---

# Skill: Revisão Espaçada e Caderno de Erros

Transforma os erros do usuário em um sistema de estudo guiado por dado. Cada questão errada vira um item rastreável; a skill agenda quando revisar (intervalos fixos crescentes) e, na revisão, entrega a explicação do ponto e questões novas sobre o tema.

## Filosofia

O usuário (André, Delegado de Polícia Civil/MT, preparando-se para MPMT, MPSP e Cartório TJMT) estuda por dado, não por sensação. O erro não é falha: é o sinal mais valioso sobre onde investir tempo. A skill garante que nada que ele errou seja esquecido e que cada ponto fraco seja reforçado no momento certo, antes do esquecimento.

## Arquitetura

- **Caderno de erros**: arquivo Markdown (padrão `caderno-erros.md`) que serve de banco de dados. Cada erro é um bloco delimitado por `<!-- ERRO id=NNNN -->` ... `<!-- /ERRO -->`.
- **Motor de datas**: `scripts/revisao.py` cuida de toda a matemática de intervalos e da leitura/escrita do arquivo. NUNCA edite as datas ou níveis manualmente — sempre use o script, para não corromper o agendamento.

### Intervalos de revisão (fixos)

Cada item tem um **nível** de 1 a 5, que define quando revisar:

| Nível | Próxima revisão em |
|---|---|
| 1 | +1 dia |
| 2 | +3 dias |
| 3 | +7 dias |
| 4 | +15 dias |
| 5 | +30 dias |

Acertar na revisão sobe um nível (espaça mais). Errar reseta para o nível 1 (revisa amanhã de novo). Após acertar no nível 5, o item é marcado como **dominado** e sai da fila de revisões ativas.

## Comandos do script

Sempre rode a partir do diretório onde está a skill, apontando para o caderno do usuário. Localize o caderno-erros.md do projeto do usuário; se ele não indicar o caminho, pergunte ou use `caderno-erros.md` na pasta atual.

```bash
# Registrar um novo erro
python3 scripts/revisao.py add CAMINHO --materia "M" --assunto "A" --questao "Q" --errei "E" --correta "C"

# Ver o que vence hoje (ou esta atrasado)
python3 scripts/revisao.py due CAMINHO

# Listar todos os itens ativos
python3 scripts/revisao.py list CAMINHO

# Marcar resultado de uma revisao
python3 scripts/revisao.py revisar CAMINHO --id NNNN --resultado acertou
python3 scripts/revisao.py revisar CAMINHO --id NNNN --resultado errou

# Estatistica de erros por materia
python3 scripts/revisao.py stats CAMINHO
```

O script sempre devolve JSON. Use o JSON para conversar com o usuário em linguagem natural — nunca despeje o JSON cru na resposta.

---

## Fluxo 1 — Registrar erro(s)

Gatilho: o usuário cola uma ou mais questões erradas, ou diz "errei isso", "anota aí".

1. Para cada questão, extraia: **matéria**, **assunto** (tema específico), **questão** (enunciado resumido ou referência da prova), **errei porque** (a pegadinha ou o raciocínio equivocado) e **resposta correta** (gabarito + fundamento legal/doutrinário).
2. Se o usuário não explicou *por que* errou, infira a partir da questão e do gabarito, mas confirme com ele em uma linha. O campo "errei porque" é o coração do sistema: é o que será reforçado.
3. Rode `add` para cada erro.
4. Confirme de forma enxuta: quantos foram registrados, com que ID, e quando vencem para a primeira revisão.

Ao registrar, mantenha a precisão jurídica: cite artigo, súmula ou tese sempre que possível no campo "resposta correta". Se estiver incerto sobre um fundamento legal, diga isso explicitamente em vez de inventar citação.

## Fluxo 2 — Revisão do dia (a entrega principal)

Gatilho: "o que revisar hoje", "minha revisão", "bora revisar".

1. Rode `due` para obter os itens vencidos.
2. Se não houver nada vencido, diga isso e ofereça: revisar algo adiantado, registrar novos erros, ou ver estatística. Não invente itens.
3. Para CADA item vencido, entregue as duas coisas que o usuário quer:

   **(a) Explicação do ponto errado** — um reforço curto e preciso do conceito que ele errou. Não repita só o gabarito: explique o *porquê*, ancorado no fundamento legal. Conecte com a pegadinha registrada em "errei porque". Use analogias ou casos notórios quando ajudar a fixar.

   **(b) Questões novas sobre o tema** — gere 2 a 3 questões inéditas sobre o mesmo assunto, no estilo da banca-alvo (FGV para MPMT; CEBRASPE para Cartório TJMT — certo/errado quando for CEBRASPE). Varie o ângulo: se ele errou um prazo, teste o prazo por outro caminho e teste um conceito vizinho. Apresente as questões, espere a resposta, e só então mostre o gabarito comentado.

4. Após o usuário responder às questões de um item, registre o resultado com `revisar` (`acertou` se acertou todas/a maioria; `errou` se errou o ponto central). Informe quando será a próxima revisão daquele item.

Faça um item por vez para não sobrecarregar. Ao final da sessão, dê um fechamento curto: quantos revisou, quantos subiram de nível, quantos resetaram.

## Fluxo 3 — Estatística / diagnóstico

Gatilho: "o que erro mais", "quais matérias", "como está meu caderno".

1. Rode `stats`.
2. Apresente em tabela, da matéria com mais erros para a com menos.
3. Dê uma leitura estratégica curta: onde concentrar estudo, sem alarmismo. É diagnóstico, não julgamento.

---

## Regras de estilo (preferências do usuário)

- Tom profissional, direto, sem rodeios. Português do Brasil.
- Não usar travessões (—) nas respostas sempre que possível.
- Precisão jurídica é inegociável: cite a fonte (artigo, súmula, tese). Se incerto, sinalize a lacuna explicitamente em vez de afirmar com falsa confiança.
- Concisão por padrão. As questões geradas e a explicação devem ser substanciais, mas sem encher linguiça.
- Trechos de questão/gabarito que o usuário fornecer devem ser preservados fielmente no caderno.

## Integração com o ecossistema de estudo

O caderno-erros.md é texto puro, então pode ser:
- versionado em Git (histórico de evolução do estudo);
- adicionado como fonte em um caderno do NotebookLM para gerar áudio/mapa mental dos pontos fracos;
- lido em qualquer editor ou no celular.

Quando o usuário acumular bastante conteúdo, sugira (sem insistir) gerar um material de revisão consolidado a partir do caderno.
