# -*- coding: utf-8 -*-
"""
Seiten-Bauer für GeoGebra-Bedienungsseiten
==========================================
Setzt aus Bausteinen eine vollständige, selbst enthaltene HTML-Lernseite zusammen.
Braucht im selben Ordner:  css.txt · helfer.js · baustein_navigation.html
(optional: koord.py für Grafiken)

Minimalbeispiel
---------------
    import sys; sys.path.insert(0, '/tmp/gg')
    from bauer import *

    B = []
    B.append(kopfzeile('Lernseite · Erarbeitung', 'Nullstellen finden',
                       'Der Befehl Nullstelle und der Weg über das Werkzeug',
                       'GeoGebra-Suite · Klasse 8 · Lernhappen 4 von 6 · ca. 20 Minuten'))
    B.append(tabs(['1 · Der Befehl', '2 · Ohne Befehl', '3 · Sonderfälle', '4 · Überprüfe dich']))
    B.append(karte_auf('k1', 'Der Befehl Nullstelle', aktiv=True))
    B.append(merk('Wo wir gerade stehen:', 'Text …'))
    B.append(bauen('Zwei Zeilen eingeben', ['Tippe <code>f(x)=x^2-4</code>.', 'Tippe <code>Nullstelle(f)</code>.']))
    B.append(karte_zu())
    B.append(ende())

    baue('nullstellen_kl8_ls.html', titel='…', beschreibung='…', keywords='…',
         thema='Nullstellen', typ='Lernseite', klasse='8', body=''.join(B), js=JS)

Regeln, die der Bauer automatisch einhält
-----------------------------------------
- alle sieben Pflicht-Meta-Tags
- MathJax-Einbindung exakt nach Vorgabe
- Farbschema passend zum `typ` (Lernseite orange · Übung/Rückblick blau · Test grau)
- T-Rex mit „Made by ASzym"
- Navigationsleiste (baustein_navigation.html) vor dem T-Rex (TEIL 3.6)
- Notfall-Anzeige für Formeln, falls MathJax nicht geladen werden kann
- Fortschrittsmarken über den Reitern (✅ bzw. ● beim Wissenstest)
- Zustand im sessionStorage unter 'aszym:<datei>:v<version>' (übersteht Neuladen, TEIL 6)
"""
import io
import os

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.environ.get('GG_ZIEL', os.getcwd())

CSS_VORLAGE = io.open(os.path.join(HIER, 'css.txt'), encoding='utf-8').read()
HELFER = io.open(os.path.join(HIER, 'helfer.js'), encoding='utf-8').read()
_NAV_PFAD = os.path.join(HIER, 'baustein_navigation.html')
if not os.path.exists(_NAV_PFAD):
    raise SystemExit('baustein_navigation.html fehlt in %s – aus dem Projektwissen '
                     '(Ordner allgemein) unverändert dorthin schreiben.' % HIER)
NAV = io.open(_NAV_PFAD, encoding='utf-8').read().strip() + '\n'

# ---------------------------------------------------------------- Farbschemata
THEMA_LERNSEITE = {
    'AK': '#c97a2e', 'AKD': '#a5611e', 'AKL': '#fbeee0',
    'BG': '#faf7f2', 'LINE': '#e4dcd0',
    'HEADER': ('background:linear-gradient(135deg,#c97a2e,#a5611e);color:#fff;'
               'padding:1.3rem 1.2rem;box-shadow:0 3px 10px rgba(0,0,0,.12);'),
    'TYPBG': 'rgba(255,255,255,.25)', 'TYPFG': '#fff',
}
THEMA_UEBUNG = {
    'AK': '#2f5fa6', 'AKD': '#1f4680', 'AKL': '#e6eefb',
    'BG': '#f6f8fb', 'LINE': '#dbe3ee',
    'HEADER': ('background:linear-gradient(135deg,#2f5fa6,#1f4680);color:#fff;'
               'padding:1.3rem 1.2rem;box-shadow:0 3px 10px rgba(0,0,0,.12);'),
    'TYPBG': 'rgba(255,255,255,.25)', 'TYPFG': '#fff',
}
THEMA_TEST = {
    'AK': '#6b7686', 'AKD': '#1f4680', 'AKL': '#eef0f3',
    'BG': '#f7f8fa', 'LINE': '#e2e6ec',
    'HEADER': ('background:#eef0f3;color:#22303f;padding:1.3rem 1.2rem;'
               'border-bottom:5px solid #1f4680;'),
    'TYPBG': '#fff', 'TYPFG': '#1f4680',
}
THEMA_ZU_TYP = {
    'Lernseite': THEMA_LERNSEITE,
    'Übung': THEMA_UEBUNG,
    'Rückblick': THEMA_UEBUNG,
    'Test': THEMA_TEST,
    'Klassenarbeit': THEMA_TEST,
    'Bonus': THEMA_LERNSEITE,
}

