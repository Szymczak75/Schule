#!/usr/bin/env python3
"""EXAM-Abgaben auswerten  (v1.1, 20.11.2026) – _wartung/exam/exam_auswerten.py

Ablauf im Test-Chat (anweisung_exam.md, Abschnitt 7):

  1) Vorbewerten – liest alle Abgabe-PDFs (eingebettete abgabe.json), prüft Codes und
     Doppelte, bewertet geschlossene Teile (auswahl, sortieren) nach dem Schlüssel und
     schreibt die Bewertungsdatei. Offene Teile (freitext, formel, beschriften) bleiben leer:
       python3 exam_auswerten.py vorbewerten PDF_ORDNER schluessel_<thema>.json bewertung_<thema>.json

  2) Claude füllt in bewertung_<thema>.json die offenen Teile aus (punkte, begruendung,
     korrekturen, kommentar) und trägt Auffälligkeiten ein (manipulation, hinweise).

  3) Ausgeben – Excel aus der Vorlage (Zeilen = Codes alphabetisch, Spalten = Aufgaben),
     Gesamt-PDF (Deckblatt + je Code EIN Korrekturblatt mit „___ von X Punkten" je Aufgabe,
     ohne die Original-Abgabe) und Begründungen (Markdown):
       python3 exam_auswerten.py ausgeben PDF_ORDNER schluessel_<thema>.json bewertung_<thema>.json \\
               Punkteerfassung_Vorlage.xlsx AUSGABE_ORDNER [--kurs "7b"]

Benötigt: pypdf, reportlab (beide in der Claude-Umgebung vorhanden).
"""
import copy
import datetime
import glob
import html
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

CODE_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ'   # wie baustein_exam.html (v1.1)
CODE_SALT = 7


# ----------------------------------------------------------------------------- Grundlagen
def code_gueltig(c):
    n = re.sub(r'[^A-Z0-9]', '', str(c).upper())
    if len(n) != 5 or any(z not in CODE_ALPHABET for z in n):
        return False
    s = CODE_SALT + sum((i + 1) * CODE_ALPHABET.index(n[i]) for i in range(4))
    return CODE_ALPHABET[s % len(CODE_ALPHABET)] == n[4]


def zeit_lokal(iso, mit_datum=False):
    """ISO-Zeit (UTC) aus abgabe.json → deutsche Ortszeit."""
    try:
        from zoneinfo import ZoneInfo
        t = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Berlin'))
        return t.strftime('%d.%m.%Y, %H:%M Uhr' if mit_datum else '%H:%M Uhr')
    except Exception:                                                # noqa: BLE001
        return iso


def lade_json(pfad):
    with open(pfad, encoding='utf-8') as f:
        return json.load(f)


def schreibe_json(pfad, daten):
    with open(pfad, 'w', encoding='utf-8') as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)


def abgaben_lesen(ordner, thema):
    """Liest abgabe.json aus allen PDFs. Gibt {code: {'datei':…, 'daten':…}} sortiert zurück."""
    from pypdf import PdfReader
    abgaben, fehler, warnungen = {}, [], []
    for pfad in sorted(glob.glob(os.path.join(ordner, '*.pdf'))):
        try:
            r = PdfReader(pfad)
            d = json.loads(r.attachments['abgabe.json'][0].decode('utf-8'))
        except Exception as e:                                       # noqa: BLE001
            fehler.append('%s: keine lesbare abgabe.json (%s)' % (os.path.basename(pfad), e))
            continue
        if d.get('format') != 'exam-abgabe-1':
            fehler.append('%s: unbekanntes Format %r' % (os.path.basename(pfad), d.get('format')))
            continue
        if d.get('thema') != thema:
            fehler.append('%s: gehört zu Thema %r, nicht %r' % (os.path.basename(pfad), d.get('thema'), thema))
            continue
        c = d.get('code', '')
        if not code_gueltig(c):
            warnungen.append('%s: Code %r passt nicht zum Code-Muster (alte Engine oder verändert?)' % (os.path.basename(pfad), c))
        if c in abgaben:
            fehler.append('Code %s doppelt: %s und %s' % (c, os.path.basename(abgaben[c]['datei']), os.path.basename(pfad)))
            continue
        abgaben[c] = {'datei': pfad, 'daten': d}
    return dict(sorted(abgaben.items())), fehler, warnungen


