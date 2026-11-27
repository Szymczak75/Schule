# -*- coding: utf-8 -*-
"""
SchILD-3-Hilfe – Seitengenerator
================================
Erzeugt die Hilfe-Seiten für Kolleginnen und Kollegen in intern/MCG/schild3/
aus den Wissensdateien in diesem Ordner (z. B. schild3_stufenleitung.md).

Aufruf (im Repo-Hauptordner):   python3 _wartung/schild3/baue_schild3.py

- Inhalte kommen NUR aus den Wissensdateien (bauanleitung_schild_hilfe_website.md).
- Keine Dino-Bausteine, keine Sozialformen: Das sind Hilfeseiten für Lehrkräfte.
- Admin-Adresse: NUR unten in ADMIN_NAME / ADMIN_DOMAIN ändern, dann neu bauen.
- Neue Rolle: Wissensdatei im gleichen Eintragsschema ablegen, in ROLLEN eintragen,
  Seiten + Selbstchecks in SEITEN ergänzen.
"""
import html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HIER, '..', '..'))
ZIEL = os.path.join(REPO, 'intern', 'MCG', 'schild3')

# ---------------------------------------------------------------- Einstellungen
ADMIN_NAME, ADMIN_DOMAIN = 'aszymczak', 'my-mcg.de'   # Admin (Probleme in SchILD/SVWS) – einzige Stelle
WEB_NAME, WEB_DOMAIN = 'aszymczak', 'my-mcg.de'       # Verwalter dieser Hilfe-Website (Anleitung unklar/fehlt) – einzige Stelle
SEITE = 'oberstufe.html'   # alle Oberstufen-Inhalte (Stufenleitung und Koordination) auf einer Seite

ROLLEN = [  # (Kürzel, Name, Wissensdatei oder None = „in Vorbereitung“)
    ('ost', 'Oberstufe – Stufenleitung & Koordination', 'schild3_stufenleitung.md'),
    ('sek1', 'Stufenleitung Sek I', None),
    ('kl', 'Klassenlehrkräfte', None),
    ('fl', 'Fachlehrkräfte', None),
    ('ad', 'Admin', None),
]

# Abschnitte der Oberstufen-Seite: Anker, Titel, Kurztext, Einträge, Selbstcheck
SEITEN = [
    {
        'datei': SEITE, 'anker': 'grundlagen', 'titel': 'Grundlagen & Einstieg', 'icon': '🧭',
        'kurz': 'Welches Programm wofür, was sich mit der Umstellung ändert, App Oberstufe öffnen, Begriffe.',
        'eintraege': ['SL-G-01', 'SL-G-02', 'SL-O-01', 'SL-G-03'],
        'check': [
            ('Wo erledigst du als Oberstufenleitung Wahlen, Blockung und Umwahlen meistens?',
             ['Im SVWS-Webclient, App Oberstufe', 'In SchILD-NRW 3 unter Gruppenprozesse', 'Weiter in LuPO und Kurs42'], 0,
             'Faustregel aus SL-G-01: Oberstufe (Wahlen, Blockung, Umwahlen) → meist SVWS-Webclient, App Oberstufe.', 'SL-G-01'),
            ('Du brauchst eine Kursliste zum Ausdrucken. Wo findest du sie?',
             ['In der App Oberstufe unter Fachwahlen', 'In SchILD-NRW 3 unter Reports', 'Nur in Untis'], 1,
             'Listen und Zeugnisse druckt man in SchILD-NRW 3 über die Reports (SL-G-01).', 'SL-G-01'),
            ('Was gilt für LuPO mit der neuen APO-GOSt?',
             ['LuPO bekommt ein Update für die neue APO-GOSt', 'LuPO wird nicht angepasst, Laufbahnplanung läuft künftig im SVWS-Webclient', 'LuPO ersetzt den Webclient'], 1,
             'LuPO wird nicht an die neue APO-GOSt angepasst. Laufbahnplanung und Blockung laufen künftig im SVWS-Webclient (SL-G-02).', 'SL-G-02'),
            ('Was ist beim Öffnen der App Oberstufe die häufigste Fehlerquelle?',
             ['Ein falscher Abiturjahrgang oder Abschnitt', 'Ein veralteter Browser', 'Eine zu kleine Bildschirmauflösung'], 0,
             'Oben in der App Abiturjahrgang und Abschnitt prüfen (SL-O-01).', 'SL-O-01'),
        ],
    },
    {
        'datei': SEITE, 'anker': 'wahlen', 'titel': 'Wahlen erfassen & prüfen', 'icon': '📝',
        'kurz': 'Laufbahnplanung, WebLuPO, Import alter LuPO-Daten, Anwahlzahlen vor der Blockung.',
        'eintraege': ['SL-O-02', 'SL-O-03'], 'ablauf': [1, 2],
        'check': [
            ('Welche alten LuPO-Dateien lassen sich in den SVWS-Server einlesen?',
             ['Nur die Lehrerdatei .lup', 'Nur die Schülerdateien .lpo', 'Beide, .lup und .lpo'], 0,
             'Eingelesen wird nur die Lehrerdatei .lup, Schülerdateien .lpo nicht (SL-O-02).', 'SL-O-02'),
            ('Du hast alle .lp-Dateien importiert. Wie findest du schnell die Laufbahnen, die du klären musst?',
             ['Fachwahlen öffnen und Zahlen vergleichen', 'In der Laufbahnplanung den Filter „Nur Fehler“ setzen', 'Die Dateien noch einmal importieren'], 1,
             'Filter „Nur Fehler“ setzen und die fehlerhaften Laufbahnen einzeln klären (SL-O-02).', 'SL-O-02'),
            ('Welche Fehlerquelle in der Laufbahnplanung nennt die Hilfe ausdrücklich?',
             ['Die Sprachenfolge', 'Die Schriftgröße', 'Die Klassenbezeichnung'], 0,
             'Die Sprachenfolge ist eine häufige Fehlerquelle, oben rechts gibt es dazu einen Link (SL-O-02).', 'SL-O-02'),
            ('Wann sollten die Fachwahlen vollständig sein?',
             ['Erst nach dem Übertragen', 'Vor der Blockung', 'Egal, die Blockung passt sich an'], 1,
             'Die Doku empfiehlt, die Fachwahlen vollständig zu haben, bevor man blockt (SL-O-03).', 'SL-O-03'),
        ],
    },
    {
        'datei': SEITE, 'anker': 'blockung', 'titel': 'Blockung: anlegen bis übertragen', 'icon': '🧩',
        'kurz': 'Schienen und Kurse, Regeln und Fixierungen, berechnen, aktivieren, übertragen, Q2-Blockung.',
        'eintraege': ['SL-O-04', 'SL-O-05', 'SL-O-06', 'SL-O-07', 'SL-O-12'], 'ablauf': [3, 4, 5, 6, 7],
        'check': [
            ('In der Kursplanung steht bei einem Kurs „14|3“. Was bedeutet das?',
             ['14 Schüler, 3 Schienen', '14 eigene und 3 externe Schüler', '14 Wochenstunden, 3 Lehrkräfte'], 1,
             'Lesehilfe aus SL-O-04: 14 eigene und 3 externe Schüler.', 'SL-O-04'),
            ('Ein Kurs soll nicht weiter wachsen. Was hilft?',
             ['Den Kurs fixieren (Pinnnadel)', 'Eine Regel mit maximaler Schülerzahl', 'Die Schiene sperren'], 1,
             'Nur eine Regel mit maximaler Schülerzahl verhindert das. Fixieren allein reicht nicht (SL-O-05).', 'SL-O-05'),
            ('Was übernimmt „Synchronisieren“ NICHT?',
             ['Einen Lehrkraftwechsel', 'Einen Schienenwechsel', 'Neu gewählte Fächer, Abwahlen und gelöschte Kurse'], 2,
             'Neu gewählte Fächer, Abwahlen und gelöschte Kurse musst du manuell nachtragen (SL-O-07, SL-O-10).', 'SL-O-07'),
            ('Ab wann ist Synchronisieren nicht mehr möglich?',
             ['Sobald Noten, Bemerkungen oder Fehlstunden eingetragen sind', 'Nach 14 Tagen', 'Sobald eine zweite Blockung existiert'], 0,
             'Mit eingetragenen Noten, Bemerkungen oder Fehlstunden geht Synchronisieren nicht mehr (SL-O-07).', 'SL-O-07'),
            ('Du willst die Q2 auf Basis der Q1-Blockung blocken. Was ist nötig?',
             ['Das Q1-Ergebnis einmal nach Q2.2 kopieren', 'Das Q1-Ergebnis zweimal hochschreiben: erst Q1.2, dann Q2.1', 'Eine neue, leere Blockung anlegen'], 1,
             'Zweimal hochschreiben (Q1.2, dann Q2.1) und unter Schülerzuordnung „Schüler in Ziel-Kursen fixieren“ (SL-O-12).', 'SL-O-12'),
        ],
    },
    {
        'datei': SEITE, 'anker': 'umwahlen', 'titel': 'Umwahlen & Sonderfälle', 'icon': '🔁',
        'kurz': 'Umwahldialog, Wahlen vor und nach dem Übertragen ändern, Sportattest, Abgang, Zugang.',
        'eintraege': ['SL-O-08', 'SL-O-09', 'SL-O-10', 'SL-O-11'], 'ablauf': [8],
        'check': [
            ('Eine Schülerin soll von GKM auf GKS wechseln. Die Blockung ist noch nicht übertragen. Wo änderst du das?',
             ['Im Umwahldialog per Drag & Drop', 'In der Laufbahnplanung', 'In SchILD-NRW 3 unter Kataloge → Kurse'], 1,
             'Die Kursart lässt sich im Umwahldialog nicht ändern. Vor dem Übertragen: in der Laufbahnplanung (SL-O-08, SL-O-09).', 'SL-O-09'),
            ('Nach dem Übertragen wählt ein Schüler einen Kurs ab. Was ist der erste Schritt?',
             ['In den Leistungsdaten das Fach im richtigen Lernabschnitt löschen', 'In der Kursplanung den Kurs löschen', 'Die Blockung neu berechnen'], 0,
             'Erst Leistungsdaten (richtiger Lernabschnitt), dann Laufbahnplanung, dann „Ungültige Kurszuordnung“ löschen (SL-O-10).', 'SL-O-10'),
            ('Ein Schüler hat ein Sportattest. Womit beginnst du?',
             ['Mit einem neuen Sportkurs in der Blockung', 'In den Leistungsdaten bei Sport die Note AT setzen', 'Mit einer Mail an die Schulleitung'], 1,
             'Note AT in den Leistungsdaten, die Laufbahnplanung passt Kursart und Stunden an, dann Ersatzfach anlegen (SL-O-11).', 'SL-O-11'),
            ('Was lässt sich im Umwahldialog NICHT ändern?',
             ['Den Kurs innerhalb derselben Kursart', 'Die Kursart (z. B. GKS ↔ GKM)', 'Die Fixierung eines Schülers'], 1,
             'Die Kursart ändert man über die Laufbahnplanung bzw. nach dem Übertragen in den Leistungsdaten (SL-O-08).', 'SL-O-08'),
        ],
    },
]

