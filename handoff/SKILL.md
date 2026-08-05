---
name: handoff
description: Comprime a sessão atual num documento de passagem para uma sessão futura (ou outro agente) continuar o trabalho do ponto exato onde parou. Use quando o usuário pedir "handoff", "passa o caso", "documento de passagem", "anota onde paramos", "encerra por hoje", "continuo amanhã em outra sessão", ou quando um trabalho longo (inquérito, peça, projeto, estudo) for atravessar sessões. Não use para registrar decisões de sabatina — a skill sabatina grava a própria ata.
---

# Handoff

Escreva um documento de passagem que permita a uma sessão nova continuar o trabalho sem depender da memória deste chat.

## Onde gravar

Na pasta de trabalho do assunto — a pasta dos autos, do projeto ou de estudos — como `handoff-<tema>-AAAA-MM-DD.md`. Nunca no scratchpad temporário (evapora entre sessões) e nunca em `Downloads` (área de passagem).

## O que contém

- **Estado** — o que foi feito, o que está em andamento, o que falta; cada pendência com seu critério de pronto.
- **Decisões vivas** — o que já foi decidido e com que fundamento. Se existe ata de sabatina, referencie-a; não a repita.
- **Referências por caminho** — autos, atas, minutas, specs, commits: aponte caminho ou URL em vez de duplicar conteúdo que já vive em outro artefato.
- **Skills sugeridas** — quais skills a próxima sessão deve invocar e em que ordem (ex.: `representacao-cautelar` depois de fechada a tese; `relatorio-final-ip` quando a instrução terminar).
- **Lacunas de fato** — os `[VERIFICAR]` em aberto, cada um com o que falta conferir e onde.
- **Foco da próxima sessão** — se o usuário disse para que vai usar a próxima sessão, oriente o documento inteiro para isso.

## Sigilo

Redija fora do documento credenciais, senhas, chaves de API e tokens — sempre, em qualquer frente. Em material da DELEGACIA o documento fica na pasta dos autos e não sai da máquina: mantenha os dados nominais necessários ao trabalho, aplicando as regras de sigilo da pasta em que estiver.

## Origem

Adaptado do `/handoff` de Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills), MIT), com destino, seções e regras de sigilo adaptados ao fluxo do usuário.