def teil_antwort(daten, tid):
    for t in daten['teile']:
        if t['id'] == tid:
            return t
    return None


def laengste_kette(folge):
    """Länge der längsten streng steigenden Teilfolge."""
    enden = []
    for x in folge:
        lo, hi = 0, len(enden)
        while lo < hi:
            m = (lo + hi) // 2
            if enden[m] < x:
                lo = m + 1
            else:
                hi = m
        if lo == len(enden):
            enden.append(x)
        else:
            enden[lo] = x
    return len(enden)


def norm_wort(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip().lower()


# ----------------------------------------------------------------------------- Bewertung
def bewerte_geschlossen(teil, antwort):
    """Gibt (punkte, details) für auswahl/sortieren zurück, sonst (None, details)."""
    a = antwort['antwort'] if antwort else None
    mx = teil['max']
    if teil['typ'] == 'auswahl':
        gewaehlt = [o['option'] for o in (a or []) if o['gewaehlt']]
        richtig = teil['richtig']
        regel = teil.get('regel', 'plusminus' if len(richtig) > 1 else 'genau')
        if regel == 'genau':
            p = mx if sorted(gewaehlt) == sorted(richtig) else 0
        else:                                                       # plusminus
            plus = len([g for g in gewaehlt if g in richtig])
            minus = len([g for g in gewaehlt if g not in richtig])
            p = max(0, min(mx, (plus - minus) * mx / len(richtig)))
        return p, {'gewaehlt': gewaehlt, 'richtig': richtig, 'regel': regel}
    if teil['typ'] == 'sortieren':
        soll = teil['reihenfolge']
        gelegt = [x['karte'] for x in (a or [])]
        folge = [soll.index(k) for k in gelegt if k in soll]
        kette = laengste_kette(folge)
        p = max(0, min(mx, kette - 1))
        return p, {'gelegt': gelegt, 'richtig': soll, 'kette': kette, 'regel': 'kette-1'}
    if teil['typ'] == 'beschriften':
        erwartet = teil.get('nummern', {})
        vorschlag = {}
        for x in (a or []):
            ok = [norm_wort(w) for w in erwartet.get(str(x['nr']), [])]
            vorschlag[str(x['nr'])] = {'antwort': x['text'], 'ok': (norm_wort(x['text']) in ok) if ok else None}
        return None, {'vorschlag': vorschlag}
    return None, {}


def vorbewerten(pdf_ordner, schluessel_pfad, ziel):
    k = lade_json(schluessel_pfad)
    abgaben, fehler, warnungen = abgaben_lesen(pdf_ordner, k['thema'])
    erg = {'thema': k['thema'], 'erstellt': datetime.datetime.now().isoformat(timespec='minutes'),
           'hinweis': 'Offene Teile (punkte: null) von Claude ausfüllen; endgültig bewertet die Lehrkraft.',
           'abgaben': {}}
    for code, ab in abgaben.items():
        d = ab['daten']
        e = {'initialen': d.get('initialen', ''), 'datei': os.path.basename(ab['datei']),
             'sperren': [p for p in d.get('protokoll', []) if p['art'] not in ('Test gestartet', 'abgegeben')],
             'manipulation': None, 'teile': {},
             'hinweise': '' if code_gueltig(code) else 'Code passt nicht zum Code-Muster – Zuordnung prüfen.'}
        for aufg in k['aufgaben']:
            for t in aufg['teile']:
                ant = teil_antwort(d, t['id'])
                p, det = bewerte_geschlossen(t, ant)
                eintrag = {'typ': t['typ'], 'max': t['max'], 'punkte': p, 'automatisch': p is not None,
                           'details': det, 'begruendung': '', 'kommentar': '', 'korrekturen': []}
                if t['typ'] in ('freitext', 'formel'):
                    eintrag['antwort'] = (ant or {}).get('antwort', '')
                if t['typ'] == 'beschriften':
                    eintrag['nummern'] = {}            # {"1": {"ok": true/false, "richtig": "…"}}
                e['teile'][t['id']] = eintrag
        erg['abgaben'][code] = e
    schreibe_json(ziel, erg)
    print('%d Abgaben gelesen → %s' % (len(abgaben), ziel))
    for f in fehler:
        print('FEHLER  ', f)
    for w in warnungen + punkte_abgleich(k, abgaben):
        print('WARNUNG ', w)
    offen = sum(1 for e in erg['abgaben'].values() for t in e['teile'].values() if t['punkte'] is None)
    print('Offene Teile für Claude: %d' % offen)
    for code, e in erg['abgaben'].items():
        zu = ['%s=%s' % (tid, ('%g' % t['punkte']) if t['punkte'] is not None else '?') for tid, t in e['teile'].items()]
        print('  %s %-3s %s' % (code, e['initialen'], '  '.join(zu)))
    return 1 if fehler else 0


def punkte_abgleich(k, abgaben):
    """Vergleicht die Höchstpunkte der Testseite (abgabe.json) mit dem Schlüssel."""
    w = []
    for ab in list(abgaben.values())[:1]:
        seite = [a.get('punkte') for a in ab['daten'].get('aufgaben', [])]
        schl = [a['max'] for a in k['aufgaben']]
        if seite and seite != schl:
            w.append('Höchstpunkte der Testseite %s ≠ Schlüssel %s – bitte angleichen' % (seite, schl))
    return w


def pruefe_bewertung(k, b):
    probleme = []
    for code, e in b['abgaben'].items():
        for aufg in k['aufgaben']:
            for t in aufg['teile']:
                x = e['teile'].get(t['id'])
                if x is None or x.get('punkte') is None:
                    probleme.append('%s Teil %s: keine Punkte' % (code, t['id']))
                elif not (0 <= x['punkte'] <= t['max']):
                    probleme.append('%s Teil %s: %s Punkte außerhalb 0…%s' % (code, t['id'], x['punkte'], t['max']))
    return probleme


def aufgaben_punkte(k, e):
    return [sum(e['teile'][t['id']]['punkte'] for t in a['teile']) for a in k['aufgaben']]


# ----------------------------------------------------------------------------- Excel (XML)
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'


def _spalte(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _spalten_nr(buchst):
    n = 0
    for ch in buchst:
        n = n * 26 + ord(ch) - 64
    return n


def _zelle_xml(ref, wert, stil):
    s = ' s="%s"' % stil if stil else ''
    if wert is None or wert == '':
        return '<c r="%s"%s/>' % (ref, s)
    if isinstance(wert, (int, float)):
        return '<c r="%s"%s><v>%s</v></c>' % (ref, s, ('%g' % wert))
    return '<c r="%s"%s t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, s, html.escape(str(wert), quote=False))


def setze_zellen(xml, werte):
    """werte: {'B3': 'Text', 'J6': 3, …}. Behält den Stil vorhandener Zellen, legt fehlende an."""
    for ref, wert in werte.items():
        m = re.match(r'([A-Z]+)(\d+)$', ref)
        sp, zeile = m.group(1), int(m.group(2))
        zell = re.search(r'<c r="%s"(?=[\s/>])[^>]*?(?:/>|>.*?</c>)' % ref, xml, re.S)
        if zell:
            stil = re.search(r'\ss="(\d+)"', zell.group(0))
            xml = xml[:zell.start()] + _zelle_xml(ref, wert, stil.group(1) if stil else None) + xml[zell.end():]
            continue
        reihe = re.search(r'<row r="%d"[^>]*?(?:/>|>(.*?)</row>)' % zeile, xml, re.S)
        neu = _zelle_xml(ref, wert, None)
        if reihe:
            if reihe.group(0).endswith('/>'):
                ersatz = reihe.group(0)[:-2] + '>' + neu + '</row>'
                xml = xml[:reihe.start()] + ersatz + xml[reihe.end():]
                continue
            innen_start = reihe.start(1)
            pos = reihe.end(1)
            for z in re.finditer(r'<c r="([A-Z]+)%d"' % zeile, reihe.group(1)):
                if _spalten_nr(z.group(1)) > _spalten_nr(sp):
                    pos = innen_start + z.start()
                    break
            xml = xml[:pos] + neu + xml[pos:]
        else:
            neue_reihe = '<row r="%d">%s</row>' % (zeile, neu)
            pos = None
            for r in re.finditer(r'<row r="(\d+)"', xml):
                if int(r.group(1)) > zeile:
                    pos = r.start()
                    break
            if pos is None:
                pos = xml.index('</sheetData>')
            xml = xml[:pos] + neue_reihe + xml[pos:]
    return xml


def excel_schreiben(vorlage, ziel, k, b, kurs):
    with zipfile.ZipFile(vorlage) as z:
        dateien = {n: z.read(n) for n in z.namelist()}
    wb = dateien['xl/workbook.xml'].decode('utf-8')
    rels = dateien['xl/_rels/workbook.xml.rels'].decode('utf-8')
    blatt = {}
    for name, rid in re.findall(r'<sheet name="([^"]+)" sheetId="\d+" r:id="(rId\d+)"', wb):
        ziel_xml = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or \
            re.search(r'Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
        blatt[html.unescape(name)] = 'xl/' + ziel_xml.group(1)
    n = len(k['aufgaben'])
    if n > 20:
        sys.exit('Die Vorlage fasst höchstens 20 Aufgaben (%d).' % n)
    teil1 = min(n, 10)
    maxp = [a['max'] for a in k['aufgaben']]
    e = {'B3': k.get('titel', 'EXAM ' + k['thema']), 'B4': kurs or k.get('kurs', ''),
         'B6': teil1, 'B7': n - teil1}
    for i in range(10):
        e['C%d' % (16 + i)] = maxp[i] if i < teil1 else None
        e['F%d' % (16 + i)] = maxp[teil1 + i] if teil1 + i < n else None
    codes = list(b['abgaben'].keys())
    if len(codes) > 40:
        sys.exit('Die Vorlage fasst höchstens 40 Codes (%d).' % len(codes))
    s = {'A%d' % (2 + i): '%s · %s' % (c, b['abgaben'][c]['initialen']) for i, c in enumerate(codes)}
    u = {}
    for i, c in enumerate(codes):
        for j, p in enumerate(aufgaben_punkte(k, b['abgaben'][c])):
            u['%s%d' % (_spalte(10 + j), 6 + i)] = p
    for name, werte in (('Einstellungen', e), ('Schülerliste', s), ('Übersicht', u)):
        pfad = blatt[name]
        dateien[pfad] = setze_zellen(dateien[pfad].decode('utf-8'), werte).encode('utf-8')
    # Zwischengespeicherte Formelergebnisse entfernen: jedes Programm muss neu rechnen
    for pfad in blatt.values():
        x = dateien[pfad].decode('utf-8')
        x = re.sub(r'(<f\b[^>]*?(?:/>|>.*?</f>))<v>.*?</v>', r'\1', x, flags=re.S)
        x = re.sub(r'(<f\b[^>]*?(?:/>|>.*?</f>))<v/>', r'\1', x, flags=re.S)
        dateien[pfad] = x.encode('utf-8')
    # Neu berechnen beim Öffnen, Speicherpfad/Autor entfernen
    wb = re.sub(r'<calcPr([^>]*?)\s*/>', lambda m: '<calcPr%s fullCalcOnLoad="1"/>' %
                re.sub(r'\sfullCalcOnLoad="\w+"', '', m.group(1)), wb)
    wb = re.sub(r'<mc:AlternateContent[^>]*>\s*<mc:Choice Requires="x15">\s*<x15ac:absPath[^>]*/>\s*</mc:Choice>\s*</mc:AlternateContent>', '', wb)
    dateien['xl/workbook.xml'] = wb.encode('utf-8')
    if 'docProps/core.xml' in dateien:
        core = dateien['docProps/core.xml'].decode('utf-8')
        core = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy>EXAM</cp:lastModifiedBy>', core)
        core = re.sub(r'<dc:creator>.*?</dc:creator>', '<dc:creator>EXAM</dc:creator>', core)
        dateien['docProps/core.xml'] = core.encode('utf-8')
    with zipfile.ZipFile(ziel, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, inhalt in dateien.items():
            z.writestr(name, inhalt)


# ----------------------------------------------------------------------------- Gesamt-PDF
def _schriften():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for name, datei in (('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')):
        for ordner in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/dejavu', '/Library/Fonts'):
            p = os.path.join(ordner, datei)
            if os.path.exists(p):
                pdfmetrics.registerFont(TTFont(name, p))
                break
        else:
            return 'Helvetica', 'Helvetica-Bold'
    return 'DV', 'DVB'


def _korrigierter_text(text, korrekturen, rot, gruen):
    """Markiert falsch → richtig im Schülertext (alle Vorkommen, ganze Wörter wenn möglich)."""
    t = html.escape(text or '(keine Angabe)')
    marken = []
    korrekturen = sorted(korrekturen or [], key=lambda x: -len(x.get('falsch', '')))   # längere zuerst
    for i, kor in enumerate(korrekturen):
        falsch = html.escape(kor.get('falsch', ''))
        if not falsch:
            continue
        muster = re.compile(r'(?<![\wÄÖÜäöüß])%s(?![\wÄÖÜäöüß])' % re.escape(falsch))
        if not muster.search(t):
            muster = re.compile(re.escape(falsch))
        ersatz = '\x00%d\x00' % i
        t = muster.sub(ersatz, t)
        marken.append((ersatz, '<strike><font color="%s">%s</font></strike> <font color="%s"><b>%s</b></font>'
                       % (rot, falsch, gruen, html.escape(kor.get('richtig', '')))))
    for ersatz, html_ in marken:
        t = t.replace(ersatz, html_)
    return t.replace('\n', '<br/>')


def gesamt_pdf(ziel, k, b, abgaben):
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                    TableStyle)
    f, fb = _schriften()
    TINTE, BLAU, GRAU, ROT, GRUEN, AMBER = '#22303f', '#1f4680', '#6b7686', '#c1272d', '#1e7d32', '#96690a'
    st = {
        'h1': ParagraphStyle('h1', fontName=fb, fontSize=16, leading=20, textColor=TINTE, spaceAfter=4),
        'h2': ParagraphStyle('h2', fontName=fb, fontSize=12.5, leading=16, textColor=BLAU, spaceBefore=8, spaceAfter=2),
        'h3': ParagraphStyle('h3', fontName=fb, fontSize=10.5, leading=13.5, textColor=TINTE, spaceBefore=3, spaceAfter=2),
        'p': ParagraphStyle('p', fontName=f, fontSize=10, leading=13.5, textColor=TINTE),
        'klein': ParagraphStyle('k', fontName=f, fontSize=8.5, leading=11, textColor=GRAU),
        'box': ParagraphStyle('b', fontName=f, fontSize=10.5, leading=14.5, textColor=TINTE),
        'warn': ParagraphStyle('w', fontName=fb, fontSize=12, leading=16, textColor=colors.white),
        'punkte': ParagraphStyle('pk', fontName=fb, fontSize=11, leading=14, textColor=TINTE, alignment=2),
    }

    def kasten(inhalt, rand, grund, breite=1.6):
        t = Table([[inhalt]], colWidths=[170 * mm])
        t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), breite, colors.HexColor(rand)),
                               ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(grund)),
                               ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                               ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
        return t

    texte = {}
    teile_def = {t['id']: (a, t) for a in k['aufgaben'] for t in a['teile']}

    def karten_text(code, tid, kid):
        ant = teil_antwort(abgaben[code]['daten'], tid)
        for x in (ant or {}).get('antwort', []) or []:
            if x.get('karte') == kid:
                return x.get('text') or kid
        return texte.get(kid, kid)

    # Kartentexte aller Abgaben sammeln (für die richtige Reihenfolge)
    for code, ab in abgaben.items():
        for t in ab['daten']['teile']:
            if t['typ'] == 'sortieren':
                for x in t['antwort']:
                    if x.get('karte'):
                        texte[x['karte']] = x['text']
            if t['typ'] == 'auswahl':
                for o in t['antwort']:
                    texte[o['option']] = o['text']

    tmp = tempfile.mkdtemp()
    korr_pdfs = {}
    for code, e in b['abgaben'].items():
        d = abgaben[code]['daten']
        s = []
        s.append(Paragraph('%s – Korrektur' % html.escape(k.get('titel', 'EXAM ' + k['thema'])), st['h1']))
        s.append(Paragraph('<b>Code %s</b> · Initialen %s · abgegeben %s' % (
            code, html.escape(e['initialen']), zeit_lokal(d.get('ende', ''), True)), st['p']))
        s.append(Paragraph('Vorbewertung durch Claude – endgültig bewertet die Lehrkraft. Die Punkte stehen in '
                           'der Excel-Tabelle und werden hier von Hand eingetragen.', st['klein']))
        s.append(Spacer(1, 4))
        if e.get('manipulation'):
            s.append(kasten(Paragraph('⚠ ACHTUNG – ANWEISUNG AN DIE KI IM SCHÜLERTEXT<br/>'
                                      '<font size="10.5">„%s“</font><br/><font size="10">Nicht befolgt. Bitte selbst '
                                      'ansehen und entscheiden.</font>' % html.escape(e['manipulation']), st['warn']),
                            ROT, ROT, 2.5))
            s.append(Spacer(1, 5))
        if e.get('sperren'):
            zeilen = '<br/>'.join('%s – %s' % (zeit_lokal(p['zeit']), html.escape(p['art']))
                                  for p in e['sperren'])
            s.append(kasten(Paragraph('<b>Sperrprotokoll (%d Einträge)</b><br/>%s' % (len(e['sperren']), zeilen),
                                      st['box']), AMBER, '#fdf3d9'))
            s.append(Spacer(1, 4))
        if e.get('hinweise'):
            s.append(kasten(Paragraph('<b>Hinweis:</b> ' + html.escape(e['hinweise']), st['box']), BLAU, '#eef0f3'))
        for aufg in k['aufgaben']:
            kopf = Table([[Paragraph(html.escape(aufg.get('titel', 'Aufgabe %s' % aufg['nr'])), st['h2']),
                           Paragraph('<b>____ von %g %s</b>' % (aufg['max'], 'Punkt' if aufg['max'] == 1 else 'Punkten'),
                                     st['punkte'])]], colWidths=[125 * mm, 45 * mm])
            kopf.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'BOTTOM'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                      ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
            s.append(kopf)
            for t in aufg['teile']:
                x = e['teile'][t['id']]
                ant = teil_antwort(d, t['id'])
                block = [Paragraph(html.escape((ant or {}).get('auftrag', 'Teil ' + t['id'])), st['h3'])]
                if t['typ'] == 'auswahl':
                    zeilen = []
                    for o in (ant or {}).get('antwort', []):
                        r = o['option'] in t['richtig']
                        if o['gewaehlt'] and r:
                            z = '<font color="%s">✔ %s</font>' % (GRUEN, html.escape(o['text']))
                        elif o['gewaehlt']:
                            z = '<font color="%s">✘ %s</font> (falsch gewählt)' % (ROT, html.escape(o['text']))
                        elif r:
                            z = '<font color="%s">○ %s</font> (fehlt – wäre richtig)' % (AMBER, html.escape(o['text']))
                        else:
                            z = '<font color="%s">· %s</font>' % (GRAU, html.escape(o['text']))
                        zeilen.append(z)
                    block.append(Paragraph('<br/>'.join(zeilen), st['p']))
                elif t['typ'] == 'sortieren':
                    soll = t['reihenfolge']
                    gelegt = x['details'].get('gelegt', [])
                    zeilen = []
                    for i, kid in enumerate(gelegt):
                        txt = html.escape(karten_text(code, t['id'], kid)) if kid else '(leer)'
                        ok = kid is not None and i < len(soll) and soll[i] == kid
                        zeilen.append('%d. <font color="%s">%s</font>' % (i + 1, GRUEN if ok else TINTE, txt))
                    richtig = ' → '.join(html.escape(karten_text(code, t['id'], kid)) for kid in soll)
                    block.append(Paragraph('<br/>'.join(zeilen), st['p']))
                    block.append(Paragraph('<font color="%s">Richtig: %s</font>' % (GRUEN, richtig), st['p']))
                    block.append(Paragraph('Längste richtig geordnete Kette: %d Karten' % x['details'].get('kette', 0),
                                           st['klein']))
                elif t['typ'] == 'beschriften':
                    reihen = [['Nr.', 'Antwort', 'Korrektur']]
                    for a_ in (ant or {}).get('antwort', []):
                        n = x.get('nummern', {}).get(str(a_['nr']), {})
                        ok = n.get('ok')
                        korr = ('<font color="%s">✔</font>' % GRUEN) if ok else (
                            '<font color="%s">✘ richtig: <b>%s</b></font>' % (ROT, html.escape(n.get('richtig', '')))
                            if ok is False else '')
                        reihen.append([str(a_['nr']), Paragraph(html.escape(a_['text'] or '(keine Angabe)'), st['p']),
                                       Paragraph(korr, st['p'])])
                    tb = Table(reihen, colWidths=[12 * mm, 75 * mm, 83 * mm])
                    tb.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), f), ('FONTNAME', (0, 0), (-1, 0), fb),
                                            ('FONTSIZE', (0, 0), (-1, -1), 9.5), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                            ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#e2e6ec'))]))
                    block.append(tb)
                else:
                    block.append(kasten(Paragraph(_korrigierter_text(x.get('antwort', ''), x.get('korrekturen'),
                                                                    ROT, GRUEN), st['box']), '#e2e6ec', '#ffffff', 1))
                if x.get('kommentar'):
                    block.append(Paragraph('<i>Anmerkung:</i> ' + html.escape(x['kommentar']), st['p']))
                s.append(KeepTogether(block))
                s.append(Spacer(1, 3))
        pfad = os.path.join(tmp, code + '.pdf')
        SimpleDocTemplate(pfad, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                          bottomMargin=16 * mm, title='Korrektur ' + code).build(s)
        korr_pdfs[code] = pfad

    # Deckblatt
    deck = os.path.join(tmp, '_deckblatt.pdf')
    s = [Paragraph('%s – Gesamt-PDF' % html.escape(k.get('titel', 'EXAM ' + k['thema'])), st['h1']),
         Paragraph('%d Abgaben, alphabetisch nach Code. Je Code ein Korrekturblatt; die Original-Abgabe '
                   'hat der Schüler selbst. Vorbewertung durch Claude – endgültig bewertet die Lehrkraft.'
                   % len(b['abgaben']), st['p']),
         Spacer(1, 6)]
    reihen = [['Code', 'Init.', 'Auffälligkeiten']]
    for code, e in b['abgaben'].items():
        auff = []
        if e.get('manipulation'):
            auff.append('<font color="%s"><b>⚠ Anweisung an die KI</b></font>' % ROT)
        if e.get('sperren'):
            auff.append('%d Sperrprotokoll-Einträge' % len(e['sperren']))
        if e.get('hinweise'):
            auff.append(html.escape(e['hinweise']))
        reihen.append([code, e['initialen'], Paragraph(' · '.join(auff) or '–', st['p'])])
    tb = Table(reihen, colWidths=[28 * mm, 16 * mm, 126 * mm])
    tb.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), f), ('FONTNAME', (0, 0), (-1, 0), fb),
                            ('FONTSIZE', (0, 0), (-1, -1), 10), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#e2e6ec'))]))
    s.append(tb)
    SimpleDocTemplate(deck, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title='Gesamt-PDF').build(s)

    w = PdfWriter()
    for p in PdfReader(deck).pages:
        w.add_page(p)
    for code in b['abgaben']:
        start = len(w.pages)
        for p in PdfReader(korr_pdfs[code]).pages:
            w.add_page(p)
        w.add_outline_item('%s · %s' % (code, b['abgaben'][code]['initialen']), start)
    w.add_metadata({'/Title': 'Gesamt-PDF ' + k.get('titel', k['thema']), '/Producer': 'EXAM-Auswertung v1.1'})
    with open(ziel, 'wb') as fh:
        w.write(fh)
    shutil.rmtree(tmp, ignore_errors=True)


