#!/usr/bin/env python3
"""Entwickleransicht einer EXAM-Seite erzeugen  (v1, 20.11.2026) – _wartung/exam/exam_vorschau.py

Stufe 1 (Entwicklung, projektanweisung_exam.md): Solange ein Test entsteht, sieht die Lehrkraft
ihn als private Entwickleransicht – alle Aufgaben mit Abbildungen (Nummern wie in der Engine),
Startreihenfolge der Karten und Musterlösungen. Die Datei kommt NIE ins Repo; Claude
veröffentlicht sie als privates Artefakt im Test-Chat.

Aufruf:
  python3 exam_vorschau.py inhalt.js schluessel_<thema>.json erwartungshorizont_<thema>.md vorschau.html

Musterlösung zum Austeilen (wenn der Test fertig bewertet ist):
  python3 exam_vorschau.py --musterloesung inhalt.js schluessel_<thema>.json \\
          erwartungshorizont_<thema>.md musterloesung_<thema>.html musterloesung_<thema>.pdf
  Aufgabenstellungen mit Lösungen, ohne Punkte und Bewertungsregeln. Geschlossene Teile kommen
  aus dem Schlüssel, Freitexte aus der Zeile „Musterlösung: …" je Teil im Erwartungshorizont
  (für eine Karte „❓ Fehlender Schritt" die Zeile „Musterlösung: …" im Abschnitt „### Teil <id>-fehlt").

- inhalt.js: genau der Block  var EXAM = { … };  (wie für exam_bauen.py)
- Schlüssel: geschlossene Teile (beschriften, sortieren, auswahl) werden daraus gelöst.
- Erwartungshorizont: der Abschnitt „### Teil <id> …" erscheint als Musterlösung unter dem Teil.
  Fehlt er, wird die Musterlösung geschlossener Teile aus dem Schlüssel gebaut.
- WARNUNG, wenn Punkte auf der Seite und im Schlüssel nicht übereinstimmen.
Nur Farben aus dem Farbschema; keine externen Dateien.
"""
import html
import json
import re
import sys


# ------------------------------------------------------------ JS-Literal -> Python
def js_literal(text):
    """Wandelt das Objekt-Literal  var EXAM = {…};  in Python-Daten (ohne Node)."""
    if 'var EXAM = {' in text:                           # auch eine fertige Seite geht
        a = text.index('var EXAM = {')
        text = text[a:text.index('\n};', a) + 3]
    a = text.index('{')
    src = text.rstrip().rstrip(';').rstrip()[a:]
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in '\'"':                                   # Zeichenkette
            q, j, buf = c, i + 1, []
            while src[j] != q:
                if src[j] == '\\':
                    nxt = src[j + 1]
                    buf.append({'n': '\n', 't': '\t'}.get(nxt, nxt)); j += 2
                else:
                    buf.append(src[j]); j += 1
            out.append(json.dumps(''.join(buf), ensure_ascii=False)); i = j + 1
        elif c == '/' and src[i:i + 2] == '//':          # Zeilenkommentar
            i = src.index('\n', i)
        elif c == '/' and src[i:i + 2] == '/*':          # Blockkommentar
            i = src.index('*/', i) + 2
        elif c.isalpha() or c == '_':                    # Bezeichner / true / false / null
            m = re.match(r'[A-Za-z_]\w*', src[i:]); w = m.group(0); i += len(w)
            k = i
            while k < n and src[k] in ' \t\r\n':
                k += 1
            if k < n and src[k] == ':':
                out.append(json.dumps(w))
            else:
                out.append(w)
        else:
            out.append(c); i += 1
    s = re.sub(r',(\s*[}\]])', r'\1', ''.join(out))      # nachgestellte Kommas
    zk = r'"(?:[^"\\]|\\.)*"'
    verkettet = re.compile('(%s)\\s*\\+\\s*(%s)' % (zk, zk))   # 'a' + 'b'
    while verkettet.search(s):
        s = verkettet.sub(lambda m: json.dumps(json.loads(m.group(1)) + json.loads(m.group(2)), ensure_ascii=False), s)
    return json.loads(s)


