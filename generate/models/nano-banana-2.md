# Nano Banana 2 (linha Gemini 3.x Image)

Modelo de acabamento: líder dos benchmarks 2026 em realismo, materiais e composição para foto de produto. Usar SOMENTE na imagem favorita já escolhida no rascunho — é pago (o rascunho também é, só que ~3x mais barato).

| Campo | Valor |
|---|---|
| Model ID | `gemini-3.1-flash-image` (estável, confirmado na lista de modelos da chave em 31/07/2026; existe também `-preview`) |
| Provedor | **Vertex AI** (ver rota preferida abaixo); AI Studio é reserva |
| Método | Sync |
| Tipo | Imagem |
| Chave | mesma do Nano Banana (`GOOGLE_AI_STUDIO_KEY`) — **exige billing ativado no projeto Google** |
| Docs | https://ai.google.dev/gemini-api/docs/image-generation |
| Custo | ~US$ 0,03–0,05 por imagem (~R$ 0,20–0,30) |

## Rota preferida: Vertex AI (crédito grátis até 30/10/2026)

Enquanto durar o crédito do teste grátis do Google Cloud, rodar este modelo pelo **Vertex**, não pelo AI Studio (ver seção "Provedores e rotas" no SKILL.md — endpoint, token via `gcloud auth print-access-token` e o `"role": "user"` obrigatório em `contents`). Testado e funcionando em 31/07/2026. Depois de 30/10/2026, voltar para a rota AI Studio prepay.

## Pré-condições (verificar antes de rodar)

1. Na rota Vertex: `gcloud auth print-access-token` retorna token (a conta de `GCLOUD_ACCOUNT` do `.env` ativa no gcloud). Na rota AI Studio: crédito pré-pago disponível.
2. É a etapa de acabamento: rodar só na imagem favorita já aprovada no rascunho.

## Endpoint e formato

Ver `nano-banana.md` (formato) e SKILL.md (endpoint Vertex), trocando o model id. Diferença: aceita resolução maior via `imageConfig` — pedir 2K para imagem de listing (zoom da Amazon precisa de 1.600px+ no lado maior):

```json
"generationConfig": {
  "responseModalities": ["TEXT", "IMAGE"],
  "imageConfig": { "aspectRatio": "1:1", "imageSize": "2K" }
}
```

`imageSize: "2K"` **confirmado funcionando em 31/07/2026** nas duas rotas: devolveu 2048x2048, acima do mínimo de 1.600px que o zoom da Amazon exige.

## Tratamento da resposta

Igual ao Nano Banana: `candidates[0].content.parts[*].inlineData.data` em base64 → salvar **com a extensão do `inlineData.mimeType`**, nunca presumindo o formato. O formato muda conforme a rota e o modelo, medido em 31/07/2026 com o mesmo prompt e `imageSize: "2K"`:

| Rota | mimeType | Dimensões | Tamanho |
|---|---|---|---|
| Vertex | `image/png` | 2048x2048 | ~5,0 MB |
| AI Studio | `image/jpeg` | 2048x2048 | ~2,2 MB |

Ou seja: no modelo de acabamento o Vertex entrega PNG sem perdas e o AI Studio entrega JPEG já comprimido. Mais um motivo para o acabamento sair pelo Vertex — vale mesmo depois que o crédito expirar, se a peça for para listing.

## Notas

- Reaproveitar o MESMO prompt e as MESMAS referências do rascunho aprovado — a etapa paga é reprodução em qualidade, não novo experimento.
- Com billing ativo os dados deixam de ser usados para treino (tier pago do Google).
