#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_hub.py – Generiert dino_hub.html aus dem Ordner Schule/.

Scannt alle *.html unter Schule/, liest die Metatags direkt aus den Seiten,
und baut die Übersichtsseite (Kacheln, Klassen, Suche, Tooltips) neu auf.

Aufruf:
    python build_hub.py                # nutzt ./Schule und schreibt ./Schule/dino_hub.html
    python build_hub.py --root PFAD --out DATEI

Konventionen (Pfad 3 – Politur lebt in den Metatags):
- Einsortierung (Fach/Klasse/Thema/Kachel) kommt aus dem PFAD.
- Icon kommt aus <meta name="typ">, sonst neutral 📄.
- Link-Titel kommt aus <title> der Seite (Fallback: Dateiname).
- Tooltip-Text: <meta name="description">, Fallback <title>.
- Suche: title + description + keywords.
- Kachel = letzter Ordner. Kachelname aus Ordnername (übersteuerbar per
  <meta name="kachel">). Emoji aus Lookup, Fallback 📂.
"""

import os, re, sys, json, argparse, html
from datetime import date
from collections import defaultdict, OrderedDict

# ──────────────────────────────────────────────────────────────────────────────
#  Konfiguration
# ──────────────────────────────────────────────────────────────────────────────

ALT_ORDNER = {"uebungen", "lernseiten", "tests"}
FACH_MAIN  = {"mathe", "bio", "kompass"}

# typ (Metatag) → (Icon, Badge-Klasse, Badge-Emoji)
TYP_ICON = {
    "Lernseite": ("📖", "ls",    "📖"),
    "Übung":     ("✏️", "ue",    "✏️"),
    "Test":      ("🔍", "test",  "🔍"),
    "Bonus":     ("⭐", "bonus", "⭐"),
    "Lehrer":    ("👨‍🏫", "lehrer", "👨‍🏫"),
}
ICON_NEUTRAL = "📄"

# Emoji-Lookup für Themen (oberthema / Ordnername, lower, ohne Umlaute-Sonderfälle)
THEMA_EMOJI = {
    "rechnen": "🔢", "geometrie": "📐", "brueche": "➗", "brueche_rechnen": "➗",
    "muster": "🔵", "muster_figuren": "🔵", "rationale_zahlen": "🔢",
    "zuordnungen": "📈", "prozent": "💯", "prozent_zinsen": "💯",
    "terme_gleichungen": "🔤", "konstruieren": "📐", "wahrscheinlichkeit": "🎲",
    "lineare_funktionen": "📈", "terme_mehrere_variablen": "🔤",
    "flaechen": "⬛", "flaecheninhalt": "⬛", "lgs": "⚖️", "lineare_gls": "⚖️",
    "kreise_dreiecke": "⭕", "quadratische_gleichungen": "🧮",
    "analysis": "📈", "funktionen": "🔄", "potenzfunktionen": "📈",
    "transformationen": "🔀", "ganzrationale_funktionen": "📉",
    "geogebra": "🖥️", "lineare_algebra": "📐", "vektorrechnung": "📐",
    "herz": "❤️", "herz_kreislauf": "❤️", "sexualerziehung": "🌱",
    "blutzucker": "🍬", "blutzucker_hormone": "🍬", "hormone": "🍬",
    "immunsystem": "🦠", "fortpflanzung": "👶",
    "koerper": "📦", "grundlagen": "📐", "sachaufgaben": "📝",
    "teilbarkeit_primzahlen": "🔍", "rechengesetze": "⚙️",
    "differentialrechnung": "📉", "cybergrooming": "🛡️",
}
# Kachel-Emoji-Fallback (letzter Ordner) – nutzt dieselbe Tabelle, sonst 📂
KACHEL_EMOJI_FALLBACK = "📂"

FACH_LABEL = {"mathe": "📐 Mathematik", "bio": "🧬 Biologie",
              "kompass": "🧭 Kompass", "sonst": "📁 Sonstiges"}
FACH_ICON  = {"mathe": "📐", "bio": "🧬", "kompass": "🧭", "sonst": "📁"}

# ──────────────────────────────────────────────────────────────────────────────
#  Metatags aus einer HTML-Datei lesen
# ──────────────────────────────────────────────────────────────────────────────

def read_meta(fp):
    try:
        with open(fp, encoding="utf-8") as f:
            h = f.read(8192)  # Kopf reicht
    except Exception:
        try:
            with open(fp, encoding="cp1252") as f:
                h = f.read(8192)
        except Exception:
            h = ""
    def m(name):
        for pat in (
            r'<meta\s+name\s*=\s*["\']' + re.escape(name) + r'["\'][^>]*?content\s*=\s*["\']([^"\']*)["\']',
            r'<meta\s+content\s*=\s*["\']([^"\']*)["\'][^>]*?name\s*=\s*["\']' + re.escape(name) + r'["\']',
        ):
            mm = re.search(pat, h, re.I)
            if mm:
                return html.unescape(mm.group(1).strip())
        return ""
    tm = re.search(r"<title[^>]*>(.*?)</title>", h, re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", tm.group(1)).strip()) if tm else ""
    return {
        "title": title,
        "description": m("description"),
        "keywords": m("keywords"),
        "typ": m("typ"),
        "klasse": m("klasse"),
        "fach": m("fach"),
        "oberthema": m("oberthema"),
        "thema": m("thema"),
        "kachel": m("kachel"),
    }

# ──────────────────────────────────────────────────────────────────────────────
#  Pfad-Analyse
# ──────────────────────────────────────────────────────────────────────────────

def parse_path(rel):
    parts = rel.split("/")
    fach = parts[0]
    main = fach if fach in FACH_MAIN else "sonst"
    kl = ""
    for seg in parts:
        mm = re.match(r"klasse(\d{2}|EF)$", seg)
        if mm:
            kl = mm.group(1)
            kl = "EF" if kl == "EF" else str(int(kl))
            break
    alt = any(seg in ALT_ORDNER for seg in parts)
    kachel_dir = parts[-2] if len(parts) >= 2 else fach
    # thema = Segment direkt nach klasseNN (neue Struktur), sonst kachel_dir
    thema_seg = ""
    for i, seg in enumerate(parts):
        if re.match(r"klasse(\d{2}|EF)$", seg) and i + 1 < len(parts) - 1:
            thema_seg = parts[i + 1]
            break
    return main, fach, kl, alt, kachel_dir, thema_seg

def prettify(name):
    name = name.replace("_", " ").replace("-", " ").strip()
    # Klassenarbeit IV etc. beibehalten, sonst Titel-Case für erstes Wort
    if not name:
        return name
    return name[0].upper() + name[1:]

def thema_emoji(key):
    return THEMA_EMOJI.get(key.lower(), None)

# ──────────────────────────────────────────────────────────────────────────────
#  Icons / Link-Titel
# ──────────────────────────────────────────────────────────────────────────────

def link_icon(typ):
    return TYP_ICON.get(typ, (ICON_NEUTRAL, "", ICON_NEUTRAL))[0]

def link_title(info, fname):
    if info.get("title"):
        return info["title"]
    # Fallback: Dateiname ohne Suffix, hübsch
    base = re.sub(r"\.html$", "", fname)
    base = re.sub(r"_(ls|ue|test|bonus)\d*$", "", base)
    return prettify(base)

def esc(s):
    return html.escape(s, quote=True)

# ──────────────────────────────────────────────────────────────────────────────
#  Kachel bauen
# ──────────────────────────────────────────────────────────────────────────────

def build_kachel(kachel_dir, files, metas):
    """files: Liste (rel, fname); metas: dict rel->info"""
    # Kachelname: <meta kachel> (erste gesetzte gewinnt) sonst Ordnername
    kachel_meta = ""
    for rel, _ in files:
        if metas[rel].get("kachel"):
            kachel_meta = metas[rel]["kachel"]; break
    if kachel_meta:
        name = kachel_meta
    else:
        em = thema_emoji(kachel_dir) or KACHEL_EMOJI_FALLBACK
        name = f"{em} {prettify(kachel_dir)}"

    # Badges zählen
    cnt = defaultdict(int)
    for rel, _ in files:
        typ = metas[rel].get("typ", "")
        if typ in TYP_ICON:
            cnt[typ] += 1
        else:
            cnt["_neutral"] += 1
    badge_parts = []
    for typ, (_, cls, em) in TYP_ICON.items():
        if cnt.get(typ):
            badge_parts.append(f'<span class="kbadge {cls}">{em} {cnt[typ]}</span>')
    if cnt.get("_neutral"):
        badge_parts.append(f'<span class="kbadge">{ICON_NEUTRAL} {cnt["_neutral"]}</span>')
    badges = "".join(badge_parts)

    # Links (ls-Einträge zuerst grob, damit Pairing im JS greift)
    def sortkey(item):
        rel, fname = item
        typ = metas[rel].get("typ", "")
        order = {"Lernseite": 0, "Übung": 1, "Test": 2, "Bonus": 3}.get(typ, 4)
        return (order, fname)
    links = []
    for rel, fname in sorted(files, key=sortkey):
        info = metas[rel]
        typ = info.get("typ", "")
        icon = link_icon(typ)
        title = link_title(info, fname)
        cls = ' class="lehrer-link"' if typ == "Lehrer" else ""
        label = title if typ == "Lehrer" else f"{icon} {title}"
        links.append(
            f'                <a href="{esc(rel)}"{cls} target="_blank" rel="noopener">{esc(label)}</a>'
        )
    links_html = "\n".join(links)
    return (
        '            <div class="kachel" onclick="toggleKachel(this, event)">\n'
        f'              <div class="kachel-name">{esc(name)}</div>\n'
        f'              <div class="kachel-badges">{badges}</div>\n'
        '              <div class="kachel-links" style="display:none">\n'
        f'{links_html}\n'
        '              </div>\n'
        '            </div>'
    )

# ──────────────────────────────────────────────────────────────────────────────
#  Hauptaufbau
# ──────────────────────────────────────────────────────────────────────────────

def klasse_sortkey(k):
    if k == "EF":
        return 99
    try:
        return int(k)
    except ValueError:
        return 100

def build(root, out):
    root = os.path.abspath(root)
    files = []
    for dirpath, _, fnames in os.walk(root):
        for fn in fnames:
            if not fn.lower().endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if rel.lower() == "dino_hub.html":
                continue
            if fn.lower().startswith("xxx"):
                continue
            files.append((rel, fn, full))

    metas = {}
    for rel, fn, full in files:
        metas[rel] = read_meta(full)

    # Gruppieren: fach -> klasse -> thema -> kachel_dir -> [(rel,fn)]
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    alt_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # fach->klasse->ordner(lernseiten/uebungen/tests)->[..]
    sonst = defaultdict(list)  # kachel_dir -> [(rel,fn)]
    search_index = OrderedDict()   # rel -> {...}
    tooltip_index = OrderedDict()  # fname -> {typ,desc}

    for rel, fn, full in files:
        main, fach, kl, alt, kdir, thema = parse_path(rel)
        info = metas[rel]
        # Such-/Tooltip-Index
        typ = info.get("typ") or ""
        desc = info.get("description") or info.get("title") or ""
        search_index[rel] = {
            "title": link_title(info, fn),
            "desc": desc,
            "kw": info.get("keywords", ""),
            "typ": typ,
            "kl": kl,
            "fach": main if main in FACH_MAIN else "",
        }
        tooltip_index[fn] = {"typ": typ or "Datei", "desc": desc}

        if main == "sonst":
            sonst[kdir].append((rel, fn))
        elif alt:
            # ordner = welches der drei
            ordner = next((s for s in rel.split("/") if s in ALT_ORDNER), "lernseiten")
            alt_tree[fach][kl][ordner].append((rel, fn))
        else:
            tree[main][kl][thema or kdir][kdir].append((rel, fn))

    # ── HTML zusammensetzen ──
    tpl_head = TPL_HEAD
    # Datum aktualisieren
    heute = date.today().strftime("%d.%m.%Y")
    tpl_head = re.sub(r'(<span class="ts">aktualisiert )\d{2}\.\d{2}\.\d{4}(</span>)',
                      rf'\g<1>{heute}\g<2>', tpl_head)

    cards = []
    fach_order = ["mathe", "bio", "kompass", "sonst"]
    for fach in fach_order:
        if fach == "sonst":
            if not sonst:
                continue
            cards.append(build_sonst_card(sonst, metas))
            continue
        if fach not in tree and fach not in alt_tree:
            continue
        cards.append(build_fach_card(fach, tree.get(fach, {}), alt_tree.get(fach, {}), metas))

    card_area = '<div class="card-area" id="cardArea">\n\n' + "\n\n".join(cards) + "\n\n</div>"

    # JS-Objekte
    mi_lines = []
    for fn, v in tooltip_index.items():
        mi_lines.append(f"  {json.dumps(fn, ensure_ascii=False)}: {{typ:{json.dumps(v['typ'],ensure_ascii=False)},desc:{json.dumps(v['desc'],ensure_ascii=False)}}},")
    meta_info_js = "const META_INFO = {\n" + "\n".join(mi_lines) + "\n};"

    m2_lines = []
    for rel, v in search_index.items():
        m2_lines.append(
            f"  {json.dumps(rel,ensure_ascii=False)}:{{title:{json.dumps(v['title'],ensure_ascii=False)},"
            f"desc:{json.dumps(v['desc'],ensure_ascii=False)},kw:{json.dumps(v['kw'],ensure_ascii=False)},"
            f"typ:{json.dumps(v['typ'],ensure_ascii=False)},kl:{json.dumps(v['kl'],ensure_ascii=False)},"
            f"fach:{json.dumps(v['fach'],ensure_ascii=False)}}},"
        )
    meta_js = "const META = {\n" + "\n".join(m2_lines) + "\n};"

    js_head = TPL_JS_HEAD
    js_mid  = TPL_JS_MID
    js_tail = TPL_JS_TAIL

    full_html = (
        tpl_head + "\n" + card_area + "\n\n" +
        js_head + meta_info_js + js_mid + meta_js + js_tail
    )

    with open(out, "w", encoding="utf-8") as f:
        f.write(full_html)

    return len(files), out


def build_fach_card(fach, klassen, alt_klassen, metas):
    label = FACH_LABEL[fach].split(" ", 1)[1]
    icon = FACH_ICON[fach]
    parts = [
        f'<div class="card" data-fach="{fach}" id="card-{fach}">',
        '  <div class="card-header">',
        f'    <span class="card-icon">{icon}</span>',
        f'    <span class="card-title">{label}</span>',
        '  </div>',
    ]
    for kl in sorted(klassen.keys(), key=klasse_sortkey):
        themen = klassen[kl]
        n_files = sum(len(kd) for th in themen.values() for kd in th.values())
        klabel = "EF" if kl == "EF" else f"Klasse {kl}"
        parts.append('  <div class="klasse-wrap">')
        parts.append(f'    <button class="klasse-btn" aria-expanded="false" onclick="toggleKlasse(this)">')
        parts.append(f'      <span class="klasse-label">📚 {klabel}</span><span class="klasse-count">{n_files}</span><span class="klasse-arrow">▼</span>')
        parts.append('    </button>')
        parts.append('    <div class="klasse-panel">')
        parts.append('      <div class="themen-bereich">')
        for thema in themen:
            em = thema_emoji(thema) or KACHEL_EMOJI_FALLBACK
            parts.append('        <div class="thema-block">')
            parts.append(f'          <div class="thema-header"><span class="thema-icon">{em}</span><span class="thema-title">{esc(prettify(thema))}</span></div>')
            parts.append('          <div class="kachel-grid">')
            for kdir, flist in themen[thema].items():
                parts.append(build_kachel(kdir, flist, metas))
            parts.append('          </div>')
            parts.append('        </div>')
        parts.append('      </div>')
        parts.append('    </div>')
        parts.append('  </div>')

    # Alte Struktur
    if alt_klassen:
        parts.append('  <div class="alt-wrap">')
        parts.append('    <button class="alt-btn" aria-expanded="false" onclick="toggleAlt(this)">')
        parts.append('      <span style="flex:1">📁 Alte Struktur – Migration ausstehend</span><span class="alt-arrow">▼</span>')
        parts.append('    </button>')
        parts.append('    <div class="alt-panel">')
        COL = {"lernseiten": ("lernen", "📖 Lernseiten"),
               "uebungen": ("uebung", "✏️ Übungen"),
               "tests": ("test", "🔍 Tests")}
        for kl in sorted(alt_klassen.keys(), key=klasse_sortkey):
            ordner = alt_klassen[kl]
            n = sum(len(v) for v in ordner.values())
            klabel = "EF" if kl == "EF" else f"Klasse {kl}"
            parts.append('      <div class="jgst">')
            parts.append('        <button class="jgst-toggle" aria-expanded="false" onclick="toggleJgst(this)">')
            parts.append(f'          <span class="jgst-label">{klabel} – alt</span><span class="jgst-count">{n}</span><span class="jgst-arrow">▼</span>')
            parts.append('        </button>')
            parts.append('        <div class="jgst-panel">')
            ncols = len(ordner)
            parts.append(f'          <div class="col-grid c{max(1,ncols)}">')
            for okey in ("lernseiten", "uebungen", "tests"):
                if okey not in ordner:
                    continue
                cls, head = COL[okey]
                parts.append(f'            <div class="col-group"><div class="col-head {cls}">{head}</div><div class="links">')
                for rel, fn in sorted(ordner[okey], key=lambda x: x[1]):
                    title = link_title(metas[rel], fn)
                    parts.append(f'              <a class="link-row" href="{esc(rel)}" target="_blank" rel="noopener"><span class="link-icon">📄</span><span class="link-name">{esc(title)}</span></a>')
                parts.append('            </div></div>')
            parts.append('          </div>')
            parts.append('        </div>')
            parts.append('      </div>')
        parts.append('    </div>')
        parts.append('  </div>')

    parts.append('</div>')
    return "\n".join(parts)


def build_sonst_card(sonst, metas):
    parts = [
        '<div class="card" data-fach="sonst" id="card-sonst">',
        '  <div class="card-header">',
        '    <span class="card-icon">📁</span>',
        '    <span class="card-title">Sonstiges</span>',
        '  </div>',
        '  <div class="themen-bereich">',
        '    <div class="thema-block">',
        '      <div class="kachel-grid">',
    ]
    for kdir, flist in sonst.items():
        parts.append(build_kachel(kdir, flist, metas))
    parts.append('      </div>')
    parts.append('    </div>')
    parts.append('  </div>')
    parts.append('</div>')
    return "\n".join(parts)


TPL_HEAD = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦖 Mathedino Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:#f0f2f8;--surface:#fff;--border:#d4daf0;--bl:#e8ecf8;
    --mathe:#1d4ed8;--ml:#eff6ff;--bio:#15803d;--biol:#f0fdf4;
    --kompass:#be185d;--kl:#fdf2f8;--sonst:#475569;--sl:#f8fafc;
    --text:#0f172a;--muted:#64748b;
    --shadow:0 4px 12px rgba(15,23,42,.10),0 12px 40px rgba(15,23,42,.08);
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:'Source Sans 3',sans-serif;font-weight:400;min-height:100vh;padding:0 0 6rem;overflow-x:hidden}

  /* topbar */
  .topbar{background:#0f1f0f;padding:1rem 1.5rem .9rem;position:sticky;top:0;z-index:50;box-shadow:0 2px 12px rgba(15,23,42,.4);border-bottom:3px solid #22c55e}
  .topbar-inner{max-width:960px;margin:0 auto}
  .topbar h1{font-family:'Playfair Display',serif;font-size:1rem;color:#e2e8f0;margin-bottom:.7rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
  .topbar h1 .ts{margin-left:auto;font-size:.7rem;opacity:.5;font-family:'Source Sans 3',sans-serif;font-weight:400}
  .lehrer-badge{background:#f59e0b;color:#0f172a;font-size:.7rem;font-weight:700;padding:.2rem .6rem;border-radius:20px;display:none}
  .lehrer-badge.visible{display:inline-block}
  .tabs{display:flex;gap:.5rem;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .tabs::-webkit-scrollbar{display:none}
  .tab-btn{display:flex;align-items:center;gap:.45rem;padding:.52rem 1rem;border-radius:10px;border:1.5px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:#94a3b8;font-family:'Source Sans 3',sans-serif;font-size:.82rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:all .18s;-webkit-tap-highlight-color:transparent;min-height:40px}
  .tab-btn:hover{background:rgba(255,255,255,.12);color:#e2e8f0}
  .tab-btn.active[data-fach="mathe"]{background:var(--mathe);color:#fff;border-color:var(--mathe)}
  .tab-btn.active[data-fach="bio"]{background:var(--bio);color:#fff;border-color:var(--bio)}
  .tab-btn.active[data-fach="kompass"]{background:var(--kompass);color:#fff;border-color:var(--kompass)}
  .tab-btn.active[data-fach="sonst"]{background:var(--sonst);color:#fff;border-color:var(--sonst)}
  .tab-btn.active[data-fach="suche"]{background:#7c3aed;color:#fff;border-color:#7c3aed}

  /* Lehrermodus */
  .lehrer-only{display:none}
  body.lehrer-mode .lehrer-only{display:block}
  body.lehrer-mode .kachel-links a.lehrer-link{display:block}
  .kachel-links a.lehrer-link{display:none;color:#92400e !important;font-style:italic}
  .kachel-links a.lehrer-link::before{content:'👨‍🏫 '}

  /* search */
  .search-bar{max-width:960px;margin:1.25rem auto 0;padding:0 1.25rem;display:none}
  .search-bar.visible{display:block}
  .search-row{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:.75rem 1rem;box-shadow:var(--shadow);margin-bottom:.75rem}
  .search-input{flex:1;min-width:180px;border:none;outline:none;font-family:'Source Sans 3',sans-serif;font-size:.95rem;color:var(--text);background:transparent}
  .search-input::placeholder{color:var(--muted)}
  .filter-group{display:flex;gap:.4rem;flex-wrap:wrap}
  .filter-btn{padding:.3rem .7rem;border-radius:20px;border:1.5px solid var(--border);background:#f8fafd;color:var(--muted);font-size:.75rem;font-weight:600;cursor:pointer;transition:all .15s;-webkit-tap-highlight-color:transparent}
  .filter-btn.active{background:#7c3aed;color:#fff;border-color:#7c3aed}
  .fach-filter-btn{padding:.3rem .7rem;border-radius:20px;border:1.5px solid var(--border);background:#f8fafd;color:var(--muted);font-size:.75rem;font-weight:600;cursor:pointer;transition:all .15s;-webkit-tap-highlight-color:transparent}
  .fach-filter-btn.active[data-val="mathe"]{background:var(--mathe);color:#fff;border-color:var(--mathe)}
  .fach-filter-btn.active[data-val="bio"]{background:var(--bio);color:#fff;border-color:var(--bio)}
  .fach-filter-btn.active[data-val=""]{background:#7c3aed;color:#fff;border-color:#7c3aed}
  .search-results{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
  .sri{display:flex;align-items:center;gap:.75rem;padding:.65rem 1.2rem;text-decoration:none;color:var(--text);border-bottom:1px solid var(--bl);transition:background .12s;min-height:48px}
  .sri:last-child{border-bottom:none}
  .sri:hover{background:#f0f4ff}
  .sri-icon{font-size:.8rem;opacity:.3;flex-shrink:0}
  .sri-info{flex:1;min-width:0}
  .sri-title{font-size:.9rem;font-weight:600}
  .sri-desc{font-size:.75rem;color:var(--muted);margin-top:.1rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .sri-tags{display:flex;gap:.3rem;flex-shrink:0}
  .no-results{padding:2rem;text-align:center;color:var(--muted);font-size:.9rem}

  /* meta hint */
  .meta-hinweis{max-width:960px;margin:0 auto 1.5rem;padding:0 1.25rem;display:none}
  .meta-hinweis.visible{display:block}
  .meta-box{background:#fffbeb;border:1.5px solid #f59e0b;border-radius:14px;padding:1rem 1.25rem}
  .meta-box h3{font-size:.85rem;font-weight:700;color:#92400e;margin-bottom:.6rem}
  .meta-box ul{list-style:none;display:flex;flex-direction:column;gap:.35rem}
  .meta-box li{display:flex;align-items:center;gap:.6rem}
  .meta-box a{font-size:.83rem;font-weight:600;color:#1d4ed8;text-decoration:none}
  .meta-box .path{font-size:.7rem;color:var(--muted)}

  /* cards */
  .card-area{padding:1.5rem 1.25rem;max-width:960px;margin:0 auto}
  .card{display:none;background:var(--surface);border:1px solid var(--border);border-radius:20px;overflow:hidden;box-shadow:var(--shadow);animation:fadeIn .2s ease}
  .card.active{display:block}
  @keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
  .card[data-fach="mathe"]{border-top:4px solid var(--mathe)}
  .card[data-fach="bio"]{border-top:4px solid var(--bio)}
  .card[data-fach="kompass"]{border-top:4px solid var(--kompass)}
  .card[data-fach="sonst"]{border-top:4px solid var(--sonst)}
  .card-header{display:flex;align-items:center;gap:1rem;padding:1.1rem 1.5rem;border-bottom:1px solid var(--bl)}
  .card[data-fach="mathe"] .card-header{background:var(--ml)}
  .card[data-fach="bio"] .card-header{background:var(--biol)}
  .card[data-fach="kompass"] .card-header{background:var(--kl)}
  .card[data-fach="sonst"] .card-header{background:var(--sl)}
  .card-icon{font-size:1.5rem}
  .card-title{font-family:'Playfair Display',serif;font-size:1.3rem;flex:1;font-weight:900}
  .card[data-fach="mathe"] .card-title{color:var(--mathe)}
  .card[data-fach="bio"] .card-title{color:var(--bio)}
  .card[data-fach="kompass"] .card-title{color:var(--kompass)}
  .card[data-fach="sonst"] .card-title{color:var(--sonst)}
  .card-meta{font-size:.7rem;color:var(--muted);background:#fff;padding:.2rem .6rem;border-radius:20px;border:1px solid var(--border);font-weight:600}

  /* klassen */
  .klasse-wrap{border-bottom:1px solid var(--bl)}
  .klasse-wrap:last-child{border-bottom:none}
  .klasse-btn{width:100%;display:flex;align-items:center;gap:.75rem;padding:.85rem 1.5rem;background:none;border:none;cursor:pointer;text-align:left;font-family:'Source Sans 3',sans-serif;font-size:1rem;font-weight:700;color:var(--text);-webkit-tap-highlight-color:transparent;transition:background .12s;min-height:52px}
  .klasse-btn:hover{background:#f8fafd}
  .card[data-fach="mathe"] .klasse-btn:hover{background:var(--ml)}
  .card[data-fach="bio"] .klasse-btn:hover{background:var(--biol)}
  .klasse-label{flex:1}
  .klasse-count{font-size:.7rem;font-weight:600;color:#fff;padding:.15rem .5rem;border-radius:12px;background:#94a3b8}
  .card[data-fach="mathe"] .klasse-count{background:var(--mathe)}
  .card[data-fach="bio"] .klasse-count{background:var(--bio)}
  .card[data-fach="kompass"] .klasse-count{background:var(--kompass)}
  .card[data-fach="sonst"] .klasse-count{background:var(--sonst)}
  .klasse-arrow{font-size:.65rem;color:var(--muted);transition:transform .22s;margin-left:.3rem}
  .klasse-btn[aria-expanded="true"] .klasse-arrow{transform:rotate(180deg)}
  .klasse-panel{display:none;border-top:2px solid var(--bl)}
  .klasse-panel.open{display:block}

  /* themen kacheln */
  .themen-bereich{padding:.75rem 1rem 1rem;display:flex;flex-direction:column;gap:.6rem}
  .thema-block{background:var(--surface);border:1px solid var(--bl);border-radius:14px;overflow:hidden}
  .thema-header{display:flex;align-items:center;gap:.6rem;padding:.6rem 1rem;border-bottom:1px solid var(--bl)}
  .card[data-fach="mathe"] .thema-header{background:var(--ml)}
  .card[data-fach="bio"] .thema-header{background:var(--biol)}
  .thema-icon{font-size:1.1rem}
  .thema-title{font-weight:700;font-size:.9rem;flex:1}
  .card[data-fach="mathe"] .thema-title{color:var(--mathe)}
  .card[data-fach="bio"] .thema-title{color:var(--bio)}
  .thema-leer{font-size:.7rem;color:var(--muted);font-style:italic}
  .kachel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:.5rem;padding:.6rem}
  .kachel{position:relative;background:#f8fafd;border:1px solid var(--bl);border-radius:10px;padding:.55rem .7rem;cursor:pointer;transition:background .12s,border-color .12s;-webkit-tap-highlight-color:transparent}
  .kachel:not(.kachel-leer):hover{background:var(--ml);border-color:#93c5fd}
  .kachel.open{background:var(--ml);border-color:#93c5fd}
  .kachel-leer{opacity:.4;cursor:default}
  .kachel-name{font-size:.82rem;font-weight:600;color:var(--text);margin-bottom:.35rem;line-height:1.3}
  .kachel-badges{display:flex;gap:.3rem;flex-wrap:wrap}
  .kbadge{font-size:.65rem;padding:.15rem .45rem;border-radius:20px;font-weight:600}
  .kbadge.ls{background:#dbeafe;color:#1d4ed8}
  .kbadge.ue{background:#ccfbf1;color:#0f766e}
  .kbadge.test{background:#fee2e2;color:#b91c1c}
  .kbadge.bonus{background:#ede9fe;color:#6d28d9}
  .kbadge.rbka{background:#fef2f2;color:#9f1239}
  .kbadge.rb{background:#fff7ed;color:#9a3412}
  .kbadge.leer{background:#f1f5f9;color:#94a3b8}
  .kbadge.lehrer{background:#fef3c7;color:#92400e;display:none}
  .kbadge.rbka{background:#fef3c7;color:#b45309}
  body.lehrer-mode .kbadge.lehrer{display:inline-block}
  /* ── Paar-Darstellung ls+ue ── */
  .kachel-links{margin-top:.5rem;border-top:1px solid var(--bl);padding-top:.4rem;display:flex;flex-direction:column;gap:.2rem}
  .kachel-links a{font-size:.78rem;color:var(--mathe);text-decoration:none;padding:.2rem .1rem;display:block}
  .kachel-links a:hover{text-decoration:underline}
  .card[data-fach="bio"] .kachel-links a{color:var(--bio)}
  .link-pair{display:grid;grid-template-columns:1fr 1fr;gap:.3rem;background:#f0f7ff;border-radius:6px;padding:.2rem .3rem}
  .card[data-fach="bio"] .link-pair{background:#f0fdf4}
  .link-pair a{font-size:.75rem;padding:.15rem .2rem}
  .link-pair a:first-child{border-right:1px solid var(--bl)}
  .link-single{display:block}

  /* ── Tooltip / Long-Press Info ── */
  .kachel-tooltip{display:none;position:absolute;top:0;left:100%;margin-left:.5rem;width:200px;max-width:60vw;padding:.5rem .65rem;background:#1e293b;color:#e2e8f0;border-radius:8px;font-size:.72rem;line-height:1.4;box-shadow:0 8px 24px rgba(15,23,42,.35);z-index:30}
  .kachel-tooltip.tt-left{left:auto;right:100%;margin-left:0;margin-right:.5rem}
  .kachel-tooltip .tt-typ{font-weight:700;color:#94a3b8;font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.15rem}
  .kachel-tooltip .tt-desc{color:#cbd5e1}
  .kachel-tooltip .tt-path{color:#475569;font-size:.62rem;margin-top:.2rem;word-break:break-all}
  .kachel.tooltip-open .kachel-tooltip{display:block}

  /* Long-press highlight */
  .kachel.pressing{outline:2px solid #f59e0b;outline-offset:2px}

  /* alt */
  .alt-wrap{border-top:2px dashed #cbd5e1}
  .alt-btn{width:100%;display:flex;align-items:center;gap:.75rem;padding:.75rem 1.5rem;background:#f8fafc;border:none;cursor:pointer;text-align:left;font-family:'Source Sans 3',sans-serif;font-size:.8rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.1em;-webkit-tap-highlight-color:transparent;transition:background .12s;min-height:48px}
  .alt-btn:hover{background:#f1f5f9}
  .alt-arrow{font-size:.65rem;transition:transform .22s;margin-left:.3rem}
  .alt-btn[aria-expanded="true"] .alt-arrow{transform:rotate(180deg)}
  .alt-panel{display:none}
  .alt-panel.open{display:block}

  /* jgst (alte Struktur) */
  .jgst{border-bottom:1px solid var(--bl)}
  .jgst:last-child{border-bottom:none}
  .jgst-toggle{width:100%;display:flex;align-items:center;gap:.75rem;padding:.85rem 1.5rem;background:none;border:none;cursor:pointer;text-align:left;color:var(--text);font-family:'Source Sans 3',sans-serif;font-size:.92rem;font-weight:700;-webkit-tap-highlight-color:transparent;transition:background .12s;min-height:48px}
  .jgst-toggle:hover{background:#f8fafd}
  .jgst-label{flex:1}
  .jgst-count{font-size:.7rem;font-weight:600;color:#fff;padding:.15rem .5rem;border-radius:12px;background:#94a3b8}
  .card[data-fach="mathe"] .jgst-count{background:var(--mathe)}
  .jgst-arrow{font-size:.65rem;color:var(--muted);transition:transform .22s;margin-left:.3rem}
  .jgst-toggle[aria-expanded="true"] .jgst-arrow{transform:rotate(180deg)}
  .jgst-panel{display:none;border-top:1px solid var(--bl);background:#f8fafd}
  .jgst-panel.open{display:block}

  /* cols */
  .col-grid{display:grid;grid-template-columns:repeat(3,1fr);align-items:start}
  .col-grid.c4{grid-template-columns:repeat(4,1fr)}
  .col-grid.c1{grid-template-columns:1fr}
  .col-group{border-right:1px solid var(--bl);min-width:0}
  .col-group:last-child{border-right:none}
  .col-head{padding:.5rem 1rem .45rem;font-size:.68rem;text-transform:uppercase;letter-spacing:.13em;font-weight:700;border-bottom:2px solid;display:flex;align-items:center;gap:.35rem}
  .col-head.lernen{color:#1d4ed8;background:#eff6ff;border-color:#1d4ed8}
  .col-head.uebung{color:#0f766e;background:#f0fdfa;border-color:#0f766e}
  .col-head.sonstig{color:#7c3aed;background:#f5f3ff;border-color:#7c3aed}
  .col-head.test{color:#b91c1c;background:#fff1f2;border-color:#b91c1c}
  .col-head.arbeit{color:#c2410c;background:#fff7ed;border-color:#c2410c}
  .col-head.ha{color:#854d0e;background:#fefce8;border-color:#854d0e}
  .links{display:flex;flex-direction:column}
  .link-row{display:flex;align-items:flex-start;gap:.55rem;padding:.6rem 1rem;text-decoration:none;color:var(--text);border-top:1px solid var(--bl);transition:background .1s;-webkit-tap-highlight-color:transparent;min-height:44px}
  .link-row:first-child{border-top:none}
  .link-row:hover{background:#e8f0fe}
  .link-icon{font-size:.72rem;opacity:.3;flex-shrink:0;margin-top:.18rem}
  .link-name{flex:1;font-size:.88rem;font-weight:600;color:var(--text);line-height:1.35}
  .link-row:hover .link-name{color:var(--mathe)}
  .empty-col{padding:.7rem 1rem;font-size:.78rem;font-style:italic;color:#94a3b8}
  .link-tag{font-size:.6rem;padding:.13rem .42rem;border-radius:20px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;flex-shrink:0;margin-top:.18rem}
  .tag-arbeit{background:#ffedd5;color:#c2410c}
  .tag-entwurf{background:#f1f5f9;color:#475569}
  .tag-bonus{background:#ede9fe;color:#6d28d9}
  .tag-test{background:#fee2e2;color:#b91c1c}
  .tag-orga{background:#fef9c3;color:#854d0e}

  @media(max-width:600px){
    .col-grid,.col-grid.c4{grid-template-columns:1fr}
    .col-group{border-right:none;border-bottom:1px solid var(--bl)}
    .col-group:last-child{border-bottom:none}
    .kachel-grid{grid-template-columns:repeat(2,1fr)}
  }

  /* Dino */
  #dino{position:fixed;bottom:1.5rem;right:1.5rem;font-size:2.2rem;cursor:pointer;user-select:none;transition:transform .25s cubic-bezier(.34,1.56,.64,1);z-index:100;filter:drop-shadow(0 3px 6px rgba(0,0,0,.25))}
  #dino:hover{transform:scale(1.25) rotate(-10deg)}
  #dino:active{transform:scale(.92) rotate(5deg)}
  body.lehrer-mode #dino{filter:drop-shadow(0 3px 12px rgba(245,158,11,.6))}
  #dino-tip{position:fixed;bottom:4.8rem;right:1.5rem;background:#0f172a;color:#e2e8f0;font-family:'Source Sans 3',sans-serif;font-size:.78rem;font-weight:600;padding:.45rem .9rem;border-radius:10px;white-space:nowrap;pointer-events:none;opacity:0;transform:translateY(6px);transition:opacity .2s,transform .2s}
  #dino-tip.visible{opacity:1;transform:translateY(0)}
  #dino-tip::after{content:'';position:absolute;top:100%;right:1.1rem;border:5px solid transparent;border-top-color:#0f172a}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-inner">
    <h1>🦖 Mathedino <span>· Materialübersicht</span>
      <span class="lehrer-badge" id="lehrerBadge">👨‍🏫 Lehrermodus</span>
      <span class="ts">aktualisiert 16.07.2026</span>
    </h1>
    <div class="tabs" id="tabBar"></div>
  </div>
</div>

<div class="search-bar" id="searchBar">
  <div class="search-row">
    <span style="font-size:1rem;opacity:.5">🔍</span>
    <input class="search-input" id="searchInput" type="search" placeholder="Schlagwort suchen…" oninput="doSearch()">
  </div>
  <div class="search-row" style="gap:.5rem;padding:.5rem .75rem;">
    <span style="font-size:.75rem;color:var(--muted);font-weight:600;white-space:nowrap;">Fach:</span>
    <div class="filter-group" id="filterFach">
      <button class="fach-filter-btn active" data-val="">Alle</button>
      <button class="fach-filter-btn" data-val="mathe">📐 Mathe</button>
      <button class="fach-filter-btn" data-val="bio">🧬 Bio</button>
      <button class="fach-filter-btn" data-val="kompass">🧭 Kompass</button>
    </div>
    <span style="font-size:.75rem;color:var(--muted);font-weight:600;white-space:nowrap;margin-left:.5rem;">Klasse:</span>
    <div class="filter-group" id="filterKlasse">
      <button class="filter-btn active" data-val="">Alle</button>
      <button class="filter-btn" data-val="5">5</button>
      <button class="filter-btn" data-val="6">6</button>
      <button class="filter-btn" data-val="7">7</button>
      <button class="filter-btn" data-val="8">8</button>
      <button class="filter-btn" data-val="9">9</button>
      <button class="filter-btn" data-val="10">10</button>
      <button class="filter-btn" data-val="EF">EF</button>
    </div>
    <span style="font-size:.75rem;color:var(--muted);font-weight:600;white-space:nowrap;margin-left:.5rem;">Typ:</span>
    <div class="filter-group" id="filterTyp">
      <button class="filter-btn active" data-val="">Alle</button>
      <button class="filter-btn" data-val="Lernseite">Lernseite</button>
      <button class="filter-btn" data-val="Übung">Übung</button>
      <button class="filter-btn" data-val="Test">Test</button>
      <button class="filter-btn" data-val="Bonus">Bonus</button>
    </div>
  </div>
  <div class="search-results" id="searchResults"></div>
</div>

<div class="meta-hinweis" id="metaHinweis">
  <div class="meta-box">
    <h3>🛠️ Vorschlag: Metadaten ergänzen</h3>
    <ul id="metaList"></ul>
  </div>
</div>

"""