# ------------------------------------------------------------ Erwartungshorizont
def ewh_teile(md):
    """{teil_id: markdown} aus den Abschnitten  ### Teil <id> …"""
    teile, akt, buf = {}, None, []
    for z in md.splitlines():
        m = re.match(r'###\s+Teil\s+(\S+)', z)
        if m or z.startswith('## ') or z.startswith('---'):
            if akt:
                teile[akt] = '\n'.join(buf).strip()
            akt, buf = (m.group(1) if m else None), []
        elif akt:
            buf.append(z)
    if akt:
        teile[akt] = '\n'.join(buf).strip()
    return teile


def md_html(md):
    """Kleines Markdown: Tabellen, Listen, nummerierte Listen, **fett**, `code`."""
    def inl(t):
        t = html.escape(t, quote=False)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        return re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    h, zeilen, i = [], md.splitlines(), 0
    while i < len(zeilen):
        z = zeilen[i]
        if z.startswith('|'):
            rows = []
            while i < len(zeilen) and zeilen[i].startswith('|'):
                if not re.match(r'^\|[\s\-|:]+\|$', zeilen[i]):
                    rows.append([c.strip() for c in zeilen[i].strip('|').split('|')])
                i += 1
            h.append('<table>' + ''.join('<tr>' + ''.join(('<th>%s</th>' if r == 0 else '<td>%s</td>') % inl(c)
                     for c in row) + '</tr>' for r, row in enumerate(rows)) + '</table>')
            continue
        for tag, pat in (('ul', r'^\s*-\s+(.*)'), ('ol', r'^\s*\d+\.\s+(.*)')):
            if re.match(pat, z):
                items = []
                while i < len(zeilen) and (re.match(pat, zeilen[i]) or (items and zeilen[i].startswith('  ') and zeilen[i].strip())):
                    m = re.match(pat, zeilen[i])
                    if m:
                        items.append(m.group(1))
                    else:
                        items[-1] += ' ' + zeilen[i].strip()
                    i += 1
                h.append('<%s>' % tag + ''.join('<li>%s</li>' % inl(x) for x in items) + '</%s>' % tag)
                break
        else:
            if z.strip():
                h.append('<p>%s</p>' % inl(z))
            i += 1
    return ''.join(h)


# ------------------------------------------------------------ Bausteine
def figur(t):
    """Abbildung mit Nummern – gleiche Darstellung wie figurSvg() in der Engine."""
    n = ''.join('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#6b7686" stroke-width="2"/>'
                '<circle cx="%s" cy="%s" r="7" fill="none" stroke="#6b7686" stroke-width="2"/>'
                '<circle cx="%s" cy="%s" r="17" fill="#1f4680"/>'
                '<text x="%s" y="%s" text-anchor="middle" font-size="18" font-weight="700" fill="#ffffff" '
                'font-family="Helvetica,Arial,sans-serif">%s</text>'
                % (p['x'], p['y'], p['zx'], p['zy'], p['zx'], p['zy'], p['x'], p['y'], p['x'], p['y'] + 6, p['nr'])
                for p in t['nummern'])
    s = t['svg']
    k = s.rindex('</svg>')
    s = s[:k] + n + '</svg>'
    return s.replace('<svg ', '<svg style="width:100%;height:auto;display:block" ', 1)


def ml(inhalt):
    return '<div class="ml"><div class="mlk">Musterlösung</div>' + inhalt + '</div>'


