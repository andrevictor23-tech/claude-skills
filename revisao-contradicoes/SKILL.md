---
name: revisao-contradicoes
description: Submete peça pronta a um subagente revisor independente que só aponta defeitos — contradições internas, afirmações sem lastro nos autos, fundamentação genérica, placeholders esquecidos e conclusão que não decorre das provas. Use quando o usuário pedir para criticar, auditar, estressar ou revisar uma peça já redigida ("revisa essa peça", "procura contradição aí", "isso está coerente?"), e como etapa obrigatória antes de entregar relatório final de IP, RAF, representação cautelar ou despacho. Sabatina interroga o usuário antes de produzir; esta skill audita o texto depois de produzido.
---

# Revisão de Contradições

Revisor independente de peça pronta. Um subagente que **não participou da redação** lê o rascunho contra as provas e devolve lista de apontamentos. Quem corrige é o fluxo principal, à vista do usuário.

O usuário é Delegado de Polícia Civil. A peça auditada aqui é a que ele assina.

## Princípio que rege tudo

**Quem escreveu não enxerga o próprio furo.** O agente que redigiu carrega as premissas da redação: sabe o que quis dizer e lê no texto a intenção, não o que está escrito. Contradição entre a seção II e a seção V, afirmação que ninguém sustentou em depoimento, requisito legal "coberto" por frase genérica — tudo isso sobrevive à releitura de quem redigiu e morre na leitura de quem chega frio.

Por isso o revisor recebe **o texto e as provas, nunca o raciocínio da redação**. Ele não deve saber qual tese o redator defendia nem qual conclusão foi pedida. Ele lê a peça como leria o Ministério Público, o juiz ou a defesa: procurando onde ela se contradiz, onde afirma sem provar e onde conclui sem decorrer.

E a divisão é inegociável:

- **O revisor aponta. Nunca corrige.** Devolve lista numerada de defeitos com localização e motivo. Não reescreve trecho, não sugere redação pronta, não "melhora" o estilo. Texto novo é do fluxo principal.
- **A correção é visível.** Cada apontamento acatado vira alteração cirúrgica no trecho indicado, e a entrega ao usuário registra o que mudou. Apontamento recusado também se registra, com o motivo.
- **Discordar é permitido.** Revisor não é carimbo. Se a peça está boa, ele diz "sem apontamentos" — e isso também é resultado. Inventar defeito para parecer útil é pior que não revisar.

## Sigilo (inviolável)

O subagente roda **local, na mesma máquina**. Nenhum dado de inquérito, RIF, nome, CPF ou conta sai daqui. É proibido:

- Acionar WebSearch, WebFetch, MCP de nuvem ou qualquer ferramenta de rede dentro da revisão;
- Passar trecho de peça real a serviço externo para "conferir jurisprudência".

Conferência de dispositivo legal ou julgado que exija consulta externa **não se faz aqui**: o revisor marca o item como `[CONFERIR EXTERNAMENTE]` e o fluxo principal decide depois, com dados anonimizados, se vale a pesquisa.

## Quando roda

**Obrigatória, antes da entrega**, em:

| Peça | Skill de origem | Módulo de critérios |
|---|---|---|
| Relatório final de IP | `relatorio-final-ip` | `references/criterios-ip.md` |
| Relatório de Análise Financeira (RAF) | `analise-rif` | `references/criterios-raf.md` |
| Representação cautelar | `representacao-cautelar` | `references/criterios-cautelar.md` |
| Despacho de plantão | `despacho-plantao` | `references/criterios-despacho.md` |

**Sob demanda**, quando o usuário pedir crítica de qualquer texto já redigido — inclusive peça que ele escreveu sozinho, ofício, portaria ou minuta trazida de fora. Nesse caso use os critérios comuns e, se a peça se encaixar em um dos tipos acima, carregue também o módulo correspondente.

**Não roda** em: parecer conciso e análise em prosa (a skill de origem já dispensa), texto de estudo/concurso, conteúdo de rede social. Revisão custa tempo e tokens; peça curta de baixo risco não paga o custo.

## Fluxo

