# Diagnóstico — as runs do André

Base: 169 runs registradas entre 13/03/2026 e 30/07/2026 (140 após excluir 29 abandonadas), extraídas de `history\*.run`. Atualizar quando o volume crescer bastante.

Números gerais: 146 horas, 4.309 andares, 19 vitórias. Ascension máxima 4 (Regent).

---

## O achado principal: o problema não é fechar a run

| Onde a run terminou | Runs | % |
|---|---|---|
| Ato 1 | 54 | 39% |
| Ato 2 | 42 | 30% |
| Ato 3 | 44 | 31% |

**Das 44 runs que chegaram ao Ato 3, 19 viraram vitória — 43%.** Quando ele chega ao Ato 3, ele ganha quase metade das vezes.

O gargalo é inteiramente **Ato 1 e Ato 2**: 69% das runs morrem antes do Ato 3. Conselho voltado a "como vencer o boss final" é energia mal gasta. O que move a agulha é sobreviver melhor à primeira metade.

---

## A diferença medível: HP entrando no Ato 3

Comparando só as 44 runs que chegaram ao Ato 3 — mesmo ponto de medição, comparação justa:

| | Elites (A1+A2) | Relíquias (andar 33) | **HP entrando no Ato 3** |
|---|---|---|---|
| Vitórias (19) | 4,9 | 14,3 | **50%** |
| Derrotas (25) | 3,8 | 12,1 | **38%** |

Os 12 pontos de HP são o sinal mais limpo dos três: medido no mesmo andar, sem viés de "quem vai bem dura mais". Elites e relíquias apontam na mesma direção, mas parte dessa diferença é causalidade reversa — uma run que já vai bem consegue lutar mais elites.

**Regra prática:** entrar no Ato 3 abaixo de 40% de HP é uma run que estatisticamente já se perdeu. Ao fim do Ato 2, se estiver nessa faixa, jogue para HP — fogueira em vez de upgrade, pule a elite marginal.

---

## O que mais o mata

Nas 121 derrotas: **58 para bosses, 47 para elites, 16 para inimigos normais**.

Perder 47 runs para elites é muito. Combinado com o dado de que ele enfrenta *menos* elites nas derrotas, o padrão é: entra na elite com deck ou HP que não comportam, perde a run ali.

**Top algozes:**

| Inimigo | Runs perdidas |
|---|---|
| Test Subject (boss A3) | 10 |
| Kaiser Crab (boss A2) | 9 |
| Terror Eel (elite) | 8 |
| The Kin (boss A1) | 7 |
| Bygone Effigy (elite) | 7 |
| Infested Prisms (elite) | 6 |
| Decimillipede (elite) | 6 |
| Vantom (boss A1) | 6 |

Terror Eel, Bygone Effigy e Decimillipede somam 21 runs — são exatamente as três elites com resposta técnica específica (Weak; burst antes de acordar; Dexterity/Intangible em vez de block bruto). Ver [guia.md](guia.md), seção 4.

---

## Por personagem

| Personagem | V/D | Win% | Asc. máx | Horas |
|---|---|---|---|---|
| **Regent** | 4/11 | **26,7%** | **4** | 15,0 |
| Silent | 4/28 | 12,5% | 3 | 33,0 |
| Ironclad | 4/44 | 8,3% | 3 | 57,8 |
| Necrobinder | 3/35 | 7,9% | 3 | 23,3 |
| Defect | 2/28 | 7,1% | 2 | 17,7 |

**O Regent é disparado o melhor personagem dele** — três vezes o win rate do Ironclad com um quarto do tempo de jogo. É o único em que passou de Ascension 3.

O Ironclad concentra 40% das horas e rende 8,3%. Se o objetivo for subir ascension, o caminho curto é Regent, não Ironclad.

O deck enxuto que o Regent pede (8–12 cartas) pode ser justamente o que corrige o vício de pegar carta demais — vale testar essa hipótese conscientemente.

---

## Cartas

**Melhor win rate** (mínimo 8 escolhas): Gather Light 57%, Child of the Stars 50%, Pull Aggro 33%, Countdown 33%, Hidden Cache 33%, Deathbringer 33%, Pinpoint 33%.

**Mais escolhidas com retorno fraco:** Prepared (20 picks, 22%), Armaments (10 picks, 19%), Shrug It Off (12 picks, 27%), Body Slam (11 picks, 23%). São cartas de utilidade que entram por hábito — candidatas naturais a skip.

**Skips bem calibrados:** Boost Away (50 skips, 0 picks), Twin Strike (41 skips, 0 picks), Havoc, Defile. Aqui o instinto está certo.

---

## Plano de correção, em ordem de impacto

1. **Meta de HP no fim do Ato 2: 50%.** É a variável mais associada a vitória. Nas últimas fogueiras do Ato 2, curar em vez de upgradar quando estiver abaixo disso.
2. **Estudar as três elites que mais matam.** Terror Eel, Bygone Effigy e Decimillipede custaram 21 runs e cada uma tem uma resposta conhecida.
3. **Piso de 2 elites por ato no Ato 1 e 2 — mas só entrando acima de 60% de HP.** Não é "mais elites", é "elites nas condições certas".
4. **Migrar as horas de Ironclad para Regent** se a meta é ascension.
5. **Cortar os picks de hábito** (Prepared, Armaments, Body Slam) quando não resolverem problema imediato.
