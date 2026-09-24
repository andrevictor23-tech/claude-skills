"""Registra no ~/.claude/settings.json o hook PreToolUse que recusa as copias
antigas de skills sincronizadas do claude.ai (ver bloquear-skills-antigas.sh).

Chamado pelo sync.ps1 no sync manual. Idempotente: se o settings.json ja cita o
script, nao toca no arquivo. JSON invalido aborta sem escrever nada.
"""
import json
import sys
from pathlib import Path

MARCA = "bloquear-skills-antigas.sh"
COMANDO = 'bash "$HOME/.claude/skills/sync-skills/scripts/bloquear-skills-antigas.sh"'


def registrar(caminho: Path) -> str:
    texto = caminho.read_text(encoding="utf-8") if caminho.exists() else "{}"
    if MARCA in texto:
        return "ja registrado"
    cfg = json.loads(texto)
    cfg.setdefault("hooks", {}).setdefault("PreToolUse", []).append({
        "matcher": "Skill",
        "hooks": [{"type": "command", "command": COMANDO, "timeout": 10}],
    })
    caminho.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return "registrado"


if __name__ == "__main__":
    padrao = Path.home() / ".claude" / "settings.json"
    print(registrar(Path(sys.argv[1]) if len(sys.argv) > 1 else padrao))