# Schritt des Ablaufs (SL-O-00) → Ziel-Eintrag
ABLAUF_ZIEL = {1: 'SL-O-02', 2: 'SL-O-03', 3: 'SL-O-04', 4: 'SL-O-05', 5: 'SL-O-06',
               6: 'SL-O-07', 7: 'SL-O-07', 8: 'SL-O-08'}

ZIEL_SEITE = {s_id: s['datei'] for s in SEITEN for s_id in s['eintraege']}

QUELL_LINKS = [  # Stichwort in der Quellenangabe → Adresse (aus dem Quellenteil der Wissensdatei)
    ('„Kursplanung“', 'https://doku.svws-nrw.de/svws-client/apps/gost/kursplanung/'),
    ('„Fachwahlen“', 'https://doku.svws-nrw.de/svws-client/apps/gost/fachwahlen/'),
    ('„Laufbahnplanung“', 'https://doku.svws-nrw.de/svws-client/apps/gost/laufbahn/'),
    ('Wiki', 'https://schulverwaltungsinfos.nrw.de/svws/wiki/index.php?title=Kurse_%28Schulbezogene_Kataloge%29'),
    ('Schulungsunterlagen', 'https://svws-nrw.github.io/Schulungsunterlagen/'),
    ('SchulMail', 'https://www.schulministerium.nrw/14072026-informationen-einfuehrung-svws-server'),
    ('Informationen zur Umstellung', 'https://www.schulministerium.nrw/system/files/media/document/file/informationen_umstellung_svws-server.pdf'),
]
FACHBERATER = 'https://www.svws.nrw.de/service/fachberatersuche'
FORUM = 'https://schulverwaltungsinfos.nrw.de/svws/forum/viewforum.php?f=87'
DOKU = 'https://doku.svws-nrw.de'
WEBLUPO = 'https://doku.svws-nrw.de/svws-client/anleitungen/anleitungen_schulform/anleitungen_gost/weblupo/'


# ---------------------------------------------------------------- Parser
def lies_wissen(datei):
    """Liest eine Wissensdatei. Rückgabe: (stand, eintraege{id: dict}, teil_c dict)."""
    text = open(os.path.join(HIER, datei), encoding='utf-8').read()
    m = re.search(r'Stand der Recherche:\s*(\d+\.\d+\.\d+)', text)
    stand = m.group(1) if m else ''
    eintraege, teil_c = {}, {'faelle': [], 'vorlage': [], 'weiter': ''}
    teil, akt, feld = None, None, None
    for zeile in text.split('\n'):
        if zeile.startswith('## '):
            teil = zeile[3:]
            akt = None
            continue
        if zeile.startswith('### '):
            m = re.match(r'### (\S+) · (.+)', zeile)
            eid, titel = m.group(1), re.sub(r'\*\*', '', m.group(2)).strip()
            bereich = 'Grundlagen' if 'Teil 0' in teil else ('Sek I' if 'Teil A' in teil else 'Oberstufe')
            prog = 'SVWS-Webclient' if 'Teil B' in teil else ''
            akt = {'id': eid, 'titel': titel, 'titel_md': m.group(2).strip(), 'bereich': bereich,
                   'programm': prog, 'felder': []}
            eintraege[eid] = akt
            feld = None
            continue
        if zeile.strip() == '---':
            akt = None
            continue
        if teil and teil.startswith('Teil C'):
            if zeile.startswith('- '):
                teil_c['faelle'].append(zeile[2:].strip())
            elif zeile.startswith('> '):
                teil_c['vorlage'].append(zeile[2:].strip())
            elif zeile.startswith('**Wenn der Admin'):
                teil_c['weiter'] = zeile.strip()
            continue
        if akt is None or not zeile.strip():
            continue
        m = re.match(r'- \*\*(.+?)\*\*\s*(\([^)]*\))?:?\s*(.*)$', zeile)
        if m:
            label = m.group(1).rstrip(':').strip()
            if m.group(2):
                label += ' ' + m.group(2)
            wert = m.group(3)
            if label == 'Bereich':
                akt['bereich'] = wert.strip()
            elif label == 'Programm':
                akt['programm'] = wert.strip()
            else:
                feld = {'label': label, 'text': wert.strip(), 'items': []}
                akt['felder'].append(feld)
            continue
        m = re.match(r'^(\s*)(\d+\.|-)\s+(.*)$', zeile)
        if m:
            einzug = len(m.group(1))
            art = 'ol' if m.group(2)[0].isdigit() else 'ul'
            if einzug == 0:  # oberste Ebene ohne Feldnamen (z. B. Ablauf SL-O-00)
                if feld is None or feld['label'] != 'Ablauf':
                    feld = {'label': 'Ablauf', 'text': '', 'items': []}
                    akt['felder'].append(feld)
                feld['items'].append((0, art, m.group(3)))
            elif feld is not None:
                feld['items'].append((einzug, art, m.group(3)))
    return stand, eintraege, teil_c


def feld(e, label):
    for f in e['felder']:
        if f['label'] == label:
            return f
    return None


# ---------------------------------------------------------------- Formatierung
PRUEF_TOKEN = '\u0001PRUEF\u0001'


def fmt(s):
    """Inline-Markdown → HTML (fett, Code, Klickpfad-Chips, Prüfhinweis)."""
    s = re.sub(r'\*\*„?an eurer Version prüfen“?\*\*|„?an eurer Version prüfen“?', PRUEF_TOKEN, s)
    s = html.escape(s, quote=False)

    def fett(m):
        inhalt = m.group(1)
        if '→' in inhalt:
            teile = [t.strip() for t in inhalt.split('→')]
            chips = '<span class="pfeil" aria-hidden="true">›</span>'.join(
                '<span class="chip">%s</span>' % t for t in teile)
            return '<span class="pfad" title="Klickpfad">%s</span>' % chips
        return '<strong>%s</strong>' % inhalt
    s = re.sub(r'\*\*(.+?)\*\*', fett, s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = s.replace(PRUEF_TOKEN, '<span class="pruefen">⚠️ an eurer Version prüfen</span>')
    s = re.sub(r'\b(SL-(?:G|O|S1)-\d\d)\b',
               lambda m: ('<a href="%s#%s">%s</a>' % (ZIEL_SEITE[m.group(1)], m.group(1), m.group(1)))
               if m.group(1) in ZIEL_SEITE else m.group(1), s)
    return s


def klartext(s):
    return re.sub(r'\*\*|`', '', s)


def liste(items):
    """[(einzug, art, text)] → verschachtelte HTML-Listen."""
    if not items:
        return ''
    raus, i = [], 0
    basis = items[0][0]
    art = items[0][1]
    cls = ' class="schritte"' if art == 'ol' else ''
    raus.append('<%s%s>' % (art, cls))
    while i < len(items):
        einzug, a, t = items[i]
        kinder = []
        j = i + 1
        while j < len(items) and items[j][0] > basis:
            kinder.append(items[j])
            j += 1
        raus.append('<li>%s%s</li>' % (fmt(t), liste(kinder)))
        i = j
    raus.append('</%s>' % art)
    return ''.join(raus)


def inline_schritte(text):
    """„1. a → 2. b → 3. c“ als nummerierte Liste."""
    if re.match(r'^1\.\s', text) and re.search(r'→\s*2\.', text):
        teile = re.split(r'\s*→\s*(?=\d+\.\s)', text)
        return '<ol class="schritte">%s</ol>' % ''.join(
            '<li>%s</li>' % fmt(re.sub(r'^\d+\.\s*', '', t)) for t in teile)
    return '<p>%s</p>' % fmt(text)


def quelle_html(text):
    teile = [t.strip() for t in text.split(';')]
    raus = []
    for t in teile:
        links = []
        for stich, url in QUELL_LINKS:
            if stich in t:
                links.append(url)
        # mehrere Doku-Seiten in einer Angabe: einzeln verlinken
        if t.startswith('SVWS-Doku') and len(links) > 1:
            namen = re.findall(r'„([^“]+)“', t)
            raus.append('SVWS-Doku: ' + ', '.join(
                '<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, html.escape(n))
                for n, u in zip(namen, links)))
        elif links:
            raus.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (links[0], html.escape(t)))
        else:
            raus.append(html.escape(t))
    return ' · '.join(raus)


