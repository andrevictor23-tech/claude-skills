---
name: representacao-cautelar
description: Redige representações da Autoridade Policial dirigidas ao Juízo, no padrão real da Delegacia de Polícia de Alta Floresta/MT e do NEAMV, apoiando-se em um banco de modelos reais do próprio Delegado. Cobre prisão preventiva, prisão temporária, busca e apreensão domiciliar, afastamento de sigilo de dados telefônicos e telemáticos, interceptação, sigilo bancário e fiscal, acesso a dados de dispositivos apreendidos, medidas assecuratórias sobre bens e destinação de bens apreendidos. Use SEMPRE que o usuário pedir para representar, redigir representação, pedir preventiva, temporária, busca e apreensão, quebra ou afastamento de sigilo, interceptação, ou disser "representa pela preventiva", "monta a representação", "faz o pedido de busca", "quebra o sigilo do alvo", "pede a interceptação", "representa pelo acesso ao celular apreendido". Use também quando o pedido tiver como alvo dados guardados por provedor de aplicação de internet, rede social, aplicativo de mensagens, aplicativo de transporte ou entrega, ou por operadora de telefonia, inclusive para os ofícios judiciais a essas empresas. Também use quando o despacho de plantão já sinalizou "é caso para REPRESENTAÇÃO PELA PRISÃO PREVENTIVA" e o usuário quiser a peça completa, quando ele entregar autos ou fatos pedindo para avaliar quais medidas cabem ("olha esses autos e vê o que cabe", "o que dá pra pedir nesse caso"), e quando pedir para adicionar ou ingerir modelos de representação na base de conhecimento da skill. Não use para despacho de plantão (use despacho-plantao) nem para relatório final de IP (use relatorio-final-ip).
---

# Representação Cautelar

Skill que redige, no padrão real da Delegacia de Polícia de Alta Floresta/MT e do NEAMV, as **representações da Autoridade Policial dirigidas ao Poder Judiciário**: prisão preventiva, prisão temporária, busca e apreensão, quebras de sigilo (telefônico, telemático, bancário, fiscal), interceptação de comunicações e acesso a dados de dispositivos apreendidos.

O usuário é o Delegado Titular. A skill produz o **rascunho da peça que ele assinaria**, pronto para revisão. Fecha o ciclo com as skills irmãs: `despacho-plantao` decide o plantão, esta skill materializa a medida cautelar representada, e `relatorio-final-ip` encerra o inquérito.

## Princípio que rege tudo

Representação cautelar é peça de convencimento sob **reserva de jurisdição**: quem decide é o juiz, e a peça só cumpre seu papel se demonstrar, com fatos concretos e individualizados, os requisitos legais da medida. Fundamentação genérica ("garantia da ordem pública" sem lastro fático) é a causa número um de indeferimento e de nulidade. Por isso a regra de ouro: **cada requisito legal recebe um parágrafo próprio, amarrado a um fato concreto dos autos, com indicação de folhas quando disponível**.

A precisão jurídica é inegociável. Medida cautelar mal fundamentada solta réu perigoso e anula prova boa. Quando faltar dado essencial (vida pregressa, endereço exato, período do sigilo), não invente: registre a lacuna nas Notas ao Delegado e, se a peça puder ser redigida com placeholder, use marcador claro `[VERIFICAR: ...]`.

## Fluxo de trabalho

### Passo 1 — Identificar a medida e carregar a referência

Dois modos de entrada:

**a) O usuário nomeia a medida** ("representa pela preventiva", "monta a busca"): siga direto para a referência correspondente.

**b) O usuário entrega os autos/fatos sem nomear a medida** ("olha esses autos e vê o que cabe"): leia o material, identifique TODAS as medidas cautelares cabíveis e os modelos aplicáveis do banco do usuário (consulte `references/catalogo-modelos.md`, somente o catálogo), e **apresente a lista ao usuário para confirmação antes de redigir qualquer peça**: cada medida com uma linha de justificativa e o modelo que seria usado. Use AskUserQuestion quando disponível (multiSelect, uma opção por medida). Só redija o que ele confirmar.

Um mesmo caso pode cumular medidas (ex.: preventiva + busca e apreensão; busca + acesso aos dados dos celulares apreendidos). Carregue a referência correspondente **antes de redigir**:

