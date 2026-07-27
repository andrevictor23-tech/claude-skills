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

## Barreira anti-vazamento (scan-sigilo)

Antes de qualquer commit automático, o hook executa `.claude/hooks/scan-sigilo.sh`, que escaneia os arquivos alterados em busca de padrões de dado sensível — CPF, CNPJ, número de processo (padrão CNJ), número de IP/ocorrência da PJC/MT e telefone celular. Qualquer ocorrência fora da allowlist (`.claude/sigilo-allowlist.txt`, que libera apenas arquivos revisados por humano e declaradamente fictícios) **bloqueia o commit inteiro**: nada é publicado até o autor revisar — anonimizar, mover ao acervo privado ou, se o dado for fictício, incluir o arquivo na allowlist. A detecção é por padrão de texto e não é infalível (nomes, por exemplo, não são detectáveis); a barreira complementa, não substitui, a regra de nunca usar a árvore de trabalho como rascunho de caso real.

## Escopo de suporte

Projeto pessoal, sem SLA. Reportes de segurança são priorizados sobre qualquer outra demanda.