PROG_BADGE = {'SVWS-Webclient': ('web', '🌐 SVWS-Webclient'), 'SchILD-NRW 3': ('schild', '🖥️ SchILD-NRW 3')}


def programme(p):
    return [k for k in PROG_BADGE if k in p]


def badges(e):
    b = ''.join('<span class="badge %s">%s</span>' % PROG_BADGE[k] for k in programme(e['programm']))
    zusatz = re.search(r'\(([^)]+)\)', e['programm'])
    if zusatz:
        b += '<span class="badge leise">%s</span>' % html.escape(zusatz.group(1))
    b += '<span class="badge bereich">%s</span>' % html.escape(e['bereich'])
    return b


KASTEN = {'Beispiel': ('beispiel', '💡 Beispiel aus dem Alltag'),
          'Beispiel 2': ('beispiel', '💡 Noch ein Beispiel'),
          'Fallstricke': ('warnung', '⚠️ Fallstricke')}
UEBERSCHRIFT = {'Wann brauche ich das?': '🕑 Wann brauche ich das?', 'Wann?': '🕑 Wann?',
                'Voraussetzungen': '✅ Voraussetzungen', 'Kurz erklärt': 'Kurz erklärt',
                'Schritte': '👣 Schritte'}
VERSTECKT = {'Frage an den Admin', 'Suchbegriffe', 'Quelle'}


def feld_html(f):
    label = f['label']
    inhalt = ''
    if f['text']:
        inhalt += inline_schritte(f['text'])
    inhalt += liste(f['items'])
    if label in KASTEN:
        cls, titel = KASTEN[label]
        return '<div class="kasten %s"><h4>%s</h4>%s</div>' % (cls, titel, inhalt)
    titel = UEBERSCHRIFT.get(label, html.escape(label))
    return '<section class="feld"><h4>%s</h4>%s</section>' % (titel, inhalt)


def admin_vorlage(e):
    f = feld(e, 'Frage an den Admin')
    if not f:
        return ''
    return klartext(f['text']).strip().strip('„“"')


def karte_html(e, glossar_eintraege=None):
    eid = e['id']
    teile = []
    if eid == 'SL-G-03' and glossar_eintraege:
        teile.append('<dl class="glossar">%s</dl>' % ''.join(
            '<dt>%s</dt><dd>%s</dd>' % (html.escape(f['label']), fmt(f['text']))
            for f in e['felder'] if f['label'] != 'Suchbegriffe'))
    else:
        for f in e['felder']:
            if f['label'] not in VERSTECKT:
                teile.append(feld_html(f))
    q = feld(e, 'Quelle')
    if q:
        teile.append('<p class="quelle"><b>Quelle:</b> %s</p>' % quelle_html(q['text']))
    s = feld(e, 'Suchbegriffe')
    such = html.escape(s['text']) if s else ''
    werkzeuge = ('<div class="werkzeuge">'
                 '<button type="button" class="knopf admin-knopf" data-id="%s" data-art="admin">✉️ Frage an den Admin</button>'
                 '<button type="button" class="knopf leise admin-knopf" data-id="%s" data-art="web">❓ Anleitung unklar? Ergänzung anfragen</button>'
                 '<button type="button" class="knopf leise druck-knopf" data-id="%s">🖨️ Karte drucken</button>'
                 '</div>') % (eid, eid, eid)
    return ('<article class="karte" id="%(id)s" data-such="%(such)s">'
            '<h3 class="karte-kopf"><button type="button" aria-expanded="false" aria-controls="%(id)s-inhalt">'
            '<span class="kid">%(id)s</span><span class="ktitel">%(titel)s</span>'
            '<span class="badges">%(badges)s</span><span class="auf" aria-hidden="true">▾</span></button></h3>'
            '<div class="karte-inhalt" id="%(id)s-inhalt" hidden>%(inhalt)s%(werkzeuge)s</div></article>') % {
        'id': eid, 'such': such, 'titel': fmt(e['titel_md']), 'badges': badges(e),
        'inhalt': ''.join(teile), 'werkzeuge': werkzeuge}


def glossar(eintraege):
    """Begriffe für Tooltips aus SL-G-03 (inkl. Abkürzungen wie „GKS (Grundkurs schriftlich)“)."""
    g = eintraege.get('SL-G-03')
    raus = []
    if not g:
        return raus
    for f in g['felder']:
        if f['label'] == 'Suchbegriffe':
            continue
        erkl = klartext(f['text'])
        abk = re.findall(r'([A-Z][A-Z0-9]+(?:/[A-Z][A-Z0-9]+)*) \(([^)]+)\)', erkl)
        if abk:
            for kuerzel, bed in abk:
                for k in kuerzel.split('/'):
                    raus.append({'w': k, 'e': '%s: %s' % (k, bed), 'abk': True})
            continue
        for wort in f['label'].split('/'):
            raus.append({'w': wort.strip(), 'e': erkl, 'abk': False})
    return raus


def such_text(e):
    t = [e['id'], e['titel']]
    for f in e['felder']:
        t.append(klartext(f['text']))
        t.extend(klartext(x[2]) for x in f['items'])
    return ' '.join(t)


def admin_daten(e, vorlage, seite):
    zeilen = []
    betreff = ''
    for z in vorlage:
        if z.startswith('Betreff:'):
            betreff = z[len('Betreff:'):].strip().replace('[ID]', e['id']).replace('[Titel]', e['titel'])
            continue
        if z.startswith('Programm:'):
            p = programme(e['programm'])
            if len(p) == 1:
                z = 'Programm: ' + p[0]
        if z.startswith('Was ich machen wollte:'):
            av = admin_vorlage(e)
            if av:
                z = 'Was ich machen wollte / meine Frage:\n' + av
        zeilen.append(z)
    p = programme(e['programm'])
    karte = '%s – %s' % (e['id'], e['titel']) if e['id'] != '[ID]' else '[welche Karte / welches Thema?]'
    web = {'betreff': 'SchILD-Hilfe Ergänzung %s' % (e['id'] if e['id'] != '[ID]' else '[Thema]') +
                      (' – %s' % e['titel'] if e['id'] != '[ID]' else ''),
           'text': '\n'.join([
               'Karte: ' + karte,
               'Programm: ' + (p[0] if len(p) == 1 else '[SVWS-Webclient / SchILD-NRW 3]'),
               'Bei welchem Schritt bin ich hängen geblieben: [ … ]',
               'Was ist in der Anleitung unklar oder fehlt: [ … ]',
               'Was ich im Programm stattdessen gesehen habe (Menüname, Knopf, Meldung): [ … ]',
               'So habe ich es am Ende gelöst (falls gelöst): [ … ]'])}
    return {'admin': {'betreff': betreff, 'text': '\n'.join(zeilen)}, 'web': web}


