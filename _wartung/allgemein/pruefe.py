# -*- coding: utf-8 -*-
"""
Prüf-Brille für interaktive Lernseiten
======================================
Statischer Linter zu `wiederkehrende_fehler_checkliste.md` und `anweisung_lernseiten.txt`.
Prüft jede HTML-Lernseite auf die Fehler, die dort als wiederkehrend dokumentiert sind.
Gilt für alle vier Projekte (Unterrichtsvorbereitung, HTML erzeugen, Debugging, GeoGebra)
und wird NUR im Wartungs-Projekt geändert.

Aufruf:   python3 pruefe.py [ordner_oder_datei ...]
          python3 pruefe.py ordner/ --kurz           (nur Dateien mit Fehlern)

Ausgabe:  pro Datei die gefundenen Verstöße mit Regel-Kürzel.
          Rückgabewert 1, wenn mindestens ein FEHLER gefunden wurde (0 bei nur Hinweisen).

Was dieser Linter NICHT kann (bleibt Handarbeit bzw. Browsertest):
  - ob eine Rückmeldung die Lösung verrät
  - ob Tipps die Rechnung vorwegnehmen
  - ob die Aufgabenwerte fachlich stimmen
  - ob Zuordnungen nach dem Prüfen sichtbar bleiben (braucht einen echten Klick)
  - ob Beispiele, Platzhalter oder Kontrollbilder die Lösung verraten
  - ob die Seite lehrplankonform ist
  - ob der Stand ein Neuladen wirklich vollständig übersteht (Browsertest: Seite
    bearbeiten, neu laden, vergleichen)

Stand: 16.10.2026 (sessionStorage erlaubt, TEIL 6)
"""
import io
import os
import re
import sys
import glob
import colorsys

# ---------------------------------------------------------------- Farbschema
ERLAUBTE_FARBEN = {
    '#22303f', '#ffffff', '#fff', '#1e7d32', '#c1272d',
    '#b8860b', '#fdf3d9', '#96690a',
    '#c97a2e', '#a5611e', '#fbeee0', '#faf7f2', '#e4dcd0',
    '#2f5fa6', '#1f4680', '#e6eefb', '#f6f8fb', '#dbe3ee',
    '#6b7686', '#eef0f3', '#f7f8fa', '#e2e6ec',
}
BEKANNT_FALSCH = {'#e07b1a', '#d98324', '#e8943c', '#1565c0', '#1976d2'}

META_PFLICHT = ['description', 'keywords', 'typ', 'klasse', 'fach', 'oberthema', 'thema']
SUFFIX_TYP = {'_ls': 'Lernseite', '_ue': 'Übung', '_test': 'Test',
              '_rbka': 'Rückblick', '_rb': 'Rückblick', '_ka': 'Klassenarbeit',
              '_bonus': 'Bonus'}
ERLAUBTE_HOSTS = ('cdn.jsdelivr.net/npm/mathjax', 'fonts.googleapis.com', 'fonts.gstatic.com')


def _hex_norm(x):
    x = x.lower()
    if len(x) == 4:
        x = '#' + x[1] * 2 + x[2] * 2 + x[3] * 2
    return x