KOPF = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<meta name="keywords" content="{keywords}">
<meta name="typ" content="{typ}">
<meta name="klasse" content="{klasse}">
<meta name="fach" content="{fach}">
<meta name="oberthema" content="{oberthema}">
<meta name="thema" content="{thema}">
<script>
  MathJax = {{
    tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }},
    svg: {{ fontCache: 'global' }}
  }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
"""

_KARTEN = []          # wird von tabs() gefüllt, von baue() ausgewertet


# ---------------------------------------------------------------- Hauptaufruf
def baue(datei, titel, beschreibung, keywords, thema, typ, klasse, body, js,
         fach='mathe', oberthema='GeoGebra Suite', version=1):
    """version: erhöhen, wenn sich der Aufbau einer schon veröffentlichten Seite ändert –
    dann passt ein alter gespeicherter Stand nicht mehr und wird ignoriert (TEIL 6)."""
    thema_farben = THEMA_ZU_TYP.get(typ, THEMA_LERNSEITE)
    css = CSS_VORLAGE
    for k, v in thema_farben.items():
        css = css.replace('%(' + k + ')s', v)

    marke = '●' if typ in ('Test', 'Klassenarbeit') else '✅'
    fortschritt = ", ".join("d%d:['k%d']" % (i + 1, i + 1) for i in range(len(_KARTEN) or 4))
    schluessel = 'aszym:%s:v%d' % (os.path.splitext(os.path.basename(datei))[0], version)
    vorlauf = ("var MARKE = '%s';\nvar FORTSCHRITT = {%s};\nvar SPEICHER = '%s';\n"
               % (marke, fortschritt, schluessel))

    html = (KOPF.format(titel=titel, beschreibung=beschreibung, keywords=keywords,
                        thema=thema, typ=typ, klasse=klasse, fach=fach,
                        oberthema=oberthema)
            + css + "</head>\n<body>\n" + body
            + '\n' + NAV
            + '<div class="trex" id="trex">\U0001F996'
              '<span class="bubble">Made by ASzym</span></div>\n'
            + "<script>\n" + vorlauf + js + "\n" + HELFER
            + "\npruefeFortschritt();\n</script>\n</body>\n</html>\n")
    pfad = os.path.join(ZIEL, datei)
    io.open(pfad, 'w', encoding='utf-8').write(html)
    print("gebaut:", pfad, len(html), "Zeichen")
    return pfad


# ---------------------------------------------------------------- Kopf & Karten
def kopfzeile(typtext, h1, unter, serie):
    return ('<header>\n  <span class="typ">%s</span>\n  <h1>%s</h1>\n'
            '  <p>%s</p>\n  <p class="serie">%s</p>\n</header>\n'
            % (typtext, h1, unter, serie))


def tabs(namen):
    """Reiterleiste. Merkt sich die Kartenzahl für die Fortschrittsmarken."""
    global _KARTEN
    _KARTEN = list(namen)
    s = '<div class="tabs">\n'
    for i, n in enumerate(namen):
        s += ('  <button class="tab%s" data-ziel="k%d">%s'
              '<span class="done" id="d%d"></span></button>\n'
              % (' aktiv' if i == 0 else '', i + 1, n, i + 1))
    return s + '</div>\n<main>\n'


def karte_auf(kid, titel, aktiv=False, unter=''):
    s = '  <section class="karte%s" id="%s">\n    <h2>%s</h2>\n' % (
        ' aktiv' if aktiv else '', kid, titel)
    if unter:
        s += '    <p>%s</p>\n' % unter
    return s


def karte_zu():
    return '  </section>\n\n'


def ende():
    return '</main>\n'


# ---------------------------------------------------------------- Textbausteine
def merk(fett, text, warnung=False):
    return ('    <div class="merk%s">\n      <b>%s</b> %s\n    </div>\n\n'
            % (' merk-warn' if warnung else '', fett, text))


def bauen(titel, schritte):
    li = "\n".join('        <li>%s</li>' % s for s in schritte)
    return ('    <div class="bauen">\n      <h3>\U0001F527 %s</h3>\n      <ol>\n%s\n'
            '      </ol>\n    </div>\n\n' % (titel, li))


def einstellung(titel, absaetze):
    p = "\n".join('      <p>%s</p>' % a for a in absaetze)
    return ('    <div class="einstellung">\n      <h3>⚙️ %s</h3>\n%s\n'
            '    </div>\n\n' % (titel, p))


def wz(titel, intro, schritte, fazit, fak=False, wid='wz1'):
    """Werkzeug-Weg: derselbe Zweck ohne Befehl, über die Werkzeugleiste."""
    li = "\n".join('        <li>%s</li>' % s for s in schritte)
    kern = ('        <p class="wz-intro">%s</p>\n        <ol>\n%s\n        </ol>\n'
            '        <p class="wz-fazit">%s</p>\n' % (intro, li, fazit))
    if fak:
        return ('    <div class="werkzeug wz-fak" id="%s">\n'
                '      <button class="wz-kopf" onclick="toggleWz(\'%s\')">\n'
                '        <span>\U0001F446 %s</span>\n'
                '        <span class="wz-pfeil">▾</span>\n'
                '      </button>\n      <div class="wz-inhalt">\n%s      </div>\n'
                '    </div>\n\n' % (wid, wid, titel, kern))
    return ('    <div class="werkzeug">\n      <h3>\U0001F446 %s</h3>\n%s    </div>\n\n'
            % (titel, kern))


def tipps(tid, stufen,
          ueberschrift="Brauchst du Hilfe? Decke so viel auf, wie du brauchst:"):
    """Gestufte Hilfen. Startet unsichtbar und wird erst nach dem Prüfen gezeigt."""
    s = ('    <div class="stufen-tipps" id="%s">\n      <h4>%s</h4>\n'
         % (tid, ueberschrift))
    for t, inhalt in stufen:
        s += ('      <div class="stufe">\n'
              '        <button class="stufe-kopf" onclick="toggleStufe(this)">'
              '<span>%s</span><span class="stufe-pfeil">▾</span></button>\n'
              '        <div class="stufe-inhalt">%s</div>\n      </div>\n' % (t, inhalt))
    return s + '    </div>\n'


def kennz(hilfsmittel, art):
    """Pflicht ab EF: Hilfsmittel und Lösungsart unter dem Aufgabentitel.
       hilfsmittel: 'gg' | 'cas' | 'frei'"""
    chips = {
        'gg':   '<span class="chip chip-hm">\U0001F4F1 mit GeoGebra</span>',
        'cas':  '<span class="chip chip-hm">\U0001F4F1 mit GeoGebra (CAS)</span>',
        'frei': '<span class="chip chip-frei">✏️ ohne Hilfsmittel</span>',
    }
    return ('    <div class="kennz">\n      %s\n'
            '      <span class="chip chip-art">%s</span>\n    </div>\n'
            % (chips[hilfsmittel], art))


# ---------------------------------------------------------------- Niveaustufen
def stufenwahl(kid):
    return ('    <div class="stufen-wahl" data-karte="%s">\n'
            '      <button class="stufe-btn aktiv" data-s="g">Grundlagen</button>\n'
            '      <button class="stufe-btn" data-s="f">Fortgeschritten</button>\n'
            '      <button class="stufe-btn" data-s="p">Profi</button>\n'
            '    </div>\n' % kid)


def stufe(kid, s, inhalt):
    return ('    <div class="stufe-block%s" data-karte="%s" data-s="%s">\n%s    </div>\n\n'
            % (' aktiv' if s == 'g' else '', kid, s, inhalt))


# ---------------------------------------------------------------- Wissenstest
def timer(minuten):
    """Pflicht-Orientierungstimer für Wissenstests. Steht über den Reitern."""
    return ('''<div class="timerleiste">
  <div class="timerbox" id="timerbox">
    <div class="timerzeile">
      <span class="timeruhr" id="uhr">--:--</span>
      <button class="timer-btn" id="btnStart" onclick="timerStart()">▶ Start</button>
      <button class="timer-btn" onclick="timerReset()">↺ Zurücksetzen</button>
      <span class="timer-hinweis">Dient nur der Orientierung – wenn die Zeit '''
            '''abgelaufen ist, passiert nichts.</span>
    </div>
    <div class="stufen-tipps zeig" style="margin:.8rem 0 0;">
      <div class="stufe">
        <button class="stufe-kopf" onclick="toggleStufe(this)">'''
            '''<span>Was hat es mit der Zeit auf sich?</span>'''
            '''<span class="stufe-pfeil">▾</span></button>
        <div class="stufe-inhalt">Die Zeit ist eine Empfehlung, kein Muss. Nach Ablauf '''
            '''kannst du normal weiterarbeiten – es wird nichts gesperrt, nichts '''
            '''abgeschickt und nichts ausgewertet.</div>
      </div>
    </div>
  </div>
</div>
''')


TIMER_JS = '''
const TESTZEIT_MIN = %d;
let restSek = TESTZEIT_MIN*60, ticker = null;
function uhrZeigen(){
  const m = Math.floor(restSek/60), s = restSek%%60;
  document.getElementById('uhr').textContent =
    String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
}
function timerStart(){
  const b = document.getElementById('btnStart');
  if(ticker){ clearInterval(ticker); ticker=null; b.textContent='▶ Weiter';
              b.classList.remove('laeuft'); return; }
  b.textContent='❚❚ Pause'; b.classList.add('laeuft');
  ticker = setInterval(()=>{
    if(restSek>0){ restSek--; uhrZeigen(); }
    if(restSek===0){ clearInterval(ticker); ticker=null;
      document.getElementById('timerbox').classList.add('abgelaufen');
      b.textContent='▶ Start'; b.classList.remove('laeuft'); }
  },1000);
}
function timerReset(){
  if(ticker){ clearInterval(ticker); ticker=null; }
  restSek = TESTZEIT_MIN*60;
  document.getElementById('timerbox').classList.remove('abgelaufen');
  const b=document.getElementById('btnStart');
  b.textContent='▶ Start'; b.classList.remove('laeuft');
  uhrZeigen();
}
uhrZeigen();
'''