# ---------------------------------------------------------------- Seitenrahmen
CSS = r"""
:root{--bg:#f4f6f9;--fl:#fff;--rand:#d5dbe5;--text:#1b2533;--leise:#5b6778;--akzent:#1d4ed8;
  --web:#1d4ed8;--webl:#dbeafe;--schild:#166534;--schildl:#dcfce7;--warn:#9a3412;--warnl:#fff4e6;
  --bsp:#0f5e75;--bspl:#e8f6fa;--mark:#fde68a}
*{box-sizing:border-box}
html{scroll-padding-top:5.5rem}
body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  font-size:1.05rem;line-height:1.55}
a{color:var(--akzent)}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;z-index:99;background:#fff;padding:.5rem 1rem}
.kopf{position:sticky;top:0;z-index:20;background:#22303f;color:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.kopf-innen{max-width:1050px;margin:0 auto;padding:.6rem 1rem;display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}
.marke{font-weight:800;font-size:1.1rem;color:#fff;text-decoration:none;white-space:nowrap}
.marke small{font-weight:500;opacity:.8}
.suche{flex:1 1 260px;display:flex;gap:.4rem}
.suche input{flex:1;min-height:44px;padding:.5rem .8rem;border-radius:.6rem;border:2px solid #fff;font-size:1.05rem;font-family:inherit}
.suche input:focus{outline:3px solid #fde68a;outline-offset:1px}
.hinweis{background:#fff8db;color:#5c4400;border-bottom:1px solid #f1e2a6;font-size:1rem}
.hinweis div{max-width:1050px;margin:0 auto;padding:.35rem 1rem}
.reiter{max-width:1050px;margin:0 auto;padding:.6rem 1rem 0;display:flex;flex-wrap:wrap;gap:.4rem}
.reiter a,.reiter span{display:inline-flex;align-items:center;gap:.35rem;min-height:44px;padding:.45rem .9rem;border-radius:.6rem;
  border:2px solid var(--rand);background:#fff;color:var(--text);text-decoration:none;font-weight:600;font-size:1rem}
.reiter a[aria-current=page]{background:#22303f;border-color:#22303f;color:#fff}
.reiter span.aus{color:#8a94a3;border-style:dashed;cursor:default}
.reiter small{font-weight:500}
main{max-width:1050px;margin:0 auto;padding:1rem}
h1{font-size:1.65rem;margin:.6rem 0 .2rem;line-height:1.25}
.unter{color:var(--leise);margin:0 0 1rem}
.knopf{display:inline-flex;align-items:center;gap:.35rem;min-height:44px;padding:.45rem 1rem;border-radius:.6rem;border:2px solid #22303f;
  background:#22303f;color:#fff;font:inherit;font-weight:700;cursor:pointer;text-decoration:none}
.knopf.leise{background:#fff;color:#22303f}
.knopf:focus-visible,button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #f59e0b;outline-offset:2px}
.leiste{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.3rem 0 1rem}
.karte{background:var(--fl);border:1px solid var(--rand);border-radius:.9rem;margin:0 0 .8rem;overflow:hidden}
.karte-kopf{margin:0;font-size:1rem}
.abschnitt{margin:0 0 2rem;scroll-margin-top:5.5rem}
.abschnitt>h2{font-size:1.45rem;margin:1.6rem 0 .2rem;padding-top:.6rem;border-top:3px solid #22303f}
.sprung{display:flex;flex-wrap:wrap;gap:.4rem;margin:.4rem 0 1rem}
.sprung a{display:inline-flex;align-items:center;min-height:44px;padding:.4rem .8rem;border-radius:.6rem;border:2px solid var(--rand);background:#fff;color:var(--text);text-decoration:none;font-weight:600}
.arten{display:flex;flex-direction:column;gap:.4rem;border:0;padding:0;margin:.6rem 0}
.arten legend{font-weight:700;margin-bottom:.3rem}
.arten label{display:flex!important;gap:.5rem;align-items:center;min-height:44px;margin:0!important;padding:.35rem .7rem;border:2px solid var(--rand);border-radius:.6rem;cursor:pointer;font-weight:600!important}
.arten input{width:1.15rem!important;height:1.15rem;margin:0;flex:0 0 auto}
.arten label:has(input:checked){border-color:#22303f;background:#eef1f6}
.karte-kopf button{all:unset;box-sizing:border-box;width:100%;display:flex;flex-wrap:wrap;gap:.35rem .7rem;align-items:center;
  padding:.8rem 1rem;cursor:pointer;min-height:56px}
.karte-kopf button:focus-visible{outline:3px solid #f59e0b;outline-offset:-3px}
.kid{font-family:ui-monospace,Consolas,monospace;font-size:1rem;background:#eef1f6;border-radius:.4rem;padding:.1rem .45rem;color:var(--leise)}
.ktitel{font-weight:750;font-size:1.15rem;flex:1 1 16rem}
.badges{display:flex;flex-wrap:wrap;gap:.3rem}
.badge{font-size:1rem;font-weight:700;border-radius:1rem;padding:.12rem .6rem;white-space:nowrap}
.badge.web{background:var(--webl);color:var(--web)}
.badge.schild{background:var(--schildl);color:var(--schild)}
.badge.bereich{background:#eef1f6;color:var(--leise)}
.badge.leise{background:#f5f6f8;color:var(--leise);font-weight:600}
.auf{transition:transform .2s;font-size:1.2rem;color:var(--leise)}
.karte.offen .auf{transform:rotate(180deg)}
.karte-inhalt{padding:0 1rem 1rem;border-top:1px solid #eef1f6}
.feld h4,.kasten h4{font-size:1.05rem;margin:1rem 0 .3rem}
.feld p,.kasten p{margin:.3rem 0}
ol.schritte{padding-left:0;list-style:none;counter-reset:s;margin:.4rem 0}
ol.schritte>li{counter-increment:s;position:relative;padding:.35rem 0 .35rem 2.6rem;font-size:1.12rem;line-height:1.5}
ol.schritte>li::before{content:counter(s);position:absolute;left:0;top:.3rem;width:1.9rem;height:1.9rem;border-radius:50%;
  background:#22303f;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:1rem}
ol.schritte ul,ol.schritte ol{font-size:1.02rem;margin:.25rem 0}
ul{padding-left:1.3rem}ul li{margin:.2rem 0}
.kasten{border-radius:.7rem;padding:.2rem .9rem .6rem;margin:.9rem 0;border-left:6px solid}
.kasten.beispiel{background:var(--bspl);border-color:var(--bsp)}
.kasten.beispiel h4{color:var(--bsp)}
.kasten.warnung{background:var(--warnl);border-color:#ea580c}
.kasten.warnung h4{color:var(--warn)}
.pfad{display:inline-flex;flex-wrap:wrap;align-items:center;gap:.15rem;vertical-align:baseline}
.chip{display:inline-block;font-size:1em;background:#fff;border:1.5px solid #64748b;border-radius:.45rem;padding:0 .45rem;font-weight:700;
  line-height:1.5;box-shadow:0 1px 0 #cbd5e1}
.pfeil{color:var(--leise);font-weight:800;padding:0 .1rem}
.pruefen{display:inline-block;background:#fef3c7;color:#7c4a03;border:1px dashed #d97706;border-radius:.4rem;padding:0 .4rem;
  font-weight:700}
code{background:#eef1f6;border-radius:.3rem;padding:0 .3rem}
.quelle{font-size:1rem;color:var(--leise);margin-top:1rem}
.werkzeuge{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;padding-top:.8rem;border-top:1px dashed var(--rand)}
dl.glossar{display:grid;grid-template-columns:minmax(9rem,max-content) 1fr;gap:.45rem 1rem;margin:1rem 0}
dl.glossar dt{font-weight:800}dl.glossar dd{margin:0}
.begriff{border-bottom:2px dotted #64748b;cursor:help;position:relative}
.begriff .tip{display:none;position:absolute;left:0;top:calc(100% + 6px);z-index:30;width:max-content;max-width:min(22rem,80vw);
  background:#22303f;color:#fff;font-size:1rem;font-weight:500;line-height:1.4;padding:.5rem .7rem;border-radius:.5rem;
  box-shadow:0 4px 12px rgba(0,0,0,.25);white-space:normal}
.begriff:hover .tip,.begriff:focus .tip{display:block}
mark{background:var(--mark);color:inherit;border-radius:.2rem;padding:0 .1rem}
.leer{color:var(--leise);font-style:italic}
.kacheln{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.7rem;margin:.6rem 0 1.4rem}
.kachel{display:block;background:#fff;border:1px solid var(--rand);border-radius:.9rem;padding:.9rem 1rem;color:var(--text);text-decoration:none}
.kachel:hover{border-color:#22303f}
.kachel b{display:block;font-size:1.1rem;margin-bottom:.25rem}
.kachel span{color:var(--leise);font-size:1rem}
.ablauf{list-style:none;padding:0;margin:.5rem 0 1.4rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.5rem;counter-reset:a}
.ablauf li{counter-increment:a}
.ablauf a{display:flex;gap:.6rem;align-items:flex-start;min-height:44px;background:#fff;border:1px solid var(--rand);border-radius:.7rem;
  padding:.6rem .7rem;text-decoration:none;color:var(--text);height:100%}
.ablauf a::before{content:counter(a);flex:0 0 1.9rem;height:1.9rem;border-radius:50%;background:#22303f;color:#fff;font-weight:800;
  display:flex;align-items:center;justify-content:center}
.ablauf a.hier{border:2px solid #22303f;background:#eef1f6}
.ablauf.klein{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));font-size:1rem}
.ablauf small{display:block;color:var(--leise)}
.block{background:#fff;border:1px solid var(--rand);border-radius:.9rem;padding:.4rem 1.1rem 1rem;margin:0 0 1.2rem}
.block h2{font-size:1.25rem;margin:.8rem 0 .4rem}
.filter{display:flex;flex-wrap:wrap;gap:.5rem;margin:.2rem 0 .8rem}
.filter label{display:flex;flex-direction:column;font-size:1rem;font-weight:700;color:var(--leise)}
.filter select{min-height:44px;font:inherit;font-size:1rem;padding:.3rem .5rem;border-radius:.5rem;border:2px solid var(--rand);background:#fff;color:var(--text)}
.treffer{list-style:none;padding:0;margin:0}
.treffer li{background:#fff;border:1px solid var(--rand);border-radius:.8rem;margin:0 0 .5rem}
.treffer a{display:block;padding:.7rem 1rem;color:var(--text);text-decoration:none}
.treffer a:hover{border-color:#22303f;background:#f8fafc}
.treffer .ttitel{font-weight:750;font-size:1.08rem}
.treffer .tsnip{color:var(--leise);font-size:1rem;margin-top:.2rem}
.check{background:#fff;border:2px solid #22303f;border-radius:.9rem;padding:.4rem 1.1rem 1rem;margin:1.6rem 0 1rem}
.check h2{font-size:1.25rem;margin:.8rem 0 .2rem}
.frage{border:1px solid var(--rand);border-radius:.7rem;padding:.6rem .9rem;margin:.8rem 0}
.frage legend{font-weight:750;padding:0 .3rem;font-size:1.05rem}
.frage label{display:flex;gap:.6rem;align-items:center;min-height:44px;padding:.3rem .6rem;border:2px solid transparent;border-radius:.6rem;cursor:pointer}
.frage label:hover{background:#f5f7fa}
.frage input{width:1.25rem;height:1.25rem;flex:0 0 auto;margin:0}
.frage label.richtig{border-color:#15803d;background:#ecfdf3}
.frage label.falsch{border-color:#b91c1c;background:#fef2f2}
.rueck{margin:.4rem 0 0;font-weight:600}
.rueck.ok{color:#15803d}.rueck.nok{color:#b91c1c}
.rueck a{font-weight:700}
.ergebnis{font-weight:800;font-size:1.1rem;min-height:1.5rem}
.weiter{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;margin:1.5rem 0 3rem}
.fuss{max-width:1050px;margin:0 auto 2rem;padding:0 1rem;color:var(--leise);font-size:1rem}
dialog.admin{width:min(40rem,calc(100vw - 1.5rem));border:2px solid #22303f;border-radius:.9rem;padding:1.1rem;color:var(--text);
  font-family:inherit;font-size:1rem;max-height:calc(100vh - 1.5rem)}
dialog.admin::backdrop{background:rgba(34,48,63,.5)}
dialog.admin h2{margin:0 0 .3rem;font-size:1.2rem}
dialog.admin label{display:block;font-weight:700;margin:.6rem 0 .2rem}
dialog.admin input,dialog.admin textarea{width:100%;font:inherit;font-size:1rem;padding:.5rem .6rem;border:2px solid var(--rand);border-radius:.6rem;color:var(--text)}
dialog.admin textarea{min-height:11rem;line-height:1.45}
dialog.admin input:focus,dialog.admin textarea:focus{outline:none;border-color:#22303f}
.datenschutz{background:#fef2f2;border-left:5px solid #b91c1c;padding:.45rem .7rem;border-radius:.5rem;margin:.7rem 0;font-weight:600}
.dlg-knoepfe{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.8rem}
.meldung{min-height:1.4rem;font-weight:700;margin:.5rem 0 0}
.meldung.ok{color:#15803d}.meldung.nok{color:#b91c1c}
@media (max-width:600px){body{font-size:1rem}.ktitel{font-size:1.05rem}ol.schritte>li{font-size:1.05rem}
  dl.glossar{grid-template-columns:1fr}dl.glossar dd{margin-bottom:.4rem}.kopf-innen{padding:.5rem .7rem}}
@media print{
  .kopf,.reiter,.leiste,.werkzeuge,.check,.weiter,.fuss,dialog,.skip,.filter,.auf{display:none!important}
  body{background:#fff;font-size:11.5pt}.hinweis{border:0;background:none}
  .karte{break-inside:avoid;border:1px solid #999}.karte-inhalt{display:block!important}
  .begriff{border:0}.begriff .tip{display:none!important}
  body.druck-einzeln main>*:not(.karten),body.druck-einzeln .abschnitt:not(.druck-ziel):not(:has(.druck-ziel)),body.druck-einzeln .abschnitt:has(.karte.druck-ziel)>:not(.druck-ziel),body.druck-einzeln .hinweis{display:none!important}
  .abschnitt>h2{border-top:0}.check{display:none!important}
  .karte[data-aus]{display:none!important}
  a{color:inherit;text-decoration:none}
}
"""

