# revisao-contradicoes

> Revisor independente de peça policial pronta: um subagente que não redigiu lê o rascunho contra as provas e devolve lista de defeitos. Aponta; nunca corrige.

**English summary:** Independent review skill for finished Brazilian police documents. Dispatches a `general-purpose` subagent that did not participate in drafting to audit a draft against its evidentiary base, looking for internal contradictions, unsupported assertions, boilerplate legal reasoning, leftover placeholders, and conclusions that do not follow from the evidence. The reviewer only reports findings — all corrections are made by the main flow and shown to the user. Runs entirely locally; network tools are forbidden because the material is confidential.

## O que faz

Fecha o ciclo das skills de peça: `despacho-plantao`, `representacao-cautelar`, `relatorio-final-ip` e `analise-rif` produzem; esta audita antes da entrega.

O subagente recebe **apenas o rascunho e a base probatória** — nunca a conversa que originou a peça, a tese escolhida ou a conclusão pretendida, porque contaminam a leitura. Ele lê como leria o Ministério Público, o juiz ou a defesa.

Cinco critérios comuns valem em toda peça: contradições internas, afirmações sem lastro, fundamentação genérica, placeholders esquecidos e coerência da conclusão. Sobre eles entram os módulos por tipo em `references/`: tipificação e excludentes no IP; recálculo de somas e deduplicação por `idComunicacao` no RAF; requisitos legais por medida na cautelar; enquadramento e providências obrigatórias no despacho.

Os apontamentos voltam classificados por gravidade (CRÍTICO, RELEVANTE, FORMAL) e são triados um a um — acatar, acatar com ressalva ou recusar. Nunca se corrige a lista inteira no automático: revisor erra, e apontamento errado acatado estraga peça boa. A entrega ao usuário registra o que foi corrigido, o que ficou pendente de dado e o que foi recusado, com o motivo.

## Quando usar

- Etapa obrigatória antes de entregar relatório final de IP, RAF, representação cautelar ou despacho de plantão;
- Pedido direto de crítica a texto já redigido: "revisa essa peça", "procura contradição aí", "isso está coerente?", "estressa esse relatório";
- Minuta trazida de fora (ofício, portaria, peça escrita pelo próprio Delegado) que precise de auditoria antes de assinar.

Não use para parecer conciso e análise em prosa, material de estudo ou conteúdo de rede social — o custo não se paga. Para interrogar o usuário **antes** de produzir, use `sabatina`; esta skill entra depois do texto pronto.

## Sigilo

O subagente roda local. É proibido acionar WebSearch, WebFetch ou MCP de nuvem durante a revisão, e proibido passar trecho de peça real a serviço externo. Conferência de jurisprudência ou dispositivo que exija consulta externa recebe `[CONFERIR EXTERNAMENTE]` e fica para depois, com dados anonimizados.

## Estrutura

```
revisao-contradicoes/
├── SKILL.md
├── README.md
└── references/
    ├── prompt-revisor.md      # prompt enviado ao subagente
    ├── criterios-ip.md        # relatório final de inquérito
    ├── criterios-raf.md       # análise financeira (RIF/COAF)
    ├── criterios-cautelar.md  # representação cautelar, por medida
    └── criterios-despacho.md  # despacho de plantão
```

## Limites

Não redige nem reescreve peça. Não substitui a leitura e a assinatura do Delegado: revisão automatizada reduz erro, não transfere responsabilidade.
