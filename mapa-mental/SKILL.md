---
name: mapa-mental
description: Gera mapa mental interativo em HTML/SVG a partir de qualquer conteúdo (tema jurídico, artigo de lei, tópico de edital ou texto colado). Use quando o usuário pedir mapa mental, mapa conceitual, esquema ou resumo visual, inclusive "mapa dos meus erros" a partir da wiki de estudos.
---

# Skill: Mapa Mental para Concursos

Gera mapas mentais visuais e interativos para estudo e revisão de conteúdos de concursos públicos e áreas jurídicas.

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
5. **Negrito** nas palavras-chave dos ramos de nível 1
6. **Tamanhos de fonte**: seguir a hierarquia definida em "Detalhes Técnicos do HTML" (seção "Fontes")

---

## Formato de Saída

### Saída Padrão: HTML Interativo
Gerar arquivo `.html` autocontido com:
- **SVG** para desenho dos ramos curvos (curvas de Bézier)
- **Layout radial** com centro na tela
- **Interatividade**: zoom (scroll), pan (drag), colapsar/expandir ramos (click)
- **Responsivo**: adapta ao tamanho da tela
- **Exportável**: botão para salvar como PNG usando só APIs nativas do navegador (serializar o SVG → `Image` → `canvas.toBlob`) — nunca biblioteca de CDN, o arquivo deve funcionar offline
- **Modo escuro/claro**: toggle no canto superior
- **Legenda de cores**: exibida no canto inferior
- Salvar como `mapa-mental-[TEMA].html`. **Onde:** se o contexto for a pasta de estudos (a que contém `wiki\`), salve em `<pasta de estudos>\mapas\` (crie se não existir — fica no Drive e sincroniza entre as máquinas) e **acrescente o link do mapa na nota da disciplina** em `wiki/disciplinas/`, como já se faz com os quizzes. Fora do contexto de estudo, salve na pasta de trabalho atual.

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

1. **Receber o input**: tema livre, artigo de lei, tópico de edital ou conteúdo colado a sintetizar.
2. **Analisar e estruturar**: identificar o tema central e extrair ramos, sub-ramos, ícones e cores conforme "Regras de Produção do Mapa Mental".
3. **Gerar o mapa**: construir o HTML/SVG conforme "Formato de Saída" e "Detalhes Técnicos do HTML" (ler antes `references/template-tecnico.md`).
4. **Entregar**: salvar conforme a convenção de "Formato de Saída", informar o caminho completo como link clicável e, no contexto de estudo, linkar o mapa na nota da disciplina da wiki. Versão em texto no chat só se solicitada.

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
6. **Cores**: seguir o "Sistema de Cores" das Regras de Produção (saturado perto do centro, tom mais claro nas pontas)

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

## Modo "Mapa do Erro" (integração com a wiki de estudos)

Ative quando o usuário pedir "mapa dos meus erros", "mapa do que eu confundo", ou citar revisão de fraquezas. Fonte: `wiki/revisao/erros.md` da pasta de estudos (e as notas de disciplina referenciadas nas entradas).

1. Leia as entradas do `erros.md` (uma disciplina ou todas) e a seção "Padrões recorrentes".
2. O centro do mapa é o padrão de erro (ex.: ⚠️ REQUISITO ACRESCIDO) ou a disciplina, conforme o pedido.
3. **Pares simétricos confundidos** (ex.: encampação × caducidade) viram dois ramos lado a lado, com os atributos contrastados em sub-ramos espelhados — o objetivo visual é fixar qual atributo pertence a qual instituto.
4. **Requisitos enumerados** ganham a contagem em destaque no ramo (ex.: "IDC: 2 pressupostos ⏰") — a contagem é a arma contra a pegadinha de requisito acrescido.
5. Cada folha terminal traz a citação exata do fundamento (artigo, súmula, tema, Info) vinda da entrada do `erros.md` — nunca invente fundamento que não esteja registrado.
6. Inclua os macetes registrados nas entradas como folhas com 💡.

---

## Notas Importantes

1. **Nunca inventar conteúdo jurídico** — se incerto sobre um ponto de direito, sinalizar explicitamente
2. **Manter fidelidade à lei vigente** — aplicar atualizações legislativas (ex: Lei 14.994/2024)
3. **Priorizar concisão** — o mapa é para REVISÃO, não para estudo primário
4. **O mapa deve caber em uma tela** — se o conteúdo for muito extenso, sugerir divisão em sub-mapas