def _hue(x):
    x = _hex_norm(x)
    r, g, b = (int(x[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def _ohne_code(h):
    """<code>-Inhalte entfernen – dort sind Schrägstriche echte GeoGebra-Eingaben."""
    return re.sub(r'<code>.*?</code>', '<code/>', h, flags=re.S)


def _style_bloecke(h):
    return "\n".join(re.findall(r'<style>(.*?)</style>', h, re.S))


def _skript_bloecke(h):
    return "\n".join(re.findall(r'<script>(.*?)</script>', h, re.S))


def _koerper_text(h):
    """Sichtbarer Text: ohne style, script und code."""
    t = re.sub(r'<style>.*?</style>', ' ', h, flags=re.S)
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<code>.*?</code>', ' ', t, flags=re.S)
    return t


def pruefe(pfad):
    """Gibt eine Liste (stufe, kuerzel, meldung) zurück. stufe: 'FEHLER' | 'HINWEIS'."""
    h = io.open(pfad, encoding='utf-8').read()
    name = os.path.basename(pfad)
    css = _style_bloecke(h)
    js = _skript_bloecke(h)
    text = _koerper_text(h)
    ohne_code = _ohne_code(h)
    f = []

    def fehler(k, m):
        f.append(('FEHLER', k, m))

    def hinweis(k, m):
        f.append(('HINWEIS', k, m))

    # ---------------------------------------------------- 1 Kopf & Meta
    meta = {}
    for m in re.finditer(r'<meta\s+name="([^"]+)"\s+content="([^"]*)"', h):
        meta[m.group(1)] = m.group(2)
    for schluessel in META_PFLICHT:
        if schluessel not in meta:
            fehler('META', 'Meta-Tag fehlt: %s' % schluessel)
        elif not meta[schluessel].strip():
            fehler('META', 'Meta-Tag leer: %s' % schluessel)

    basis = name[:-5] if name.endswith('.html') else name
    suffix = next((s for s in sorted(SUFFIX_TYP, key=len, reverse=True) if basis.endswith(s)), None)
    if suffix and 'typ' in meta and meta['typ'] != SUFFIX_TYP[suffix]:
        fehler('TYP', 'Suffix %s erwartet typ="%s", gesetzt ist typ="%s"'
               % (suffix, SUFFIX_TYP[suffix], meta['typ']))
    if suffix is None:
        hinweis('TYP', 'Dateiname trägt kein bekanntes Suffix')

    if 'tex-svg.js' not in h:
        fehler('MATHJAX', 'MathJax nicht eingebunden')
    elif 'inlineMath' not in h:
        fehler('MATHJAX', 'MathJax-Konfiguration (inlineMath) fehlt')

    for m in re.finditer(r'(?:src|href)="(https?://[^"]+)"', h):
        url = m.group(1)
        if not any(g in url for g in ERLAUBTE_HOSTS):
            fehler('EXTERN', 'nicht erlaubte externe Ressource: %s' % url[:70])

    ordner = os.path.dirname(os.path.abspath(pfad))
    for m in re.finditer(r'(?:src|href)="(?!https?://|#|data:|mailto:)([^"]+)"', h):
        ziel = m.group(1)
        if not os.path.exists(os.path.join(ordner, ziel)):
            fehler('DATEI', 'verweist auf nicht vorhandene Datei: %s' % ziel)

    # ---------------------------------------------------- 2 Farben & Typografie
    for hexw in set(re.findall(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', css)):
        nh = _hex_norm(hexw)
        if nh in BEKANNT_FALSCH:
            fehler('FARBE', 'bekannt falscher Ton: %s' % hexw)
            continue
        if nh in ERLAUBTE_FARBEN:
            continue
        grad, saettigung, helligkeit = _hue(nh)
        if saettigung > 0.35 and (18 <= grad <= 48 or 195 <= grad <= 250):
            hinweis('FARBE', 'eigener Orange-/Blauton außerhalb des Schemas: %s' % hexw)

    for m in re.finditer(r'font-size:\s*([0-9.]+)(rem|px|em)', css):
        wert, einheit = float(m.group(1)), m.group(2)
        if (einheit == 'rem' and wert < 1) or (einheit == 'px' and wert < 16):
            fehler('SCHRIFT', 'font-size unter 16px: %s%s' % (m.group(1), einheit))
    em_ketten = [m for m in re.findall(r'font-size:\s*([0-9.]+)em', css) if float(m) != 1]
    if len(em_ketten) > 2:
        hinweis('SCHRIFT', 'mehrere em-Schriftgrößen (%d) – Gefahr multiplizierter Ketten'
                % len(em_ketten))

    # ---------------------------------------------------- 6 Formeln & Rendering
    if re.search(r'(?:^|[};])\s*svg\s*\{', css):
        fehler('SVGGLOBAL', 'globale svg-Regel – bläht MathJax-Formeln auf')
    for m in re.finditer(r'([.#][\w-]+)\s+svg\s*\{', css):
        fehler('SVGNACHFAHRE',
               '%s svg{…} ist ein Nachfahren-Selektor: trifft auch MathJax-SVGs im '
               'selben Container. Auf "%s > svg" ändern.' % (m.group(1), m.group(1)))
    for m in re.finditer(r'mjx-container[^{]*\{([^}]*)\}', css):
        inhalt = m.group(1)
        rest = re.sub(r'max-width:\s*100%;?|overflow-x:\s*auto;?|\s', '', inhalt)
        if re.search(r'(width|height|font-size|transform)', rest):
            fehler('MJXGROESSE', 'Größenregel auf mjx-container: %s' % inhalt.strip()[:60])
    if re.search(r'\.frac\s+span', css):
        fehler('FRAC', '.frac span ist ein Nachfahren-Selektor – erzeugt Doppelbrüche')
    if re.search(r'>\s*\d+\s*/\s*\d+\s*<', ohne_code):
        fehler('BRUCH', 'Bruch mit Schrägstrich außerhalb von <code>')
    for rest in re.findall(r'\\(?:;|quad|qquad|,)', re.sub(r'\\\(.*?\\\)', ' ', text, flags=re.S)):
        fehler('LATEXREST', 'LaTeX-Abstandsbefehl außerhalb von \\(…\\): %s' % rest)
        break
    if 'tex-svg.js' in h and 'mathNotfall' not in h and 'MATHJAX-FALLBACK' not in h:
        hinweis('NOTFALL', 'MathJax-Notfall-Anzeige fehlt (baustein_mathjax_notfall.js)')
    for m in re.finditer(r'MathJax\.typesetPromise\(', js):
        davor = js[max(0, m.start() - 160):m.start()]
        if 'window.MathJax' not in davor and 'try' not in davor:
            fehler('TYPESET', 'MathJax.typesetPromise ohne Absicherung '
                              '(if(window.MathJax …) + try/catch)')
            break
    namen = re.findall(r'(?m)^\s*function\s+([A-Za-z_$][\w$]*)\s*\(', js)
    for n in sorted(set(x for x in namen if namen.count(x) > 1)):
        fehler('DOPPELT', 'Funktion %s() ist %d-mal definiert – die letzte gewinnt '
                          'stillschweigend' % (n, namen.count(n)))
    if '\\color{' in h:
        fehler('COLORCMD', '\\color{…} in einer Formel – zieht eine CDN-Extension nach')
    if re.search(r'textContent\s*=\s*[\'"`][^\'"`]*\\\(', js):
        fehler('TEXTCONTENT', 'Formel per textContent gesetzt – bleibt Rohtext')

    # ---------------------------------------------------- 3 Kartengerüst
    typ = meta.get('typ', '')
    tabs = re.findall(r'data-ziel="k\d+"[^>]*>([^<]*)', h)
    if typ in ('Übung', 'Test', 'Rückblick'):
        if not re.search(r'Auswertung', h):
            fehler('AUSWERTUNG', '%s ohne Auswertungskarte' % typ)
        if not re.search(r'Wiederholung', h):
            fehler('WIEDERHOLUNG', '%s ohne Wiederholungskarte' % typ)
        elif len(tabs) >= 2 and 'Wiederholung' not in tabs[-2]:
            hinweis('WIEDERHOLUNG',
                    'Wiederholungskarte ist nicht die vorletzte Karte (vorletzte: %s)'
                    % tabs[-2].strip())
    if typ == 'Test' and 'TESTZEIT_MIN' not in js:
        fehler('TIMER', 'Wissenstest ohne Orientierungstimer-Konstante TESTZEIT_MIN')

    if meta.get('klasse') in ('EF', 'Q1', 'Q2'):
        aufgaben = len(re.findall(r'class="aufgabe"', h))
        kennz = len(re.findall(r'class="(?:kennz|op-tags)"', h))
        if kennz == 0 and aufgaben:
            fehler('KENNZ', 'Oberstufe ohne Kennzeichnung (Hilfsmittel/Lösungsart)')
        elif aufgaben and kennz < aufgaben:
            hinweis('KENNZ', '%d Aufgaben-Blöcke, aber nur %d Kennzeichnungs-Zeilen – '
                             'prüfen, ob jede Aufgabenkarte eine hat' % (aufgaben, kennz))

    if 'href="#"' in h or "location.href='#'" in h or 'location.href="#"' in h:
        fehler('WEITER', 'toter Weiter-Button (Ziel "#")')

    # ---------------------------------------------------- 4 Antwortlogik
    if 'mcwahl' in h or 'data-ok' in h:
        if 'mische(' not in js and 'Fisher' not in js:
            fehler('MCMISCHEN', 'MC-Optionen werden nicht gemischt')
        if re.search(r"dataset\.(?:ok|c)\s*===?\s*['\"]0['\"]", js):
            fehler('DATAOK', 'data-ok invertiert und im Prüf-Code kompensiert')
        if re.search(r'(?:wahl|antwort|index)\s*===?\s*0\b', js):
            hinweis('MCINDEX', 'Auswertung könnte an einem festen Index hängen')
    if 'btn-pruefen' in h and 'btn-leeren' not in h:
        fehler('LEEREN', 'Prüfen-Button ohne Leeren-Button')
    if re.search(r'class="(?:stufen-tipps|tipp-box)"', h) and \
       not re.search(r'\.(?:stufen-tipps|tipp-inhalt)\s*\{[^}]*display:\s*none', css):
        hinweis('TIPPZU', 'Tipp-Block ist womöglich schon vor dem Prüfen offen')

    # ---------------------------------------------------- 7 Grafiken
    for m in re.finditer(r'<svg[^>]*role="img"[^>]*>(.*?)</svg>', h, re.S):
        inhalt = m.group(1)
        label = re.search(r'aria-label="([^"]*)"', m.group(0))
        label = label.group(1) if label else '(ohne Beschriftung)'
        if not inhalt.strip():
            hinweis('SVGLEER', 'SVG wird erst per JavaScript gefüllt (%s) – Achsen, '
                                'Einheiten und Pfeile nur im Browser prüfbar' % label[:45])
            continue
        # Als Koordinatensystem gilt nur, was Achsennamen x und y beschriftet hat.
        beschriftungen = re.findall(r'<text[^>]*>([^<]*)</text>', inhalt)
        istkoord = 'x' in beschriftungen and 'y' in beschriftungen
        if istkoord:
            if '<polygon' not in inhalt:
                fehler('KOORD', 'Koordinatensystem ohne Pfeilspitzen: %s' % label[:45])
            zahlen = [t for t in beschriftungen if re.match(r'^[−-]?\d', t)]
            if len(zahlen) < 2:
                fehler('KOORD', 'Koordinatensystem ohne beschriftete Einheiten: %s' % label[:45])
    for m in re.finditer(r'<svg(?![^>]*role=)', h):
        hinweis('SVGLABEL', 'SVG ohne role="img"/aria-label')
        break

    # ---------------------------------------------------- 8 Layout & Abschluss
    # Zustand (TEIL 6): nur sessionStorage, jeder Zugriff in try/catch.
    if 'localStorage' in h:
        fehler('STORAGE', 'localStorage verwendet – erlaubt ist nur sessionStorage (TEIL 6)')
    if re.search(r'document\.cookie', js):
        fehler('STORAGE', 'Cookies verwendet – erlaubt ist nur sessionStorage (TEIL 6)')
    for m in re.finditer(r'sessionStorage\s*\.\s*(?:getItem|setItem|removeItem|clear)\s*\(', js):
        davor = js[max(0, m.start() - 200):m.start()]
        if 'try' not in davor:
            fehler('SPEICHERTRY', 'sessionStorage-Zugriff ohne try/catch – bei blockiertem '
                                  'Speicher bricht das Skript ab (TEIL 6)')
            break
    interaktiv = ('btn-pruefen' in h or 'mcwahl' in h or 'data-ok' in h
                  or re.search(r'<input|<textarea', h))
    if interaktiv and 'sessionStorage' not in js:
        hinweis('NEULADEN', 'interaktive Seite ohne sessionStorage – der Stand geht beim '
                            'Neuladen verloren (TEIL 6)')
    if '\U0001F996' not in h:
        fehler('TREX', 'T-Rex 🦖 fehlt')
    elif 'Made by ASzym' not in h:
        fehler('TREX', 'T-Rex ohne Hinweis „Made by ASzym"')
    if 'backface-visibility' in css and 'min-height' not in css:
        fehler('FLIP', 'Flip-Card ohne min-height')

    return f


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    kurz = '--kurz' in sys.argv
    ziele = []
    for a in (args or ['.']):
        if os.path.isdir(a):
            ziele += sorted(glob.glob(os.path.join(a, '*.html')))
        else:
            ziele.append(a)

    gesamt_f = gesamt_h = 0
    zaehler = {}
    sauber = []
    for pfad in ziele:
        funde = pruefe(pfad)
        fs = [x for x in funde if x[0] == 'FEHLER']
        hs = [x for x in funde if x[0] == 'HINWEIS']
        gesamt_f += len(fs)
        gesamt_h += len(hs)
        for stufe, k, _ in funde:
            zaehler[k] = zaehler.get(k, 0) + 1
        if not funde:
            sauber.append(os.path.basename(pfad))
            continue
        if kurz and not fs:
            continue
        print('\n%s' % os.path.basename(pfad))
        for stufe, k, m in funde:
            print('   %-8s [%s] %s' % ('FEHLER' if stufe == 'FEHLER' else 'Hinweis', k, m))

    print('\n' + '=' * 70)
    print('%d Dateien geprüft · %d Fehler · %d Hinweise · %d ohne Befund'
          % (len(ziele), gesamt_f, gesamt_h, len(sauber)))
    if zaehler:
        print('\nnach Regel:')
        for k, n in sorted(zaehler.items(), key=lambda x: -x[1]):
            print('   %-14s %d' % (k, n))
    return 1 if gesamt_f else 0


if __name__ == '__main__':
    sys.exit(main())
