# -*- coding: utf-8 -*-
"""
Prüf-Brille für interaktive Lernseiten
======================================
Statischer Linter zu `wiederkehrende_fehler_checkliste.md` und `anweisung_lernseiten.txt`.
Prüft jede HTML-Lernseite auf die Fehler, die dort als wiederkehrend dokumentiert sind.
Gilt für alle vier Projekte (Unterrichtsvorbereitung, HTML erzeugen, Debugging, GeoGebra)
und wird nur per Pull Request im Repo geändert (anweisung_lernseiten.txt, TEIL 0 Nr. 26).

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

Stand: 13.11.2026 (Gruppenarbeit: Baustein Gruppen-Check, Regeln GC/GCALT/GRUPPE, TEIL 2.10;
       Kernkompetenzen: Meta-Tag kernkompetenzen, Prüfung KERN, TEIL 2.9;
       Rückblick-KA-Engine v5: Anrede über data-anrede, Kurswahl für Parallelkurse (KA.kurse);
       Rückblick-KA-Engine v4 mit KA.kern / Karte „Fit bleiben";
       Navigationsleiste v6 mit neutralen Feedback-Texten; Anrede: Oberstufe „Sie", Prüfung ANREDE, TEIL 3.7;
       Rückblick-KA-Engine v2: negative soll-Werte, art 'zeichen';
       Rückblick KA _rbka aus baustein_rueckblick_klassenarbeit.html, TEIL 2.8; neues Suffix
       _kavb für KA-Vorbereitung, TEIL 9; Schritt für Schritt _sfs, TEIL 2.7; Navigationsleiste
       Pflicht, TEIL 3.6; Google Fonts nicht mehr erlaubt, TEIL 8.1)
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
              '_rbka': 'Rückblick KA', '_kavb': 'KA-Vorbereitung',
              '_rb': 'Rückblick', '_ka': 'Klassenarbeit',
              '_bonus': 'Bonus', '_sfs': 'Schritt für Schritt'}
ERLAUBTE_HOSTS = ('cdn.jsdelivr.net/npm/mathjax',)   # Google Fonts seit 16.10.2026 nicht mehr

# Schritt-für-Schritt-Engine (baustein_schritt_fuer_schritt.html, TEIL 2.7)
SFS_TYP = 'Schritt für Schritt'
SFS_VERSION = 'v1'
SFS_MARKE = 'BAUSTEIN: Schritt-für-Schritt-Engine'

# Rückblick-KA-Engine (baustein_rueckblick_klassenarbeit.html, TEIL 2.8)
RBKA_TYP = 'Rückblick KA'
RBKA_VERSION = 'v5'
RBKA_MARKE = 'BAUSTEIN: Rückblick-KA-Engine'

# Gruppenarbeit & Gruppen-Check (baustein_gruppencheck.html, TEIL 2.10)
GC_VERSION = 'v2'
GC_MARKE = 'BAUSTEIN: Gruppen-Check-Engine'

# Kernkompetenzen (kernkompetenzen.md, TEIL 2.9): Anzahl Kürzel je Jahrgang.
# Ändert sich kernkompetenzen.md, wird diese Tabelle mitgezogen. Klasse 9: noch keine Liste.
KERN_ANZAHL = {5: 8, 6: 6, 7: 12, 8: 20, 9: 0, 10: 12}
KERN_TYPEN = ('Übung', 'Test', 'Rückblick', 'KA-Vorbereitung', 'Rückblick KA', 'Schritt für Schritt')
KERN_KUERZEL = re.compile(r'^K(\d{1,2})-(\d{1,2})$')

# Navigationsleiste (baustein_navigation.html, TEIL 3.6)
NAV_VERSION = 'v6'
NAV_START = 'https://szymczak75.github.io/Schule/dino_hub.html'
NAV_BLOCK = re.compile(r'<!-- =+\s*BAUSTEIN: Navigationsleiste.*?ENDE BAUSTEIN Navigationsleiste =+ -->',
                       re.S)


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


# Anrede (TEIL 3.7): Du-Formen, die auf Oberstufenseiten nicht vorkommen dürfen
DU_WORT = re.compile(r'\b(?:du|dich|dir|dein(?:e[mnrs]?)?|Du|Dich|Dir|Dein(?:e[mnrs]?)?)\b')
# Du-Imperative am Satzanfang („Bestimme …"), ohne folgendes „Sie"
DU_IMPERATIV = re.compile(
    r'(?:^|[.!?:;>"„(–]\s*|\n\s*)'
    r'(Bestimme|Berechne|Prüfe|Wähle|Gib|Nenne|Zeichne|Löse|Erkläre|Begründe|Ordne|Vergleiche|'
    r'Setze|Schreibe|Trage|Tippe|Ziehe|Überlege|Nutze|Probiere|Lies|Markiere|Ergänze|Beschreibe|'
    r'Untersuche|Skizziere|Gehe|Achte|Versuche|Schau|Hol|Wende|Erkunde|Fülle|Klicke|Öffne|'
    r'Multipliziere|Addiere|Subtrahiere|Dividiere|Rechne|Entscheide|Notiere|Formuliere|Zeige|'
    r'Beweise|Bilde|Leite|Vereinfache|Forme|Kürze|Beobachte|Verändere|Verschiebe|Stelle(?=\s+(?:die|den|das|dem|eine|einen|ein|sie|ihn|es|dir|dich|fest|zuerst|dann|dein\w*))|Teste|'
    r'Denk|Denke|Merke|Sieh|Gib)\b(?!\s+(?:Sie|ich|wir)\b)(?!\()', re.M)   # Wort direkt vor ( ist ein GeoGebra-Befehl
_JS_STR = r"'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\""
# Umschaltstellen „SIE ? 'Sie …' : 'du …'" (GeoGebra-helfer.js) sind kein Verstoß
_SIE_WEICHE = re.compile(r'\bSIE\s*\?\s*(?:%s)\s*:\s*(?:%s)' % (_JS_STR, _JS_STR))


def _du_formen(eigen, js, mit_skript):
    """Du-Formen im sichtbaren Text, in Attributen und (optional) in Skript-Zeichenketten."""
    t = re.sub(r'<!--.*?-->', ' ', eigen, flags=re.S)
    attr = ' '.join(re.findall(r'\b(?:placeholder|aria-label|title|alt|data-(?!anrede|version)[\w-]+)="([^"]*\s[^"]*)"', t))
    t = re.sub(r'<[^>]+>', ' ', _koerper_text(t)) + ' ' + attr
    funde = DU_WORT.findall(t) + DU_IMPERATIV.findall(t)
    if mit_skript:
        j = re.sub(r'/\*.*?\*/', ' ', js, flags=re.S)
        j = re.sub(r'(?<![:\'"\\])//[^\n]*', ' ', j)
        j = _SIE_WEICHE.sub(' ', j)
        for z in re.findall(_JS_STR + r'|`[^`]*`', j):
            z = re.sub(r'<code\b.*?</code>', ' ', z)                # Code (GeoGebra-Eingaben) ist kein Text
            z = re.sub(r'\b(?!placeholder|aria-label|title|alt)[\w-]+=\\?"[^"\\]*\\?"', ' ', z)   # Attributwerte (class="…") sind kein Text
            funde += DU_WORT.findall(z) + DU_IMPERATIV.findall(z[1:-1])
    return funde


def pruefe(pfad):
    """Gibt eine Liste (stufe, kuerzel, meldung) zurück. stufe: 'FEHLER' | 'HINWEIS'."""
    h = io.open(pfad, encoding='utf-8').read()
    name = os.path.basename(pfad)
    # Seiteneigener Teil ohne den Navigations-Baustein: dessen Skript und Feedback-Textfeld
    # gehören nicht zur Aufgabenlogik (sonst Fehlalarme bei DOPPELT und NEULADEN).
    # Reine Weiterleitung einer umbenannten Seite (hubignore + refresh) ist keine Lernseite.
    if 'name="hubignore"' in h and 'http-equiv="refresh"' in h:
        return []
    eigen = NAV_BLOCK.sub(' ', h)
    css = _style_bloecke(h)
    js = _skript_bloecke(eigen)
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

    # Nur nachgeladene Ressourcen zählen (src=…, <link href=…>). Ein normaler Link <a href=…>
    # (Startseite, Video-Link-Karte, TEIL 8.2) lädt nichts nach.
    for m in re.finditer(r'<(\w+)\b[^>]*?\b(?:src|href)="(https?://[^"]+)"', h):
        if m.group(1).lower() == 'a':
            continue
        url = m.group(2)
        if not any(g in url for g in ERLAUBTE_HOSTS):
            if 'fonts.googleapis.com' in url or 'fonts.gstatic.com' in url:
                fehler('EXTERN', 'Google Fonts nicht mehr erlaubt (Datenschutz) – Link '
                                 'entfernen, Systemschrift genügt (TEIL 8.1)')
            else:
                fehler('EXTERN', 'nicht erlaubte externe Ressource: %s' % url[:70])
    if '@import' in h and 'fonts.googleapis.com' in h:
        fehler('EXTERN', 'Google Fonts per @import – entfernen, Systemschrift genügt (TEIL 8.1)')

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
    # Reiter-Knöpfe; „ka“ = Auswertung auf einigen Klasse-5-Seiten. Nur echte <button>, nicht JS-Selektoren.
    tabs = re.findall(r'<button[^>]*data-ziel="k(?:\d+|a)"[^>]*>([^<]*)', h)
    if typ in ('Übung', 'Test', 'Rückblick', 'KA-Vorbereitung', SFS_TYP):
        if not re.search(r'Auswertung', h):
            fehler('AUSWERTUNG', '%s ohne Auswertungskarte' % typ)
        if not re.search(r'Wiederholung', h):
            fehler('WIEDERHOLUNG', '%s ohne Wiederholungskarte' % typ)
        elif len(tabs) >= 2 and 'Wiederholung' not in tabs[-2]:
            hinweis('WIEDERHOLUNG',
                    'Wiederholungskarte ist nicht die vorletzte Karte (vorletzte: %s)'
                    % tabs[-2].strip())
    # Kernkompetenzen (TEIL 2.9): Meta-Tag mit Kürzeln, keine aus späteren Jahrgängen
    kern_meta = []
    kl = meta.get('klasse', '')
    kl_zahl = int(kl) if kl.isdigit() else None
    if 'kernkompetenzen' in meta:
        roh = meta['kernkompetenzen'].strip()
        if not roh or 'ANPASSEN' in roh:
            fehler('KERN', 'Meta-Tag kernkompetenzen ist leer bzw. noch nicht ausgefüllt')
        else:
            for k in [x.strip() for x in roh.split(',') if x.strip()]:
                km = KERN_KUERZEL.match(k)
                if not km or int(km.group(1)) not in KERN_ANZAHL or \
                   not 1 <= int(km.group(2)) <= KERN_ANZAHL[int(km.group(1))]:
                    fehler('KERN', 'unbekanntes Kürzel im Meta-Tag kernkompetenzen: %s '
                                   '(siehe kernkompetenzen.md)' % k)
                    continue
                kern_meta.append(k)
                if kl_zahl is not None and int(km.group(1)) > kl_zahl:
                    fehler('KERN', '%s stammt aus Klasse %s – auf einer Seite der Klasse %s ist das '
                                   'Vorgriff, keine Wiederholung (TEIL 2.9)' % (k, km.group(1), kl))
    elif meta.get('fach') == 'mathe' and typ in KERN_TYPEN and \
            meta.get('oberthema') != 'GeoGebra Suite':
        hinweis('KERN', 'Meta-Tag kernkompetenzen fehlt – welche Kernkompetenzen nutzt die Seite? '
                        '(TEIL 2.9, beim Debuggen nachtragen)')
    if meta.get('fach') == 'mathe' and typ in ('Rückblick', 'KA-Vorbereitung') and \
            meta.get('oberthema') != 'GeoGebra Suite':
        if not any('Kernkompetenz' in t for t in tabs) and \
                not re.search(r'Wiederholung\s*(?:·|&middot;)\s*Kernkompetenzen', h):
            hinweis('KERN', '%s ohne Karte „Wiederholung · Kernkompetenzen" (TEIL 2.9)' % typ)
        elif len(kern_meta) < 3:
            hinweis('KERN', '%s: Kernkompetenz-Karte soll mindestens drei Kürzel mischen '
                            '(im Meta-Tag stehen %d)' % (typ, len(kern_meta)))

    # Schritt für Schritt (TEIL 2.7): Engine-Baustein, jeder Schritt mit Lösung, eindeutige Schritt-IDs
    ohne_kommentar = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    if typ == SFS_TYP:
        if SFS_MARKE not in h:
            fehler('SFS', 'typ="%s" ohne Engine aus baustein_schritt_fuer_schritt.html' % SFS_TYP)
        elif '%s  (%s' % (SFS_MARKE, SFS_VERSION) not in h:
            hinweis('SFSALT', 'Schritt-für-Schritt-Engine ist nicht die aktuelle Fassung %s – '
                              'Baustein ersetzen' % SFS_VERSION)
        n_schritt = len(re.findall(r'class="schritt"', ohne_kommentar))
        n_loes = len(re.findall(r'class="loesung"', ohne_kommentar))
        if n_schritt == 0:
            fehler('SFS', 'Schritt-für-Schritt-Seite ohne Schritte (div class="schritt")')
        elif n_loes < n_schritt:
            fehler('SFS', '%d Schritte, aber nur %d Lösungen (div class="loesung")' % (n_schritt, n_loes))
        ids = re.findall(r'data-step="([^"]+)"', ohne_kommentar)
        for d in sorted(set(i for i in ids if ids.count(i) > 1)):
            fehler('SFS', 'data-step="%s" mehrfach vergeben – Stände überschreiben sich' % d)
        if 'data-auswertung' not in ohne_kommentar:
            fehler('SFS', 'Auswertungskarte ohne data-auswertung – die Engine füllt sie nicht')
    elif SFS_MARKE in h:
        fehler('TYP', 'Seite nutzt die Schritt-für-Schritt-Engine, trägt aber typ="%s" – '
                      'richtig ist typ="%s" und Suffix _sfs' % (typ, SFS_TYP))
    else:
        titel = re.search(r'<title>(.*?)</title>', h, re.S)
        if titel and re.search(r'schritt\s*f(?:ü|ue)r\s*schritt', titel.group(1), re.I):
            hinweis('SFS', 'Titel nennt „Schritt für Schritt“ – gehört die Seite als _sfs auf '
                           'baustein_schritt_fuer_schritt.html (TEIL 2.7)?')

    # Gruppenarbeit & Gruppen-Check (TEIL 2.10)
    if 'id="gc-box"' in h or GC_MARKE in h:
        if GC_MARKE not in h:
            fehler('GC', 'Teile von baustein_gruppencheck.html ohne dessen Engine')
        else:
            if '%s (%s' % (GC_MARKE, GC_VERSION) not in h:
                hinweis('GCALT', 'Gruppen-Check-Engine ist nicht die aktuelle Fassung %s – '
                                 'Baustein ersetzen' % GC_VERSION)
            gd = re.search(r'var GRUPPE\s*=(.*?)ENDE ANPASSEN', h, re.S)
            if not gd:
                fehler('GC', 'Datenblock var GRUPPE fehlt')
            else:
                if 'ANPASSEN' in gd.group(1):
                    fehler('GC', 'Datenblock GRUPPE noch nicht angepasst (key)')
                checks = re.findall(r"'([^']+)'", (re.search(r'checks:\s*\[(.*?)\]', gd.group(1), re.S)
                                                   or re.search('()', '')).group(1))
                if checks and 'gc-codebox' not in h:
                    fehler('GC', 'GRUPPE.checks gesetzt, aber Codebox (TEIL B) fehlt')
                ohne_kommentar = re.sub(r'<!--.*?-->', '', h, flags=re.S)
                if checks and not re.search(r'GC\.melde\(', ohne_kommentar):
                    fehler('GC', 'Gruppen-Check ohne GC.melde(…) in der Aufgaben-Engine – Sterne werden nie gezählt')
                if checks and 'gc-re-erg' not in h:
                    hinweis('GC', 'Gruppen-Check ohne Teampunkte-Karte (TEIL C)')
            if 'id="gc-box"' in h and 'data-gr="3"' not in h:
                fehler('GC', 'Sozialform-Wahl ohne Gruppengröße 3–7')
    elif re.search(r'Teampunkte berechnen|id="re-erg"', h) and \
            not re.search(r'von\s*(?:\'\s*\+\s*\w+\s*\+\s*\'\s*)?m(?:ö|oe|&ouml;)glichen', h):
        hinweis('GRUPPE', 'Gruppenergebnis ohne Vergleich mit der Höchstpunktzahl („x von max möglichen“, TEIL 2.10)')

    # Rückblick KA (TEIL 2.8): Engine-Baustein, je Teilaufgabe genau zwei Übungen mit soll + 2 Tipps
    if typ == RBKA_TYP:
        if RBKA_MARKE not in h:
            fehler('RBKA', 'typ="%s" ohne Engine aus baustein_rueckblick_klassenarbeit.html' % RBKA_TYP)
        else:
            if '%s (%s' % (RBKA_MARKE, RBKA_VERSION) not in h:
                hinweis('RBKAALT', 'Rückblick-KA-Engine ist nicht die aktuelle Fassung %s – '
                                   'Baustein ersetzen' % RBKA_VERSION)
            daten = re.search(r'var KA\s*=(.*?)ENDE ANPASSEN', h, re.S)
            if not daten:
                fehler('RBKA', 'Datenblock „ANPASSEN: Daten der Klassenarbeit" (var KA = …) fehlt')
            else:
                d = daten.group(1)
                kern_m = re.search(r'\n\s*kern\s*:\s*\[', d)
                kern_d = d[kern_m.end():] if kern_m else ''
                if kern_m:
                    d = d[:kern_m.start()]
                    eintraege = re.split(r"\{\s*kk:\s*'", kern_d)[1:]
                    if not 2 <= len(eintraege) <= 4:
                        hinweis('KERN', 'KA.kern hat %d Kernkompetenzen – vorgesehen sind 2 bis 4 (TEIL 2.8)'
                                % len(eintraege))
                    for e in eintraege:
                        kid = e.split("'", 1)[0]
                        n_ueb = len(re.findall(r'\bfrage:', e))
                        if n_ueb not in (1, 2):
                            fehler('KERN', 'KA.kern %s hat %d Aufgaben statt 1 oder 2' % (kid, n_ueb))
                        n_soll = len(re.findall(r'\bsoll:\s*\[\s*-?\d+\s*,\s*[1-9]\d*\s*\]', e)) + \
                                 len(re.findall(r"\bart:\s*'zeichen'[^}]*?\bsoll:\s*'[<>=]'", e))
                        if n_soll < n_ueb:
                            fehler('KERN', 'KA.kern %s: nicht jede Aufgabe hat einen gültigen soll-Wert' % kid)
                        if len(re.findall(r'\btipps:\s*\[', e)) < n_ueb:
                            fehler('KERN', 'KA.kern %s: nicht jede Aufgabe hat tipps' % kid)
                        if kid not in kern_meta:
                            hinweis('KERN', 'KA.kern %s steht nicht im Meta-Tag kernkompetenzen' % kid)
                elif meta.get('fach') == 'mathe':
                    hinweis('KERN', 'Rückblick KA ohne KA.kern – Karte „Fit bleiben" fehlt (TEIL 2.8/2.9)')
                ids = re.findall(r"\bid:\s*'([^']+)'", d)
                for x in sorted(set(i for i in ids if ids.count(i) > 1)):
                    fehler('RBKA', 'Teilaufgabe id="%s" mehrfach vergeben' % x)
                teile = re.split(r"\{\s*id:\s*'", d)[1:]
                for t in teile:
                    tid = t.split("'", 1)[0]
                    n_ueb = len(re.findall(r'\bfrage:', t))
                    if n_ueb != 2:
                        fehler('RBKA', 'Teilaufgabe %s hat %d ähnliche Aufgaben statt genau 2' % (tid, n_ueb))
                    n_soll = len(re.findall(r'\bsoll:\s*\[\s*-?\d+\s*,\s*[1-9]\d*\s*\]', t)) + \
                             len(re.findall(r"\bart:\s*'zeichen'[^}]*?\bsoll:\s*'[<>=]'", t))
                    if n_soll < n_ueb:
                        fehler('RBKA', 'Teilaufgabe %s: nicht jede Übung hat soll: [Zähler, Nenner] '
                                       'bzw. bei art \'zeichen\' soll: \'<\'|\'>\'|\'=\'' % tid)
                    if len(re.findall(r'\btipps:\s*\[', t)) < n_ueb:
                        fehler('RBKA', 'Teilaufgabe %s: nicht jede Übung hat tipps' % tid)
                    if not re.search(r"\bname:\s*'[^']*[A-Za-zÄÖÜäöü]{3}", t) or \
                       re.search(r"\bname:\s*'(Aufgabe|Teilaufgabe)\s*\d", t):
                        hinweis('RBKA', 'Teilaufgabe %s: Kartentitel soll den Rechentyp beschreiben' % tid)
    elif RBKA_MARKE in h:
        fehler('TYP', 'Seite nutzt die Rückblick-KA-Engine, trägt aber typ="%s" – '
                      'richtig ist typ="%s" und Suffix _rbka' % (typ, RBKA_TYP))

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
        sfs = SFS_MARKE in h
        if sfs and 'data-anrede="sie"' not in h:
            fehler('ANREDE', 'Schritt-für-Schritt-Seite der Oberstufe ohne <body data-anrede="sie"> (TEIL 3.7)')
        du = _du_formen(eigen, js, not sfs)
        if du:
            zahl = {}
            for w in du:
                zahl[w] = zahl.get(w, 0) + 1
            fehler('ANREDE', 'Oberstufe wird gesiezt (TEIL 3.7) – Du-Formen gefunden: ' +
                   ', '.join('„%s" ×%d' % (w, n) for w, n in sorted(zahl.items(), key=lambda x: -x[1])))

    if 'href="#"' in h or "location.href='#'" in h or 'location.href="#"' in h:
        fehler('WEITER', 'toter Weiter-Button (Ziel "#")')

    # ---------------------------------------------------- 4 Antwortlogik
    if 'mcwahl' in h or 'data-ok' in h:
        if 'mische(' not in js and 'shuffle(' not in js and 'Fisher' not in js:
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
            # Skalenzahlen aus einer JS-Schablone (${fmt(x)}) zählen ebenfalls
            zahlen = [t for t in beschriftungen if re.match(r'^[−-]?\d', t) or '${' in t]
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
    interaktiv = ('btn-pruefen' in eigen or 'mcwahl' in eigen or 'data-ok' in eigen
                  or re.search(r'<input|<textarea', eigen))
    if interaktiv and 'sessionStorage' not in js:
        hinweis('NEULADEN', 'interaktive Seite ohne sessionStorage – der Stand geht beim '
                            'Neuladen verloren (TEIL 6)')
    if 'dino-ikon' not in h:
        if re.search(r'''(?:id|class)="[^"]*\b(?:t?rex|dino)\b[^"]*"[^>]*>\s*(?:\U0001F996|&#129430;)''', h):
            hinweis('TREX', 'altes 🦖-Emoji statt Dino-Baustein – nachruesten_dino.py '
                            'laufen lassen (8.3)')
        else:
            fehler('TREX', 'Dino fehlt – baustein_dino.html einsetzen (8.3)')
    elif 'Made by ASzym' not in h:
        fehler('TREX', 'T-Rex ohne Hinweis „Made by ASzym"')
    if 'backface-visibility' in css and 'min-height' not in css:
        fehler('FLIP', 'Flip-Card ohne min-height')

    # Navigationsleiste (TEIL 3.6) – nicht auf Ordner-Übersichten/Weiterleitungen (hubignore)
    if 'name="hubignore"' not in h:
        nav = NAV_BLOCK.search(h)
        if not nav:
            fehler('NAV', 'Navigationsleiste fehlt – baustein_navigation.html unverändert vor '
                          'dem T-Rex bzw. vor </body> einfügen (TEIL 3.6)')
        else:
            n = nav.group(0)
            if ('class="dino-nav"' not in n or 'class="dino-home"' not in n
                    or NAV_START not in n or 'dino-nav-fb' not in n):
                fehler('NAV', 'Navigationsleiste unvollständig oder verändert – Baustein neu '
                              'einsetzen (TEIL 3.6)')
            elif 'Navigationsleiste  (%s' % NAV_VERSION not in n:
                hinweis('NAVALT', 'Navigationsleiste ist nicht die aktuelle Fassung %s – '
                                  'Baustein ersetzen' % NAV_VERSION)
            if len(NAV_BLOCK.findall(h)) > 1:
                fehler('NAV', 'Navigationsleiste steht mehrfach in der Seite')
            if re.search(r'<main\b', h) and h.find('</main>') > nav.start():
                fehler('NAV', 'Navigationsleiste steht innerhalb von <main> – gehört ans '
                              'Seitenende vor den T-Rex')

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
