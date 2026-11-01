# -*- coding: utf-8 -*-
"""
Nachrüst-Skript für bestehende Lernseiten  (Schritt 3, sicherer Teil)
=====================================================================
Setzt EINMALIG über alle bestehenden HTML-Seiten (außer `_wartung/` und
Seiten mit <meta name="hubignore">) drei mechanisch sichere Änderungen um:

  1. NAV   – Navigationsleiste (baustein_navigation.html, v3) unverändert
             direkt VOR dem T-Rex einfügen (bzw. vor </body>, wenn kein T-Rex).
             Alte Leisten-Blöcke (falls vorhanden) werden vorher ersetzt.
  2. FONTS – Google-Fonts-Einbindungen entfernen (Datenschutz, LG München 2022):
             <link ...fonts.googleapis/gstatic...>, zugehörige preconnect-/
             dns-prefetch-<link>, und @import ...fonts.googleapis...
             font-family-Angaben bleiben stehen und fallen auf Systemschrift zurück.
  3. UTF8  – Seiten, die KEIN gültiges UTF-8 sind, werden NICHT verändert,
             nur gemeldet. Blindes Umkodieren wäre falsch (es würde bereits
             korrekte UTF-8-Umlaute doppelt kodieren); die echte Reparatur
             beschädigter Bytes ist Handarbeit und liegt in repariere_bytes.py.

Der Neulade-Schutz (sessionStorage, Stufe 1) ist NICHT Teil dieses Skripts –
er kommt in einem eigenen PR.

Aufruf:
    python3 nachruesten.py --repo <pfad> [--apply] [--limit N]

Ohne --apply: Trockenlauf, schreibt NICHTS, nur Bericht.
Mit  --apply: schreibt die Änderungen und gibt denselben Bericht aus.

Das Skript ist idempotent: ein zweiter Lauf findet nichts mehr zu tun
(Leiste am Version-Marker erkannt, Fonts bereits entfernt, schon UTF-8).
"""
import argparse
import io
import os
import re
import sys
import pathlib

NAV_VERSION_MARKER = 'BAUSTEIN: Navigationsleiste  (v4'
NAV_BLOCK_RE = re.compile(
    r'<!-- =+\s*BAUSTEIN: Navigationsleiste.*?ENDE BAUSTEIN Navigationsleiste =+ -->',
    re.S)
# erster T-Rex-Container, in allen beobachteten Attribut-Varianten
TREX_RE = re.compile(r'<div\b[^>]*class="trex"[^>]*>')


def lade_baustein(repo):
    p = os.path.join(repo, '_wartung', 'allgemein', 'baustein_navigation.html')
    if not os.path.exists(p):
        raise SystemExit('baustein_navigation.html fehlt in _wartung/allgemein/')
    return io.open(p, encoding='utf-8').read().rstrip('\n')


def lies(pfad):
    """Liest strikt als UTF-8. Gibt (text, 'utf-8') zurück, oder (None, None),
    wenn die Datei kein gültiges UTF-8 ist. Dieses Skript kodiert NICHT um:
    eine blinde Umkodierung (cp1252/latin-1) würde bereits korrekte UTF-8-Umlaute
    doppelt kodieren. Beschädigte Dateien werden nur gemeldet und übersprungen –
    ihre Reparatur ist Handarbeit (siehe repariere_bytes.py)."""
    roh = pathlib.Path(pfad).read_bytes()
    try:
        return roh.decode('utf-8'), 'utf-8'
    except UnicodeDecodeError:
        return None, None


# ------------------------------------------------------------------ Google Fonts
def entferne_fonts(h):
    """Entfernt Google-Fonts-<link>, zugehörige preconnect und @import.
    Gibt (neuer_text, anzahl_entfernt) zurück."""
    n = 0

    def weg(m):
        nonlocal n
        n += 1
        return ''

    # 1) <link ... href="...fonts.googleapis/gstatic..." ...>
    h = re.sub(r'[ \t]*<link\b[^>]*href="https?://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>[ \t]*\n?',
               weg, h, flags=re.I)
    # 2) preconnect/dns-prefetch zu fonts.googleapis/gstatic (ohne href-Reihenfolge-Annahme)
    h = re.sub(r'[ \t]*<link\b[^>]*\b(?:rel="(?:preconnect|dns-prefetch)")[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>[ \t]*\n?',
               weg, h, flags=re.I)
    h = re.sub(r'[ \t]*<link\b[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*\brel="(?:preconnect|dns-prefetch)"[^>]*>[ \t]*\n?',
               weg, h, flags=re.I)
    # 3) @import ...fonts.googleapis...;  (in <style>) – bis zum nächsten ';'.
    #    Deckt url(), direkte Strings und typografische Anführungszeichen (‘ ’ „ “) mit ab.
    h = re.sub(r'[ \t]*@import\b[^;]*fonts\.googleapis\.com[^;]*;[ \t]*\n?',
               weg, h, flags=re.I)
    return h, n


