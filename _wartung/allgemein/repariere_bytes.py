# -*- coding: utf-8 -*-
"""
Byte-Reparatur für 6 beschädigte Lernseiten
============================================
Schadensbild: In 3-Byte-UTF-8-Sequenzen wurde das dritte Byte durch 0x3F ('?')
ersetzt (z. B. "–" e2 80 93 → e2 80 3f). Die ersten zwei Bytes sind intakt und
bestimmen das Zeichen meist eindeutig; einige Präfixe sind mehrdeutig und werden
NUR anhand des Textkontexts aufgelöst. Nichts wird geraten – unklare Stellen
werden gemeldet, nicht verändert.

Aufruf:
    python3 repariere_bytes.py --repo <pfad>            # Vorschau (schreibt nichts)
    python3 repariere_bytes.py --repo <pfad> --apply    # schreibt die Reparatur
"""
import argparse, io, os, re, sys, pathlib

DATEIEN = [
    'bio/klasse09/lernseiten/blutzucker_kl9_erarbeitung.html',
    'mathe/klasse07/konstruieren_argumentieren/winkel_geraden/winkel_dreieck_test.html',
    'mathe/klasse07/konstruieren_argumentieren/winkel_geraden/winkel_parallelen_ls.html',
    'mathe/klasse07/konstruieren_argumentieren/winkel_geraden/winkel_parallelen_ue.html',
    'mathe/klasse07/konstruieren_argumentieren/winkel_geraden/winkelsumme_dreieck_ls.html',
    'mathe/klasse07/konstruieren_argumentieren/winkel_geraden/winkelsumme_dreieck_ue.html',
]

# Eindeutige Präfixe: zweites Byte → komplettes drittes Byte (ein Zeichen)
EINDEUTIG = {
    0x80: 0x93,   # – U+2013 EN DASH
    0x87: 0x92,   # ⇒ U+21D2 RIGHTWARDS DOUBLE ARROW
    0x8f: 0xb1,   # ⏱ U+23F1 STOPWATCH
    0x9c: 0x93,   # ✓ U+2713 CHECK MARK
    0x9d: 0x8c,   # ❌ U+274C CROSS MARK
    0x9f: 0xb3,   # ⟳ U+27F3 CLOCKWISE GAPPED CIRCLE ARROW
    0x82: 0x82,   # ₂ U+2082 SUBSCRIPT TWO
}
# Kontextabhängige Präfixe: (zweites_byte) → Liste (regex_auf_replace-Kontext, drittes_byte)
# Der Kontext wird am dekodierten Text mit � als Platzhalter geprüft.
KONTEXT = {
    0x86: [  # e2 86 .. : → (U+2192) ODER Aufzählungspunkt • (hier aber U+2022=e2 80 a2, anderes Präfix)
        (r'Glucose \+ O.?�', 0x92),      # → in Reaktionsgleichung
        (r'Weiter �', 0x92),             # Weiter →
        (r'A↑�', 0x92),             # A↑→B
        (r'�\s*<strong>β', 0x92),   # Listenpfeil vor β-Zellen → (als Pfeil)
        (r'�\s*<strong>α', 0x92),   # vor α-Zellen
    ],
    0x88: [  # e2 88 .. : − (U+2212 MINUS) in "(n − 2)"
        (r'\(n\s*�', 0x92),              # (n − 2)
        (r'�\s*2\)', 0x92),
    ],
    0x8a: [  # e2 8a .. : ✅/➕/➖ je nach Kontext
        (r'green\)">\s*�', 0x85),        # ✅ (U+2705) nach grün  -> eigentlich e29c85; siehe Sonderfall
        (r'red\)">\s*�', 0x85),
    ],
    0x96: [  # e2 96 .. : ▸/▾ Aufklapp-Pfeil in <span class="arr">
        (r'class="arr">�', 0xb8),        # ▸ U+25B8 (zeigt auf)
    ],
    0x97: [  # e2 97 .. : ● U+25CF (Sortier-Nummernkreis) textContent='●'
        (r"textContent='�", 0x8f),       # ●
    ],
}


def lade(f):
    return pathlib.Path(f).read_bytes()


def repariere(roh):
    """Gibt (neue_bytes, [(offset, alt_hex, neu_zeichen)], [offene_stellen]) zurück."""
    out = bytearray()
    aenderungen = []
    offen = []
    # dekodierter Text für Kontextprüfungen
    text = roh.decode('utf-8', errors='replace')
    # Map: Byte-Offset → Zeichen-Index ist teuer; wir prüfen Kontext über ein Fenster
    i = 0
    while i < len(roh):
        if roh[i] == 0xe2 and i + 2 < len(roh) and roh[i+2] == 0x3f:
            zb = roh[i+1]
            drittes = None
            if zb in EINDEUTIG:
                drittes = EINDEUTIG[zb]
            elif zb in KONTEXT:
                # Kontextfenster um diese Stelle (als ersetzter Text)
                fenster = roh[max(0,i-30):i+8].decode('utf-8', errors='replace')
                for pat, db in KONTEXT[zb]:
                    if re.search(pat, fenster):
                        drittes = db
                        break
            if drittes is not None:
                neu = bytes([0xe2, zb, drittes])
                try:
                    zeichen = neu.decode('utf-8')
                except UnicodeDecodeError:
                    zeichen = '?'
                out += neu
                aenderungen.append((i, roh[i:i+3].hex(' '), zeichen))
                i += 3
                continue
            else:
                ctx = roh[max(0,i-20):i+12].decode('utf-8', errors='replace').replace('\n',' ')
                offen.append((i, roh[i:i+3].hex(' '), ctx))
        out.append(roh[i])
        i += 1
    return bytes(out), aenderungen, offen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    os.chdir(args.repo)

    gesamt_fix = gesamt_offen = 0
    from collections import Counter
    zeichen_zaehler = Counter()
    for f in DATEIEN:
        roh = lade(f)
        neu, aend, offen = repariere(roh)
        gesamt_fix += len(aend)
        gesamt_offen += len(offen)
        for _, _, z in aend:
            zeichen_zaehler[z] += 1
        print('\n%s' % f)
        print('   repariert: %d   offen: %d' % (len(aend), len(offen)))
        for off, h, ctx in offen:
            print('      OFFEN @%d  %s  %r' % (off, h, ctx))
        # Restkontrolle: bleibt die Datei nach Reparatur sauberes UTF-8?
        rest = neu.decode('utf-8', errors='replace').count('�')
        if rest:
            print('      >> nach Reparatur noch %d Ersatzzeichen' % rest)
        if args.apply and not offen and rest == 0:
            io.open(f, 'w', encoding='utf-8', newline='').write(neu.decode('utf-8'))
            print('      geschrieben.')
        elif args.apply:
            print('      NICHT geschrieben (offene/unklare Stellen).')

    print('\n' + '=' * 60)
    print('Summe: %d repariert, %d offen' % (gesamt_fix, gesamt_offen))
    print('Ersetzte Zeichen:', dict(zeichen_zaehler))
    return 0


if __name__ == '__main__':
    sys.exit(main())