| Medida | Referência | Fundamento nuclear |
|---|---|---|
| Prisão preventiva | `references/preventiva-temporaria.md` | arts. 311 a 316 do CPP |
| Prisão temporária | `references/preventiva-temporaria.md` | Lei 7.960/89 |
| Busca e apreensão | `references/busca-apreensao.md` | arts. 240 a 250 do CPP |
| Quebra de sigilo de dados / interceptação / bancário / fiscal / dispositivos | `references/quebra-sigilo.md` | Lei 9.296/96, Marco Civil, LC 105/01, Lei 12.850/13 |

As referências contêm os requisitos legais de cada medida, as armadilhas que geram indeferimento e os blocos de fraseologia específicos. O template estrutural comum (endereçamento, cabeçalho, fecho) está em `templates/modelo_base.md`.

**Banco de modelos do usuário**: o usuário mantém um acervo de modelos reais das suas peças, indexado em `references/catalogo-modelos.md`. Abra **o catálogo** (nunca a pasta de modelos inteira), escolha o que se aplica ao caso e carregue só os arquivos escolhidos. Havendo modelo compatível, ele é o esqueleto preferencial: a fraseologia real do usuário prevalece sobre os blocos genéricos das referências. O catálogo explica como combinar corpo de peça e blocos de pedidos, e quais medidas não têm modelo (essas usam as referências acima).

O acervo e o catálogo são material sigiloso e ficam fora deste repositório. Se `references/catalogo-modelos.md` não existir, leia `references/catalogo-modelos.LEIA-ME.md` para restaurá-lo; sem ele a skill continua funcionando, apenas sem a fraseologia do usuário.

Para adicionar modelos novos, siga o procedimento de ingestão descrito no catálogo (`scripts/ingest_modelos.py` faz a extração e a sanitização).

### Passo 2 — Verificar cabimento antes de redigir

Antes de escrever uma linha da peça, confira o cabimento. Se a medida pedida não couber, **diga isso ao usuário com o fundamento e proponha a alternativa cabível**, em vez de redigir peça natimorta. Exemplos típicos:

- Preventiva por crime com pena máxima igual ou inferior a 4 anos, sem reincidência dolosa e fora de violência doméstica: não passa pelo art. 313 do CPP. Alternativa: cautelares diversas do art. 319.
- Temporária por crime fora do rol do art. 1º, III, da Lei 7.960/89: incabível, o rol é taxativo. Alternativa: avaliar preventiva.
- Temporária após oferecimento de denúncia: incabível, medida exclusiva da fase investigatória.
- Busca e apreensão lastreada apenas em denúncia anônima, sem diligência prévia de corroboração: alto risco de indeferimento e de nulidade da prova. Alternativa: realizar campana/verificação prévia e documentá-la, depois representar.
- Dados cadastrais de linha telefônica: não precisa de representação, a autoridade policial requisita diretamente (art. 15 da Lei 12.850/13; art. 13-A do CPP nos crimes ali listados). Não gaste jurisdição com o que a lei já autoriza.

### Passo 3 — Extrair os elementos do caso

Se vierem **arquivos** (autos em PDF, BO digitalizado, termos escaneados), **não os leia direto no contexto** — extraia primeiro:

```powershell
$py = "$env:USERPROFILE\.claude\tools\docling-venv\Scripts\python.exe"
$ex = "$env:USERPROFILE\.claude\tools\extrair.py"
& $py $ex "autos.pdf"
```

Leia o `.md` gerado. Ver `sync-skills/references/extracao-documentos.md`. **Confira contra o original** qualquer trecho que for citado literalmente na peça — o OCR erra dígito e caractere.

Do relato ou dos arquivos fornecidos (BO, APF, despacho de plantão, termos de declaração), extraia: número do IP e da ocorrência; qualificação do investigado (nome completo, filiação, CPF, endereço, o que houver); vítima; fatos com datas e locais; elementos de materialidade e indícios de autoria já colhidos, com folhas; vida pregressa (APFs, condenações, medidas protetivas anteriores, processos com número); e o dado específico da medida (endereço exato da busca, número da linha e período do sigilo, operadora, IMEI do aparelho apreendido).

Se veio de um despacho de plantão desta casa, aproveite a síntese fática e o bloco de preventiva já sinalizado, expandindo-o com a estrutura completa da peça.

### Passo 4 — Redigir a peça

Estrutura fixa de toda representação da unidade (detalhes e cabeçalho em `templates/modelo_base.md`):

