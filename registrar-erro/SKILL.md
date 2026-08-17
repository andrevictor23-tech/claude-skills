---
name: registrar-erro
description: Transforma questão errada colada crua — do QConcursos, do Decorando a Lei Seca, de quiz local ou de prova refeita — em entrada formatada no caderno de erros (wiki/revisao/erros.md), inferindo disciplina, motivo e fundamento. Use ao colar enunciado + gabarito e pedir "registra esse erro", "errei essa", "anota no erros.md", "joga no caderno de erros", ou ao colar várias questões de uma vez depois de uma sessão de QC. Não use para responder questão (treino-wiki/simulado-quiz), gerar flashcard (anki) nem ver estatísticas (desempenho).
---

# Registrar erro

Ponte entre "errei uma questão no celular" e o registro estruturado. O usuário cola material bruto; a skill escreve a entrada. **Ele não formata nada.**

Arquivo de destino: `wiki/revisao/erros.md` (na pasta `Meu Drive\VS CODE TESTE\`). É a base única — nunca criar arquivo paralelo nem sugerir o aposentado `CARTÓRIO MT.docx`.

## O que aceitar como entrada

Qualquer uma destas colagens, sem exigir arrumação prévia:

1. **QC completo** — enunciado + alternativas + gabarito + comentário do professor.
2. **QC parcial** — só o enunciado e "gabarito C, marquei D". É o caso mais comum no celular.
3. **DLS** — o trecho de lei com a lacuna errada, ou só "errei o art. 130 da LRP, esqueci que os efeitos correm da data do registro".
4. **Lote** — várias questões seguidas, separadas por linha em branco, numeração ou "---".
5. **Print/screenshot** do app.

## Fluxo

1. **Nunca perguntar antes de tentar.** Extrair da colagem: tema, disciplina, fonte, o que ele marcou, o gabarito, o fundamento.
2. **Fundamento vem do que ele colou** — comentário do professor, artigo citado, texto da alternativa correta. Se não veio nada e o ponto é de lei seca conhecida, escrever o dispositivo. Se depender de jurisprudência (tese, tema, informativo, ADI), **confirmar na web antes de afirmar** — vigência e desfecho não se deduzem do acervo. Não confirmando, escrever `[VERIFICAR]` e dizer o que falta.
3. **Zero material novo.** O fundamento cabe em 2–4 linhas: o dispositivo, o contraste que a banca explorou e, quando ajudar, um macete. Não abrir manual, não expandir a teoria.
4. **Inserir** ao fim da seção da disciplina correspondente, no formato canônico do arquivo. Notarial e Registral tem subseções (Notas, RI, RCPN, RTD/RCPJ, Protesto, regime jurídico/CNN) — usar `####` ali e `###` nas demais disciplinas.
5. **Confirmar em uma linha só**: "Registrado em Tributário — ITCD/MT (3ª entrada do tema)." Sem eco do conteúdo.

## Formato da entrada

```
### [Tema curto] — [QC / DLS / quiz-data `nome` / prova], [data ou nº]
- **Erro:** marquei X; gabarito Y (síntese da alternativa correta)
- **Motivo:** <vocabulário fechado>
- **Fundamento correto:** dispositivo + contraste + macete
- **Revisar em:** [link relativo à lei seca ou à nota da disciplina]
```

**Motivo usa vocabulário fechado**, senão o dashboard da skill `desempenho` não agrupa: `lei seca` · `jurisprudência` · `requisito acrescido` · `inversão de par simétrico` · `prazo/número` · `competência` · `distração`.

Alvos de "Revisar em" (caminhos relativos a `wiki/revisao/`):

| Matéria | Link |
|---|---|
| Lei 8.935, CNN, provimentos | `../../cartorio/lei-seca/2026-08-09-Lei-8935-notarios-e-registradores.md` e `...-CNN-Prov-149-2023-codigo-de-normas-nacional.md` |
| RI, concentração | `../../cartorio/lei-seca/2026-08-05-LRP-182-216-Lei-13097-54-58.md` |
| RCPN, RTD, RCPJ | `../../cartorio/lei-seca/2026-08-09-LRP-registro-civil-RTD-RCPJ-RI.md` |
| Protesto | `../../cartorio/lei-seca/2026-08-09-Lei-9492-protesto.md` |
| Parcelamento, usucapião extrajudicial | `../../cartorio/lei-seca/2026-08-07-Lei-6766-e-LRP-234-235-parcelamento.md` |
| ITBI, ITCD/MT, DOI, emolumentos | `../../cartorio/lei-seca/2026-08-09-Tributario-cartorio-ITBI-ITCD-DOI-emolumentos-MT.md` |
| Civil, Empresarial, PC, Constitucional, Administrativo, Penal, PP | `../disciplinas/<disciplina>.md` |

Só existem as sete notas de disciplina listadas — não inventar `protesto.md`, `rcpn.md` e afins.

## Reincidência

Antes de inserir, procurar no arquivo entrada do mesmo tema. Havendo:

- não duplicar o fundamento;
- acrescentar à entrada existente a linha `- **⚠️ Reincidente:** errei de novo em [fonte, data] — [o que mudou na pegadinha]`;
- avisar na confirmação. Tema com 3+ reincidências é candidato a bloco de revisão dirigida na semana final.

## Lote

Processar tudo sem interromper: uma entrada por questão, agrupadas por disciplina, num único write. Ao fim, resumo de 3 linhas: quantas entradas, em que disciplinas, e qual padrão de erro se repetiu (requisito acrescido, inversão de par, prazo). Se o padrão bater com os já anotados na seção "Padrões recorrentes", atualizar aquela seção — é o que vale mais que o erro isolado.

## Quando faltar informação

Só perguntar depois de gravar o que dá para gravar, e no máximo uma pergunta por lote. Falta de "o que marquei" não impede o registro — o fundamento é a parte útil. Registrar com `[preencher]` é preferível a travar o fluxo.
