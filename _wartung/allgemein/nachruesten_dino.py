#!/usr/bin/env python3
"""Ersetzt das Eck-Emoji 🦖 (Markenzeichen, Lernseiten-Anweisung 8.3) durch den
feiernden Dino (_wartung/allgemein/dino_ikon.webp, eingebettet als data-URI, 72 px).

Aufruf:  python3 _wartung/allgemein/nachruesten_dino.py [Datei|Ordner ...]
Ohne Argumente: alle .html im Repo (außer dino_hub.html). Mehrfach ausführbar –
schon umgestellte Seiten (class="dino-ikon") werden übersprungen.

Vorgehen je Seite:
- Emoji, das allein in einem Element mit class/id „trex/rex/dino" steht (oder in
  einem button/span darin), wird zu <img class="dino-ikon">.
- Das Eck-Element bekommt class „dino-ecke", ein innerer button/span „dino-huelle".
- Ein eigener position:fixed-Tooltip („Made by …") bekommt „dino-tipp-fest".
- Vor </head> kommt einmal der Stilblock DINO_STIL: alter Kreis/Rahmen weg,
  Tooltips links neben den Dino. Bestehendes JS bleibt unverändert.
"""
import base64, glob, io, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
B64 = base64.b64encode(open(os.path.join(HIER, 'dino_ikon.webp'), 'rb').read()).decode()
IMG = ('<img class="dino-ikon" src="data:image/webp;base64,%s" alt="Dino" '
       'width="72" height="72" draggable="false">' % B64)
DINO_STIL = """<style id="dino-stil">
/* Markenzeichen: feiernder Dino (Lernseiten-Anweisung 8.3) */
.dino-ecke{width:auto!important;height:auto!important;min-width:0!important;min-height:0!important;padding:0!important;background:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;opacity:1!important;font-size:1rem!important;line-height:1.3!important;filter:none!important}
.dino-huelle{all:unset;display:block;cursor:pointer}
.dino-ikon{display:block;width:72px;height:72px;max-width:none;-webkit-user-drag:none;user-select:none}
.dino-ecke>:not(.dino-huelle):not(.dino-ikon){position:absolute!important;right:calc(100% + 6px)!important;bottom:26px!important;left:auto!important;top:auto!important;white-space:nowrap}
.dino-tipp-fest{right:96px!important;bottom:34px!important;left:auto!important;top:auto!important}
</style>
"""
EMOJI = '\U0001F996'
EMOJI_RE = re.compile('\U0001F996|&#129430;|&#x1[fF]996;')
MASKOTTCHEN = re.compile(r'''\b(?:class|id)\s*=\s*["'][^"']*(?:t?rex|dino)[^"']*["']''', re.I)
TAG_VOR = re.compile(r'<([a-zA-Z][\w-]*)\b([^<>]*)>\s*$')


def klasse_dazu(tag, neu):
    m = re.search(r'''\bclass\s*=\s*(["'])(.*?)\1''', tag)
    if m:
        return tag[:m.start(2)] + m.group(2) + ' ' + neu + tag[m.end(2):]
    return re.sub(r'^<([a-zA-Z][\w-]*)', r'<\1 class="%s"' % neu, tag)


def maskiere(h):
    """Bereiche, in denen nichts ersetzt werden darf (head, script, style)."""
    sperr = [(m.start(), m.end()) for m in re.finditer(r'<(script|style|head)\b.*?</\1>', h, re.S | re.I)]
    return lambda p: any(a <= p < b for a, b in sperr)


