---
name: escrita-para-agentes
description: Referência de escrita de documentos consumidos por agente — SKILL.md (principalmente o campo description), CLAUDE.md, AGENTS.md e arquivos de memória. Use ao criar ou revisar qualquer um desses, quando uma skill dispara errado ou deixa de disparar, quando as descriptions estão inchadas ("poda as skills", "revisa as descriptions"), ou antes de acrescentar regra nova ao CLAUDE.md. Complementa a skill-creator, que cuida da mecânica (pastas, frontmatter, empacotamento, evals) — aqui é a qualidade da escrita em si.
---

# Escrita para agentes

Referência para escrever qualquer documento que um agente consome — uma skill, um `CLAUDE.md`, um arquivo alcançado por ponteiro. A embalagem varia; a escrita não: as mesmas alavancas tornam cada um previsível — o agente seguindo o mesmo **processo** em toda execução, não produzindo o mesmo texto.

## Ponteiros de contexto

Um **ponteiro de contexto** é uma referência que vive no contexto do agente, nomeia material fora do contexto e codifica a condição para alcançá-lo. O `description:` de uma skill é um; uma linha do `CLAUDE.md` apontando um documento é o mesmo objeto. A **redação** do ponteiro, não o alvo, decide quando o agente chega ao material — e com que confiabilidade. Alvo indispensável atrás de ponteiro mal redigido é bug de variância: afie a redação primeiro; só inline o material se afiar não resolver.

O ponteiro faz dois trabalhos — dizer o que o material é, e listar os **ramos** que devem disparar o acesso (ramo = caso distinto que o documento trata; execuções diferentes percorrem caminhos diferentes). Cada palavra de um ponteiro sempre-carregado custa em todo turno, então merece poda mais dura que o corpo:

- **Comece pela palavra que dispara** — o ponteiro existe para disparar.
- **Um gatilho por ramo.** Sinônimos que renomeiam o mesmo ramo são um ramo escrito duas vezes; colapse-os e mantenha só ramos genuinamente distintos.
- **Corte identidade que o corpo já carrega.**

## As duas cargas

Todo documento e todo ponteiro gastam um de dois orçamentos:

- **Carga de contexto** — o custo do material sempre-carregado na janela do agente: uma linha de `CLAUDE.md`, um description de skill, tudo que ocupa tokens e atenção em todo turno, dispare ou não.
- **Carga cognitiva** — o custo sobre o humano: saber quais documentos existem e quando invocar cada um. O humano é o índice. Não é custo a zerar — é o preço da agência humana; gaste onde o julgamento dele importa, remova onde não importa.

Material alcançado só por ponteiro escapa da carga de contexto ao preço da linha do próprio ponteiro; material sem ponteiro algum corre inteiro por conta da carga cognitiva.

## Hierarquia da informação

Um documento se constrói de dois tipos de conteúdo — **passos** (as ações ordenadas que o agente executa) e **referência** (definições, regras, fatos consultados sob demanda) — que se misturam livremente. A decisão central é onde cada peça senta na **hierarquia da informação**, uma escada ordenada por quão imediatamente o agente precisa do material:

1. **Passo no arquivo** — o degrau primário: o que o agente faz, em ordem.
2. **Referência no arquivo** — consultada sob demanda. Muitas vezes um conjunto legitimamente plano (todas as regras de uma revisão num degrau só) — arranjo válido, não defeito.
3. **Referência divulgada** — empurrada para arquivo separado, alcançada por ponteiro, carregada só quando o ponteiro dispara.

Empurre de menos e o topo incha; empurre demais e você esconde material que o agente precisa. Essa tensão é a decisão inteira.

**Divulgação progressiva** é o movimento escada abaixo — para fora do arquivo principal, atrás de um ponteiro — para o topo continuar legível. Não é primariamente economia de token: é como se protege a hierarquia. O teste mais limpo é o ramo: inline o que todo ramo precisa; divulgue atrás de ponteiro o que só alguns ramos alcançam. Quando o documento tem passos, referência que deveria estar divulgada os soterra — e prestar atenção neles vira cara-ou-coroa.

**Co-localização** é a companheira dentro do arquivo: a escada decide *quão fundo* a peça senta; a co-localização decide *o que senta ao lado* dela. Definição, regras e ressalvas de um conceito sob um mesmo título, não espalhadas — ler uma parte traz as vizinhas junto. O teste: o documento deve ler como documentação escrita para o agente. (Distinto de duplicação: aquela repete um significado em dois lugares; espalhamento fragmenta um significado em muitos.)

**Sprawl** é o modo de falha: documento simplesmente longo demais, mesmo com cada linha viva e única. A atenção rareia sobre o excesso, e cada linha extra é mais uma para manter relevante. A cura é a escada: divulgue referência atrás de ponteiros e divida por ramo ou por sequência, para cada caminho carregar só o que precisa.

## Passos e critérios de conclusão

Todo passo termina num **critério de conclusão** — a condição que diz ao agente que o trabalho acabou. Duas propriedades o tornam alavanca:

