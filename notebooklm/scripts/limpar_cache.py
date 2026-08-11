#!/usr/bin/env python3
"""Limpa o cache do perfil de browser da skill, preservando a sessao autenticada.

O perfil do Chromium em data/browser_state/browser_profile/ acumula centenas de
MB de cache regeneravel (codigo compilado, modelos on-device, shaders). Nada
disso e necessario para manter o login: a sessao vive nos cookies, no Local
Storage e no state.json, que este script nunca toca.

Uso:
    python limpar_cache.py            # mostra o que seria removido, sem apagar
    python limpar_cache.py --aplicar  # remove de fato

Rode com o browser da skill FECHADO. Se algum arquivo estiver em uso, ele e
pulado com aviso e o resto segue.
"""

import argparse
import shutil
import sys
from pathlib import Path

# Caches regeneraveis, relativos a browser_profile/. O Chromium recria cada um
# na proxima execucao; o custo e um primeiro carregamento mais lento.
DESCARTAVEIS = [
    "Default/Code Cache",
    "Default/Cache",
    "Default/GPUCache",
    "Default/DawnWebGPUCache",
    "Default/DawnGraphiteCache",
    "optimization_guide_model_store",
    "component_crx_cache",
    "WasmTtsEngine",
    "OnDeviceHeadSuggestModel",
    "GrShaderCache",
    "ShaderCache",
]

# Caminhos que sustentam o login. Verificados antes e depois; se algum sumir,
# o script falha em voz alta em vez de deixar a skill silenciosamente deslogada.
CREDENCIAIS = [
    "browser_state/state.json",
    "browser_state/browser_profile/Default/Network/Cookies",
    "browser_state/browser_profile/Default/Local Storage",
    "browser_state/browser_profile/Default/Login Data",
]


def tamanho(caminho: Path) -> int:
    if caminho.is_file():
        return caminho.stat().st_size
    return sum(f.stat().st_size for f in caminho.rglob("*") if f.is_file())


def mb(n: int) -> str:
    return f"{n / 1024 / 1024:.1f} MB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aplicar", action="store_true",
                    help="remove de fato (sem esta flag, so mostra o que faria)")
    ap.add_argument("--data-dir", type=Path,
                    help="pasta data/ da skill (padrao: ../data ao lado deste script)")
    args = ap.parse_args()

    data = args.data_dir or (Path(__file__).resolve().parent.parent / "data")
    if not data.is_dir():
        print(f"ERRO: pasta de dados nao encontrada: {data}", file=sys.stderr)
        return 1

    perfil = data / "browser_state" / "browser_profile"
    if not perfil.is_dir():
        print(f"Nada a fazer: perfil de browser inexistente em {perfil}")
        return 0

    presentes_antes = [c for c in CREDENCIAIS if (data / c).exists()]
    if not presentes_antes:
        print("AVISO: nenhum arquivo de sessao encontrado — a skill provavelmente\n"
              "nao esta autenticada. A limpeza segue, mas confira o login depois.")

    antes = tamanho(perfil)
    alvos = [(rel, perfil / rel) for rel in DESCARTAVEIS if (perfil / rel).exists()]

    if not alvos:
        print(f"Nada a limpar. Perfil ja esta em {mb(antes)}.")
        return 0

    liberado = 0
    for rel, caminho in alvos:
        tam = tamanho(caminho)
        liberado += tam
        if args.aplicar:
            try:
                shutil.rmtree(caminho)
                print(f"  removido  {rel:<40} {mb(tam):>10}")
            except OSError as e:
                liberado -= tam
                print(f"  PULADO    {rel:<40} (em uso? {e.strerror})")
        else:
            print(f"  removeria {rel:<40} {mb(tam):>10}")

    print()
    if not args.aplicar:
        print(f"Perfil: {mb(antes)} -> ficaria em {mb(antes - liberado)} "
              f"(liberaria {mb(liberado)}).")
        print("Rode de novo com --aplicar para remover.")
        return 0

    # A sessao tem de sobreviver; se nao sobreviveu, isso e um erro, nao um aviso.
    perdidas = [c for c in presentes_antes if not (data / c).exists()]
    if perdidas:
        print("ERRO: arquivos de sessao desapareceram na limpeza:", file=sys.stderr)
        for c in perdidas:
            print(f"  - {c}", file=sys.stderr)
        return 1

    print(f"Perfil: {mb(antes)} -> {mb(tamanho(perfil))} (liberado {mb(liberado)}).")
    if presentes_antes:
        print(f"Sessao preservada ({len(presentes_antes)} arquivos de credencial intactos).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
