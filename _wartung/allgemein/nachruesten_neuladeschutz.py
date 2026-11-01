# -*- coding: utf-8 -*-
"""
Nachrüst-Skript: Neulade-Schutz Stufe 1  (Schritt 3b)
=====================================================
Setzt den Baustein `baustein_neuladeschutz.html` in bestehende interaktive
Seiten ein, die noch keinen sessionStorage-Schutz haben. Der Block wird
UNMITTELBAR VOR den Navigations-Baustein gesetzt (der seit PR #5 auf jeder
Seite steht); fehlt dieser, vor den T-Rex bzw. vor </body>.

Übersprungen werden:
  - Seiten mit <meta name="hubignore"> (Übersichten/Weiterleitungen),
  - Seiten ohne Eingabefelder (nichts zu schützen),
  - Seiten, die bereits `sessionStorage` nutzen (Baukasten-Stufe 2 oder
    schon nachgerüstet) – im seiteneigenen Teil, Navigations-Baustein zählt nicht.

Aufruf:
    python3 nachruesten_neuladeschutz.py --repo <pfad> [--apply] [--limit N]

Ohne --apply: Trockenlauf (schreibt nichts). Idempotent: ein zweiter Lauf
findet nichts mehr (Marker NL_VERSION erkannt bzw. sessionStorage vorhanden).
"""
import argparse, io, os, re, sys, pathlib

NL_VERSION = 'Neulade-Schutz Stufe 1  (v1'
NL_BLOCK = re.compile(
    r'<!-- =+\s*BAUSTEIN: Neulade-Schutz.*?ENDE BAUSTEIN Neulade-Schutz Stufe 1 =+ -->',
    re.S)
NAV_BLOCK = re.compile(
    r'<!-- =+\s*BAUSTEIN: Navigationsleiste.*?ENDE BAUSTEIN Navigationsleiste =+ -->',
    re.S)
TREX = re.compile(r'<div\b[^>]*class="trex"[^>]*>')
FELD = re.compile(r'<input|<textarea|<select', re.I)


def lade_block(repo):
    p = os.path.join(repo, '_wartung', 'allgemein', 'baustein_neuladeschutz.html')
    if not os.path.exists(p):
        raise SystemExit('baustein_neuladeschutz.html fehlt in _wartung/allgemein/')
    b = io.open(p, encoding='utf-8').read().rstrip('\n')
    if NL_VERSION not in b:
        raise SystemExit('baustein_neuladeschutz.html ist nicht v1 – abgebrochen.')
    return b


def lies(pfad):
    roh = pathlib.Path(pfad).read_bytes()
    try:
        return roh.decode('utf-8')
    except UnicodeDecodeError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    block = lade_block(repo)
    root = pathlib.Path(repo)
    seiten = sorted(p for p in root.rglob('*.html')
                    if '.git' not in p.parts and '_wartung' not in p.parts)

    ber = {'eingefügt': [], 'schon_nl': [], 'schon_ss': [], 'hubignore': [],
           'kein_feld': [], 'utf8_skip': [], 'kein_anker': []}
    getan = 0
    for p in seiten:
        if args.limit and getan >= args.limit:
            break
        rel = str(p.relative_to(root))
        h = lies(str(p))
        if h is None:
            ber['utf8_skip'].append(rel); continue
        if 'name="hubignore"' in h:
            ber['hubignore'].append(rel); continue

        # seiteneigener Teil ohne Navigations-Baustein (dessen Feedback-Textfeld
        # und Skript nicht mitzählen)
        eigen = NAV_BLOCK.sub(' ', h)
        if NL_BLOCK.search(h):
            ber['schon_nl'].append(rel); continue
        if not FELD.search(eigen):
            ber['kein_feld'].append(rel); continue
        if 'sessionStorage' in eigen:
            ber['schon_ss'].append(rel); continue

        # Einsetzen: vor den Navigations-Baustein, sonst vor T-Rex, sonst vor </body>
        nav = NAV_BLOCK.search(h)
        if nav:
            pos = nav.start()
        else:
            m = TREX.search(h)
            if m:
                pos = m.start()
            else:
                pos = h.lower().rfind('</body>')
                if pos == -1:
                    ber['kein_anker'].append(rel); continue
        neu = h[:pos] + block + '\n' + h[pos:]
        ber['eingefügt'].append(rel)
        if args.apply:
            io.open(str(p), 'w', encoding='utf-8', newline='').write(neu)
        getan += 1

    def z(t, l, zeige=0):
        print('%-30s %4d' % (t, len(l)))
        for f in l[:zeige]:
            print('      ', f)

    print('\n' + '=' * 70)
    print('NEULADE-SCHUTZ Stufe 1  (%s)' % ('ANGEWENDET' if args.apply else 'TROCKENLAUF'))
    print('=' * 70)
    print('%-30s %4d' % ('Seiten gesamt', len(seiten)))
    z('Block eingefügt', ber['eingefügt'])
    z('schon Neulade-Schutz', ber['schon_nl'])
    z('schon sessionStorage (Stufe 2)', ber['schon_ss'], 50)
    z('ohne Eingabefeld', ber['kein_feld'])
    z('hubignore', ber['hubignore'])
    z('UTF-8 defekt (übersprungen)', ber['utf8_skip'], 50)
    z('kein Anker', ber['kein_anker'], 50)
    print('=' * 70)
    if not args.apply:
        print('Trockenlauf – nichts geschrieben. Mit --apply anwenden.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
