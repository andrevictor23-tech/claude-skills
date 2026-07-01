# Template Técnico — Mapa Mental HTML/SVG

Referência para gerar o arquivo `.html` autocontido do mapa mental: HTML único (sem dependências externas obrigatórias), layout radial, curvas de Bézier, zoom/pan, colapsar/expandir, modo claro-escuro e exportação PNG.

## Como usar
1. Monte a árvore como objeto `data` (centro + ramos + sub-ramos + folhas).
2. Cole o `data` no lugar indicado no template.
3. Ajuste título e ícones.
4. Salve como `mapa-mental-[TEMA].html` na pasta de saída e apresente com `present_files`.

O algoritmo distribui ramos por ângulo (360°/nº de ramos), desenha curvas de Bézier do centro a cada nó e posiciona o texto na ponta. Zoom por scroll, pan por arraste, clique colapsa/expande nós com filhos.

## Estrutura do objeto `data`
```js
const data = {
  titulo: "FEMINICÍDIO", icone: "⚖️",
  ramos: [
    { texto:"Conceito", cor:"#2563EB", icone:"⚖️",
      filhos:[ {texto:"Art. 121-A CP",filhos:[]}, {texto:"Condição de mulher",filhos:[]} ] },
    { texto:"Pena", cor:"#DC2626", icone:"🚫",
      filhos:[ {texto:"20 a 40 anos",filhos:[]} ] }
    // 3 a 8 ramos no total
  ]
};
```
Regras (ver SKILL.md): uma palavra-chave por ramo, máx. 4 níveis, 3 a 8 ramos principais, uma cor por ramo.

