# Nano Banana 2 (linha Gemini 3.x Image)

Modelo de acabamento: líder dos benchmarks 2026 em realismo, materiais e composição para foto de produto. Usar SOMENTE na imagem favorita já escolhida no rascunho grátis — é pago.

| Campo | Valor |
|---|---|
| Model ID | `gemini-3.1-flash-image` (estável, confirmado na lista de modelos da chave em 31/07/2026; existe também `-preview`) |
| Provedor | Google AI Studio (API Gemini direta) |
| Método | Sync |
| Tipo | Imagem |
| Chave | mesma do Nano Banana (`GOOGLE_AI_STUDIO_KEY`) — **exige billing ativado no projeto Google** |
| Docs | https://ai.google.dev/gemini-api/docs/image-generation |
| Custo | ~US$ 0,03–0,05 por imagem (~R$ 0,20–0,30) |

## Pré-condições (verificar antes de rodar)

1. Billing ativo na conta do AI Studio — sem billing a chamada falha com erro de cota/permissão. Se falhar, avisar o André que o passo é ativar billing no console (o gasto real continua sendo centavos).
2. Cotar em R$ e obter OK explícito. Uma aprovação = uma execução.

## Endpoint e formato

Idênticos ao Nano Banana (ver `nano-banana.md`), trocando o model id na URL. Diferença: aceita resolução maior via `imageConfig` — pedir 2K para imagem de listing (zoom da Amazon precisa de 1.600px+ no lado maior):

```json
"generationConfig": {
  "responseModalities": ["TEXT", "IMAGE"],
  "imageConfig": { "aspectRatio": "1:1", "imageSize": "2K" }
}
```

(Campo de tamanho: confirmar o nome exato — `imageSize` — na página de docs na primeira chamada; ajustar esta receita se tiver mudado.)

## Tratamento da resposta

Igual ao Nano Banana: `candidates[0].content.parts[*].inlineData.data` em base64 → salvar `.png`.

## Notas

- Reaproveitar o MESMO prompt e as MESMAS referências do rascunho aprovado — a etapa paga é reprodução em qualidade, não novo experimento.
- Com billing ativo os dados deixam de ser usados para treino (tier pago do Google).
