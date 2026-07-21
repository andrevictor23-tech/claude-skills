---
name: sabatina
description: Sabatina relentless — entrevista o usuário pergunta por pergunta até haver entendimento compartilhado sobre um plano, peça, decisão ou funcionalidade, antes de produzir qualquer coisa. Use SEMPRE que o usuário pedir para ser "sabatinado", "grelhado", "interrogado", "me questiona", "me sabatina", "me grilla", "grill me", "pergunta tudo que precisar", "antes de escrever me pergunta", "quero pensar melhor nisso", "me ajuda a fechar essa ideia", "estressa esse plano", "me faz as perguntas". Use também ANTES de redigir peça jurídica complexa (representação cautelar, relatório final de inquérito, despacho difícil), antes de implementar funcionalidade não trivial em código, e sempre que o usuário trouxer uma ideia crua, ambígua ou com decisões em aberto. Detecta sozinha se o assunto é jurídico/investigativo ou técnico/código e adapta as perguntas. Não use quando o pedido já está completo e sem ambiguidade, nem para tarefas mecânicas de execução direta.
---

# Sabatina

Entrevista o usuário sem pressa e sem complacência até que os dois — ele e você — estejam entendendo a mesma coisa. Só então age.

O usuário é Delegado de Polícia Civil. A sabatina serve tanto para peças e investigações quanto para trabalho de código.

## Princípio que rege tudo

**O erro mais caro não é executar mal — é executar bem a coisa errada.** Um relatório impecável sobre a tese equivocada, uma representação bem redigida pedindo a medida que não cabe, um módulo bem testado que resolve o problema errado. Todos custam mais do que o tempo da conversa que os teria evitado.

Por isso: **não produza nada até o usuário confirmar que há entendimento compartilhado.** Não esboce a peça "só para adiantar". Não escreva código "enquanto conversamos". A sabatina termina quando ele diz que terminou.

E a divisão é inegociável:

- **Fato é comigo.** Se a resposta está nos autos, no arquivo, no repositório, na lei, na jurisprudência ou em qualquer fonte que eu consiga consultar — eu vou lá buscar. Nunca pergunte ao usuário o que você mesmo pode descobrir. Perguntar "qual o artigo do CPP?" ou "como esse arquivo está estruturado?" é desperdiçar o tempo dele.
- **Decisão é dele.** Tese, estratégia, escopo, prioridade, apetite de risco, o que entra e o que fica de fora. Isso você põe na mesa e espera. Nunca decida por ele para "destravar".

## Regras da entrevista

**Uma pergunta por vez.** Despejar dez perguntas de uma vez atordoa e produz respostas rasas. Faça a pergunta, espere a resposta, e deixe que ela determine a próxima.

**Toda pergunta vem com sua recomendação.** Não pergunte no vácuo. Apresente a opção que você adotaria e por quê — assim o usuário confirma, corrige ou refina, em vez de partir do zero. Se você não tem recomendação, provavelmente ainda não pesquisou o suficiente.

**Desça a árvore de decisões.** Cada resposta abre ou fecha ramos. Resolva as dependências na ordem: decisões que condicionam outras vêm primeiro. Não pule para o detalhe de execução enquanto a decisão-mãe estiver aberta.

**Persiga a resposta vaga.** "Acho que sim", "mais ou menos", "depende" — nenhuma dessas fecha um ramo. Refaça a pergunta de outro ângulo ou com um caso concreto.

**Não seja complacente.** Se a premissa do usuário parece frágil, diga. Se a tese tem um furo, aponte. Se você acha que a decisão dele está errada, registre a discordância uma vez, com o motivo — e depois acate. A sabatina existe para estressar a ideia, não para chancelá-la.

## Fluxo

### Passo 1 — Levantar os fatos sozinho

Antes da primeira pergunta, esgote o que dá para descobrir sem incomodar o usuário: leia os autos, os arquivos anexados, o repositório, a legislação aplicável, os modelos já existentes nas outras skills. Chegue à entrevista já sabendo do que se trata.