def begruendungen_md(ziel, k, b):
    z = ['# Vorbewertung – %s' % k.get('titel', k['thema']), '',
         'Vorbewertung durch Claude, endgültig bewertet die Lehrkraft. Höchstpunkte: %g.' %
         sum(a['max'] for a in k['aufgaben']), '']
    kopf = '| Code | Init. | ' + ' | '.join('A%s (%g)' % (a['nr'], a['max']) for a in k['aufgaben']) + ' | Summe |'
    z += [kopf, '|' + '---|' * (len(k['aufgaben']) + 3)]
    for code, e in b['abgaben'].items():
        p = aufgaben_punkte(k, e)
        z.append('| %s | %s | %s | **%g** |' % (code, e['initialen'], ' | '.join('%g' % x for x in p), sum(p)))
    z.append('')
    for code, e in b['abgaben'].items():
        z.append('## %s · %s' % (code, e['initialen']))
        if e.get('manipulation'):
            z.append('> **⚠ ACHTUNG – Anweisung an die KI im Schülertext:** „%s“ – nicht befolgt.' % e['manipulation'])
        if e.get('sperren'):
            z.append('- Sperrprotokoll: ' + '; '.join('%s %s' % (zeit_lokal(p['zeit']), p['art']) for p in e['sperren']))
        for a in k['aufgaben']:
            for t in a['teile']:
                x = e['teile'][t['id']]
                txt = x.get('begruendung') or ('automatisch nach Schlüssel' if x.get('automatisch') else '')
                z.append('- Teil %s: **%g / %g** – %s' % (t['id'], x['punkte'], t['max'], txt))
        z.append('')
    with open(ziel, 'w', encoding='utf-8') as f:
        f.write('\n'.join(z))