JS_GEMEINSAM = r"""
var ADMIN_NAME = '%(name)s', ADMIN_DOMAIN = '%(domain)s';   /* Adressen: nur in baue_schild3.py ändern */
var WEB_NAME = '%(wname)s', WEB_DOMAIN = '%(wdomain)s';
var GLOSSAR = %(glossar)s;
var ADMIN = %(admin)s;

function norm(s){ return (s||'').toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss'); }
function woerter(q){ return norm(q).split(/[\s,;]+/).filter(function(w){ return w.length > 0; }); }
function regexFuer(w){
  var t = w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')
           .replace(/ae/g,'(?:ae|ä)').replace(/oe/g,'(?:oe|ö)').replace(/ue/g,'(?:ue|ü)').replace(/ss/g,'(?:ss|ß)');
  return t;
}
function markiere(wurzel, liste){
  entmarkiere(wurzel);
  if (!liste.length) return;
  var re = new RegExp('(' + liste.map(regexFuer).join('|') + ')', 'gi');
  var gang = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT, null), knoten = [], n;
  while ((n = gang.nextNode())) { if (n.parentNode.closest('.tip,script,style')) continue; knoten.push(n); }
  knoten.forEach(function(k){
    var t = k.nodeValue; re.lastIndex = 0;
    if (!re.test(t)) return;
    var frag = document.createDocumentFragment(), last = 0; re.lastIndex = 0; var m;
    while ((m = re.exec(t))) {
      if (m[0].length === 0) { re.lastIndex++; continue; }
      frag.appendChild(document.createTextNode(t.slice(last, m.index)));
      var mk = document.createElement('mark'); mk.textContent = m[0]; frag.appendChild(mk);
      last = m.index + m[0].length;
    }
    frag.appendChild(document.createTextNode(t.slice(last)));
    k.parentNode.replaceChild(frag, k);
  });
}
function entmarkiere(wurzel){
  wurzel.querySelectorAll('mark').forEach(function(m){ m.replaceWith(document.createTextNode(m.textContent)); });
  wurzel.normalize();
}

/* Glossar-Tooltips: jeweils das erste Vorkommen eines Begriffs pro Karte */
function glossarAnwenden(wurzel){
  wurzel.querySelectorAll('.karte-inhalt').forEach(function(inhalt){
    if (inhalt.closest('#SL-G-03')) return;
    var gesehen = {};
    GLOSSAR.forEach(function(g){
      if (gesehen[g.w]) return;
      var re = g.abk ? new RegExp('(^|[^A-Za-zÄÖÜäöü0-9])(' + g.w + ')(?![A-Za-zÄÖÜäöü0-9])')
                     : new RegExp('(^|[^A-Za-zÄÖÜäöüß])(' + g.w + ')', 'i');
      var gang = document.createTreeWalker(inhalt, NodeFilter.SHOW_TEXT, null), n;
      while ((n = gang.nextNode())) {
        if (n.parentNode.closest('.begriff,.chip,a,code,h4,.werkzeuge,mark')) continue;
        var m = re.exec(n.nodeValue);
        if (!m) continue;
        var start = m.index + m[1].length, ende = start + m[2].length;
        var rest = n.splitText(start); rest.splitText(ende - start);
        var sp = document.createElement('span');
        sp.className = 'begriff'; sp.tabIndex = 0;
        sp.setAttribute('aria-label', rest.nodeValue + ' – ' + g.e);
        sp.textContent = rest.nodeValue;
        var tip = document.createElement('span'); tip.className = 'tip'; tip.setAttribute('aria-hidden','true'); tip.textContent = g.e;
        sp.appendChild(tip);
        rest.parentNode.replaceChild(sp, rest);
        gesehen[g.w] = true;
        break;
      }
    });
  });
}

/* Karten auf- und zuklappen */
function oeffne(karte, auf){
  var b = karte.querySelector('.karte-kopf button'), inh = karte.querySelector('.karte-inhalt');
  if (auf === undefined) auf = inh.hidden;
  inh.hidden = !auf; b.setAttribute('aria-expanded', auf ? 'true' : 'false');
  karte.classList.toggle('offen', auf);
}
document.querySelectorAll('.karte-kopf button').forEach(function(b){
  b.addEventListener('click', function(){ oeffne(b.closest('.karte')); });
});
function alleKarten(auf){ document.querySelectorAll('.karte').forEach(function(k){ if (!k.dataset.aus) oeffne(k, auf); }); }

/* Drucken */
function drucke(karte){
  var offen = [];
  document.querySelectorAll('.karte').forEach(function(k){ offen.push([k, !k.querySelector('.karte-inhalt').hidden]); });
  if (karte) {
    document.body.classList.add('druck-einzeln'); karte.classList.add('druck-ziel');
    if (karte.classList.contains('karte')) oeffne(karte, true);
    else karte.querySelectorAll('.karte').forEach(function(k){ oeffne(k, true); });
  } else alleKarten(true);
  var fertig = function(){
    document.body.classList.remove('druck-einzeln');
    if (karte) karte.classList.remove('druck-ziel');
    offen.forEach(function(p){ oeffne(p[0], p[1]); });
    window.removeEventListener('afterprint', fertig);
  };
  window.addEventListener('afterprint', fertig);
  window.print();
}
document.querySelectorAll('.druck-knopf').forEach(function(b){
  b.addEventListener('click', function(){ drucke(b.closest('.karte')); });
});

/* Frage an den Admin */
(function(){
  var dlg = document.getElementById('admin-dlg');
  if (!dlg) return;
  var adresse = '', aktId = 'allgemein';
  var betreff = document.getElementById('admin-betreff'), text = document.getElementById('admin-text');
  var meldung = document.getElementById('admin-meldung'), erinnert = false;
  function melde(t, ok){ meldung.textContent = t; meldung.className = 'meldung ' + (ok ? 'ok' : 'nok'); }
  function art(){ var r = dlg.querySelector('input[name="frage-art"]:checked'); return r ? r.value : 'admin'; }
  function fuelle(){
    var a = art(), d = (ADMIN[aktId] || ADMIN['allgemein'])[a];
    adresse = a === 'web' ? WEB_NAME + '@' + WEB_DOMAIN : ADMIN_NAME + '@' + ADMIN_DOMAIN;
    document.getElementById('admin-adresse').textContent = adresse;
    document.getElementById('web-hinweis').hidden = a !== 'web';
    betreff.value = d.betreff;
    text.value = d.text + '\n\n(Aus der SchILD-Hilfe: ' + location.href.split('#')[0].split('?')[0] + (aktId !== 'allgemein' ? '#' + aktId : '') + ')';
    melde('', true); erinnert = false;
    text.focus(); text.scrollTop = 0;
    var p = text.value.indexOf('[');
    if (p >= 0) { text.setSelectionRange(p, text.value.indexOf(']', p) + 1); }
  }
  function oeffneDlg(id, a){
    aktId = id || 'allgemein';
    dlg.querySelector('input[name="frage-art"][value="' + (a || 'admin') + '"]').checked = true;
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    fuelle();
  }
  window.adminFrage = oeffneDlg;
  dlg.querySelectorAll('input[name="frage-art"]').forEach(function(r){
    r.addEventListener('change', function(){
      var geaendert = text.value.indexOf('[') < 0 || erinnert;
      fuelle();
      if (geaendert) melde('Hinweis: Der Text wurde für die neue Auswahl neu vorausgefüllt.', true);
    });
  });
  document.querySelectorAll('.admin-knopf').forEach(function(b){
    b.addEventListener('click', function(){ oeffneDlg(b.dataset.id, b.dataset.art); });
  });
  function platzhalterOffen(){
    if (erinnert) return false;
    if (/\[[^\]]*\]/.test(betreff.value + text.value)) {
      erinnert = true;
      melde('Es stehen noch Platzhalter in [eckigen Klammern] im Text. Bitte ergänzen oder löschen – oder noch einmal klicken, um trotzdem fortzufahren.', false);
      return true;
    }
    return false;
  }
  function ganz(){ return 'Betreff: ' + betreff.value + '\n\n' + text.value; }
  document.getElementById('admin-senden').addEventListener('click', function(){
    if (platzhalterOffen()) return;
    location.href = 'mailto:' + adresse + '?subject=' + encodeURIComponent(betreff.value) + '&body=' + encodeURIComponent(text.value);
    melde('Das Mailprogramm öffnet sich.', true);
  });
  document.getElementById('admin-kopieren').addEventListener('click', function(){
    if (platzhalterOffen()) return;
    var t = ganz();
    function ersatz(){
      var ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      melde(ok ? 'Kopiert! Jetzt in Mail, Messenger oder Ticket einfügen.' : 'Kopieren ging nicht – bitte Text markieren und kopieren.', ok);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function(){ melde('Kopiert! Jetzt in Mail, Messenger oder Ticket einfügen.', true); }, ersatz);
    else ersatz();
  });
  document.getElementById('admin-zu').addEventListener('click', function(){
    if (typeof dlg.close === 'function') dlg.close(); else dlg.removeAttribute('open');
  });
})();
"""