def teil_html(t, kt, ewh):
    e = esc = lambda x: html.escape(str(x), quote=False)
    h = '<p class="auf">%s%s</p>' % (e(t.get('auftrag', '')), ' <i>(%s P.)</i>' % kt['max'] if kt else '')
    loes = ''
    if t['typ'] == 'beschriften':
        h += '<div class="fig">%s</div>' % figur(t)
        if kt:
            loes = '<table><tr><th>Nr</th><th>erwartet</th><th>auch richtig</th></tr>' + ''.join(
                '<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (nr, esc(v[0]), esc(', '.join(v[1:])))
                for nr, v in sorted(kt['nummern'].items(), key=lambda x: int(x[0]))) + '</table>'
    elif t['typ'] == 'sortieren':
        karten = {k['id']: k for k in t['karten']}
        li = lambda k: '<li class="%s">%s</li>' % ('fehlt' if k.get('fehlt') else '', e(k['t']))
        h += '<div class="zwei"><div><h3>So stehen die Karten am Anfang</h3><ul class="karten">' + \
             ''.join(li(k) for k in t['karten']) + '</ul></div><div>@@LOES@@</div></div>'
        if kt:
            loes = '<ol>' + ''.join('<li>%s</li>' % e(karten[i]['t']) for i in kt['reihenfolge']) + '</ol>'
        return h.replace('@@LOES@@', ml(md_html(ewh) if ewh else loes) if (ewh or kt) else '')
    elif t['typ'] == 'formel':
        h += '<p><i>Eingabe: %s</i></p>' % {'getrennt': 'Zähler und Nenner getrennt', 'gemischt': 'gemischte Zahl'}.get(
            t.get('eingabe'), 'Formeltool')
    elif t['typ'] == 'auswahl':
        richtig = set(kt.get('richtig', [])) if kt else set()
        h += '<ul class="karten">' + ''.join('<li class="%s">%s%s</li>' % (
            'ok' if o['id'] in richtig else '', '✔ ' if o['id'] in richtig else '', e(o['t'])) for o in t['optionen']) + '</ul>'
        if kt:
            loes = '<p>Richtig: %s · Regel: %s</p>' % (', '.join(sorted(richtig)), kt.get('regel', 'plusminus'))
    if loes or ewh:
        h += ml(md_html(ewh) if ewh else loes)   # Erwartungshorizont hat Vorrang (mit Hinweisen)
    elif not kt:
        h += '<div class="warn">Kein Eintrag im Schlüssel für Teil %s.</div>' % e(t['id'])
    return h


CSS = """:root{color-scheme:light}*{box-sizing:border-box;min-width:0}
body{margin:0;background:#f7f8fa;color:#22303f;font:16px/1.55 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
main{max-width:960px;margin:0 auto;padding:16px}
.kopf{background:#eef0f3;border:3px solid #1f4680;border-radius:16px;padding:16px 20px}.kopf h1{margin:0;font-size:1.5rem}.kopf p{margin:.3rem 0 0;color:#6b7686}
.status{background:#fdf3d9;border:2px solid #b8860b;border-radius:10px;padding:10px 14px;margin:14px 0;font-weight:600}
.warn{background:#c1272d;color:#fff;border-radius:10px;padding:10px 14px;margin:8px 0;font-weight:600}
section{background:#fff;border:2px solid #e2e6ec;border-radius:16px;padding:16px 20px;margin:16px 0}
h2{margin:0 0 .5rem;font-size:1.3rem;color:#1f4680}h2 span{font-size:1rem;color:#6b7686}h3{font-size:1rem;margin:.4rem 0}
.auf{font-weight:700;margin:1rem 0 .4rem}.auf i{font-weight:400;color:#6b7686}
.fig{border:2px solid #e2e6ec;border-radius:12px;padding:6px;background:#fff}
.ml{background:#fdf3d9;border:2px solid #b8860b;border-radius:10px;padding:10px 14px;margin:.6rem 0}.mlk{font-weight:700;color:#96690a;margin-bottom:4px}
.ml ul,.ml ol{margin:.2rem 0;padding-left:1.3rem}.ml p{margin:.3rem 0}
table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:4px 8px;border-bottom:1px solid #e4dcd0;vertical-align:top}
.zwei{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.karten{list-style:none;padding:0;margin:0}.karten li{border:2px solid #e2e6ec;border-radius:10px;padding:8px 12px;margin:6px 0}
.karten li.fehlt{border:2px dashed #b8860b;background:#fdf3d9;font-weight:700}.karten li.ok{border-color:#1e7d32;font-weight:700}"""