def ausgeben(pdf_ordner, schluessel_pfad, bewertung_pfad, vorlage, ordner, kurs=''):
    k, b = lade_json(schluessel_pfad), lade_json(bewertung_pfad)
    abgaben, fehler, warnungen = abgaben_lesen(pdf_ordner, k['thema'])
    for w in warnungen + punkte_abgleich(k, abgaben):
        print('WARNUNG ', w)
    probleme = fehler + pruefe_bewertung(k, b)
    fehlt = [c for c in b['abgaben'] if c not in abgaben]
    probleme += ['%s: PDF fehlt im Ordner' % c for c in fehlt]
    if probleme:
        for p in probleme:
            print('FEHLER  ', p)
        return 1
    b['abgaben'] = dict(sorted(b['abgaben'].items()))
    os.makedirs(ordner, exist_ok=True)
    name = re.sub(r'[^A-Za-z0-9]+', '_', k['thema'])
    excel_schreiben(vorlage, os.path.join(ordner, 'Punkte_EXAM_%s.xlsx' % name), k, b, kurs)
    gesamt_pdf(os.path.join(ordner, 'Gesamt_EXAM_%s.pdf' % name), k, b, abgaben)
    begruendungen_md(os.path.join(ordner, 'Vorbewertung_EXAM_%s.md' % name), k, b)
    print('fertig:', ', '.join(sorted(os.listdir(ordner))))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    kurs = ''
    if '--kurs' in a:
        i = a.index('--kurs')
        kurs = a[i + 1]
        del a[i:i + 2]
    if len(a) == 4 and a[0] == 'vorbewerten':
        sys.exit(vorbewerten(a[1], a[2], a[3]))
    if len(a) == 6 and a[0] == 'ausgeben':
        sys.exit(ausgeben(a[1], a[2], a[3], a[4], a[5], kurs))
    sys.exit(__doc__)