DIALOG = """
<dialog class="admin" id="admin-dlg" aria-labelledby="admin-titel">
  <h2 id="admin-titel">✉️ Frage stellen</h2>
  <fieldset class="arten">
    <legend>Worum geht es?</legend>
    <label><input type="radio" name="frage-art" value="admin" checked><span>🛠️ Problem im Programm (Rechte, Fehlermeldung, ausgegraut) → <b>Admin</b></span></label>
    <label><input type="radio" name="frage-art" value="web"><span>❓ Bedienung bleibt unklar, in der Anleitung fehlt etwas → <b>Verwalter dieser Hilfe</b></span></label>
  </fieldset>
  <p>Ergänze die Stellen in <b>[eckigen Klammern]</b>. Der Rest ist schon vorausgefüllt.</p>
  <label for="admin-betreff">Betreff</label>
  <input id="admin-betreff" type="text">
  <label for="admin-text">Nachricht</label>
  <textarea id="admin-text"></textarea>
  <p class="datenschutz">🔒 Keine Schülerdaten (Namen, Noten) per E-Mail senden. Nutze stattdessen die ID oder ein Kürzel.</p>
  <div class="dlg-knoepfe">
    <button type="button" class="knopf" id="admin-senden">✉️ Per E-Mail senden</button>
    <button type="button" class="knopf leise" id="admin-kopieren">📋 Text kopieren</button>
    <button type="button" class="knopf leise" id="admin-zu">Schließen</button>
  </div>
  <p class="meldung" id="admin-meldung" aria-live="polite"></p>
  <p>Kein Mailprogramm? Text kopieren und an <b id="admin-adresse"></b> schicken.</p>
  <p class="unter" id="web-hinweis" hidden>Danke! Mit deiner Rückmeldung wird die Anleitung ergänzt, damit die Nächsten nicht an derselben Stelle hängen bleiben.</p>
</dialog>
"""


def kopf(titel, aktiv, stand, such_platzhalter, such_ziel_index):
    reiter = ['<a href="index.html"%s>🏠 Übersicht</a>' % (' aria-current="page"' if aktiv == 'index.html' else '')]
    reiter.append('<a href="%s"%s>🎓 Oberstufe – Stufenleitung &amp; Koordination</a>' % (
        SEITE, ' aria-current="page"' if aktiv == SEITE else ''))
    such = ('<form class="suche" role="search" action="index.html" method="get" id="suchform">'
            '<label for="q" class="skip">Suche</label>'
            '<input id="q" name="q" type="search" autocomplete="off" placeholder="%s">'
            '</form>') % such_platzhalter
    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="SchILD-NRW 3 / SVWS – Hilfe zum Selberlernen für die Oberstufenleitung: %(titel)s">
<meta name="keywords" content="SchILD-NRW 3, SVWS, Oberstufe, Laufbahnplanung, Kursplanung, Blockung">
<meta name="hubignore" content="1">
<title>%(titel)s – SchILD-Hilfe Oberstufe</title>
<style>%(css)s</style>
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf"><div class="kopf-innen">
  <a class="marke" href="index.html">SchILD-Hilfe <small>· Oberstufenleitung</small></a>
  %(such)s
</div></header>
<div class="hinweis" role="note"><div>📅 Stand: %(stand)s. Menünamen können sich nach Updates ändern (SVWS-Server und SchILD-NRW 3 werden quartalsweise aktualisiert).</div></div>
<nav class="reiter" aria-label="Themen der Oberstufenleitung">%(reiter)s</nav>
""" % {'titel': html.escape(titel), 'css': CSS, 'such': such, 'stand': stand, 'reiter': ''.join(reiter)}


def fuss(js):
    return """
