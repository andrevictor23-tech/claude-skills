# mapa-mental

> Gera mapas mentais visuais e interativos em HTML/SVG, no padrão da metodologia Buzan, para estudo e revisão de conteúdos jurídicos e de concursos públicos.

## O que faz

Transforma qualquer conteúdo de estudo (tema livre, artigos de lei, tópicos de
edital, anotações de aula ou texto colado) em um mapa mental radial, seguindo as
regras canônicas de Tony Buzan (imagem central, pensamento radiante, uma
palavra-chave por ramo, linhas curvas, cores por ramo, hierarquia visual) e
princípios de autores de técnicas de estudo para concursos (Fernando Mesquita,
William Douglas & Felipe Lima, Alexandre Meirelles).

O mapa segue estrutura obrigatória: centro com ícone + título, 3 a 8 ramos
principais (cada um com cor própria de uma paleta padrão para temas jurídicos),
sub-ramos e detalhes terminais, com no máximo 4 níveis de profundidade. Inclui
ícones/emojis por categoria (princípios, vedações, prazos, súmulas etc.) e traz
adaptações de ramos típicos por disciplina (Penal, Constitucional, Processual
Penal, Civil, Administrativo e legislação especial).

## Quando usar

A skill é ativada quando você pede algo como:

- "Faça/crie/monte um mapa mental de [tema]"
- "Mind map", "diagrama de estudo", "esquema visual", "mapa conceitual"
- "Esquematiza esse conteúdo", "resumo visual", "mapa de revisão"
- "Mapa mental do Art. 5º da CF" (artigos de lei)
- Colar um texto longo e pedir para "visualizar" ou "mapear" o conteúdo

## Como usar

Exemplos concretos de prompts:

1. "Mapa mental do crime de feminicídio"
2. "Faça um mapa mental de Direito Penal - Crimes contra a pessoa"
3. "Mapa mental: Poder de Polícia"
4. "Mapa mental do Art. 5º da CF, primeiros 10 incisos"
5. "Esquematiza esse texto em um mapa mental: [cola o conteúdo]"

Você pode pedir personalização de cores, número de ramos e profundidade — a
skill sempre oferece esse ajuste ao entregar.

## O que a skill entrega

- **Saída padrão**: arquivo `mapa-mental-[TEMA].html` autocontido (sem
  dependências externas), com desenho em SVG, layout radial, curvas de Bézier e
  interatividade completa: **zoom** (scroll), **pan** (arraste),
  colapsar/expandir ramos (clique), modo claro/escuro, legenda de cores e botão
  de exportação para PNG.
- **Saída alternativa**: se você pedir "mapa em texto" ou "mapa no chat",
  entrega a hierarquia em texto indentado com emojis, direto na conversa.

## Estrutura da pasta

```
mapa-mental/
├── SKILL.md                        # instruções da skill (metodologia, regras, fluxo)
└── references/
    └── template-tecnico.md         # template HTML/SVG completo (layout radial,
                                    # Bézier, zoom/pan, modo escuro, export PNG)
```

## Requisitos

Nenhum além do Claude Code. O HTML gerado abre em qualquer navegador, sem
instalação de bibliotecas.

## Avisos

- O mapa é ferramenta de **revisão**, não de estudo primário: confira sempre o
  conteúdo com a fonte original (lei, doutrina, material do curso).
- A skill sinaliza explicitamente quando estiver incerta sobre um ponto de
  direito, em vez de inventar conteúdo jurídico — ainda assim, valide
  fundamentos legais e atualizações legislativas antes de usar na prova.
- Conteúdos muito extensos podem não caber em uma tela; nesse caso a skill
  sugere dividir em sub-mapas.