def vorschau(exam, schluessel, ewh_md):
    kteile = {t['id']: t for a in schluessel.get('aufgaben', []) for t in a['teile']}
    ewh = ewh_teile(ewh_md)
    warn, secs = [], []
    for a_nr, a in enumerate(exam['aufgaben'], 1):
        ka = next((x for x in schluessel.get('aufgaben', []) if x['nr'] == a_nr), None)
        if not ka or ka['max'] != a.get('punkte'):
            warn.append('Aufgabe %d: Punkte Seite %s ≠ Schlüssel %s' % (a_nr, a.get('punkte'), ka and ka['max']))
        secs.append('<section><h2>%s <span>(%s Punkte)</span></h2>%s%s</section>' % (
            html.escape(a['titel']), a.get('punkte', '?'), a.get('einleitung', ''),
            ''.join(teil_html(t, kteile.get(t['id']), ewh.get(t['id'], '')) for t in a['teile'])))
    gesamt = sum(a.get('punkte', 0) for a in exam['aufgaben'])
    return ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" '
            'content="width=device-width, initial-scale=1"><title>%s – Entwicklung</title><style>%s</style></head>'
            '<body><main><div class="kopf"><h1>%s</h1><p>%s · Anrede %s · Richtzeit %s min · %s Punkte</p></div>'
            '<div class="status">🛠 Entwickleransicht (%s) – mit Musterlösungen. Nur für die Lehrkraft, nie im Repo. '
            'Die scharfe Testseite enthält nichts davon.</div>%s%s</main></body></html>') % (
        html.escape(exam.get('titel', 'EXAM').replace('🧠 ', '')), CSS, html.escape(exam.get('titel', '')),
        html.escape(exam.get('untertitel', '')), exam.get('anrede', ''), exam.get('zeit', '?'), gesamt,
        html.escape(exam.get('speicher', '')), ''.join('<div class="warn">%s</div>' % html.escape(w) for w in warn),
        ''.join(secs)), warn


# ------------------------------------------------------------ Musterlösung für die Klasse
def ewh_musterloesungen(md):
    """{teil_id: text} aus den Zeilen „Musterlösung: …" im Erwartungshorizont (bis Leerzeile)."""
    out = {}
    for tid, block in ewh_teile(md).items():
        m = re.search(r'^\**Musterlösung\**:\s*(.+?)(?:\n\s*\n|\Z)', block, flags=re.S | re.M)
        if m:
            out[tid] = ' '.join(z.strip() for z in m.group(1).splitlines())
    return out


CSS_ML = """@page{size:A4;margin:14mm 16mm}*{box-sizing:border-box}
body{margin:0;color:#22303f;font:10.5pt/1.45 'DejaVu Sans',Helvetica,Arial,sans-serif}
h1{font-size:16pt;margin:0 0 2mm;color:#1f4680}.unter{color:#6b7686;margin:0 0 5mm}
section{break-inside:avoid;margin:0 0 5mm}h2{font-size:12.5pt;color:#1f4680;margin:0 0 1.5mm;break-after:avoid}
.ein{color:#6b7686;margin:0 0 2mm}.auf{font-weight:700;margin:2mm 0 1mm;break-after:avoid}
.loes{border-left:4px solid #1e7d32;background:#f3f8f3;padding:2mm 3mm;margin:0 0 2mm;break-inside:avoid}
.fig{max-width:150mm;margin:1mm 0}.fig svg{width:100%;height:auto;display:block}
.spalten{columns:2;column-gap:8mm}.spalten div{break-inside:avoid}ol{margin:0;padding-left:6mm}
.ok{color:#1e7d32;font-weight:700}"""


