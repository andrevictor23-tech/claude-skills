# Veo 3.1 (vídeo, via Vertex AI)

Modelo de vídeo para o Instagram da loja. Roda pelo Vertex consumindo o crédito do teste grátis do Google Cloud (~US$ 300, expira 30/10/2026). **Regra inegociável: cotar (modelo, duração, resolução, custo estimado em R$) e esperar OK explícito antes de cada execução. Uma aprovação = uma execução.**

| Campo | Valor |
|---|---|
| Model ID | `veo-3.1-generate-preview` (há também `veo-3.1-fast-...` e `veo-3.1-lite-...`, mais baratos — conferir ids frescos na lista de modelos) |
| Provedor | Vertex AI (projeto em `GOOGLE_CLOUD_PROJECT` no `.env` local) |
| Método | **Async** (`predictLongRunning` → poll até terminar) |
| Tipo | Vídeo (clipes ~8 s, 720p+) |
| Auth | token OAuth: `gcloud auth print-access-token` (ver SKILL.md) |
| Docs | https://cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos |
| Custo | ordem de US$ 0,20–0,40/segundo — conferir preço vigente ANTES de cotar |

## Padrão async (na primeira execução real, confirmar campos nos docs e completar esta receita)

1. `POST .../publishers/google/models/{MODEL}:predictLongRunning` com o prompt (e imagem inicial, se houver — ideal: partir da imagem de produto já aprovada).
2. A resposta traz um nome de operação (`operations/...`).
3. Poll a cada 10–15 s (`fetchPredictOperation` / GET da operação) até `done: true`.
4. Baixar o vídeo imediatamente (URLs de resultado expiram) e salvar em `generations\` com sidecar JSON.

## Notas

- Formato Instagram: aspect ratio 9:16 (Reels) ou 1:1 (feed).
- Partir de imagem (image-to-video) mantém o produto fiel — usar a imagem final aprovada como start frame, nunca só texto.
- Monitorar o consumo do crédito em "Análise de gastos" no console do Cloud; alertas de orçamento configuráveis lá.
