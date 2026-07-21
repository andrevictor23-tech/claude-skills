# Extração de documentos — referência compartilhada

Procedimento único para qualquer skill que precise ler PDF, DOCX, XLSX, PPTX,
imagem, e-mail ou HTML. **Roda 100% local — nenhum dado sai da máquina.**

## Regra inegociável

**NUNCA leia um PDF grande direto no contexto.** Sempre extraia primeiro e leia
o `.md` resultante.

Um PDF de 41 páginas escaneadas custa ~60–80k tokens lido como imagem, e ~9k
lido como Markdown extraído. A skill `simulado-quiz` aprendeu isso da pior
maneira: *"Read em PDF grande já estourou uma sessão de 100 MB"*.

## Comando

```powershell
$py = "$env:USERPROFILE\.claude\tools\docling-venv\Scripts\python.exe"
$ex = "$env:USERPROFILE\.claude\tools\extrair.py"

# 1. Diagnosticar primeiro (instantâneo, não extrai)
& $py $ex "ARQUIVO.pdf" --info

# 2. Extrair (decide sozinho entre texto nativo e OCR)
& $py $ex "ARQUIVO.pdf"

# Vários arquivos de uma vez
& $py $ex "$dir\*.pdf" --out "$dir\textos"
```

O comando imprime o caminho do `.md` gerado. **Leia esse arquivo**, não o PDF.

### Opções

| Flag | Quando usar |
|---|---|
| `--info` | Só diagnosticar: o PDF tem texto ou é escaneado? |
| `--ocr` | Forçar OCR mesmo havendo texto nativo (PDF com texto ruim) |
| `--no-ocr` | Proibir OCR — rápido, quando só interessa o texto nativo |
| `--force` | Ignorar cache e reextrair |
| `--stdout` | Imprimir em vez de salvar |
| `--out DIR` | Salvar cópia do `.md` em DIR |

## Como decide a estratégia

Sempre a via mais barata que resolve:

1. **Cache** — já extraído antes? devolve na hora (custo zero)
2. **Texto nativo** (PyMuPDF) — PDF com texto embutido: instantâneo
3. **Docling + EasyOCR `pt`** — só quando escaneado (< 200 chars/página)

## Cache sincronizado

Vai para `G:\Meu Drive\VS CODE TESTE\extracao-cache` quando o Drive existe —
**um auto extraído numa máquina não precisa ser reprocessado nas outras.**
Sem Drive, cai em `~/.claude/cache/extracao`.

A chave é o conteúdo do arquivo, não o nome: renomear não invalida o cache.

## Limites — importante para peça jurídica

**OCR não é transcrição fiel.** Medido no acervo real, o texto sai bom para ler,
analisar e localizar, mas com defeitos típicos:

- `0` no lugar de `o` (`d0 que`, `0 caráter`)
- `Nª` no lugar de `Nº`
- ordem de palavras trocada em linhas com layout complexo

**Toda citação literal em peça deve ser conferida contra o original.** Use o
extrato para trabalhar; confira o PDF antes de colar entre aspas em documento
que vai ao Judiciário.

## Desempenho

| Tipo | Tempo |
|---|---|
| PDF nativo | instantâneo |
| PDF escaneado | ~28s/página (200 folhas ≈ 1h35) |
| Cache | zero |

Escaneado grande: rode em background e avise o usuário do tempo estimado.

## Instalação numa máquina nova

```powershell
& "$env:USERPROFILE\.claude\skills\sync-skills\scripts\setup-extracao.ps1"
```

O venv tem ~1,3 GB e não vai para o git; o script o recria. Na primeira
conversão com OCR baixa ~500 MB de modelos (uma vez só).

Se o comando falhar com "Docling não encontrado", é isso que está faltando —
rode o setup antes de tentar de novo.
