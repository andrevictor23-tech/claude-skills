# -*- coding: utf-8 -*-
"""Extrai questoes de PDFs de simulado (enunciado + espelho) para JSON.

Best-effort: o agente DEVE validar o resultado (contagem, amostras, gabaritos null).
Nunca le o PDF como imagem — usa pdftotext (poppler).
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

Q_SPLIT = re.compile(r"(?:QUEST[AÃ]O|Quest[aã]o)\s+(\d{1,3})\b")
ALT_RE = re.compile(r"^\s*\(?([a-eA-E])[\)\.]\s+(.*)")
GAB_RE = re.compile(r"(?:Gabarito|Resposta(?:\s+correta)?|Alternativa\s+correta)\s*[:\-]\s*(?:letra\s*)?[\"'“]?\(?([a-eA-E])\)?(?![\wçã])", re.IGNORECASE)


def pdf_to_text(pdf: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        out = Path(tmp.name)
    subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), str(out)], check=True)
    text = out.read_text(encoding="utf-8", errors="replace")
    out.unlink(missing_ok=True)
    return text


def split_questions(text: str) -> dict:
    """Divide o texto em blocos por numero de questao."""
    parts = Q_SPLIT.split(text)
    blocks = {}
    # parts = [preambulo, num1, corpo1, num2, corpo2, ...]
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        body = parts[i + 1]
        # Mantem o primeiro bloco de cada numero (evita sumarios/indices repetirem)
        if num not in blocks or len(body) > len(blocks[num]):
            blocks[num] = body
    return blocks


def parse_enunciado_block(body: str) -> dict:
    lines = body.splitlines()
    stem_lines, alts, current = [], {}, None
    for ln in lines:
        m = ALT_RE.match(ln)
        if m:
            current = m.group(1).upper()
            alts[current] = m.group(2).strip()
        elif current is not None:
            extra = ln.strip()
            if extra:
                alts[current] += " " + extra
        else:
            stem_lines.append(ln.rstrip())
    stem = re.sub(r"\n{3,}", "\n\n", "\n".join(stem_lines)).strip()
    return {"enunciado": stem, "alternativas": alts}


def parse_espelho_block(body: str) -> dict:
    gab = None
    m = GAB_RE.search(body)
    if m:
        gab = m.group(1).upper()
    else:
        # fallback: "correta e a alternativa 'c'" — exige a letra entre aspas ou parenteses
        m = re.search(r"alternativa\s+[\"'“(]([a-eA-E])[\"'”)]", body, re.IGNORECASE)
        if m:
            gab = m.group(1).upper()
    comentario = body.strip()
    if len(comentario) > 6000:
        comentario = comentario[:6000] + " [...]"
    return {"gabarito": gab, "comentario": comentario}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enunciado", required=True)
    ap.add_argument("--espelho", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--id", help="id do simulado, ex.: simulado-01 (default: nome do arquivo out)")
    args = ap.parse_args()

    enun_text = pdf_to_text(Path(args.enunciado))
    esp_text = pdf_to_text(Path(args.espelho))

    enun_blocks = split_questions(enun_text)
    esp_blocks = split_questions(esp_text)

    sim_id = args.id or Path(args.out).stem
    questions = []
    for num in sorted(enun_blocks):
        q = {"numero": num, "materia": None}
        q.update(parse_enunciado_block(enun_blocks[num]))
        q.update(parse_espelho_block(esp_blocks.get(num, "")) if num in esp_blocks
                 else {"gabarito": None, "comentario": ""})
        questions.append(q)

    data = {"id": sim_id, "fonte_enunciado": args.enunciado,
            "fonte_espelho": args.espelho, "questoes": questions}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    sem_gab = [q["numero"] for q in questions if not q["gabarito"]]
    poucas_alts = [q["numero"] for q in questions if len(q["alternativas"]) < 4]
    print(f"OK: {len(questions)} questoes extraidas -> {out}")
    print(f"Sem gabarito ({len(sem_gab)}): {sem_gab[:20]}")
    print(f"Com menos de 4 alternativas ({len(poucas_alts)}): {poucas_alts[:20]}")
    print("VALIDE amostras antes de gerar o quiz. Campo 'materia' pode ser preenchido depois.")


if __name__ == "__main__":
    sys.exit(main())