## Template HTML completo
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mapa Mental</title>
<style>
  :root{--bg:#f8fafc;--fg:#0f172a;--line:#94a3b8;--panel:#fff;--shadow:rgba(0,0,0,.12)}
  html[data-theme="dark"]{--bg:#0b1120;--fg:#e2e8f0;--line:#475569;--panel:#1e293b;--shadow:rgba(0,0,0,.5)}
  *{box-sizing:border-box} text{user-select:none;pointer-events:none}
  body{margin:0;font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--fg);overflow:hidden}
  #toolbar{position:fixed;top:12px;right:12px;z-index:10;display:flex;gap:8px}
  #toolbar button{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:8px 12px;cursor:pointer;box-shadow:0 2px 6px var(--shadow);font-size:14px}
  #legend{position:fixed;bottom:12px;left:12px;z-index:10;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 12px;box-shadow:0 2px 6px var(--shadow);font-size:12px}
  #legend .row{display:flex;align-items:center;gap:6px;margin:2px 0}
  #legend .dot{width:12px;height:12px;border-radius:50%}
  #stage{width:100vw;height:100vh;cursor:grab} #stage:active{cursor:grabbing}
  .node-hit{cursor:pointer}
</style>
</head>
<body>
<div id="toolbar">
  <button onclick="zoomBy(1.2)">+</button><button onclick="zoomBy(0.8)">−</button>
  <button onclick="resetView()">Centralizar</button><button onclick="toggleTheme()">Tema</button>
  <button onclick="exportPNG()">PNG</button>
</div>
<div id="legend"></div>
<svg id="stage"><g id="viewport"></g></svg>
<script>
/* ====== COLE AQUI O OBJETO data ====== */
const data = {
  titulo:"TEMA CENTRAL", icone:"🎯",
  ramos:[
    {texto:"Ramo 1",cor:"#2563EB",icone:"⚖️",filhos:[{texto:"Sub 1.1",filhos:[]}]},
    {texto:"Ramo 2",cor:"#DC2626",icone:"🚫",filhos:[{texto:"Sub 2.1",filhos:[]}]}
  ]
};
/* ===================================== */
const SVG="http://www.w3.org/2000/svg";
const stage=document.getElementById("stage"), vp=document.getElementById("viewport");
let view={x:0,y:0,k:1}; const collapsed=new Set();
function el(t,a){const e=document.createElementNS(SVG,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
function layout(){
  const W=innerWidth,H=innerHeight,cx=W/2,cy=H/2,nodes=[],links=[];
  nodes.push({id:"root",x:cx,y:cy,texto:data.titulo,icone:data.icone,level:0});
  const n=data.ramos.length;
  data.ramos.forEach((r,i)=>{
    const ang=(2*Math.PI*i/n)-Math.PI/2,R1=210;
    const x1=cx+Math.cos(ang)*R1,y1=cy+Math.sin(ang)*R1,id1="r"+i;
    nodes.push({id:id1,x:x1,y:y1,texto:r.texto,icone:r.icone,level:1,cor:r.cor,hasChildren:(r.filhos||[]).length>0});
    links.push({from:{x:cx,y:cy},to:{x:x1,y:y1},cor:r.cor,w:6});
    if(collapsed.has(id1))return;
    const F=r.filhos||[],spread=Math.PI/3.2;
    F.forEach((f,j)=>{
      const a2=ang+(F.length>1?(-spread/2+spread*j/(F.length-1)):0),R2=R1+150;
      const x2=cx+Math.cos(a2)*R2,y2=cy+Math.sin(a2)*R2,id2=id1+"_"+j;
      nodes.push({id:id2,x:x2,y:y2,texto:f.texto,level:2,cor:r.cor,hasChildren:(f.filhos||[]).length>0});
      links.push({from:{x:x1,y:y1},to:{x:x2,y:y2},cor:r.cor,w:3});
      if(collapsed.has(id2))return;
      (f.filhos||[]).forEach((g,k2)=>{
        const a3=a2+(-0.25+0.5*(k2/Math.max(1,(f.filhos.length-1)))),R3=R2+130;
        const x3=cx+Math.cos(a3)*R3,y3=cy+Math.sin(a3)*R3;
        nodes.push({id:id2+"_"+k2,x:x3,y:y3,texto:g.texto,level:3,cor:r.cor});
        links.push({from:{x:x2,y:y2},to:{x:x3,y:y3},cor:r.cor,w:1.5});
      });
    });
  });
  return {nodes,links};
}
function bezier(a,b){const mx=(a.x+b.x)/2;return `M ${a.x} ${a.y} C ${mx} ${a.y}, ${mx} ${b.y}, ${b.x} ${b.y}`;}
function render(){
  vp.innerHTML="";const {nodes,links}=layout();
  links.forEach(l=>vp.appendChild(el("path",{d:bezier(l.from,l.to),stroke:l.cor,"stroke-width":l.w,fill:"none","stroke-linecap":"round",opacity:.85})));
  nodes.forEach(nd=>{
    const fs=nd.level===0?26:nd.level===1?17:nd.level===2?14:12;
    const label=(nd.icone?nd.icone+" ":"")+nd.texto,pad=8,w=label.length*fs*0.6+pad*2,h=fs+pad*2;
    const g=el("g",{class:nd.hasChildren?"node-hit":"",transform:`translate(${nd.x},${nd.y})`});
    g.appendChild(el("rect",{x:-w/2,y:-h/2,width:w,height:h,rx:h/2,fill:nd.level===0?"var(--panel)":nd.cor,opacity:nd.level===0?1:.14,stroke:nd.cor,"stroke-width":nd.level===0?2:1}));
    const t=el("text",{x:0,y:fs*0.35,"text-anchor":"middle","font-size":fs,"font-weight":nd.level<=1?"700":"500",fill:"var(--fg)"});
    t.textContent=label;g.appendChild(t);
    if(nd.hasChildren)g.addEventListener("click",e=>{e.stopPropagation();collapsed.has(nd.id)?collapsed.delete(nd.id):collapsed.add(nd.id);render();});
    vp.appendChild(g);
  });
  applyView();buildLegend();
}
function applyView(){vp.setAttribute("transform",`translate(${view.x},${view.y}) scale(${view.k})`);}
function zoomBy(f){view.k=Math.max(.2,Math.min(4,view.k*f));applyView();}
function resetView(){view={x:0,y:0,k:1};applyView();}
function buildLegend(){const L=document.getElementById("legend");L.innerHTML="<b>Legenda</b>";
  data.ramos.forEach(r=>{const row=document.createElement("div");row.className="row";
    row.innerHTML=`<span class="dot" style="background:${r.cor}"></span>${(r.icone||"")} ${r.texto}`;L.appendChild(row);});}
let drag=null;
stage.addEventListener("mousedown",e=>drag={x:e.clientX-view.x,y:e.clientY-view.y});
addEventListener("mouseup",()=>drag=null);
addEventListener("mousemove",e=>{if(drag){view.x=e.clientX-drag.x;view.y=e.clientY-drag.y;applyView();}});
stage.addEventListener("wheel",e=>{e.preventDefault();zoomBy(e.deltaY<0?1.1:0.9);},{passive:false});
function toggleTheme(){const h=document.documentElement;h.dataset.theme=h.dataset.theme==="dark"?"":"dark";}
function exportPNG(){
  const W=innerWidth,H=innerHeight,clone=stage.cloneNode(true);
  clone.setAttribute("width",W);clone.setAttribute("height",H);clone.setAttribute("xmlns",SVG);
  const bg=getComputedStyle(document.body).backgroundColor;
  clone.insertBefore(el("rect",{x:0,y:0,width:W,height:H,fill:bg}),clone.firstChild);
  const xml=new XMLSerializer().serializeToString(clone),img=new Image();
  img.onload=()=>{const c=document.createElement("canvas");c.width=W;c.height=H;c.getContext("2d").drawImage(img,0,0);
    const a=document.createElement("a");a.download="mapa-mental.png";a.href=c.toDataURL("image/png");a.click();};
  img.src="data:image/svg+xml;base64,"+btoa(unescape(encodeURIComponent(xml)));
}
addEventListener("resize",render);render();
</script>
</body>
</html>
```

## Notas de adaptação
- O export PNG usa só APIs nativas do browser (sem `html2canvas`): arquivo 100% autocontido. Para mapas muito grandes, é aceitável importar `html2canvas` por CDN, mas avise que passa a exigir internet.
- Mapas densos: reduza níveis ou divida em sub-mapas, em vez de espremer tudo numa tela.
- Paleta e ícones por categoria estão no SKILL.md; uma cor por ramo principal mantém a legenda coerente.
- Versão em texto: não use este template; entregue a árvore indentada com emojis no chat.
