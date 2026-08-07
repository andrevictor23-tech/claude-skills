---
name: generate
description: Gera imagens (e futuramente vídeos) via API de modelos de IA do Google — Gemini / Nano Banana para imagem e Veo para vídeo — pela rota Vertex AI, consumindo o crédito do Google Cloud. Gatilhos - /generate, gera imagem, gerar imagem, criar imagem, imagem de anúncio, imagem do produto, foto do kit, thumbnail, infográfico do anúncio, gerar vídeo, animar imagem, nano banana, veo, vertex, imagem pelo Gemini, usar o crédito do Google.
---

# /generate

Skill de geração de mídia. Padrão: rascunho grátis → final paga só na imagem escolhida → texto sempre no Canva, nunca no prompt.

## Modelos

| Tarefa | Modelo padrão | Rota | Receita |
|---|---|---|---|
| Imagem (rascunho, padrão) | Nano Banana 2 Lite (gemini-3.1-flash-lite-image) — ~R$ 0,10/img | **Vertex AI** (crédito grátis até 30/10/2026) | models/nano-banana.md |
| Imagem (final, 2K) | Nano Banana 2 (gemini-3.1-flash-image) | **Vertex AI** (crédito grátis até 30/10/2026) | models/nano-banana-2.md |
| Vídeo | Veo 3.1 | **Vertex AI** (crédito grátis até 30/10/2026) — sempre cotar e esperar OK | models/veo-3-1.md |

## Provedores e rotas

Duas rotas para os mesmos modelos Google. **Enquanto houver crédito do teste grátis, usar o Vertex para tudo** — inclusive rascunho. Razão: o crédito do Cloud é grande e tem prazo de validade (vira pó se não for usado), enquanto o saldo pré-pago do AI Studio é pequeno e não expira. Gastar primeiro o que expira.

1. **AI Studio (API Gemini direta)** — chave `GOOGLE_AI_STUDIO_KEY` no `.env`, saldo pré-pago pequeno. **Reserva**: usar só depois que o crédito do Vertex acabar ou expirar, ou se a rota Vertex estiver fora do ar. Contas novas NÃO têm cota grátis de imagem na API (`limit: 0`, verificado 31/07/2026); só texto é grátis.
2. **Vertex AI** — mesmos modelos + Veo, consumindo o **crédito do teste grátis do Google Cloud (~US$ 300, expira 30/10/2026)**. Projeto e conta ficam no `.env` local (`GOOGLE_CLOUD_PROJECT` e `GCLOUD_ACCOUNT`) — nunca escrever esses valores nesta skill, que vive em repo público. Auth: token OAuth via `gcloud auth print-access-token` (a conta de `GCLOUD_ACCOUNT` precisa estar ativa no gcloud; token dura ~1h, gerar a cada execução). Testado e funcionando em 31/07/2026. **Peculiaridade:** o Vertex exige `"role": "user"` em cada item de `contents` (sem isso, erro 400 "Please use a valid role"). **No PowerShell 5.1**, antes de chamar: `[System.Net.ServicePointManager]::Expect100Continue = $false` — sem isso o `Invoke-RestMethod` manda `Expect: 100-continue` e o endpoint devolve `417 Expectation Failed` com a página "Sorry..." do Google, que parece bloqueio antibot mas não é (verificado 31/07/2026). Endpoint: `https://aiplatform.googleapis.com/v1/projects/{GOOGLE_CLOUD_PROJECT}/locations/global/publishers/google/models/{MODEL}:generateContent` com header `Authorization: Bearer {token}`.
3. Após 30/10/2026 (ou crédito esgotado), o Vertex passa a cobrar por uso na conta — reavaliar rotas nessa data.

Leia o arquivo de receita antes de cada geração.

## Como chamar (use o script, não monte a chamada à mão)

`scripts\gerar-imagem.ps1` já resolve as três armadilhas abaixo, lê projeto/chave/pasta do `.env` e grava o sidecar. Preferir sempre ele:

