---
name: mapa-mental
description: Gera mapas mentais visuais interativos em HTML/SVG para estudo e revisão de conteúdos jurídicos e de concursos públicos. Use SEMPRE que o usuário pedir para criar, fazer, gerar, montar ou desenhar um mapa mental, mind map, diagrama de estudo, esquema visual, resumo visual ou mapa conceitual — seja sobre qualquer tema (Direito, legislação, doutrina, jurisprudência, matérias de concurso, planejamento, organização de ideias). Também use quando o usuário mencionar "mapear", "visualizar conteúdo", "esquematizar", "resumo em mapa", "mapa de revisão", ou qualquer variação. Funciona com texto livre, artigos de lei, tópicos de edital, anotações de aula, ou qualquer conteúdo que precise ser organizado visualmente. Entrega arquivo HTML interativo com zoom, pan, cores, ícones e estrutura radial fiel à metodologia Buzan.
---

# Skill: Mapa Mental para Concursos

Gera mapas mentais visuais, interativos e cientificamente fundamentados para estudo e revisão de conteúdos de concursos públicos e áreas jurídicas.

## Fundamentação Metodológica

Esta skill segue os princípios consolidados pelos maiores expoentes em mapas mentais e técnicas de estudo para concursos:

### Tony Buzan — O Criador (Regras Canônicas)
1. **Imagem Central**: Sempre iniciar com uma imagem/ícone + título no centro
2. **Pensamento Radiante**: Ramos irradiam do centro para fora (nunca linear)
3. **Palavra-chave Única**: Cada ramo contém UMA palavra-chave (máximo duas)
4. **Linhas Curvas**: Ramos orgânicos e curvos (nunca retos — curvas criam conexões mais fortes)
5. **Cores**: Mínimo 3, ideal 5-7 cores distintas — uma cor por ramo principal
6. **Imagens/Ícones**: Usar em todo o mapa — imagens são processadas 60.000x mais rápido que texto
7. **Hierarquia Visual**: Linhas mais grossas perto do centro, afinando nas extremidades
8. **Perspectiva e Variação**: Variar tamanho de fontes para transmitir hierarquia
9. **Espaço Organizado**: Layout limpo com espaço entre ramos

### Fernando Mesquita — Mapas para Concursos (Ciclo EARA)
1. **Desenhos são 50% da retenção** — mesmo rústicos, devem ser feitos
2. **Mapas como ferramenta PRINCIPAL de revisão** (não secundária)
3. **Quanto mais você domina o assunto, menor o mapa fica** — síntese progressiva
4. **Folha paisagem** (horizontal) para máximo aproveitamento do espaço
5. **Integração com ciclo de revisão espaçada** — o mapa é revisado periodicamente
6. **Não confundir esquema com mapa mental** — esquemas são lineares, mapas são radiais

### William Douglas & Felipe Lima — Memorização e Mapas (Projeto GENIUS)
1. **Engrenagem de 3 rodas**: Aprendizagem → Mapa Mental → Revisão Cíclica
2. **Associações absurdas/divertidas** fixam melhor que associações lógicas
3. **Consultar fontes ao fazer o mapa** (livros, apostilas) — não fazer só de memória
4. **Revisão sistemática** dos mapas para manutenção da memória de longo prazo
5. **Cores, formas e estórias** mesmo absurdas produzem resultados eficazes
6. **Na véspera da prova**: revisar apenas pelos mapas mentais e esquemas

### Alexandre Meirelles — Ciclo de Estudo e Revisão
1. **Um só livro por disciplina** — e o mapa reflete esse material
2. **Memória visual da posição** — lembrar onde o assunto estava na página/mapa
3. **Revisão periódica obrigatória** — mapas são inúteis sem revisão
4. **Exercícios + Mapas** = combinação ótima para fixação

---

## Regras de Produção do Mapa Mental

### Estrutura Obrigatória
1. **Centro**: Ícone emoji + título do tema em fonte grande e bold
2. **Ramos Principais** (Nível 1): 3-8 ramos irradiando do centro, cada um com cor distinta
3. **Sub-ramos** (Nível 2): Derivam dos ramos principais, mesma cor mas tom mais claro
4. **Detalhes** (Nível 3+): Folhas terminais com informações específicas
5. **Máximo 4 níveis** de profundidade para manter legibilidade