- **Clareza** — o agente distingue pronto de não-pronto? Fronteira vaga ("entendimento alcançado") convida à **conclusão prematura**: encerrar o passo antes de ele estar genuinamente pronto, com a atenção escorregando para *estar pronto*. Os passos visíveis adiante fornecem a tração; a clareza do critério é a resistência. Defenda nesta ordem: **afie a fronteira primeiro** (local e barato); só se ela for irredutivelmente difusa *e* você observar a pressa, esconda os passos seguintes dividindo a sequência — e esconder só funciona através de fronteira real de contexto (um handoff ou um subagente; chamada inline deixa os passos à vista e não esconde nada).
- **Exigência** — quanto o critério cobra. "Todo modelo modificado contabilizado" força trabalho minucioso onde "produza uma lista de mudanças" não força. Exigência gera **legwork** — a escavação que o agente faz dentro do trabalho, latente na redação em vez de escrita como passo próprio — e não se limita a passos: "toda regra aplicada" cobra de um corpo de referência plana tanto quanto "todo passo feito" cobra de uma sequência.

Os critérios mais fortes são checáveis **e** exaustivos.

## Quando dividir

Dividir um documento em dois gasta uma das duas cargas, então divida só quando o corte pagar:

- **Por sequência** — divida uma corrida de passos quando os passos posteriores tentam o agente a apressar o passo em frente. Mantê-los fora de vista aumenta o legwork na tarefa atual. Cuidado com o inverso: fundir sequências expõe cada passo ao que vem depois, convidando à conclusão prematura.
- **Por invocação** — específico de skill: a mecânica é assunto da `skill-creator`.

## Palavras-guia

Uma **palavra-guia** é um conceito compacto que já vive no pré-treino do modelo e com o qual o agente pensa enquanto executa o documento (*fronteira*, *legwork*, *tracer bullet*, *relentless*). Repetida como token, nunca como frase, acumula definição distribuída e ancora uma região inteira de comportamento no mínimo de tokens, recrutando priors que o modelo já tem. Cunhar palavra própria funciona se bem definida, mas palavra inventada não recruta prior nenhum — você paga em tokens de definição o que a palavra pré-treinada dá de graça.

Ela ancora duas vezes. No corpo, *execução*: o agente busca o mesmo comportamento toda vez que a palavra aparece. No ponteiro, *invocação*: quando a mesma palavra vive nos seus prompts, nos seus documentos e no seu vocabulário, o agente liga essa linguagem compartilhada ao material e o alcança com mais confiabilidade. (É por isso que a skill de handoff daqui se chama pelo termo que o usuário realmente usa, e a de sabatina idem.)

Cace oportunidades de refatorar com palavras-guia: uma tríade soletrada em três lugares, um ponteiro gastando uma frase para gesticular uma ideia — cada um é passagem implorando para colapsar num token só. Ganha-se duas vezes: menos tokens e gancho mais afiado.

**Negação** é o modo de falha vizinho: dirigir por proibição arrasta o comportamento proibido para o contexto e o torna **mais** disponível, não menos. *Não pense num elefante* — e o elefante é tudo que há; a negação é modificador fraco que o conceito fortemente ativado atropela, e a proibição meio que se lê como instrução de fazer a coisa. Formule o **positivo** — o comportamento-alvo ("comentários de uma linha") — para o proibido nunca ser falado. Proibição só ganha lugar como guarda-corpo duro que não há como formular positivamente; mesmo aí, emparelhe com o alvo positivo.

## Poda

- Mantenha cada significado numa **fonte única de verdade**: um lugar autoritativo, para mudar o comportamento ser edição de um lugar só. **Duplicação** — o mesmo significado em mais de um lugar — custa manutenção e tokens, e infla a proeminência do significado na escada acima do seu posto real. (O inverso acidental da palavra-guia, que repete o token de propósito, nunca o significado.)
- O **ambiente** também é fonte de verdade — scripts do `package.json`, arquivos de config, o layout de pastas, saída de `--help` — e documento que o reescreve é **cache**: cópia de uma consulta, que só paga a carga quando a consulta é cara. Cacheie o que o agente não acha olhando: a convenção não escrita, o porquê de uma escolha, a pegadinha que nenhum config confessa. Deixe as consultas de um-arquivo-um-comando com o ambiente, onde não envelhecem.
- Cheque cada linha por **relevância**: ainda incide sobre o que o documento faz? Uma linha perde relevância por nunca incidir na tarefa (exposição pura, ou ramo que deveria ser divulgado) ou por envelhecer quando o comportamento ou o mundo muda. Documentos curtos são mais fáceis de manter relevantes. Sem disciplina de poda o destino é **sedimento**: camadas velhas que assentam porque adicionar parece seguro e remover parece arriscado.
- Cace **no-ops** frase por frase: instrução que o modelo já obedece por padrão paga carga para dizer nada. O teste — muda o comportamento em relação ao padrão? — é relativo ao modelo, não ao leitor: duas pessoas discordando sobre um no-op discordam sobre o padrão, e resolvem executando o documento, não debatendo. Falhou o teste, delete a frase inteira. O teste também avalia palavras-guia: palavra fraca demais para vencer o padrão (*seja minucioso* quando o agente já é razoavelmente minucioso) é no-op — a correção é palavra mais forte (*relentless*), não outra técnica.

## Aplicação local

As 30+ skills de `~/.claude/skills` pagam cada `description:` em toda sessão, e o bundle do claude.ai já duplicou parte delas — aqui a alavanca de maior retorno é a poda de ponteiros: colapsar sinônimos que renomeiam o mesmo gatilho, cortar identidade que o corpo já carrega, e caçar no-ops nas regras acumuladas.

## Origem

Adaptado do `/writing-for-agents` de Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills), MIT). A parte de mecânica de skills (`SKILL-MECHANICS.md`) não foi portada — esse papel aqui é da `skill-creator`.
