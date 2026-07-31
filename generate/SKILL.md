---
name: generate
description: Gera imagens (e futuramente vídeos) via API de modelos de IA. Gatilhos - /generate, gera imagem, gerar imagem, criar imagem, imagem de anúncio, imagem do produto, foto do kit, thumbnail, infográfico do anúncio, gerar vídeo, animar imagem.
---

# /generate

Skill de geração de mídia. Padrão: rascunho grátis → final paga só na imagem escolhida → texto sempre no Canva, nunca no prompt.

## Modelos

| Tarefa | Modelo padrão | Receita |
|---|---|---|
| Imagem (rascunho, padrão) | Nano Banana 2 Lite (gemini-3.1-flash-lite-image) — ~R$ 0,10/img, exige billing | models/nano-banana.md |
| Imagem (final, 2K) | Nano Banana 2 (gemini-3.1-flash-image) — ~R$ 0,25/img, exige billing | models/nano-banana-2.md |
| Vídeo | ainda não configurado — quando chegar a hora do Instagram da loja, criar receita (Seedance/Kling/Veo) e cotar custo antes | — |

**Atenção (verificado em 31/07/2026):** contas novas do AI Studio NÃO têm cota grátis de imagem na API (`limit: 0`); só texto continua grátis. Enquanto o billing não estiver ativo, o caminho grátis é manual: a skill prepara o prompt em inglês + separa as referências de `generations\refs\`, o André gera na interface web do AI Studio (cota gratuita própria) e salva em `generations\`; a skill grava o sidecar JSON.

Leia o arquivo de receita antes de cada geração.

## Chave de API

- Ler de `C:\Users\andre\.claude\.env` → variável `GOOGLE_AI_STUDIO_KEY`.
- Esse arquivo é local por máquina e **nunca** entra em git (nem no repo de skills, que é sincronizado no GitHub). Se a chave não existir na máquina atual, parar e pedir ao André para criá-la no Google AI Studio (aistudio.google.com → Get API key) e colar no `.env`.
- Nunca colar a chave em código, log, sidecar ou resposta.

## Saída

- Salvar todo arquivo FLAT em `e:\Users\andre\Documents\PROJETOS\lefran-\generations\`
- Sem subpastas. Imagens de referência ficam em `generations\refs\`
- Nomenclatura: `{projeto}_{descricao}_{timestamp}.{ext}` (ex.: `lefran_kit-talheres-cena-cozinha_1785600000.png`)
- Após cada salvamento, gravar o sidecar JSON com o mesmo nome-base e extensão `.json`:

```json
{
  "model": "gemini-2.5-flash-image",
  "prompt": "o prompt completo enviado à API",
  "refs": ["refs/talheres-catalogo.jpg"],
  "params": { "aspect": "1:1" },
  "created": "2026-07-31T12:00:00Z"
}
```

## Regras

1. **Referência real, nunca descrita.** Produto, logo ou rosto entram como arquivo de imagem em `generations\refs\`, jamais descritos em texto. Se a referência não existir, parar e pedir o arquivo.
2. **Texto dentro da imagem é proibido no prompt.** Infográfico, medidas, selo, preço: gerar a imagem base limpa e compor o texto no Canva (conector já ligado). Texto gerado por IA erra português.
3. **Rascunho grátis primeiro.** Iterar no Nano Banana grátis. Só refazer no modelo pago quando o André escolher a favorita — e mesmo assim cotar o custo (~R$ 0,20–0,30/imagem) e esperar o OK. Uma aprovação = uma execução.
4. **Vídeo é sempre cotado antes** (modelo, duração, resolução, custo em R$) e espera aprovação explícita.
5. Uma geração por vez (rate limit do free tier).
6. Prompts para o modelo em **inglês** (rendem melhor), mesmo com a conversa em português. Guardar o prompt exato no sidecar.
7. Amazon: imagem principal do anúncio segue as regras do listing (fundo branco etc.); imagens geradas entram como secundárias/cena de uso. A Dani obteve liberação para IA — na dúvida sobre um uso novo, perguntar antes.
