#!/usr/bin/env python3
"""
Lista todos os notebooks da conta NotebookLM (incluindo dentro de coleções).
Uso: python scripts/run.py list_account_notebooks.py
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from patchright.sync_api import sync_playwright
from browser_utils import BrowserFactory
from auth_manager import AuthManager

HOME = "https://notebooklm.google.com"

COLLECT_JS = """
() => {
  const out = { anchors: [], cards: [] };
  document.querySelectorAll('a[href]').forEach(a => {
    out.anchors.push({ href: a.getAttribute('href'), text: (a.innerText || '').trim().slice(0, 120) });
  });
  document.querySelectorAll('project-button, mat-card').forEach((el, i) => {
    const t = (el.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 150);
    if (t) out.cards.push({ index: i, text: t });
  });
  return out;
}
"""


def get_anchors_notebooks(page):
    data = page.evaluate(COLLECT_JS)
    nbs = {}
    for a in data["anchors"]:
        href = a["href"] or ""
        if "/notebook/" in href:
            url = href if href.startswith("http") else HOME + href
            nbs[url] = a["text"] or "(sem título)"
    return nbs, data["cards"]


def collection_titles(page):
    """Títulos das coleções na home (cards com 'N notebooks')."""
    _, cards = get_anchors_notebooks(page)
    cols = []
    for c in cards:
        m = re.search(r"category\s+(.+?)\s+(?:.*?)?(\d+)\s+notebooks?", c["text"])
        if m:
            # remove emojis/avatares do fim do título
            title = m.group(1).strip()
            cols.append({"title": title, "count": int(m.group(2)), "raw": c["text"]})
    return cols


def dismiss_overlays(page):
    """Fecha modais/anúncios que interceptam cliques (ex.: dialog de rebrand)."""
    try:
        page.evaluate("""
        () => {
          const overlay = document.querySelector('.cdk-overlay-container');
          if (!overlay) return 'sem overlay';
          const btns = overlay.querySelectorAll('button');
          if (btns.length) { btns[btns.length - 1].click(); return 'botao clicado'; }
          overlay.innerHTML = '';
          return 'overlay removido';
        }
        """)
        time.sleep(1)
        page.keyboard.press("Escape")
        time.sleep(1)
        # Garantia final: esvazia o container de overlay
        page.evaluate("""
        () => { const o = document.querySelector('.cdk-overlay-container'); if (o) o.innerHTML = ''; }
        """)
    except Exception:
        pass


def open_home(page):
    page.goto(HOME, wait_until="domcontentloaded", timeout=30000)
    time.sleep(6)
    dismiss_overlays(page)


def click_card_by_text(page, text_fragment):
    """Clica no card (mat-card/project-button) cujo texto contém o fragmento."""
    loc = page.locator("mat-card, project-button").filter(has_text=text_fragment)
    if loc.count() == 0:
        return False
    loc.first.click()
    time.sleep(5)
    return True


def harvest_collection(page, col_title):
    """Dentro da vista de uma coleção, captura (titulo, url) de cada notebook."""
    found = {}
    nbs, cards = get_anchors_notebooks(page)
    if nbs:
        return nbs, cards

    # Sem anchors: clicar em cada card de notebook e capturar a URL
    skip_words = ("Criar", "notebooks", "Create")
    nb_cards = [c for c in cards if not any(w in c["text"] for w in skip_words)]
    for i in range(len(nb_cards)):
        # A cada iteração a página foi recarregada; re-localiza os cards
        loc = page.locator("mat-card, project-button")
        count = loc.count()
        # Reconstrói a lista filtrada na página atual
        current = []
        for j in range(count):
            t = loc.nth(j).inner_text().strip().replace("\n", " ")
            if t and not any(w in t for w in skip_words):
                current.append((j, t))
        if i >= len(current):
            break
        j, title_raw = current[i]
        try:
            loc.nth(j).click()
            page.wait_for_url(re.compile(r"/notebook/"), timeout=15000)
            time.sleep(2)
            url = page.url
            # Título real da página, se disponível
            title = title_raw.split("more_vert")[-1].strip() or title_raw
            found[url] = title
        except Exception as e:
            print(f"AVISO: falha no card {i} da coleção {col_title}: {e}")
        # Volta para a coleção
        page.go_back()
        time.sleep(4)
    return found, cards


def main():
    auth = AuthManager()
    if not auth.is_authenticated():
        print("NAO AUTENTICADO. Rode: python scripts/run.py auth_manager.py setup")
        sys.exit(1)

    playwright = sync_playwright().start()
    context = None
    try:
        context = BrowserFactory.launch_persistent_context(playwright, headless=True)
        page = context.new_page()
        open_home(page)
        if "accounts.google.com" in page.url:
            print("SESSAO EXPIRADA. Rode: python scripts/run.py auth_manager.py reauth")
            sys.exit(1)

        cols = collection_titles(page)
        print(f"Coleções na home: {[(c['title'], c['count']) for c in cols]}")

        result = {"collections": []}
        loose, _ = get_anchors_notebooks(page)
        if loose:
            result["sem_colecao"] = [{"title": t, "url": u} for u, t in loose.items()]

        for col in cols:
            open_home(page)
            if not click_card_by_text(page, col["title"]):
                print(f"AVISO: não achei o card da coleção {col['title']}")
                continue
            nbs, raw_cards = harvest_collection(page, col["title"])
            result["collections"].append({
                "title": col["title"],
                "expected": col["count"],
                "notebooks": [{"title": t, "url": u} for u, t in nbs.items()],
                "raw_cards": [c["text"] for c in raw_cards],
            })

        print("===JSON===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        if context:
            context.close()
        playwright.stop()


if __name__ == "__main__":
    main()