```powershell
# rascunho
.\scripts\gerar-imagem.ps1 -PromptFile prompt.txt -Refs foto.jpg,ref.jpg -OutName projeto_desc_1785600000 -Aspect 9:16
# acabamento 2K
.\scripts\gerar-imagem.ps1 -PromptFile prompt.txt -Refs foto.jpg -OutName projeto_desc_1785600000_2k -Model gemini-3.1-flash-image -ImageSize 2K
```

## Armadilhas do PowerShell 5.1 (medidas em 07/08/2026)

Todas com o mesmo sintoma enganoso — parecem bloqueio, cota ou modelo errado, e não são. Se for montar a chamada fora do script, tratar as três:

1. **`ConvertTo-Json` com base64 trava a máquina.** Ele escapa a string caractere a caractere; com uma referência de poucos MB o processo chegou a **12 GB de RAM e 19 minutos sem terminar**. Montar o JSON em streaming com `StreamWriter`, escrevendo o base64 direto no arquivo. Nenhum base64 pode passar por `ConvertTo-Json`.
2. **`ConvertTo-Json` sobre string longa não devolve string.** Acima de ~1 KB ele retorna o objeto `{"value": "...", "Count": ...}`. O Vertex responde `400 Invalid value at 'contents[0].parts[0]' (text), Starting an object on a scalar field` — que parece prompt malformado, mas é o serializador. Prompt longo exige escape manual (função `ConvertTo-JsonString` no script).
3. **`Invoke-RestMethod` também sufoca na resposta**, que traz a imagem em base64. Usar `curl.exe` (nativo no Windows 10+) gravando direto em arquivo e extrair `mimeType`/`data` por regex, sem materializar o objeto.

Somam-se às duas já conhecidas: `Expect100Continue = $false` antes da chamada (senão `417`, com a página "Sorry..." do Google) e `"role": "user"` obrigatório em cada item de `contents` no Vertex.

## Chave de API

- Ler de `~\.claude\.env` (`$env:USERPROFILE\.claude\.env`) → variável `GOOGLE_AI_STUDIO_KEY`. Caminho relativo ao perfil porque as três máquinas têm nomes de usuário diferentes.
- Esse arquivo é local por máquina e **nunca** entra em git (nem no repo de skills, que é sincronizado no GitHub). Se a chave não existir na máquina atual, parar e pedir ao André para criá-la no Google AI Studio (aistudio.google.com → Get API key) e colar no `.env`.
- Nunca colar a chave em código, log, sidecar ou resposta.

## Saída

- Salvar todo arquivo FLAT na pasta de saída da máquina atual: variável `GENERATE_OUT` do `.env`; se ela não existir, usar `~\Documents\PROJETOS\LEFRAN\generations\`. O caminho do projeto muda de máquina para máquina, por isso não fica escrito aqui.
- A pasta do projeto é repo git: `generations/` precisa estar no `.gitignore` dele para as imagens não serem versionadas.
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
3. **Rascunho barato primeiro.** Iterar no Lite (~R$ 0,10/img, sai do crédito do Vertex — não é grátis, mas é ordem de grandeza mais barato). Só refazer no modelo final quando o André escolher a favorita — e mesmo assim cotar o custo (~R$ 0,20–0,30/imagem) e esperar o OK. Uma aprovação = uma execução.
4. **Vídeo é sempre cotado antes** (modelo, duração, resolução, custo em R$) e espera aprovação explícita.
5. Uma geração por vez (rate limit do free tier).
6. Prompts para o modelo em **inglês** (rendem melhor), mesmo com a conversa em português. Guardar o prompt exato no sidecar.
7. Amazon: imagem principal do anúncio segue as regras do listing (fundo branco etc.); imagens geradas entram como secundárias/cena de uso. A Dani obteve liberação para IA — na dúvida sobre um uso novo, perguntar antes.