TPL_JS_HEAD = r"""<script>
// ── Lehrermodus ──────────────────────────────────────────────────────────────
let dinoClicks = 0, dinoTimer;
function dinoClick() {
  dinoClicks++;
  clearTimeout(dinoTimer);
  dinoTimer = setTimeout(() => { dinoClicks = 0; }, 1200);
  if (dinoClicks >= 3) {
    dinoClicks = 0;
    toggleLehrerModus();
  }
  // Tip bei Einfachklick
  document.getElementById('dino-tip').classList.toggle('visible');
  setTimeout(() => document.getElementById('dino-tip').classList.remove('visible'), 1500);
}

function setLehrerModus(aktiv) {
  document.body.classList.toggle('lehrer-mode', aktiv);
  document.getElementById('lehrerBadge').classList.toggle('visible', aktiv);
  document.getElementById('dino-tip').textContent = aktiv ? '👨‍🏫 Lehrermodus aktiv!' : 'Made by Mathedino 🦖';
}

function toggleLehrerModus() {
  const aktiv = !document.body.classList.contains('lehrer-mode');
  setLehrerModus(aktiv);
}

// URL-Parameter ?lehrer=1
const params = new URLSearchParams(window.location.search);
if (params.get('lehrer') === '1') setLehrerModus(true);
const fachParam = (params.get('fach') || 'alle').toLowerCase();

// ── Tabs ─────────────────────────────────────────────────────────────────────
const order = ['mathe','bio','kompass','sonst'];
const allowed = fachParam === 'alle' ? order : fachParam.split(',').map(f=>f.trim()).filter(f=>order.includes(f));
let suchFach = (fachParam !== 'alle' && allowed.length === 1) ? allowed[0] : '';

const tabBar = document.getElementById('tabBar');
const sb = document.createElement('button'); sb.className='tab-btn'; sb.dataset.fach='suche'; sb.textContent='🔍 Suche'; sb.onclick=()=>showCard('suche',sb); tabBar.appendChild(sb);
const labels = {mathe:'📐 Mathematik',bio:'🧬 Biologie',kompass:'🧭 Kompass',sonst:'📁 Sonstiges'};
allowed.forEach((f,i)=>{const b=document.createElement('button');b.className='tab-btn'+(i===0?' active':'');b.dataset.fach=f;b.textContent=labels[f];b.onclick=()=>showCard(f,b);tabBar.appendChild(b);});
order.forEach(f=>{if(!allowed.includes(f)){const c=document.getElementById('card-'+f);if(c)c.remove();}});
const firstCard=document.getElementById('card-'+allowed[0]);if(firstCard)firstCard.classList.add('active');

if(suchFach){document.querySelectorAll('#filterFach .fach-filter-btn').forEach(b=>{b.classList.toggle('active',b.dataset.val===suchFach);});}
let fF=suchFach,fK='',fT='';

function showCard(fach,btn){
  document.querySelectorAll('.card').forEach(c=>c.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  if(fach==='suche'){
    document.getElementById('searchBar').classList.add('visible');
    document.getElementById('cardArea').style.display='none';
    document.getElementById('searchInput').focus();
    showMetaHinweis();
  } else {
    document.getElementById('searchBar').classList.remove('visible');
    document.getElementById('metaHinweis').classList.remove('visible');
    document.getElementById('cardArea').style.display='';
    const c=document.getElementById('card-'+fach);if(c)c.classList.add('active');
    window.scrollTo({top:0,behavior:'smooth'});
  }
}

function toggleKlasse(btn){const p=btn.nextElementSibling;const open=p.classList.toggle('open');btn.setAttribute('aria-expanded',open);}
function toggleJgst(btn){const p=btn.nextElementSibling;const open=p.classList.toggle('open');btn.setAttribute('aria-expanded',open);}
function toggleAlt(btn){const p=btn.nextElementSibling;const open=p.classList.toggle('open');btn.setAttribute('aria-expanded',open);}
function toggleKachel(k, event){
  if(k.classList.contains('kachel-leer'))return;
  // Klick auf einen Link soll die Kachel NICHT schließen
  if(event && event.target.closest('a')) return;
  const l=k.querySelector('.kachel-links');if(!l)return;
  const open=l.style.display!=='none';
  l.style.display=open?'none':'flex';
  k.classList.toggle('open',!open);
  // Build pairs on first open
  if(!open && !l.dataset.paired){
    pairLinks(l);
    l.dataset.paired='1';
  }
}

// ── Paar-Gruppierung ────────────────────────────────────────────────────────
function pairLinks(container){
  const links = Array.from(container.querySelectorAll('a'));
  if(!links.length) return;

  // Stem: remove _ls / _ue / _ls2 / _ue2 suffix before .html
  function stem(href){
    return href.replace(/_(ls|ue)\d*\.html$/,'').replace(/_(ls|ue)\d*$/,'');
  }

  const paired = new Set();
  const result = [];

  links.forEach((a, i) => {
    if(paired.has(i)) return;
    const isLS = /_(ls)\d*\.html$/.test(a.href);
    if(!isLS){ result.push({type:'single', a}); return; }

    // Look for matching _ue
    const s = stem(a.href);
    const partner = links.findIndex((b, j) => j > i && !paired.has(j) && /_(ue)\d*\.html$/.test(b.href) && stem(b.href) === s);
    if(partner !== -1){
      paired.add(i); paired.add(partner);
      result.push({type:'pair', ls:a, ue:links[partner]});
    } else {
      result.push({type:'single', a});
    }
  });
  // Add singles that were partners
  links.forEach((a,i)=>{ if(paired.has(i) && !result.find(r=>r.ue===a||r.ls===a)) result.push({type:'single',a}); });

  // Rebuild DOM
  container.innerHTML='';
  result.forEach(r=>{
    if(r.type==='pair'){
      const div=document.createElement('div');
      div.className='link-pair';
      div.appendChild(r.ls.cloneNode(true));
      div.appendChild(r.ue.cloneNode(true));
      container.appendChild(div);
    } else {
      const wrap=document.createElement('div');
      wrap.className='link-single';
      wrap.appendChild(r.a.cloneNode(true));
      container.appendChild(wrap);
    }
  });
}

// ── Long-Press / Mouseover Info ─────────────────────────────────────────────
"""

