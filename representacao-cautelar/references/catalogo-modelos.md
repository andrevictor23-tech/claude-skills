# Catálogo de Modelos do Usuário

Índice do banco de modelos reais do Delegado, armazenados em `assets/modelos/` (um arquivo .md por modelo). **Leia SOMENTE este catálogo para decidir quais modelos se aplicam ao caso; depois carregue apenas o(s) arquivo(s) escolhido(s).** Nunca carregue a pasta inteira.

## Como usar (fluxo de correspondência)

1. Com os autos/fatos lidos, identifique medida(s) cabível(is) e o tipo penal.
2. Filtre a tabela abaixo por `medida` e `hipótese`.
3. Apresente ao usuário a lista dos modelos aplicáveis (nome + uma linha de justificativa) e **confirme com ele quais usar antes de redigir**.
4. Carregue só os arquivos confirmados e use-os como esqueleto, adaptando ao caso concreto. Nunca copie nomes, números ou datas do modelo.

## Tabela de modelos

| arquivo | medida | hipótese / quando usar | observações |
|---|---|---|---|
| (vazio — aguardando ingestão de modelos) | | | |

## Ingestão de novos modelos (procedimento para o Claude)

Quando o usuário disser "adiciona esses modelos na base", "ingere os modelos", ou colocar arquivos em `assets/modelos-brutos/`:

1. Para cada arquivo bruto (.docx, .pdf, .txt): extrair o texto (docx: `python-docx` ou pandoc; pdf: extração nativa, OCR só se necessário).
2. **Sanitizar**: substituir nomes de pessoas por `[INVESTIGADO]`, `[VÍTIMA]`, `[TESTEMUNHA]`; números de IP/BO/autos por `[Nº IP]`, `[Nº BO]`, `[Nº AUTOS]`; endereços por `[ENDEREÇO]`; datas por `[DATA]`. Preservar integralmente a fraseologia, os fundamentos jurídicos e a estrutura, que são o valor do modelo.
3. Salvar como `assets/modelos/<medida>-<hipotese>.md` (kebab-case, ex.: `preventiva-descumprimento-protetiva.md`, `busca-trafico-denuncia-corroborada.md`).
4. Acrescentar UMA linha na tabela acima: arquivo, medida, hipótese de uso em até 15 palavras, observação curta se houver.
5. Apagar o arquivo bruto de `modelos-brutos/` após a conversão (o usuário mantém o original dele).
6. Se dois modelos forem quase idênticos, manter o mais completo e anotar a variação na coluna de observações, em vez de duplicar.