<p class="fuss">Hilfe für Kolleginnen und Kollegen am MCG. Grundlage: offizielle SVWS-Dokumentation, SchILD-NRW-3-Wiki und
SVWS-Schulungsunterlagen. Etwas unklar oder fehlt? Auf jeder Karte „Anleitung unklar? Ergänzung anfragen“ – die Anleitung wird dann ergänzt.</p>
%s
<script>
%s
</script>
</body>
</html>
""" % (DIALOG, js)


def ablauf_html(eintraege, ziel_seite, hier=None, klein=False):
    ab = feld(eintraege['SL-O-00'], 'Ablauf')
    li = []
    for nr, (_, _, t) in enumerate(ab['items'], 1):
        ref = re.search(r'\((SL-[^)]*)\)', t)
        ganz = klartext(re.sub(r'\s*\(SL-[^)]*\)', '', t)).strip()
        haupt, _, rest = ganz.partition(' – ')
        zid = ABLAUF_ZIEL[nr]
        cls = ' class="hier"' if hier and nr in hier else ''
        klein_txt = ' · '.join(x for x in [rest, ref.group(1) if ref else zid] if x)
        li.append('<li><a%s href="%s#%s"><span>%s<small>%s</small></span></a></li>' % (
            cls, ziel_seite[zid], zid, html.escape(haupt), html.escape(klein_txt)))
    return '<ol class="ablauf%s">%s</ol>' % (' klein' if klein else '', ''.join(li))


def check_html(s):
    k = s['anker']
    out = ['<section class="check" aria-labelledby="check-%s"><h3 id="check-%s" style="font-size:1.2rem;margin:.8rem 0 .2rem">🎯 Selbstcheck: %s</h3>'
           '<p class="unter">Kreuze jeweils eine Antwort an und klicke auf „Prüfen“. Nichts wird gespeichert oder verschickt.</p>'
           % (k, k, html.escape(s['titel']))]
    for i, (frage, opts, richtig, erkl, ref) in enumerate(s['check']):
        out.append('<fieldset class="frage" data-richtig="%d"><legend>%d. %s</legend>' % (richtig, i + 1, html.escape(frage)))
        for j, o in enumerate(opts):
            out.append('<label><input type="radio" name="%s-f%d" value="%d"> %s</label>' % (k, i, j, html.escape(o)))
        out.append('<p class="rueck" aria-live="polite" data-erkl="%s" data-ref="%s"></p></fieldset>' % (html.escape(erkl), ref))
    out.append('<div class="leiste"><button type="button" class="knopf pruefen">✔️ Prüfen</button>'
               '<button type="button" class="knopf leise leeren">↺ Leeren</button></div>'
               '<p class="ergebnis" aria-live="polite"></p></section>')
    return ''.join(out)


def oberstufe_seite(eintraege, stand, ziel_seite, admin, glo):
    out = [kopf('Oberstufe', SEITE, stand, 'Suchen, z. B. „Blockung übertragen“, „Attest“ …', True)]
    out.append('<main id="inhalt">')
    out.append('<h1>🎓 Oberstufe – Stufenleitung und Koordination</h1>'
               '<p class="unter">Alle Anleitungen für die gymnasiale Oberstufe, vom Einstieg bis zu Umwahlen und Sonderfällen. '
               'Jede Karte lässt sich aufklappen. Bleibt etwas unklar: auf der Karte „Anleitung unklar? Ergänzung anfragen“.</p>')
    out.append('<nav class="sprung" aria-label="Abschnitte">%s</nav>' % ''.join(
        '<a href="#%s">%s %s</a>' % (s['anker'], s['icon'], html.escape(s['titel'])) for s in SEITEN))
    out.append('<p class="unter" style="margin-bottom:.2rem"><b>🗺️ Ablauf auf einen Blick</b> – Klick öffnet die Anleitung:</p>')
    out.append(ablauf_html(eintraege, ziel_seite, klein=True))
    out.append('<div class="leiste">'
               '<label for="filter" class="skip">Auf dieser Seite filtern</label>'
               '<input id="filter" type="search" placeholder="Auf dieser Seite filtern …" '
               'style="flex:1 1 220px;min-height:44px;padding:.45rem .8rem;border-radius:.6rem;border:2px solid var(--rand);font:inherit">'
               '<button type="button" class="knopf leise" id="alle-auf">Alle aufklappen</button>'
               '<button type="button" class="knopf leise" id="alle-zu">Alle zuklappen</button>'
               '<button type="button" class="knopf leise" id="seite-drucken">🖨️ Alles drucken</button></div>')
    out.append('<p class="leer" id="keine" hidden>Nichts gefunden. Versuch ein anderes Wort – oder frag nach: '
               '<button type="button" class="knopf leise admin-knopf" data-id="allgemein" data-art="web">❓ Ergänzung anfragen</button></p>')
    out.append('<div class="karten">')
    for s in SEITEN:
        out.append('<section class="abschnitt" id="%s" aria-labelledby="%s-h"><h2 id="%s-h">%s %s</h2><p class="unter">%s</p>'
                   % (s['anker'], s['anker'], s['anker'], s['icon'], html.escape(s['titel']), html.escape(s['kurz'])))
        out.append('<div class="leiste"><button type="button" class="knopf leise druck-abschnitt">🖨️ Abschnitt drucken</button></div>')
        for eid in s['eintraege']:
            out.append(karte_html(eintraege[eid], glossar_eintraege=True))
        out.append(check_html(s))
        out.append('</section>')
    out.append('</div>')
    out.append('<nav class="weiter" aria-label="Weiter"><a class="knopf leise" href="index.html">← Übersicht</a>'
               '<a class="knopf" href="index.html#admin">Wann frage ich den Admin? →</a></nav>')
    out.append('</main>')
    js = JS_GEMEINSAM % {'name': ADMIN_NAME, 'domain': ADMIN_DOMAIN, 'wname': WEB_NAME, 'wdomain': WEB_DOMAIN,
                         'glossar': json.dumps(glo, ensure_ascii=False),
                         'admin': json.dumps(admin, ensure_ascii=False)}
    js += JS_THEMA
    out.append(fuss(js))
    return '\n'.join(out)


JS_THEMA = r"""
glossarAnwenden(document);
document.getElementById('alle-auf').addEventListener('click', function(){ alleKarten(true); });
document.getElementById('alle-zu').addEventListener('click', function(){ alleKarten(false); });
document.getElementById('seite-drucken').addEventListener('click', function(){ drucke(null); });

/* Filter auf dieser Seite */
var filter = document.getElementById('filter'), karten = document.querySelectorAll('.karte');
function filtere(){
  var w = woerter(filter.value), sichtbar = 0;
  karten.forEach(function(k){
    var hay = norm(k.textContent + ' ' + (k.dataset.such || ''));
    var ok = w.every(function(x){ return hay.indexOf(x) >= 0; });
    if (ok) { delete k.dataset.aus; k.hidden = false; sichtbar++; } else { k.dataset.aus = '1'; k.hidden = true; }
    markiere(k, w);
    if (w.length && ok) oeffne(k, true);
  });
  document.querySelectorAll('.abschnitt').forEach(function(a){
    a.hidden = !!w.length && !a.querySelector('.karte:not([hidden])');
    a.querySelector('.check').hidden = !!w.length;
  });
  document.getElementById('keine').hidden = sichtbar > 0;
}
filter.addEventListener('input', filtere);

/* Sprung per #ID: Karte öffnen */
function sprung(){
  var id = decodeURIComponent(location.hash.slice(1));
  var k = id && document.getElementById(id);
  if (k && k.classList.contains('karte')) { oeffne(k, true); k.scrollIntoView(); k.querySelector('.karte-kopf button').focus({preventScroll:true}); }
  else if (k) k.scrollIntoView();
}
window.addEventListener('hashchange', sprung);
var pq = new URLSearchParams(location.search).get('q');
if (pq) { filter.value = pq; filtere(); }
sprung();