TPL_JS_MID = r"""

function getInfo(href){
  const file = href.split('/').pop();
  return META_INFO[file] || null;
}

function showTooltip(kachel, href){
  // Remove old tooltip
  const old = kachel.querySelector('.kachel-tooltip');
  if(old) old.remove();
  const info = getInfo(href);
  const file = href.split('/').pop();
  const path = href.replace('mathe/','').replace('bio/','').replace('kompass/','');
  const div = document.createElement('div');
  div.className = 'kachel-tooltip';
  div.innerHTML = `<div class="tt-typ">${info ? info.typ : 'Datei'}</div>
    ${info ? `<div class="tt-desc">${info.desc}</div>` : ''}
    <div class="tt-path">📄 ${file}</div>`;
  kachel.appendChild(div);
  kachel.classList.add('tooltip-open');
  // Seitlich rechts als Standard; bei Platzmangel am Bildschirmrand nach links ausweichen
  const rect = kachel.getBoundingClientRect();
  const tooltipWidth = Math.min(200, window.innerWidth * 0.6);
  if(rect.right + tooltipWidth + 24 > window.innerWidth){
    div.classList.add('tt-left');
  }
}

function hideTooltip(kachel){
  kachel.classList.remove('tooltip-open');
  const t = kachel.querySelector('.kachel-tooltip');
  if(t) t.remove();
}

// Long-press für iPad
let pressTimer, pressTarget, pressHref;
document.addEventListener('pointerdown', e=>{
  const link = e.target.closest('.kachel-links a');
  if(!link) return;
  const kachel = link.closest('.kachel');
  if(!kachel) return;
  pressTarget = kachel;
  pressHref = link.getAttribute('href');
  kachel.classList.add('pressing');
  pressTimer = setTimeout(()=>{
    showTooltip(kachel, pressHref);
    kachel.classList.remove('pressing');
  }, 600);
}, {passive:true});

document.addEventListener('pointerup', e=>{
  clearTimeout(pressTimer);
  if(pressTarget) pressTarget.classList.remove('pressing');
}, {passive:true});

document.addEventListener('pointermove', e=>{
  clearTimeout(pressTimer);
  if(pressTarget) pressTarget.classList.remove('pressing');
}, {passive:true});

// Mouseover für Desktop
document.addEventListener('mouseover', e=>{
  const link = e.target.closest('.kachel-links a');
  if(!link) return;
  const kachel = link.closest('.kachel');
  if(!kachel) return;
  showTooltip(kachel, link.getAttribute('href'));
});

document.addEventListener('mouseout', e=>{
  const link = e.target.closest('.kachel-links a');
  if(!link) return;
  const related = e.relatedTarget;
  const kachel = link.closest('.kachel');
  if(!kachel) return;
  if(!kachel.contains(related)) hideTooltip(kachel);
});

// Klick auf Tooltip schließt ihn
document.addEventListener('click', e=>{
  if(e.target.closest('.kachel-tooltip')){
    hideTooltip(e.target.closest('.kachel'));
  }
});

// ── Filter ───────────────────────────────────────────────────────────────────
document.querySelectorAll('#filterFach .fach-filter-btn').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#filterFach .fach-filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');fF=b.dataset.val;doSearch();}));
document.querySelectorAll('#filterKlasse .filter-btn').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#filterKlasse .filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');fK=b.dataset.val;doSearch();}));
document.querySelectorAll('#filterTyp .filter-btn').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#filterTyp .filter-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');fT=b.dataset.val;doSearch();}));

"""

