---
name: reels-delegado
description: Fluxo completo de publicação de reels no Instagram institucional de Delegado de Polícia Civil - edição de vídeo com ffmpeg no Windows (cortes, legendas, texto na tela), escolha de capa por grade de frames com timestamp, texto do post no estilo do usuário e respostas a comentários. Use SEMPRE que o usuário pedir para editar vídeo ou reel, cortar trecho de vídeo, colocar legenda ou texto em vídeo, criar capa de reels, escrever texto de post do Instagram, ou responder comentários do Instagram. Ative também para "edita esse vídeo", "faz a capa", "texto pro reels", "responde esses comentários".
---

# Reels do Instagram institucional (Delegado PC-MT)

## Estilo de texto (INEGOCIÁVEL — o usuário já corrigiu isso antes)
- NUNCA usar travessão (—): "dá impressão de ser IA".
- Frases curtas. Tom humano e direto, não institucional-robótico.
- Respostas a comentários: curtas e concisas. Adaptar ao interlocutor quando o usuário indicar quem é (ex.: ex-chefe, autoridade local).

## Salvaguardas (perfil de autoridade policial)
- Nada que viole sigilo investigativo, LGPD ou vedações da Corregedoria/PCMT.
- Não expor rosto/dados de investigados, vítimas ou menores em frames e capas.
- Em tema jurídico, precisão técnica: citar a lei certa, sem sensacionalismo.

## ffmpeg no Windows — receitas TESTADAS (não improvise o escaping)

**Fonte em drawtext** (a causa clássica de "Error parsing filterchain" / "Fontconfig error"): use caminho com barras normais e `\:` no dois-pontos do drive, entre aspas simples:
```
drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':text='SEU TEXTO':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-160:box=1:boxcolor=black@0.45:boxborderw=18
```
Nunca use `font=Arial` (dispara Fontconfig error). Sempre `fontfile=` explícito.

**Cortar trecho** (re-encode para corte preciso):
```
ffmpeg -y -ss HH:MM:SS -to HH:MM:SS -i entrada.mp4 -c:v libx264 -crf 18 -preset fast -c:a aac corte.mp4
```

**Remover trecho do meio** (ex.: tirar 00:09-00:13): cortar as partes boas e concatenar com filtro concat (NÃO usar demuxer concat com re-encode misto):
```
ffmpeg -y -i entrada.mp4 -filter_complex "[0:v]trim=0:9,setpts=PTS-STARTPTS[v1];[0:a]atrim=0:9,asetpts=PTS-STARTPTS[a1];[0:v]trim=13,setpts=PTS-STARTPTS[v2];[0:a]atrim=13,asetpts=PTS-STARTPTS[a2];[v1][v2]concat=n=2:v=1:a=0[v];[a1][a2]concat=n=2:v=0:a=1[a]" -map "[v]" -map "[a]" saida.mp4
```
Após cortes, SEMPRE confira as bordas: extraia 1 frame ~1s antes e depois de cada junção e olhe (o usuário já reclamou "ainda aparece o outro casal" depois de um corte).

**Formato reels**: 1080x1920 (9:16). Vídeo horizontal: `scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2` ou crop central se a pessoa estiver centralizada.

**Áudio/música desde o começo**: `-filter_complex "[1:a]volume=0.25[m];[0:a][m]amix=inputs=2:duration=first"` com a música como segunda entrada.

## Capa: SEMPRE por grade, nunca às cegas

O usuário precisa VER as opções antes de escolher (já houve loop de "FRAME RUIM"/"NÃO ESTOU VENDO"). Use o script pronto:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\reels-delegado\scripts\capa_grid.ps1" -Video "caminho\video.mp4" -OutDir "caminho\capas" [-Intervalo 3]
```

Ele gera:
1. `capas\grade.png` — mosaico de frames com o timestamp queimado em cada um;
2. `capas\frame_HH-MM-SS.png` — cada frame individual em alta resolução.

Fluxo: gere a grade → mostre ao usuário (Read no PNG) → ele diz o timestamp → entregue o frame individual correspondente. Capa sem texto por padrão (o usuário já pediu "não precisa escrever nada"); só adicionar texto se ele pedir.

## Texto do post
Estrutura que funcionou: gancho em 1 linha → 2-4 frases curtas de conteúdo (a informação jurídica em linguagem simples) → chamada leve para comentários/salvamento → hashtags no final (5-8, misturando institucionais e do tema). Sem travessão, sem emoji em excesso (0-3).

## Comentários
Peça ao usuário para colar os comentários de uma vez só. Responda todos em bloco numerado, curtos, no tom dele. Sinalize qualquer comentário que seja melhor NÃO responder (provocação, tema sub judice, pedido de informação sigilosa).
