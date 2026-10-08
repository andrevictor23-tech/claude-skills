# Ofícios requisitórios

Base: ofícios reais do Núcleo de Inteligência da Delegacia Regional de Alta Floresta, sanitizados e corrigidos. O sistema da PJC gera cabeçalho, número ("OFÍCIO Nº AAAA.UU.NNNN/NI/DR-AFL"), local e data. O texto abaixo começa no destinatário.

Correções em relação às fontes reais, para não repetir:

- A advertência de não notificação citava o "art. 2º, § 1º, da Lei 12.830/2013". Esse dispositivo não é crime; o embaraço à investigação de organização criminosa é o art. 2º, § 1º, da Lei 12.850/2013.
- Ofício a operadora pedia "ID do terminal (UTID)" e "ID do roteador Starlink", campos que só a Starlink tem.
- Ofício por IP não informava a porta lógica de origem.
- Período ficou entre colchetes no texto expedido.

## 1. Corpo — requisição de dados cadastrais

```
Senhor(a) [DIRETOR(A) | RESPONSÁVEL],
[Departamento Jurídico | Setor de Atendimento a Autoridades]
[RAZÃO SOCIAL DO DESTINATÁRIO]
[Endereço, quando exigido]

Assunto: REQUISIÇÃO DE DADOS CADASTRAIS

Senhor(a) [cargo],

Com o fito de instruir o Inquérito Policial nº [número] ([número interno]), em curso nesta unidade, REQUISITO a Vossa Senhoria que encaminhe, no prazo de [24 | 48] horas, os dados cadastrais [do(s) usuário(s) | do(s) assinante(s)] vinculado(s) ao(s) identificador(es) abaixo[, no período de DD/MM/AAAA a DD/MM/AAAA]:

[identificador 1]
[identificador 2]

Requisitam-se os seguintes dados: [campos da seção 4, conforme o destinatário].

A presente requisição fundamenta-se no [fundamento da seção 2].

Considerando o sigilo do inquérito policial (art. 20 do Código de Processo Penal), requisito, ainda, que o(s) titular(es) NÃO seja(m) notificado(s) acerca desta requisição. [Somente em investigação de organização criminosa: Registro que a recusa ou a omissão dos dados requisitados configura, em tese, o crime previsto no art. 21 da Lei nº 12.850/2013.]

A resposta e eventuais arquivos deverão ser encaminhados [via sistema LERS | ao e-mail institucional (endereço)], aos cuidados de [nome do responsável].
```

## 2. Fundamento por hipótese

Cite o dispositivo da hipótese, não a lei inteira. Conferência completa na seção 0 de `representacao-cautelar/references/quebra-sigilo.md`.

| Hipótese | Fundamento |
|---|---|
| Usuário de provedor de internet (Google, Meta, Microsoft, Apple, plataformas) | Art. 10, § 3º, da Lei 12.965/2014, c/c art. 11 do Decreto 8.771/2016 |
| Investigação de organização criminosa (qualquer destinatário da lista legal) | Art. 15 da Lei 12.850/2013 |
| Investigação de lavagem de dinheiro | Art. 17-B da Lei 9.613/1998. **Não** o 17-D, que trata de afastamento de servidor |
| Crimes do rol do art. 13-A do CPP (sequestro, cárcere, redução a condição análoga, tráfico de pessoas, extorsão com restrição da liberdade ou mediante sequestro, art. 239 do ECA) | Art. 13-A do CPP |
| Demais casos | Art. 2º, § 2º, da Lei 12.830/2013 (poder requisitório do Delegado), somado ao dispositivo específico do destinatário, se houver |

Cumule quando couber (ex.: organização criminosa com uso de conta Google: art. 15 da Lei 12.850/2013 e art. 10, § 3º, da Lei 12.965/2014).

## 3. Preservação de registros

Parágrafo a acrescentar ao ofício, ou ofício próprio, quando se pretende pedir depois ao juiz os registros de conexão ou de acesso:

```
Requisito, ainda, com fundamento nos arts. 13, § 2º, e 15, § 2º, da Lei nº 12.965/2014, a preservação dos registros de conexão e de acesso a aplicações de internet vinculados ao(s) identificador(es) acima, no período de [DD/MM/AAAA a DD/MM/AAAA], até ulterior ordem judicial.
```

Prazo de 60 dias, contados do requerimento, para ingressar com o pedido judicial de acesso (art. 13, § 3º). Registre esse prazo nas Notas ao Delegado.

## 4. Campos por tipo de destinatário

Peça apenas campos que o destinatário tem e que cabem em requisição direta. O que estiver na coluna "vai ao juiz" sai do ofício e entra nas Notas, com remissão à `representacao-cautelar`.

| Destinatário | Identificador que o ofício deve trazer | Campos cadastrais | Vai ao juiz |
|---|---|---|---|
| Google | e-mail completo | nome informado, e-mail e telefone de recuperação, data de criação da conta | registros de acesso (IPs de login), conteúdo, localização. IP de criação: [VERIFICAR] a prática do provedor |
| Meta (WhatsApp, Instagram, Facebook) | número com DDI e DDD, ou URL/ID do perfil | nome de perfil, e-mail e telefone vinculados, data de criação | registros de acesso, conteúdo, contatos, grupos |
| Operadora, linha telefônica | número com DDD | nome, CPF/CNPJ, filiação, endereço, data de habilitação, plano | extrato de chamadas, ERB, localização |
| Provedor de conexão, por IP (operadora, provedor regional) | **IP, porta lógica de origem, data, hora e fuso horário** | nome, CPF/CNPJ, endereço de instalação, telefone, e-mail, número do contrato | demais registros de conexão |
| Starlink (SpaceX) | IP, porta, data, hora e fuso; ou número da conta | os do provedor de conexão, mais ID do terminal (UTID), ID do roteador e endereço de serviço | demais registros |
| Banco ou instituição de pagamento (titular de conta ou chave PIX) | chave PIX, agência e conta, ou identificador da transação | nome, CPF/CNPJ, data de abertura | extratos e movimentação (LC 105/2001) |

Identificação por IP: a associação do registro de conexão a dados pessoais tem regra própria no art. 10, § 1º, da Lei 12.965/2014, e há provedores que só respondem com ordem judicial. Registre nas Notas: [VERIFICAR] se o destinatário atende por requisição; se recusar, representar.

Instituição financeira fora das hipóteses de organização criminosa e lavagem: a titularidade de conta ou chave PIX pode ser tratada como dado sob sigilo bancário. Apresente ao usuário as duas vias (requisição direta e representação judicial) com o risco de cada uma e recomende.

## 5. Canal e prazo

- **Google:** sistema LERS, com indicação do responsável que receberá a resposta.
- **Meta:** portal de solicitações de autoridades da própria empresa. [VERIFICAR] endereço vigente.
- **Operadoras e demais:** e-mail do setor de atendimento a autoridades. [VERIFICAR] contato vigente. A resposta vai ao e-mail institucional da unidade.
- **Prazo:** 24 horas quando houver urgência concreta (risco à vida, prisão, flagrante, preservação de prova); 48 horas como regra; prazo maior para volume grande de dados. Urgência alegada pede motivo de uma linha no próprio ofício.