### Sistema de Cores (Paleta Padrão para Concursos Jurídicos)
Cada ramo principal recebe uma cor distinta. A paleta padrão é:

| Posição | Cor         | Hex       | Uso Sugerido                        |
|---------|-------------|-----------|-------------------------------------|
| 1       | Azul Royal  | `#2563EB` | Conceitos fundamentais / Princípios |
| 2       | Vermelho    | `#DC2626` | Penalidades / Vedações / Proibições |
| 3       | Verde       | `#16A34A` | Direitos / Garantias / Permissões   |
| 4       | Laranja     | `#EA580C` | Procedimentos / Prazos              |
| 5       | Roxo        | `#9333EA` | Competência / Jurisdição            |
| 6       | Teal        | `#0D9488` | Classificações / Espécies           |
| 7       | Rosa        | `#DB2777` | Exceções / Observações importantes  |
| 8       | Âmbar       | `#D97706` | Jurisprudência / Súmulas            |

O usuário pode solicitar paleta personalizada. Se o tema não for jurídico, adaptar as associações de cor ao contexto.

### Ícones/Emojis por Categoria (Referência Rápida)
- ⚖️ Princípios / Fundamentos
- 🔒 Vedações / Proibições
- ✅ Direitos / Garantias
- ⏰ Prazos
- 📋 Procedimentos
- 🏛️ Competência / Órgãos
- ⚠️ Exceções
- 📌 Súmulas / Jurisprudência
- 📝 Requisitos
- 🔄 Processos / Fases
- 👤 Sujeitos / Partes
- 💰 Valores / Quantias
- 🚫 Crimes / Infrações
- 🛡️ Proteção / Medidas protetivas

### Regras de Texto
1. **UMA palavra-chave por ramo** (máximo 2-3 palavras em casos excepcionais como nomes de institutos jurídicos)
2. **NUNCA frases completas** nos ramos
3. **Artigos de lei**: representar como "Art. 5º, CF" (forma abreviada)
4. **Prazos**: sempre em destaque com ícone ⏰
5. **Fonte maior no centro**, diminuindo progressivamente nos sub-ramos
6. **Negrito** nas palavras-chave dos ramos de nível 1

---

## Formato de Saída

### Saída Padrão: HTML Interativo
Gerar arquivo `.html` autocontido com:
- **SVG** para desenho dos ramos curvos (curvas de Bézier)
- **Layout radial** com centro na tela
- **Interatividade**: zoom (scroll), pan (drag), colapsar/expandir ramos (click)
- **Responsivo**: adapta ao tamanho da tela
- **Exportável**: botão para salvar como PNG (usando html2canvas ou similar)
- **Modo escuro/claro**: toggle no canto superior
- **Legenda de cores**: exibida no canto inferior
- Salvar como `mapa-mental-[TEMA].html` na pasta de saída da sessão (não use caminho fixo de sistema; ele varia conforme o ambiente)

### Saída Alternativa: Texto Estruturado
Se o usuário pedir "mapa mental em texto", "mapa simples" ou "mapa no chat":
- Usar indentação com emojis para representar hierarquia
- Cores representadas por emojis de círculos coloridos
- Formato:
```
🎯 [TEMA CENTRAL]
├── 🔵 [Ramo 1]
│   ├── [Sub-ramo 1.1]
│   │   └── [Detalhe]
│   └── [Sub-ramo 1.2]
├── 🔴 [Ramo 2]
│   ├── [Sub-ramo 2.1]
│   └── [Sub-ramo 2.2]
```

---

## Fluxo de Trabalho

### Passo 1: Receber o Input
O input pode ser:
- **Tema livre**: "Faça um mapa mental de Direito Penal - Crimes contra a pessoa"
- **Artigos de lei**: "Mapa mental do Art. 5º da CF"
- **Tópico de edital**: "Mapa mental: Poder de Polícia"
- **Conteúdo colado**: Texto longo que precisa ser sintetizado em mapa

### Passo 2: Analisar e Estruturar
1. Identificar o tema central
2. Extrair 3-8 ramos principais (categorias/tópicos)
3. Para cada ramo, extrair sub-ramos (2-5 por ramo)
4. Para cada sub-ramo, extrair detalhes terminais (1-4)
5. Selecionar ícones/emojis apropriados
6. Atribuir cores seguindo a paleta

