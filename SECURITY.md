# Política de Segurança e Dados Sensíveis

Este repositório é **público** e trata de fluxos de trabalho de Polícia Judiciária. Por isso, a principal preocupação de segurança não é vulnerabilidade de código, e sim **vazamento de dados sigilosos**.

## O que este repositório NÃO deve conter

- Dados de casos reais: nomes de investigados, vítimas ou testemunhas, números de procedimento (IP, APF, TCO, BOC, RIF), endereços, documentos
- Peças processuais reais, ainda que parcialmente editadas
- Credenciais, tokens, chaves de API (inclusive do NotebookLM ou GitHub)
- Qualquer informação coberta por sigilo funcional, segredo de justiça ou protegida pela LGPD (Lei 13.709/2018)

O acervo de modelos reais fica em repositório privado separado; aqui são versionados apenas os arquivos `LEIA-ME` que explicam essa separação. A política está documentada nos comentários do `.gitignore` da raiz.

## Encontrou dado sensível publicado?

Se você encontrar neste repositório (inclusive no histórico do git) qualquer dado que pareça real ou sigiloso:

1. **Não abra issue pública** descrevendo o dado.
2. Escreva diretamente para **andrevictor23@gmail.com** com o caminho do arquivo/commit.
3. O conteúdo será removido — inclusive do histórico, com reescrita e força de push se necessário — e as pessoas afetadas, comunicadas quando cabível.

## Vulnerabilidades em scripts

As skills incluem scripts Python e PowerShell executados localmente. Se encontrar comportamento perigoso (exclusão indevida de arquivos, envio de dados a terceiros, injeção de comandos a partir de entrada não confiável), reporte pelo mesmo e-mail acima ou, se não envolver dado sensível, abra uma [issue](../../issues).

## Aviso sobre o hook de auto-sync

O `.claude/settings.json` deste repo registra um hook que faz **commit e push automáticos** ao final de sessões do Claude Code abertas na pasta. Quem clona o repositório inteiro deve remover o hook ou garantir que nunca deixe arquivos sensíveis na árvore de trabalho — eles seriam publicados automaticamente.

## Escopo de suporte

Projeto pessoal, sem SLA. Reportes de segurança são priorizados sobre qualquer outra demanda.