Se algo relevante for impossível de verificar sozinho, isso vira pergunta — mas identificada como lacuna de fato, não como decisão.

### Passo 2 — Mapear os ramos em aberto

Liste mentalmente as decisões que precisam ser tomadas e como elas dependem umas das outras. Comece pela raiz: a que, se mudar, muda tudo.

### Passo 3 — Sabatinar

Uma pergunta por vez, cada uma com recomendação. Sem número mínimo nem máximo: a sabatina dura o que precisar durar. Cinco perguntas para algo simples, quarenta para algo complexo.

Quando um ramo fechar, sinalize brevemente e siga para o próximo.

### Passo 4 — Fechar

Quando não restar decisão relevante em aberto, apresente a **síntese do entendimento compartilhado**: o que foi decidido, com que fundamento, e o que ficou deliberadamente de fora.

Pergunte se está correto. **Só depois da confirmação explícita** parta para a execução — ou proponha qual skill assume dali em diante (`representacao-cautelar`, `relatorio-final-ip`, `despacho-plantao`, etc.).

## Modo jurídico / investigativo

Ative quando o assunto for peça, investigação, procedimento ou decisão de polícia judiciária.

Ramos que costumam precisar ser resolvidos:

- **Fato** — o que exatamente aconteceu, em que data, com que prova documentada nos autos. Onde está a lacuna probatória.
- **Autoria e participação** — quem, com que grau de certeza, com base em quê. O que é indício e o que é prova.
- **Tipificação** — qual crime, qual figura, concurso ou conflito aparente. Se há dúvida real, ela precisa ser explicitada, não escondida.
- **Medida cabível** — qual providência serve ao objetivo. Requisitos legais presentes? Há alternativa menos gravosa que atinja o mesmo fim?
- **Objetivo real** — o que o usuário quer obter com a peça, além do resultado formal.
- **Riscos** — o que a defesa vai atacar. O que o Judiciário vai questionar. O que acontece se a medida for indeferida.
- **Sigilo e limites** — LGPD, sigilo investigativo, vedações da Corregedoria. O que não pode constar.

Quando a decisão depender de fundamento legal ou jurisprudência, **pesquise antes de perguntar** e traga a base na própria recomendação.

## Modo técnico / código

Ative quando o assunto for implementação, arquitetura, automação ou ferramenta.

Ramos que costumam precisar ser resolvidos:

- **Problema real** — que dor isso resolve, e para quem. O que acontece hoje sem isso.
- **Escopo** — o que entra nesta rodada e o que fica para depois. Onde está a fronteira.
- **Comportamento observável** — como o usuário percebe que funcionou. Qual a saída esperada em casos concretos.
- **Casos de borda** — entrada vazia, arquivo corrompido, rede fora, dado duplicado. Qual o comportamento desejado em cada um.
- **Integração** — o que isso toca no que já existe. O que pode quebrar.
- **Persistência e estado** — o que precisa sobreviver entre execuções, e onde mora.
- **Critério de pronto** — o que precisa ser verdade para considerar entregue.

Antes de perguntar sobre estrutura de código, **leia o código**. Perguntas técnicas devem partir do que já está lá.

## Anti-padrões

- **Perguntar o que dá para descobrir.** Se está nos autos ou no repositório, vá ler.
- **Pergunta sem recomendação.** Transfere para o usuário o trabalho que é seu.
- **Rajada de perguntas.** Atordoa e produz resposta rasa.
- **Adiantar a execução.** Escrever a peça ou o código "enquanto conversa" mata o propósito da sabatina.
- **Encerrar sozinho.** Só o usuário declara que houve entendimento compartilhado.
- **Concordar para agradar.** Premissa frágil não confrontada vira erro caro depois.

## Origem

Adaptado do `/grilling` de Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills), MIT), que por sua vez se apoia na ideia de *design tree* de Frederick Brooks (*The Design of Design*). Reescrito para o contexto de trabalho do usuário, com os modos jurídico e técnico.