### Passo 3: Gerar o Mapa
- Construir o HTML/SVG com a estrutura mapeada
- Aplicar layout radial com algoritmo de distribuição angular
- Renderizar curvas de Bézier para ramos
- Posicionar textos ao longo dos ramos
- Adicionar interatividade (zoom, pan, collapse)

### Passo 4: Entregar
- Salvar o arquivo HTML na pasta de saída da sessão
- Apresentar ao usuário com `present_files`
- Oferecer versão em texto no chat se solicitado

---

## Detalhes Técnicos do HTML

### Consultar antes de gerar
Antes de gerar o HTML, leia o arquivo de referência técnica incluído na skill: `references/template-tecnico.md` (caminho relativo à pasta da skill).
Esse arquivo contém o template HTML completo com:
- Algoritmo de layout radial
- Curvas de Bézier para ramos orgânicos
- Sistema de cores com CSS variables
- Interatividade (zoom, pan, collapse)
- Modo escuro/claro
- Exportação PNG

### Princípios do Layout
1. **Centro absoluto** do canvas = tema central
2. **Distribuição angular** dos ramos: dividir 360° pelo número de ramos
3. **Comprimento do ramo** proporcional à importância (ramos principais mais longos)
4. **Curvas suaves**: usar `quadraticCurveTo` ou curvas de Bézier cúbicas
5. **Sem sobreposição**: algoritmo de detecção de colisão para textos
6. **Cores em gradiente**: do saturado (perto do centro) ao suave (nas pontas)

### Fontes
- Centro: `'Segoe UI', system-ui, sans-serif` — 22-28px, bold
- Nível 1: 16-18px, semibold
- Nível 2: 13-15px, regular
- Nível 3+: 11-13px, regular, cor mais clara

---

## Adaptações por Contexto

### Direito Penal
- Ramos típicos: Tipo Penal → Sujeitos → Elemento Subjetivo → Qualificadoras → Pena → Ação Penal → Consumação/Tentativa

### Direito Constitucional
- Ramos típicos: Princípios → Direitos Fundamentais → Organização do Estado → Poder Legislativo → Poder Executivo → Poder Judiciário → Controle de Constitucionalidade

### Direito Processual Penal
- Ramos típicos: Inquérito → Ação Penal → Jurisdição/Competência → Provas → Medidas Cautelares → Procedimentos → Recursos → Execução

### Direito Civil
- Ramos típicos: Pessoa → Bens → Fatos Jurídicos → Prescrição/Decadência → Obrigações → Contratos → Responsabilidade Civil

### Direito Administrativo
- Ramos típicos: Administração Pública → Atos Administrativos → Poder de Polícia → Licitação → Contratos → Servidores → Responsabilidade → Bens Públicos

### Legislação Extravagante / Especial
- Adaptar ramos ao diploma específico (Lei Maria da Penha, ECA, CDC, etc.)

---

## Exemplos de Uso

**Usuário**: "Mapa mental do crime de feminicídio"
→ Centro: ⚖️ FEMINICÍDIO (Art. 121-A CP)
→ Ramos: Conceito | Sujeitos | Qualificadoras | Pena (20-40a) | Causas de Aumento | Ação Penal | Lei 14.994/2024

**Usuário**: "Mapa mental: Poder de Polícia"
→ Centro: 🏛️ PODER DE POLÍCIA
→ Ramos: Conceito (Art. 78 CTN) | Atributos (DAC) | Espécies | Limites | Meios de Atuação | Delegação | Prescrição

**Usuário**: "Mapa mental do Art. 5º, CF - primeiros 10 incisos"
→ Centro: 🛡️ ART. 5º CF - DIREITOS FUNDAMENTAIS
→ Ramos organizados por inciso com palavras-chave

---

## Notas Importantes

1. **Nunca inventar conteúdo jurídico** — se incerto sobre um ponto de direito, sinalizar explicitamente
2. **Manter fidelidade à lei vigente** — aplicar atualizações legislativas (ex: Lei 14.994/2024)
3. **Priorizar concisão** — o mapa é para REVISÃO, não para estudo primário
4. **O mapa deve caber em uma tela** — se o conteúdo for muito extenso, sugerir divisão em sub-mapas
5. **Sempre oferecer personalização** — perguntar se o usuário quer ajustar cores, ramos ou profundidade
