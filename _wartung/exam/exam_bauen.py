#!/usr/bin/env python3
"""EXAM-Seite aus dem Baustein bauen  (v1, 19.11.2026) – _wartung/exam/exam_bauen.py

Setzt den Inhalt (var EXAM = {...};) und die Meta-Angaben in eine Kopie von
baustein_exam.html ein. Die Engine bleibt dadurch garantiert unverändert.

Aufruf:
  python3 exam_bauen.py baustein_exam.html inhalt.js ziel.html \\
      titel="EXAM · Neurobiologie" klasse=Q1 fach=bio oberthema=Neurobiologie \\
      thema="Neuron und Synapse" description="…" keywords="…"

inhalt.js enthält genau den Block  var EXAM = { … };  (Aufbau: anweisung_exam.md, 3).
Ohne Angabe bleiben Meta-Werte des Bausteins stehen – description und keywords
bitte immer setzen.
"""
import html
import re
import sys

ANFANG = 'var EXAM = {'
ENDE = '/* ========================= ENDE EXAM-INHALT'
META = ('description', 'keywords', 'klasse', 'fach', 'oberthema', 'thema')


def bauen(baustein, inhalt, meta):
    a = baustein.index(ANFANG)
    e = baustein.index(ENDE)
    inhalt = inhalt.strip()
    if not inhalt.startswith(ANFANG) or not inhalt.rstrip().endswith('};'):
        sys.exit('inhalt.js muss mit "var EXAM = {" beginnen und mit "};" enden.')
    s = baustein[:a] + inhalt + '\n' + baustein[e:]
    for k, v in meta.items():
        if k == 'titel':
            s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(v, quote=False) + '</title>', s, count=1)
        elif k in META:
            s, n = re.subn(r'(<meta name="%s" content=")[^"]*(">)' % k,
                           lambda m: m.group(1) + html.escape(v) + m.group(2), s, count=1)
            if not n:
                sys.exit('Meta-Tag %s nicht gefunden.' % k)
        else:
            sys.exit('Unbekannte Angabe: %s (erlaubt: titel, %s)' % (k, ', '.join(META)))
    # Grobe Prüfungen
    ids = re.findall(r"\bid:\s*'([^']+)'\s*,\s*typ:", inhalt)
    if len(ids) != len(set(ids)):
        sys.exit('Teil-Kennungen (id) sind nicht eindeutig: %s' % ids)
    for wort in ('loesung', 'lösung', 'richtig:', 'korrekt:'):
        if wort in inhalt.lower():
            print('WARNUNG: "%s" im Inhalt – stehen dort Lösungen? Lösungen gehören nur in den Erwartungshorizont.' % wort)
    return s


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    b = open(sys.argv[1], encoding='utf-8').read()
    i = open(sys.argv[2], encoding='utf-8').read()
    meta = dict(x.split('=', 1) for x in sys.argv[4:])
    open(sys.argv[3], 'w', encoding='utf-8').write(bauen(b, i, meta))
    print('gebaut:', sys.argv[3])
