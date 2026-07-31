# Nano Banana 2 Lite (gemini-3.1-flash-lite-image)

Modelo padrão para rascunhos e iteração — o mais barato da linha atual. **Não existe mais cota grátis de imagem na API para contas novas** (verificado em 31/07/2026: `generate_content_free_tier_requests, limit: 0`); exige billing/crédito pré-pago ativo no projeto do AI Studio.

**Alternativa grátis enquanto não houver billing:** gerar manualmente na interface web do AI Studio (aistudio.google.com), que tem cota gratuita própria, separada da API. Nesse modo a skill prepara o prompt em inglês e as referências, o André gera na web e salva o resultado em `generations\` — o sidecar JSON é gravado do mesmo jeito.

| Campo | Valor |
|---|---|
| Model ID | `gemini-3.1-flash-lite-image` |
| Provedor | Google AI Studio (API Gemini direta) |
| Método | Sync (resposta na mesma chamada) |
| Tipo | Imagem |
| Chave | `C:\Users\andre\.claude\.env` → `GOOGLE_AI_STUDIO_KEY` |
| Docs | https://ai.google.dev/gemini-api/docs/image-generation |
| Custo | ~US$ 0,01–0,02 por imagem (~R$ 0,10) — conferir na página de preços |

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-image:generateContent?key={GOOGLE_AI_STUDIO_KEY}
Content-Type: application/json
```

A chave vai na URL (padrão Google), não em header.

## Formato da requisição

```json
{
  "contents": [{
    "parts": [
      { "text": "prompt em inglês descrevendo a cena — o produto vem das referências, não do texto" },
      { "inline_data": { "mime_type": "image/jpeg", "data": "<base64 da referência 1>" } },
      { "inline_data": { "mime_type": "image/png", "data": "<base64 da referência 2>" } }
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": { "aspectRatio": "1:1" }
  }
}
```

- Referências: as fotos reais de `generations\refs\`, em base64. Até ~3 funciona bem.
- `aspectRatio`: "1:1" para listing Amazon; "4:5" ou "9:16" para Instagram; "16:9" para banner.

## Tratamento da resposta

A imagem vem em base64 dentro de:

```
candidates[0].content.parts[*].inlineData.data
```

(pode haver uma part de texto antes; procurar a part com `inlineData`). Decodificar o base64 e salvar como `.png` na pasta de saída.

## Notas

- Erro 429 com `free_tier_requests, limit: 0`: billing não está ativo — é a condição desta conta, não um bug. Ver caminho manual acima ou ativar crédito pré-pago.
- Erro 404 "model not found": o id mudou de versão — listar com `GET .../v1beta/models?key=...` e atualizar esta receita.
- Modelos aposentados para contas novas (não usar): `gemini-2.5-flash-image`, `gemini-2.5-flash`.
- Free tier de TEXTO continua funcionando nesta chave (`gemini-flash-latest`, `gemini-3.1-flash-lite`) — útil para a skill refinar prompts sem custo.
