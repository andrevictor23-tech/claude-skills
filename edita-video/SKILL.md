---
name: edita-video
description: Edição automática de vídeos falados (Reels, stories, vídeos institucionais) — remove muletas verbais ("né", "hã", "hum"), corta silêncios e pausas mortas com auto-editor, e melhora o tom de voz (clareza de dicção, presença, de-esser, volume padronizado). Use SEMPRE que o usuário pedir para editar um vídeo dele falando, "tira os né", "corta os ham", "remove as hesitações", "melhora minha voz", "reduz a língua presa", "corta os silêncios", "limpa o áudio", "deixa o vídeo mais dinâmico", ou enviar um vídeo bruto pedindo tratamento. Não use para gerar vídeo novo por IA (use o MCP de mídia) nem para artes estáticas.
---

# edita-video — pipeline de edição de vídeo falado

Pipeline local (nada sai da máquina) para transformar um vídeo bruto do usuário
falando em versão limpa: sem muletas verbais, sem pausas mortas e com voz mais
clara e padronizada.

## Dependências (já instaladas nesta máquina)

- Python 3.12 com `faster-whisper` (modelos `large-v3` e `small` já no cache HF)
- `auto-editor` (CLI, binário standalone com ffmpeg embutido)
- `imageio-ffmpeg` (ffmpeg 7.1 usado pelos scripts — não precisa de ffmpeg no PATH)
- `demucs` (separação voz/música, para suavizar trilha de fundo em material de TV)

Se algo faltar em outra máquina: `pip install faster-whisper auto-editor imageio-ffmpeg demucs`.

## Fluxo (ordem importa)

Os scripts vivem em `scripts/` desta skill. Trabalhe numa pasta de rascunho e
entregue só o arquivo final ao usuário.

### 1. Transcrever com timestamps por palavra

```
python scripts/transcrever.py VIDEO.mp4 --modelo large-v3
```

- Gera `VIDEO.mp4.transcricao.json`.
- `large-v3` é o padrão (melhor para pt-BR); use `--modelo small` só para
  rascunho rápido ou vídeo muito longo. CPU int8: espere ~0,5–1× a duração do
  vídeo com large-v3.
- **Limitação conhecida:** o Whisper às vezes omite hesitações puras ("ham",
  "ééé") da transcrição — essas sobras normalmente caem no passo 3 (silêncio),
  porque são trechos de baixa energia.

### 2. Detectar muletas e revisar ANTES de cortar

```
python scripts/detectar_cortes.py VIDEO.mp4.transcricao.json
```

- Gera `*.cortes.json` (máquina) e `*.cortes.txt` (revisão humana, com contexto
  de 3 palavras antes/depois de cada muleta).
- **Sempre mostre o `.cortes.txt` ao usuário antes de aplicar** — "né" às vezes
  é pergunta retórica intencional. Para preservar um trecho, basta remover a
  entrada no `.cortes.json`.
- Muletas padrão: né, hã, ham, hum, uhm, ãh, ãhn, ãã, hem, hein + hesitações
  alongadas (éé..., aa..., hmm...). Ajuste com `--muletas "né,tipo assim"`.

### 3. Aplicar cortes de muletas

```
python scripts/aplicar_cortes.py VIDEO.mp4 VIDEO.mp4.transcricao.cortes.json
```

- Gera `VIDEO_sem-muletas.mp4` (reencode x264 CRF 18 — visualmente idêntico).

### 4. Cortar silêncios e pausas mortas (auto-editor)

```
auto-editor VIDEO_sem-muletas.mp4 --edit audio:threshold=0.04 --margin 0.2sec -o VIDEO_dinamico.mp4
```

- `--margin 0.2sec` mantém respiro natural; para ritmo mais agressivo de Reels
  use `0.1sec`, para tom institucional calmo use `0.3sec`.
- Rode DEPOIS do corte de muletas (os buracos deixados pelas muletas somem aqui).

### 4b. Material de terceiros (TV): suavizar trilha de fundo

Matéria de telejornal quase sempre tem trilha musical sob a fala. O passo 5
(compressor + loudnorm) REALÇA essa trilha — trate antes dele:

```
python -m demucs --two-stems=vocals -n htdemucs -o separado AUDIO.wav
ffmpeg -i separado/htdemucs/AUDIO/vocals.wav -i separado/htdemucs/AUDIO/no_vocals.wav -filter_complex "[1]volume=0.18[m];[0][m]amix=inputs=2:duration=first:normalize=0" audio_suave.wav
```

- **Padrão do usuário: suavizar (~-15 dB, volume=0.18), não remover** — a trilha
  vira ambiência. Remoção total (só `vocals.wav`) apenas se ele pedir.
- Remuxar o áudio tratado no vídeo (`-map 0:v -map 1:a -c:v copy`) e só então
  seguir para auto-editor e passo 5.

### 5. Melhorar a voz

```
python scripts/melhorar_audio.py VIDEO_dinamico.mp4
```

- Gera `*_voz.mp4` (vídeo copiado, só áudio processado): highpass 75 Hz,
  de-esser, +3 dB de presença em 3 kHz (consoantes mais nítidas — atenua a
  percepção de língua presa), compressão suave e loudnorm -16 LUFS (padrão de
  redes sociais).
- Voz ainda embolada? Suba a presença: `--presenca 4`.
- **Opção mais pesada (externa):** Adobe Podcast Enhance Speech
  (podcast.adobe.com/enhance, grátis, upload manual pelo usuário) reconstrói o
  timbre e trata dicção de forma muito mais agressiva que filtros locais.
  Ofereça quando o resultado local não bastar — mas lembre que o áudio sai da
  máquina (nunca para material de trabalho da DELEGACIA).

## Regras

1. **Nunca aplique cortes sem mostrar a lista de revisão** (passo 2). O usuário
   decide; muleta pode ser ênfase intencional.
1b. **Em material com mais de um locutor (TV, entrevista), nunca atribua fala
   por inferência textual da transcrição.** Antes de recortar "a parte do
   usuário", extraia quadros do trecho (folha de contatos via ffmpeg
   `fps=1,tile=`) e confirme QUEM está na tela. Frases como "como fulano falou"
   enganam — em 04/08/2026 uma fala do apresentador de estúdio quase foi
   entregue como fala do usuário. Dúvida remanescente vira [VERIFICAR] para o
   usuário, não decisão silenciosa.
1c. **Vídeo de TV: confira tarjas/GC (lower thirds) antes de usar quadro como
   capa ou trecho em reel.** A tarja do telejornal pode expor dado que a
   comunicação oficial do usuário promete proteger (parentesco, nome, local —
   caso tramitando em segredo de justiça). Corte a tarja do enquadramento
   (`crop`) ou escolha outro quadro.
2. Preserve o original intacto; toda saída ganha sufixo novo.
3. Vídeo de trabalho institucional (DELEGACIA) é dado sob sigilo: pipeline 100%
   local, sem Adobe Podcast, sem upload a MCP de mídia.
4. Ao final, informe: duração original → final, nº de muletas removidas,
   segundos de silêncio cortados (o auto-editor imprime o resumo).
5. Se o usuário pedir só uma parte (só silêncios, só áudio), rode só o passo
   correspondente — os passos são independentes entre si.