def musterloesung(exam, schluessel, ewh_md):
    """Musterlösung zum Austeilen: Aufgabenstellungen + Lösungen, ohne Bewertungsregeln."""
    kteile = {t['id']: t for a in schluessel.get('aufgaben', []) for t in a['teile']}
    texte = ewh_musterloesungen(ewh_md)
    fehlt, secs = [], []
    e = lambda x: html.escape(str(x), quote=False)
    for a in exam['aufgaben']:
        h = '<section><h2>%s</h2>' % e(a['titel'])
        ein = re.sub(r'<p>', '<p class="ein">', a.get('einleitung', ''))
        h += ein
        for t in a['teile']:
            kt = kteile.get(t['id'], {})
            h += '<p class="auf">%s</p>' % e(t.get('auftrag', ''))
            if t['typ'] == 'beschriften':
                vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', t['svg']).group(1).split()]
                h += '<div class="fig" style="max-width:%dmm">%s</div>' % (150 if vb[2] / vb[3] > 2 else 105, figur(t))
                h += '<div class="loes spalten">' + ''.join('<div><b>%s</b> %s</div>' % (nr, e(v[0]))
                     for nr, v in sorted(kt.get('nummern', {}).items(), key=lambda x: int(x[0]))) + '</div>'
            elif t['typ'] == 'sortieren':
                karten = {k['id']: k['t'] for k in t['karten']}
                reihe = kt.get('reihenfolge', [])
                zeilen = []
                for kid in reihe:
                    if karten.get(kid, '').startswith('❓'):
                        zeilen.append('<b>%s</b>' % e(texte.get(t['id'] + '-fehlt', texte.get(t['id'], '(fehlender Schritt)'))))
                    else:
                        zeilen.append(e(karten.get(kid, kid)))
                h += '<div class="loes"><ol>' + ''.join('<li>%s</li>' % z for z in zeilen) + '</ol></div>'
            elif t['typ'] == 'auswahl':
                richtig = set(kt.get('richtig', []))
                h += '<div class="loes">' + '<br>'.join(('<span class="ok">✔ %s</span>' if o['id'] in richtig else '○ %s')
                     % e(o['t']) for o in t['optionen']) + '</div>'
            else:
                if t['id'] in texte:
                    h += '<div class="loes">%s</div>' % e(texte[t['id']])
                else:
                    fehlt.append(t['id'])
                    h += '<div class="loes">(Musterlösung fehlt im Erwartungshorizont)</div>'
        secs.append(h + '</section>')
    seite = ('<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Musterlösung – %s</title>'
             '<style>%s</style></head><body><h1>Musterlösung · %s</h1><p class="unter">%s</p>%s</body></html>') % (
        e(exam.get('thema', '')), CSS_ML, e(re.sub(r'^\W+\s*', '', exam.get('titel', '')).replace('EXAM · ', '')),
        e(exam.get('untertitel', '')), ''.join(secs))
    return seite, fehlt


def als_pdf(html_pfad, pdf_pfad):
    """HTML → PDF mit Chromium (Playwright)."""
    from playwright.sync_api import sync_playwright
    import os
    with sync_playwright() as pw:
        try:
            br = pw.chromium.launch()
        except Exception:                                    # noqa: BLE001
            br = pw.chromium.launch(executable_path=next(p for p in ('/usr/bin/google-chrome', '/usr/bin/chromium')
                                                         if os.path.exists(p)))
        pg = br.new_page()
        pg.goto('file://' + os.path.abspath(html_pfad))
        pg.pdf(path=pdf_pfad, format='A4', print_background=True, prefer_css_page_size=True)
        br.close()


if __name__ == '__main__':
    if len(sys.argv) in (6, 7) and sys.argv[1] == '--musterloesung':
        exam = js_literal(open(sys.argv[2], encoding='utf-8').read())
        schl = json.load(open(sys.argv[3], encoding='utf-8'))
        seite, fehlt = musterloesung(exam, schl, open(sys.argv[4], encoding='utf-8').read())
        open(sys.argv[5], 'w', encoding='utf-8').write(seite)
        for t in fehlt:
            print('WARNUNG: keine „Musterlösung:“-Zeile im Erwartungshorizont für Teil', t)
        if len(sys.argv) == 7:
            als_pdf(sys.argv[5], sys.argv[6])
            print('Musterlösung (PDF):', sys.argv[6])
        print('Musterlösung (HTML):', sys.argv[5])
        sys.exit(0)
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    exam = js_literal(open(sys.argv[1], encoding='utf-8').read())
    schl = json.load(open(sys.argv[2], encoding='utf-8'))
    seite, warn = vorschau(exam, schl, open(sys.argv[3], encoding='utf-8').read())
    open(sys.argv[4], 'w', encoding='utf-8').write(seite)
    for w in warn:
        print('WARNUNG:', w)
    print('Entwickleransicht:', sys.argv[4])