### Passo 1 — Reunir o dossiê do revisor

O revisor precisa de duas coisas, e só delas:

1. **O rascunho íntegro** da peça, como seria entregue.
2. **A base probatória** — resumo das provas dos autos, tabelas consolidadas do RIF, fatos narrados pelo usuário no plantão. O que existir de lastro.

Não inclua: a conversa que originou a peça, a tese escolhida, a conclusão pretendida, nem os apontamentos de revisões anteriores. Contaminam a leitura.

Se a base probatória não existir (o usuário colou um texto solto pedindo crítica), diga isso a ele em uma linha e rode assim mesmo — o revisor audita coerência interna, forma e fundamentação, mas **não pode auditar lastro**, e isso entra na entrega como limite declarado.

### Passo 2 — Disparar o subagente

Use a ferramenta Agent (`general-purpose`), **um subagente só**, em foreground, com o dossiê do Passo 1 e o prompt do `references/prompt-revisor.md`, acrescido do módulo de critérios da peça.

Um subagente basta. Peça longa (relatório de 500+ páginas de autos) pode ir em dois: um para contradições e lastro, outro para tipificação e forma. Acima disso não melhora o resultado, só dispersa.

### Passo 3 — Triar os apontamentos

O revisor devolve lista numerada. Antes de corrigir, classifique cada item:

- **Acatar** — defeito real. Corrigir cirurgicamente, só no trecho apontado.
- **Acatar com ressalva** — defeito real, mas a correção depende de dado que não existe. Vira `[VERIFICAR: ...]` no texto e entra nas notas ao usuário.
- **Recusar** — o revisor se enganou (leu mal, cobrou requisito inaplicável, "contradição" que não é). Registrar o motivo em uma linha.

Nunca corrija no automático a lista inteira. Revisor erra, e apontamento errado acatado estraga peça boa.

### Passo 4 — Registrar na entrega

Ao entregar a peça ao usuário, acrescente seção enxuta ao final:

```
**Revisão independente**: [N] apontamentos — [N] corrigidos, [N] pendentes de dado, [N] recusados.
- Corrigido: [defeito] ([onde])
- Pendente: [defeito] — falta [dado], marcado [VERIFICAR]
- Recusado: [defeito] — [motivo em uma linha]
```

Sem apontamentos, uma linha: `**Revisão independente**: sem apontamentos.`

Onde a skill de origem já tiver seção própria de notas (Notas ao Delegado, na `representacao-cautelar`), o resultado entra ali em vez de criar seção nova.

## Critérios comuns (valem em toda peça)

Os módulos em `references/` acrescentam critérios do tipo de peça. Estes cinco valem sempre:

1. **Contradições internas** — datas, nomes, qualificações, valores, horários e sequência dos fatos divergentes entre seções, ou entre o corpo do texto e as tabelas/anexos. Apontar as duas ocorrências, não só uma.
2. **Afirmações sem lastro** — todo fato afirmado deve corresponder a prova identificável (depoimento de quem, perícia qual, documento em que folha). Afirmação órfã é defeito, ainda que verdadeira. Hipótese apresentada como fato é o caso mais grave.
3. **Fundamentação genérica** — requisito legal "atendido" por fórmula vazia, sem fato concreto amarrado. Causa número um de indeferimento e nulidade.
4. **Placeholders e pendências** — `[VERIFICAR]`, `[nome]`, `XXX`, campo de modelo não preenchido, folha citada como `fl. __`.
5. **Coerência da conclusão** — o pedido, o indiciamento ou a decisão decorre logicamente do que foi exposto. Conclusão que não fecha com a fundamentação é defeito estrutural, não de redação.

## Limites

- Não redige nem reescreve peça: audita a que existe. Para produzir, use a skill da peça.
- Não interroga o usuário antes de produzir (isso é `sabatina`); entra depois do texto pronto.
- Não substitui a leitura e a assinatura do Delegado. Revisão automatizada reduz erro, não transfere responsabilidade.
- Não confere jurisprudência nem legislação em fonte externa (sigilo): marca `[CONFERIR EXTERNAMENTE]`.
