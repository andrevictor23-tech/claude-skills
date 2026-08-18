#!/usr/bin/env python3
"""
Descoberta em lote: pergunta a cada notebook qual é seu conteúdo usando o
fluxo testado de ask_question.ask_notebooklm, salvando resultados
incrementalmente em JSON.
Uso: python scripts/run.py batch_discover.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ask_question import ask_notebooklm, FOLLOW_UP_REMINDER
from auth_manager import AuthManager
from config import DATA_DIR

OUT_FILE = DATA_DIR / "batch_discover_results.json"

QUESTION = (
    "Qual é o conteúdo deste notebook? Quais temas e tipos de fonte são abordados? "
    "Responda de forma breve e concisa, em no máximo 5 frases, e ao final liste "
    "de 5 a 8 palavras-chave separadas por vírgula."
)

NOTEBOOKS = [
    # ESTUDO
    {"collection": "ESTUDO", "title": "Normas das Serventias Extrajudiciais de Mato Grosso", "url": "https://notebooklm.google.com/notebook/d29459f4-531e-441b-a2b3-3bdeee0fa4c2"},
    {"collection": "ESTUDO", "title": "Compêndio de Direito Civil: Pessoas, Bens e Fatos Jurídicos", "url": "https://notebooklm.google.com/notebook/d076253f-f354-4ff9-8886-6c1dd499d68e"},
    {"collection": "ESTUDO", "title": "Lei das Garantias e Atualizações sobre Alienação Fiduciária e Hipoteca", "url": "https://notebooklm.google.com/notebook/66fb8143-b544-443a-842b-1a8b86106490"},
    {"collection": "ESTUDO", "title": "Constitucional + Humanos", "url": "https://notebooklm.google.com/notebook/3780051c-d71c-42d7-9e89-78dec0ea9d03"},
    {"collection": "ESTUDO", "title": "Direito Eleitoral", "url": "https://notebooklm.google.com/notebook/1d639a35-9135-49e2-a1ee-c56a857b5158"},
    {"collection": "ESTUDO", "title": "Direito Empresarial: Questões Discursivas e Jurisprudência do STJ", "url": "https://notebooklm.google.com/notebook/a67b0448-ee25-409e-820b-e98ccd6f49f0"},
    {"collection": "ESTUDO", "title": "VadeTeoria: Direito da Infância e Juventude para o MPDFT", "url": "https://notebooklm.google.com/notebook/4168a4cf-6a92-4cee-b849-abaa5ca112af"},
    {"collection": "ESTUDO", "title": "Administrativo", "url": "https://notebooklm.google.com/notebook/9ed99b8c-3d7a-41e0-8107-4b7a89c4ddfb"},
    # PROGRAMAÇÃO & IA
    {"collection": "PROGRAMACAO-IA", "title": "Guia de Configuração: Claude Code, OpenRouter e Evey-Setup", "url": "https://notebooklm.google.com/notebook/5547a9e3-399e-4479-ac44-c2ca8ca1f96d"},
    {"collection": "PROGRAMACAO-IA", "title": "Claude Code + NotebookLM = HACK DESBLOQUEADO", "url": "https://notebooklm.google.com/notebook/d70d92ba-a7a0-4b9f-86a4-4a5f69de5f16"},
    {"collection": "PROGRAMACAO-IA", "title": "Programação", "url": "https://notebooklm.google.com/notebook/1f56a94f-fb6a-4594-b701-b744b1fcaca6"},
]


def save(results):
    OUT_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    auth = AuthManager()
    if not auth.is_authenticated():
        print("NAO AUTENTICADO")
        sys.exit(1)

    results = []
    for i, nb in enumerate(NOTEBOOKS):
        entry = dict(nb)
        try:
            answer = ask_notebooklm(QUESTION, nb["url"], headless=True)
            if answer:
                entry["status"] = "success"
                entry["answer"] = answer.replace(FOLLOW_UP_REMINDER, "").strip()
            else:
                entry["status"] = "error"
                entry["answer"] = "sem resposta (timeout ou falha)"
        except Exception as e:
            entry["status"] = "error"
            entry["answer"] = str(e)
        results.append(entry)
        save(results)
        print(f"[{i+1}/{len(NOTEBOOKS)}] {nb['title']}: {entry['status']}")
        time.sleep(3)

    print(f"OK — resultados em {OUT_FILE}")


if __name__ == "__main__":
    main()