TPL_JS_TAIL = r"""

function doSearch(){
  const q=document.getElementById('searchInput').value.trim().toLowerCase();
  const res=document.getElementById('searchResults');
  const hits=Object.entries(META).filter(([path,m])=>{
    if(fF&&m.fach!==fF)return false;
    if(fK&&m.kl!==fK)return false;
    if(fT&&m.typ!==fT)return false;
    if(!q)return true;
    return q.split(/\s+/).every(w=>(m.title+' '+m.desc+' '+m.kw).toLowerCase().includes(w));
  });
  if(!q&&!fF&&!fK&&!fT){res.innerHTML='';return;}
  if(!hits.length){res.innerHTML='<div class="no-results">🦖 Keine Ergebnisse gefunden</div>';return;}
  const tagMap={'Lernseite':'tag-lernen','Übung':'tag-uebung','Test':'tag-test','Bonus':'tag-bonus'};
  const emoji={mathe:'📐',bio:'🧬',kompass:'🧭'};
  res.innerHTML=hits.map(([path,m])=>`<a class="sri" href="${path}" target="_blank" rel="noopener"><span class="sri-icon">${emoji[m.fach]||'📄'}</span><div class="sri-info"><div class="sri-title">${m.title}</div><div class="sri-desc">${m.desc}</div></div><div class="sri-tags"><span class="link-tag ${tagMap[m.typ]||''}">${m.typ}</span><span style="font-size:.6rem;padding:.13rem .42rem;border-radius:20px;font-weight:700;background:#f1f5f9;color:#475569">Kl. ${m.kl}</span></div></a>`).join('');
}

function showMetaHinweis(){
  const keys=Object.keys(META).sort(()=>Math.random()-.5).slice(0,2);
  document.getElementById('metaList').innerHTML=keys.map(p=>{const m=META[p];return`<li><a href="${p}" target="_blank">${m.title}</a><span class="path"> ${p}</span></li>`;}).join('');
  document.getElementById('metaHinweis').classList.add('visible');
}

// Swipe
let tx=0;
document.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;},{passive:true});
document.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)<60)return;
  const cur=document.querySelector('.card.active')?.dataset.fach;if(!cur)return;
  const i=allowed.indexOf(cur);const n=dx<0?Math.min(i+1,allowed.length-1):Math.max(i-1,0);
  if(n!==i){const b=document.querySelector(`.tab-btn[data-fach="${allowed[n]}"]`);if(b)showCard(allowed[n],b);}
},{passive:true});
</script>
</body>
</html>
"""

HEAD_FALLBACK = "<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Schule")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = args.out or os.path.join(args.root, "dino_hub.html")
    n, path = build(args.root, out)
    print(f"OK – {n} Dateien verarbeitet → {path}")