/* Selbstcheck – je Abschnitt */
document.querySelectorAll('.check').forEach(function(c){
  c.querySelector('.pruefen').addEventListener('click', function(){
    var fragen = c.querySelectorAll('.frage'), punkte = 0, offen = 0;
    fragen.forEach(function(f){
      var r = f.querySelector('input:checked'), rueck = f.querySelector('.rueck'), richtig = f.dataset.richtig;
      f.querySelectorAll('label').forEach(function(l){ l.classList.remove('richtig','falsch'); });
      if (!r) { rueck.textContent = 'Noch keine Antwort gewählt.'; rueck.className = 'rueck nok'; offen++; return; }
      var ok = r.value === richtig;
      r.closest('label').classList.add(ok ? 'richtig' : 'falsch');
      rueck.className = 'rueck ' + (ok ? 'ok' : 'nok');
      rueck.innerHTML = '';
      rueck.appendChild(document.createTextNode(ok ? '✔ Richtig. ' + rueck.dataset.erkl + ' ' : '✘ Noch nicht. Lies noch einmal in der Karte nach: '));
      var a = document.createElement('a'); a.href = '#' + rueck.dataset.ref; a.textContent = rueck.dataset.ref; rueck.appendChild(a);
      if (ok) punkte++;
    });
    c.querySelector('.ergebnis').textContent = punkte + ' von ' + fragen.length + ' richtig' +
      (offen ? ' (' + offen + ' noch offen).' : (punkte === fragen.length ? ' – sehr gut!' : '.'));
  });
  c.querySelector('.leeren').addEventListener('click', function(){
    c.querySelectorAll('.frage').forEach(function(f){
      f.querySelectorAll('input').forEach(function(i){ i.checked = false; });
      f.querySelectorAll('label').forEach(function(l){ l.classList.remove('richtig','falsch'); });
      var r = f.querySelector('.rueck'); r.textContent = ''; r.className = 'rueck';
    });
    c.querySelector('.ergebnis').textContent = '';
  });
});
document.querySelectorAll('.druck-abschnitt').forEach(function(b){
  b.addEventListener('click', function(){ drucke(b.closest('.abschnitt')); });
});
"""


def start_seite(eintraege, stand, teil_c, ziel_seite, admin, glo):
    out = [kopf('Übersicht', 'index.html', stand, 'Suchen, z. B. „Blockung übertragen“, „Attest“, „LuPO“ …', False)]
    out.append('<main id="inhalt">')
    out.append('<h1>SchILD-NRW 3 / SVWS – Hilfe zum Selberlernen</h1>'
               '<p class="unter">Schritt-für-Schritt-Anleitungen für die Oberstufenleitung: suchen, nachlesen, ausprobieren. '
               'Auf jeder Karte gibt es zwei Knöpfe: <b>„Frage an den Admin“</b>, wenn im Programm etwas nicht geht, '
               'und <b>„Anleitung unklar? Ergänzung anfragen“</b>, wenn die Bedienung offen bleibt – dann wird die Hilfe ergänzt.</p>')
    # Rollen
    rollen = []
    for k, name, datei in ROLLEN:
        if datei and k == 'ost':
            rollen.append('<a href="%s">🎓 %s</a>' % (SEITE, html.escape(name)))
        else:
            rollen.append('<span class="aus" aria-disabled="true">%s <small>· in Vorbereitung</small></span>' % html.escape(name))
    out.append('<nav class="reiter" style="padding:0;margin:0 0 1rem" aria-label="Rollen">%s</nav>' % ''.join(rollen))
    # Suche
    out.append('<section class="block" aria-labelledby="such-titel"><h2 id="such-titel">🔎 Suche</h2>'
               '<div class="filter">'
               '<label>Bereich<select id="f-bereich"><option value="">alle</option><option>Grundlagen</option><option>Oberstufe</option></select></label>'
               '<label>Programm<select id="f-prog"><option value="">alle</option><option value="SVWS-Webclient">SVWS-Webclient</option><option value="SchILD-NRW 3">SchILD-NRW 3</option></select></label>'
               '<label>Rolle<select id="f-rolle"><option>Oberstufenleitung</option>%s</select></label>'
               '</div><p class="unter" id="such-info">Tippe oben ins Suchfeld. Umlaute, Groß-/Kleinschreibung und Wortteile sind egal.</p>'
               '<ul class="treffer" id="treffer"></ul></section>' % ''.join(
                   '<option disabled>%s (in Vorbereitung)</option>' % html.escape(n) for k, n, d in ROLLEN if k != 'ost'))
    # Themen
    out.append('<h2 id="themen" style="font-size:1.3rem;margin:1.4rem 0 .2rem">📚 Themen</h2><div class="kacheln">')
    for s in SEITEN:
        out.append('<a class="kachel" href="%s"><b>%s %s</b><span>%s</span></a>' % (
            s['datei'] + '#' + s['anker'], s['icon'], html.escape(s['titel']), html.escape(s['kurz'])))
    out.append('</div>')
    # Ablauf
    out.append('<h2 style="font-size:1.3rem;margin:1.4rem 0 .2rem">🗺️ Ablauf auf einen Blick (Oberstufe)</h2>'
               '<p class="unter">Klick auf einen Schritt öffnet die passende Anleitung.</p>')
    out.append(ablauf_html(eintraege, ziel_seite))
    # Teil C
    vorlage = '\n'.join(teil_c['vorlage'])
    weiter = klartext(teil_c['weiter'])
    weiter = html.escape(weiter)
    weiter = weiter.replace('Fachberatung', '<a href="%s" target="_blank" rel="noopener">Fachberatung</a>' % FACHBERATER, 1)
    weiter = weiter.replace('Anwenderforum', '<a href="%s" target="_blank" rel="noopener">Anwenderforum</a>' % FORUM, 1)
    weiter = weiter.replace('support@svws-nrw.de', '<a href="mailto:support@svws-nrw.de">support@svws-nrw.de</a>', 1)
    out.append('<section class="block" id="admin" aria-labelledby="admin-h"><h2 id="admin-h">🙋 Wann frage ich den Admin?</h2>'
               '<p>Typische Fälle, die die Stufenleitung <b>nicht</b> selbst lösen kann:</p><ul>%s</ul>'
               '<p><b>Allgemeine Vorlage für jede Admin-Frage</b> – auf jeder Karte ist sie schon passend vorausgefüllt:</p>'
               '<pre style="white-space:pre-wrap;background:#f5f7fa;border-radius:.6rem;padding:.7rem .9rem;font-size:.98rem">%s</pre>'
               '<p class="leiste"><button type="button" class="knopf admin-knopf" data-id="allgemein" data-art="admin">✉️ Allgemeine Frage an den Admin</button></p>'
               '<h3 style="font-size:1.1rem;margin:1.2rem 0 .3rem">❓ Bedienung unklar? Hilfe ergänzen lassen</h3>'
               '<p>Wenn du eine Anleitung befolgt hast und trotzdem nicht weiterkommst – ein Menü heißt anders, ein Schritt fehlt, '
               'ein Begriff ist unklar –, schick eine kurze Rückmeldung an den Verwalter dieser Hilfe. Die Anleitung wird dann ergänzt.</p>'
               '<p class="leiste"><button type="button" class="knopf leise admin-knopf" data-id="allgemein" data-art="web">❓ Ergänzung anfragen</button></p>'
               '<p>%s</p>'
               '<p>Zum Nachlesen: <a href="%s" target="_blank" rel="noopener">SVWS-Dokumentation</a> · '
               '<a href="%s" target="_blank" rel="noopener">WebLuPO-Anleitung</a></p></section>' % (
                   ''.join('<li>%s</li>' % fmt(f) for f in teil_c['faelle']), html.escape(vorlage), weiter, DOKU, WEBLUPO))
    out.append('</main>')
    index = []
    for s in SEITEN:
        for eid in s['eintraege']:
            e = eintraege[eid]
            sb = feld(e, 'Suchbegriffe')
            index.append({'id': eid, 'titel': e['titel'], 'bereich': e['bereich'], 'prog': programme(e['programm']),
                          'seite': s['datei'], 'seitentitel': s['titel'], 'text': such_text(e),
                          'such': klartext(sb['text']) if sb else ''})
    # SL-O-00 selbst ist auch suchbar
    e = eintraege['SL-O-00']
    index.append({'id': 'SL-O-00', 'titel': e['titel'], 'bereich': 'Oberstufe', 'prog': ['SVWS-Webclient'],
                  'seite': 'index.html', 'seitentitel': 'Übersicht', 'text': such_text(e),
                  'such': klartext(feld(e, 'Suchbegriffe')['text'])})
    js = JS_GEMEINSAM % {'name': ADMIN_NAME, 'domain': ADMIN_DOMAIN, 'wname': WEB_NAME, 'wdomain': WEB_DOMAIN,
                         'glossar': json.dumps(glo, ensure_ascii=False),
                         'admin': json.dumps(admin, ensure_ascii=False)}
    js += 'var INDEX = %s;\n' % json.dumps(index, ensure_ascii=False) + JS_START
    out.append(fuss(js))
    return '\n'.join(out)


JS_START = r"""
var q = document.getElementById('q'), liste = document.getElementById('treffer'), info = document.getElementById('such-info');
var fb = document.getElementById('f-bereich'), fp = document.getElementById('f-prog');
document.getElementById('suchform').addEventListener('submit', function(ev){ ev.preventDefault(); suche(); });
function schnipsel(text, w){
  var n = norm(text), p = -1;
  for (var i = 0; i < w.length && p < 0; i++) p = n.indexOf(w[i]);
  if (p < 0) return text.slice(0, 160) + (text.length > 160 ? ' …' : '');
  var a = Math.max(0, p - 60);
  return (a > 0 ? '… ' : '') + text.slice(a, a + 170) + (a + 170 < text.length ? ' …' : '');
}
function suche(){
  var w = woerter(q.value);
  liste.innerHTML = '';
  if (!w.length) { info.textContent = 'Tippe oben ins Suchfeld. Umlaute, Groß-/Kleinschreibung und Wortteile sind egal.'; history.replaceState(null, '', location.pathname); return; }
  var treffer = INDEX.filter(function(e){
    if (fb.value && e.bereich !== fb.value) return false;
    if (fp.value && e.prog.indexOf(fp.value) < 0) return false;
    var hay = norm(e.text + ' ' + e.such);
    return w.every(function(x){ return hay.indexOf(x) >= 0; });
  });
  treffer.sort(function(a, b){
    var pa = w.filter(function(x){ return norm(a.titel + ' ' + a.such).indexOf(x) >= 0; }).length;
    var pb = w.filter(function(x){ return norm(b.titel + ' ' + b.such).indexOf(x) >= 0; }).length;
    return pb - pa;
  });
  info.textContent = treffer.length ? treffer.length + (treffer.length === 1 ? ' Treffer' : ' Treffer') + ':' :
    'Nichts gefunden. Versuch ein anderes Wort – oder frag den Admin (unten).';
  treffer.forEach(function(e){
    var li = document.createElement('li'), a = document.createElement('a');
    a.href = e.seite + '?q=' + encodeURIComponent(q.value) + '#' + e.id;
    if (e.seite === 'index.html') a.href = '#themen';
    a.innerHTML = '<div class="ttitel"></div><div class="tsnip"></div>';
    a.querySelector('.ttitel').textContent = e.id + ' · ' + e.titel + '  (' + e.seitentitel + ')';
    a.querySelector('.tsnip').textContent = schnipsel(e.text, w);
    li.appendChild(a); liste.appendChild(li);
  });
  markiere(liste, w);
  history.replaceState(null, '', location.pathname + '?q=' + encodeURIComponent(q.value));
}
q.addEventListener('input', suche); fb.addEventListener('change', suche); fp.addEventListener('change', suche);
var pq = new URLSearchParams(location.search).get('q');
if (pq) { q.value = pq; suche(); }
"""

# Themenseiten: die Suche oben springt zur Übersicht (dort ist der Index)
JS_THEMA = r"""
document.getElementById('suchform').addEventListener('submit', function(ev){
  ev.preventDefault(); location.href = 'index.html?q=' + encodeURIComponent(document.getElementById('q').value);
});
""" + JS_THEMA


# ---------------------------------------------------------------- Bauen
def main():
    stand, eintraege, teil_c = lies_wissen('schild3_stufenleitung.md')
    glo = glossar(eintraege)
    ziel_seite = {}
    for s in SEITEN:
        for eid in s['eintraege']:
            if eid not in eintraege:
                raise SystemExit('Eintrag %s fehlt in der Wissensdatei' % eid)
            ziel_seite[eid] = s['datei']
    for s in SEITEN:
        for _, _, _, _, ref in s['check']:
            assert ref in ziel_seite, ref
    admin = {}
    for eid, e in eintraege.items():
        if eid in ziel_seite:
            admin[eid] = admin_daten(e, teil_c['vorlage'], ziel_seite[eid])
    admin['allgemein'] = admin_daten({'id': '[ID]', 'titel': '[Titel]', 'programm': '', 'felder': []}, teil_c['vorlage'], '')
    os.makedirs(ZIEL, exist_ok=True)
    dateien = {'index.html': start_seite(eintraege, stand, teil_c, ziel_seite, admin, glo),
               SEITE: oberstufe_seite(eintraege, stand, ziel_seite, admin, glo)}
    for name, inhalt in dateien.items():
        with open(os.path.join(ZIEL, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(inhalt)
        print('geschrieben:', os.path.relpath(os.path.join(ZIEL, name), REPO))


if __name__ == '__main__':
    main()
