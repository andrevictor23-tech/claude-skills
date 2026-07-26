# reels-delegado

> Fluxo completo de publicação de reels no Instagram institucional de Delegado de Polícia Civil: edição com ffmpeg no Windows, capa escolhida por grade de frames, texto do post e respostas a comentários.

## O que faz

Cobre as quatro etapas da publicação de um reel:

1. **Edição de vídeo com ffmpeg no Windows** — receitas testadas (sem improvisar escaping) para cortar trechos com precisão, remover trecho do meio com filtro concat, aplicar texto na tela com `drawtext` (caminho de fonte explícito, evitando o clássico "Fontconfig error"), converter para o formato reels 1080x1920 (9:16) e mixar música desde o começo do vídeo.
2. **Capa por grade de frames** — o script `capa_grid.ps1` extrai frames em intervalo configurável com o timestamp queimado em cada um, monta um mosaico (`grade.png`) e salva cada frame individual em alta resolução. O usuário vê a grade, escolhe pelo timestamp e recebe o frame correspondente. Nunca escolher capa "às cegas".
3. **Texto do post** — estrutura validada: gancho em 1 linha, 2-4 frases curtas com a informação jurídica em linguagem simples, chamada leve para comentários/salvamento e 5-8 hashtags. Sem travessão, com no máximo 0-3 emojis.
4. **Respostas a comentários** — o usuário cola os comentários de uma vez; a skill responde todos em bloco numerado, curto e no tom dele, sinalizando os que é melhor não responder (provocação, tema sub judice, pedido de informação sigilosa).

## Quando usar

A skill ativa quando o usuário pedir para:

- Editar vídeo ou reel, cortar trecho, remover parte do meio do vídeo.
- Colocar legenda ou texto em vídeo.
- Criar ou escolher capa de reels.
- Escrever o texto do post do Instagram.
- Responder comentários do Instagram.
- Frases como "edita esse vídeo", "faz a capa", "texto pro reels", "responde esses comentários".

## Como usar

Exemplos de prompts:

1. "Edita esse vídeo: corta de 00:09 a 00:13 e deixa no formato de reels."
2. "Coloca o texto 'PENSÃO ALIMENTÍCIA' na parte de baixo do vídeo."
3. "Faz a capa desse reel" (a skill gera a grade de frames, mostra, e o usuário escolhe pelo timestamp).
4. "Escreve o texto do post sobre esse reel de medida protetiva."
5. "Responde esses comentários pra mim" (colando os comentários no chat).

## O que a skill entrega

- Vídeo editado no formato reels (1080x1920), com cortes conferidos frame a frame nas junções.
- `capas/grade.png` (mosaico com timestamps) e `capas/frame_HH-MM-SS.png` (frames individuais em alta resolução) — capa sem texto por padrão; texto só se o usuário pedir.
- Texto do post pronto para publicar, no estilo do usuário.
- Respostas aos comentários em bloco numerado, com alertas sobre comentários de risco.

Fluxo da capa: gerar a grade → mostrar ao usuário (Read no PNG) → ele indica o timestamp → entregar o frame individual correspondente.

## Estrutura da pasta

- `SKILL.md` — regras de estilo, salvaguardas e receitas testadas de ffmpeg (drawtext, cortes, concat, formato 9:16, mixagem de áudio).
- `scripts/capa_grid.ps1` — script PowerShell que gera os candidatos a capa: frames com timestamp queimado + grade mosaico. Uso: `capa_grid.ps1 -Video video.mp4 -OutDir capas [-Intervalo 3]`.

## Requisitos

- **ffmpeg** instalado e no PATH do Windows (usado tanto na edição direta quanto pelo `capa_grid.ps1`, que depende dele para extrair frames e montar o mosaico).
- **PowerShell** (o script de capa roda com `-ExecutionPolicy Bypass`).
- Fontes do Windows em `C:/Windows/Fonts/` (o `drawtext` usa `fontfile=` explícito, ex.: `arialbd.ttf`).

## Avisos

- **Estilo inegociável**: nunca usar travessão (—) nos textos; frases curtas, tom humano e direto, não institucional-robótico.
- **Salvaguardas de autoridade policial**: nada que viole sigilo investigativo, LGPD ou vedações da Corregedoria/PCMT; não expor rosto ou dados de investigados, vítimas ou menores em frames e capas; em tema jurídico, precisão técnica e sem sensacionalismo.
- Após cortes, sempre conferir as bordas das junções extraindo frames ~1s antes e depois de cada emenda.
- No `drawtext`, nunca usar `font=Arial` (dispara Fontconfig error): sempre `fontfile=` com caminho explícito, barras normais e `\:` no dois-pontos do drive.