# ------------------------------------------------------------------ Navigationsleiste
def setze_leiste(h, baustein):
    """Fügt die Leiste vor dem T-Rex (sonst vor </body>) ein; ersetzt eine
    bereits vorhandene (evtl. ältere) Leiste. Gibt (neuer_text, status) zurück.
    status: 'eingefügt' | 'ersetzt' | 'aktuell' | 'kein-anker'."""
    vorhanden = NAV_BLOCK_RE.search(h)
    if vorhanden:
        if NAV_VERSION_MARKER in vorhanden.group(0):
            return h, 'aktuell'
        # ältere Fassung → durch aktuellen Baustein ersetzen
        h = NAV_BLOCK_RE.sub(lambda _: baustein, h, count=1)
        # evtl. weitere (doppelte) alte Blöcke entfernen
        h = NAV_BLOCK_RE.sub(lambda m: '' if NAV_VERSION_MARKER not in m.group(0) else m.group(0), h)
        return h, 'ersetzt'

    einschub = baustein + '\n'
    m = TREX_RE.search(h)
    if m:
        return h[:m.start()] + einschub + h[m.start():], 'eingefügt'
    # kein T-Rex-Div: vor das letzte </body>
    idx = h.lower().rfind('</body>')
    if idx == -1:
        return h, 'kein-anker'
    return h[:idx] + einschub + h[idx:], 'eingefügt'


# ------------------------------------------------------------------ Hauptlauf
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    baustein = lade_baustein(repo)
    if NAV_VERSION_MARKER not in baustein:
        raise SystemExit('baustein_navigation.html ist nicht v3 – abgebrochen.')

    root = pathlib.Path(repo)
    seiten = sorted(p for p in root.rglob('*.html')
                    if '.git' not in p.parts and '_wartung' not in p.parts)

    ber = {'nav_ein': [], 'nav_ersetzt': [], 'nav_aktuell': [], 'nav_kein_anker': [],
           'fonts': [], 'utf8_skip': [], 'hubignore': [], 'unveraendert': [], 'hub': []}
    getan = 0

    for p in seiten:
        if args.limit and getan >= args.limit:
            break
        rel = str(p.relative_to(root))
        # Startseite/Hub nie anfassen: wird von build_hub.py erzeugt, hat eigene
        # Navigation und würde beim nächsten Hub-Rebuild ohnehin überschrieben.
        if p.name == 'dino_hub.html':
            ber['hub'].append(rel)
            continue
        h, kod = lies(str(p))
        if h is None:
            # Kein gültiges UTF-8 → nicht anfassen, nur melden (Reparatur: repariere_bytes.py)
            ber['utf8_skip'].append(rel)
            continue

        if 'name="hubignore"' in h:
            # hubignore: Leiste NICHT setzen; Google Fonts trotzdem entfernen
            ber['hubignore'].append(rel)
            h2, nf = entferne_fonts(h)
            if nf:
                ber['fonts'].append(rel)
            if nf and args.apply:
                io.open(str(p), 'w', encoding='utf-8', newline='').write(h2)
            if not nf:
                ber['unveraendert'].append(rel)
            getan += 1
            continue

        orig = h
        h, nf = entferne_fonts(h)
        if nf:
            ber['fonts'].append(rel)
        h, status = setze_leiste(h, baustein)
        if status == 'eingefügt':
            ber['nav_ein'].append(rel)
        elif status == 'ersetzt':
            ber['nav_ersetzt'].append(rel)
        elif status == 'aktuell':
            ber['nav_aktuell'].append(rel)
        elif status == 'kein-anker':
            ber['nav_kein_anker'].append(rel)

        geaendert = (h != orig)
        if geaendert and args.apply:
            io.open(str(p), 'w', encoding='utf-8', newline='').write(h)
        if not geaendert:
            ber['unveraendert'].append(rel)
        getan += 1

    # ---- Bericht
    def zeile(titel, liste, zeige=0):
        print('%-26s %4d' % (titel, len(liste)))
        for f in liste[:zeige]:
            print('      ', f)

    print('\n' + '=' * 70)
    print('NACHRÜST-BERICHT  (%s)' % ('ANGEWENDET' if args.apply else 'TROCKENLAUF'))
    print('=' * 70)
    print('%-26s %4d' % ('Seiten gesamt', len(seiten)))
    zeile('Leiste eingefügt', ber['nav_ein'])
    zeile('Leiste ersetzt (alt→v3)', ber['nav_ersetzt'], 50)
    zeile('Leiste schon aktuell', ber['nav_aktuell'])
    zeile('Leiste: KEIN Anker', ber['nav_kein_anker'], 50)
    zeile('Google Fonts entfernt', ber['fonts'])
    zeile('UTF-8 defekt (übersprungen)', ber['utf8_skip'], 50)
    zeile('hubignore (ohne Leiste)', ber['hubignore'], 50)
    zeile('Hub/Startseite (nie angefasst)', ber['hub'], 50)
    zeile('ohne Änderung', ber['unveraendert'])
    print('=' * 70)
    if not args.apply:
        print('Trockenlauf – nichts geschrieben. Mit --apply anwenden.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