def feste_tipps(h):
    """Markiert eigene position:fixed-Tooltips („Made by …") mit dino-tipp-fest."""
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
    def ersetze(m):
        tag = m.group(1)
        if re.search(r'dino-(ecke|tipp-fest|ikon|huelle)', tag):
            return m.group(0)
        namen = ['#' + n for n in re.findall(r'''\bid\s*=\s*["']([^"']+)["']''', tag)]
        namen += ['.' + c for k in re.findall(r'''\bclass\s*=\s*["']([^"']+)["']''', tag) for c in k.split()]
        for n in namen:
            for r in re.finditer(re.escape(n) + r'(?![\w-])[^{}]*\{([^}]*)\}', css):
                if re.search(r'position\s*:\s*fixed', r.group(1)):
                    return klasse_dazu(tag, 'dino-tipp-fest') + m.group(2)
        return m.group(0)
    return re.sub(r'(<[a-zA-Z][\w-]*\b[^<>]*>)(\s*Made by)', ersetze, h)


def bearbeite(h):
    if 'class="dino-ikon"' in h:
        return h, 'schon'
    gesperrt = maskiere(h)
    for e in [(m.start(), m.end() - m.start()) for m in EMOJI_RE.finditer(h)]:
        p, n = e
        if gesperrt(p):
            continue
        nach = h[p + n:p + n + 200]
        if not re.match(r'\s*<', nach):
            continue                      # Emoji steht in Fließtext
        m = TAG_VOR.search(h[max(0, p - 600):p])
        if not m:
            continue
        t_start = max(0, p - 600) + m.start()
        tag = m.group(0).rstrip()
        tag = tag[:tag.rfind('>') + 1]
        t_end = t_start + len(tag)
        if MASKOTTCHEN.search(tag):
            wurzel = (t_start, tag); huelle = None
        elif m.group(1).lower() in ('button', 'span'):
            davor = list(re.finditer(r'<[a-zA-Z][\w-]*\b[^<>]*>', h[max(0, t_start - 400):t_start]))
            basis = max(0, t_start - 400)
            # nur Vorfahren: Element darf vor dem Emoji noch nicht geschlossen sein
            kand = [d for d in davor if MASKOTTCHEN.search(d.group(0))
                    and '</' + re.match(r'<([a-zA-Z][\w-]*)', d.group(0)).group(1)
                    not in h[basis + d.end():t_start]]
            if not kand:
                continue
            d = kand[-1]
            wurzel = (max(0, t_start - 400) + d.start(), d.group(0)); huelle = (t_start, tag)
        else:
            continue
        # ersetzen (von hinten nach vorn, damit Positionen stimmen)
        h = h[:p] + IMG + h[p + n:]
        if huelle:
            h = h[:huelle[0]] + klasse_dazu(huelle[1], 'dino-huelle') + h[huelle[0] + len(huelle[1]):]
        w_pos, w_tag = wurzel
        neu = klasse_dazu(w_tag, 'dino-ecke')
        h = h[:w_pos] + neu + h[w_pos + len(w_tag):]
        h = feste_tipps(h)
        if '<style id="dino-stil">' not in h:
            i = h.lower().find('</head>')
            h = h[:i] + DINO_STIL + h[i:]
        return h, 'ok'
    return h, 'kein'


def main(args):
    wurzel = os.path.abspath(os.path.join(HIER, '..', '..'))
    if not args:
        args = [wurzel]
    dateien = []
    for a in args:
        if os.path.isdir(a):
            dateien += glob.glob(os.path.join(a, '**', '*.html'), recursive=True)
        else:
            dateien.append(a)
    stat = {'ok': [], 'schon': [], 'kein': []}
    for f in sorted(dateien):
        if os.path.basename(f) == 'dino_hub.html':
            continue
        h = io.open(f, encoding='utf-8').read()
        if not EMOJI_RE.search(h) and 'dino-ikon' not in h:
            continue
        neu, s = bearbeite(h)
        if s == 'ok':
            io.open(f, 'w', encoding='utf-8').write(neu)
        stat[s].append(os.path.relpath(f, wurzel))
    print('umgestellt: %d, schon erledigt: %d, ohne Eck-Dino: %d'
          % (len(stat['ok']), len(stat['schon']), len(stat['kein'])))
    for f in stat['kein']:
        print('  ohne Eck-Dino:', f)


if __name__ == '__main__':
    main(sys.argv[1:])