```
[Endereçamento]  EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [VARA] DA COMARCA DE ALTA FLORESTA/MT

[Referência]  IP nº [número], BO nº [número], autos nº [se houver]

[Preâmbulo]  A Autoridade Policial que esta subscreve, no exercício de suas atribuições
legais, com fulcro no [dispositivo], vem à presença de Vossa Excelência REPRESENTAR
pela [MEDIDA EM MAIÚSCULAS] em desfavor de [NOME EM MAIÚSCULAS], [qualificação],
pelos fatos e fundamentos a seguir expostos.

I. DOS FATOS
   Narrativa cronológica e objetiva da investigação, citando folhas dos autos.
   Encerrar com a síntese do estado atual da apuração.

II. DO DIREITO / DOS FUNDAMENTOS DA MEDIDA
    Um bloco por requisito legal, cada um amarrado a fato concreto:
    fumus commissi delicti, periculum (ou fundadas razões, ou imprescindibilidade),
    cabimento (art. 313 / rol da temporária / hipóteses do art. 240),
    adequação e insuficiência de medida menos gravosa quando exigível.

III. DO PEDIDO
     Pedidos numerados, específicos e exequíveis (o juiz defere o que está escrito:
     pedido vago gera decisão vaga). Incluir os acessórios da medida
     (ver referência específica).

[Fecho]  Nestes termos, pede deferimento.
         Alta Floresta/MT, [data por extenso].
         ANDRE VICTOR DE OLIVEIRA LEITE
         Delegado de Polícia
```

Regras de redação da casa:

- Português do Brasil, formal, técnico e impessoal. **Não usar travessões** nas peças.
- Tipificação sempre "em tese", com artigo, parágrafo, inciso e diploma exatos.
- Crimes, nomes de investigados e a medida representada em **maiúsculas/negrito** nos pontos decisivos, seguindo o padrão das peças da unidade.
- Citar folhas dos autos para cada afirmação de fato relevante; se não houver autos formados ainda (representação pós-flagrante), citar as peças do APF.
- Jurisprudência: citar apenas a consolidada e pertinente (súmulas, teses de repetitivo/repercussão geral, ADIs referidas nas referências). Na dúvida sobre vigência ou teor, sinalizar nas Notas ao Delegado em vez de citar com falsa confiança.
- Peça concisa e densa. Representação não é parecer acadêmico: cada parágrafo deve empurrar o convencimento.

### Passo 5 — Cumulações e acessórios

Verifique sempre se a medida principal pede acessórios, e inclua-os no pedido:

- **Busca e apreensão**: pedido expresso de **autorização de acesso aos dados dos dispositivos que vierem a ser apreendidos** (evita segunda representação e discussão de nulidade); apreensão de veículos, valores e documentos relacionados; cumprimento no período diurno (5h às 21h, art. 22, §1º, III, da Lei 13.869/2019).
- **Preventiva**: pedido subsidiário de cautelares do art. 319 do CPP quando estrategicamente adequado; expedição de mandado com validade e difusão nos sistemas.
- **Quebra de sigilo**: período delimitado, linhas/contas/perfis individualizados, e ofício direto da autoridade policial às operadoras/instituições para agilizar o cumprimento.
- **Temporária**: prazo requerido (5 dias, ou 30 em hediondos), condução à unidade e comunicações legais.

### Passo 6 — Notas ao Delegado (fora do corpo da peça)

Após a peça, em seção separada e enxuta, liste: **premissas assumidas** por falta de dado; **pontos de atenção jurídica** (cabimento duvidoso, jurisprudência a conferir, risco de indeferimento); **dados a completar** antes do protocolo (`[VERIFICAR: ...]` deixados no texto); e **diligências recomendadas** para robustecer a representação se houver tempo.

## Formato de saída

Por padrão, entregue a peça **direto no chat**, formatada, pronta para revisar e colar. Gere arquivo .docx apenas se o usuário pedir ("quero em Word", "gera o arquivo"); nesse caso use as configurações jurídicas da unidade (A4, Arial 12, entrelinha 1,5, justificado, cabeçalho e rodapé conforme `templates/modelo_base.md`).

## Limites

- Não decide o plantão nem lavra APF/TCO/BOC (use `despacho-plantao`).
- Não produz relatório final de inquérito (use `relatorio-final-ip`).
- Não substitui a decisão do Delegado: produz rascunho fundamentado para revisão e assinatura humana.
- Dados pessoais sob sigilo funcional: a peça compila apenas o que a medida exige; não expandir dados sensíveis de vítimas e terceiros além do necessário.
