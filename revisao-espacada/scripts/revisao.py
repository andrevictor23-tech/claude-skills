#!/usr/bin/env python3
"""
revisao.py - Motor de revisao espacada para o caderno de erros.

Le um arquivo Markdown com erros de questoes/simulados, calcula quais itens
vencem hoje (intervalos fixos: 1, 3, 7, 15, 30 dias) e atualiza as datas
apos cada revisao.

O caderno de erros usa blocos delimitados assim (um por erro):

<!-- ERRO id=0001 -->
- **Materia:** Direito Civil
- **Assunto:** Prescricao e decadencia
- **Questao:** (texto da questao ou referencia)
- **Errei porque:** (o que voce errou / pegadinha)
- **Resposta correta:** (gabarito + fundamento)
- **Status:** ativo
- **Nivel:** 1
- **Proxima revisao:** 2026-06-17
- **Historico:** 2026-06-16(criado)
<!-- /ERRO -->

USO:
    python revisao.py due    <caderno.md>            # lista o que vence hoje (JSON)
    python revisao.py list   <caderno.md>            # lista todos os itens ativos (JSON)
    python revisao.py add    <caderno.md> --materia M --assunto A --questao Q --errei E --correta C
    python revisao.py revisar <caderno.md> --id 0001 --resultado acertou|errou
    python revisao.py stats  <caderno.md>            # contagem por materia (JSON)
"""

import argparse
import datetime
import json
import os
import re
import sys

# Intervalos fixos de revisao espacada (em dias). Nivel 1 -> +1 dia, etc.
INTERVALOS = [1, 3, 7, 15, 30]

BLOCO_RE = re.compile(
    r"<!--\s*ERRO\s+id=(?P<id>\w+)\s*-->(?P<corpo>.*?)<!--\s*/ERRO\s*-->",
    re.DOTALL,
)

CAMPO_RE = re.compile(r"-\s*\*\*(?P<chave>[^:*]+):\*\*\s*(?P<valor>.*)")


def hoje():
    return datetime.date.today()


def parse_data(s):
    return datetime.datetime.strptime(s.strip(), "%Y-%m-%d").date()


def ler_blocos(caminho):
    if not os.path.exists(caminho):
        return "", []
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()
    blocos = []
    for m in BLOCO_RE.finditer(texto):
        campos = {}
        for linha in m.group("corpo").splitlines():
            cm = CAMPO_RE.match(linha.strip())
            if cm:
                chave = cm.group("chave").strip().lower()
                campos[chave] = cm.group("valor").strip()
        campos["id"] = m.group("id")
        campos["_raw"] = m.group(0)
        blocos.append(campos)
    return texto, blocos


def montar_bloco(c):
    return (
        f"<!-- ERRO id={c['id']} -->\n"
        f"- **Materia:** {c.get('materia','')}\n"
        f"- **Assunto:** {c.get('assunto','')}\n"
        f"- **Questao:** {c.get('questao','')}\n"
        f"- **Errei porque:** {c.get('errei porque','')}\n"
        f"- **Resposta correta:** {c.get('resposta correta','')}\n"
        f"- **Status:** {c.get('status','ativo')}\n"
        f"- **Nivel:** {c.get('nivel','1')}\n"
        f"- **Proxima revisao:** {c.get('proxima revisao','')}\n"
        f"- **Historico:** {c.get('historico','')}\n"
        f"<!-- /ERRO -->"
    )


def proximo_id(blocos):
    maior = 0
    for b in blocos:
        try:
            maior = max(maior, int(b["id"]))
        except (ValueError, KeyError):
            pass
    return f"{maior + 1:04d}"


def cmd_due(caminho):
    _, blocos = ler_blocos(caminho)
    venc = []
    for b in blocos:
        if b.get("status", "ativo") != "ativo":
            continue
        pr = b.get("proxima revisao", "")
        if not pr:
            continue
        try:
            if parse_data(pr) <= hoje():
                venc.append(_resumo(b))
        except ValueError:
            continue
    print(json.dumps({"data": str(hoje()), "vencidos": venc, "total": len(venc)},
                     ensure_ascii=False, indent=2))


def cmd_list(caminho):
    _, blocos = ler_blocos(caminho)
    ativos = [_resumo(b) for b in blocos if b.get("status", "ativo") == "ativo"]
    print(json.dumps({"itens": ativos, "total": len(ativos)},
                     ensure_ascii=False, indent=2))


def cmd_stats(caminho):
    _, blocos = ler_blocos(caminho)
    cont = {}
    for b in blocos:
        if b.get("status", "ativo") != "ativo":
            continue
        m = b.get("materia", "(sem materia)")
        cont[m] = cont.get(m, 0) + 1
    ordenado = dict(sorted(cont.items(), key=lambda x: x[1], reverse=True))
    print(json.dumps({"por_materia": ordenado, "total_ativos": sum(cont.values())},
                     ensure_ascii=False, indent=2))


def _resumo(b):
    return {
        "id": b["id"],
        "materia": b.get("materia", ""),
        "assunto": b.get("assunto", ""),
        "questao": b.get("questao", ""),
        "errei_porque": b.get("errei porque", ""),
        "resposta_correta": b.get("resposta correta", ""),
        "nivel": b.get("nivel", "1"),
        "proxima_revisao": b.get("proxima revisao", ""),
    }


def cmd_add(caminho, args):
    texto, blocos = ler_blocos(caminho)
    novo_id = proximo_id(blocos)
    nivel = 1
    prox = hoje() + datetime.timedelta(days=INTERVALOS[0])
    c = {
        "id": novo_id,
        "materia": args.materia or "",
        "assunto": args.assunto or "",
        "questao": args.questao or "",
        "errei porque": args.errei or "",
        "resposta correta": args.correta or "",
        "status": "ativo",
        "nivel": str(nivel),
        "proxima revisao": str(prox),
        "historico": f"{hoje()}(criado)",
    }
    bloco = montar_bloco(c)
    if texto.strip():
        novo_texto = texto.rstrip() + "\n\n" + bloco + "\n"
    else:
        cabecalho = "# Caderno de Erros\n\n_Gerado e mantido pela skill revisao-espacada._\n\n"
        novo_texto = cabecalho + bloco + "\n"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(novo_texto)
    print(json.dumps({"adicionado": novo_id, "proxima_revisao": str(prox)},
                     ensure_ascii=False, indent=2))


def cmd_revisar(caminho, args):
    texto, blocos = ler_blocos(caminho)
    alvo = None
    for b in blocos:
        if b["id"] == args.id:
            alvo = b
            break
    if alvo is None:
        print(json.dumps({"erro": f"id {args.id} nao encontrado"}, ensure_ascii=False))
        sys.exit(1)

    nivel = int(alvo.get("nivel", "1"))
    if args.resultado == "acertou":
        nivel += 1
        if nivel > len(INTERVALOS):
            # Dominou: passa o ultimo intervalo e marca como dominado.
            alvo["status"] = "dominado"
            prox = hoje() + datetime.timedelta(days=INTERVALOS[-1])
            marca = "dominado"
        else:
            prox = hoje() + datetime.timedelta(days=INTERVALOS[nivel - 1])
            marca = f"acertou->nivel{nivel}"
    else:  # errou: volta ao nivel 1
        nivel = 1
        prox = hoje() + datetime.timedelta(days=INTERVALOS[0])
        marca = "errou->reset"

    alvo["nivel"] = str(nivel)
    alvo["proxima revisao"] = str(prox)
    hist = alvo.get("historico", "")
    alvo["historico"] = (hist + f"; {hoje()}({marca})").lstrip("; ")

    novo_bloco = montar_bloco(alvo)
    novo_texto = texto.replace(alvo["_raw"], novo_bloco)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(novo_texto)
    print(json.dumps({
        "id": args.id, "resultado": args.resultado,
        "novo_nivel": nivel, "proxima_revisao": str(prox),
        "status": alvo.get("status", "ativo"),
    }, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="Motor de revisao espacada")
    sub = p.add_subparsers(dest="cmd", required=True)

    for nome in ("due", "list", "stats"):
        sp = sub.add_parser(nome)
        sp.add_argument("caderno")

    sa = sub.add_parser("add")
    sa.add_argument("caderno")
    sa.add_argument("--materia")
    sa.add_argument("--assunto")
    sa.add_argument("--questao")
    sa.add_argument("--errei")
    sa.add_argument("--correta")

    sr = sub.add_parser("revisar")
    sr.add_argument("caderno")
    sr.add_argument("--id", required=True)
    sr.add_argument("--resultado", required=True, choices=["acertou", "errou"])

    args = p.parse_args()
    if args.cmd == "due":
        cmd_due(args.caderno)
    elif args.cmd == "list":
        cmd_list(args.caderno)
    elif args.cmd == "stats":
        cmd_stats(args.caderno)
    elif args.cmd == "add":
        cmd_add(args.caderno, args)
    elif args.cmd == "revisar":
        cmd_revisar(args.caderno, args)


if __name__ == "__main__":
    main()
