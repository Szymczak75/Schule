# -*- coding: utf-8 -*-
"""Statische Koordinatensystem-SVGs (Kontrollbilder) fuer die Klasse-8-Seiten.
Projektvorgabe: Achsen mit Pfeilen, beschriftet, Einheiten angeschrieben."""

W, H = 340, 260
PAD = 16
INK = "#22303f"
GITTER = "#e8e2d8"


def _mk(xmin, xmax, ymin, ymax):
    sx = lambda x: PAD + (x - xmin) / (xmax - xmin) * (W - 2 * PAD)
    sy = lambda y: (H - PAD) - (y - ymin) / (ymax - ymin) * (H - 2 * PAD)
    return sx, sy


def _clip(m, b, xmin, xmax, ymin, ymax):
    """Sichtbares Stueck der Geraden y = m*x + b als (x1,y1,x2,y2) oder None."""
    pts = []
    for x in (xmin, xmax):
        y = m * x + b
        if ymin - 1e-9 <= y <= ymax + 1e-9:
            pts.append((x, y))
    if abs(m) > 1e-12:
        for y in (ymin, ymax):
            x = (y - b) / m
            if xmin - 1e-9 <= x <= xmax + 1e-9:
                pts.append((x, y))
    # Duplikate raus
    ent = []
    for p in pts:
        if not any(abs(p[0] - q[0]) < 1e-7 and abs(p[1] - q[1]) < 1e-7 for q in ent):
            ent.append(p)
    if len(ent) < 2:
        return None
    ent.sort()
    return ent[0][0], ent[0][1], ent[-1][0], ent[-1][1]


def koord(xmin, xmax, ymin, ymax, geraden=(), punkte=(), xschritt=1, yschritt=1,
          alt="Koordinatensystem", gitter=True, extra="", kurven=()):
    """geraden: (m, b, farbe, breite, gestrichelt)
       punkte : (x, y, label, farbe)"""
    sx, sy = _mk(xmin, xmax, ymin, ymax)
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, H, alt)]

    if gitter:
        x = xmin - xmin % xschritt
        while x <= xmax:
            if abs(x) > 1e-9:
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                         % (sx(x), sy(ymin), sx(x), sy(ymax), GITTER))
            x += xschritt
        y = ymin - ymin % yschritt
        while y <= ymax:
            if abs(y) > 1e-9:
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                         % (sx(xmin), sy(y), sx(xmax), sy(y), GITTER))
            y += yschritt

    # Geraden
    for (m, b, farbe, breite, gestr) in geraden:
        c = _clip(m, b, xmin, xmax, ymin, ymax)
        if not c:
            continue
        d = ' stroke-dasharray="6 4"' if gestr else ''
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" '
                 'stroke-linecap="round"%s/>'
                 % (sx(c[0]), sy(c[1]), sx(c[2]), sy(c[3]), farbe, breite, d))

    # Kurven (Funktionen), am Fenster geclippt
    for (fn, farbe, breite) in kurven:
        stueck, n = [], 400
        for i in range(n + 1):
            x = xmin + (xmax - xmin) * i / n
            try:
                y = fn(x)
            except Exception:
                y = None
            if y is None or y != y or y < ymin or y > ymax:
                if len(stueck) > 1:
                    s.append('<polyline fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
                             'points="%s"/>' % (farbe, breite, " ".join(stueck)))
                stueck = []
            else:
                stueck.append("%.1f,%.1f" % (sx(x), sy(y)))
        if len(stueck) > 1:
            s.append('<polyline fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
                     'points="%s"/>' % (farbe, breite, " ".join(stueck)))

    # Achsen mit Pfeilen
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.7"/>'
             % (sx(xmin), sy(0), sx(xmax) + 6, sy(0), INK))
    s.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
             % (sx(xmax) + 12, sy(0), sx(xmax) + 3, sy(0) - 4, sx(xmax) + 3, sy(0) + 4, INK))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.7"/>'
             % (sx(0), sy(ymin), sx(0), sy(ymax) - 6, INK))
    s.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
             % (sx(0), sy(ymax) - 12, sx(0) - 4, sy(ymax) - 3, sx(0) + 4, sy(ymax) - 3, INK))

    # Striche + Zahlen
    x = xmin - xmin % xschritt
    while x <= xmax:
        if abs(x) > 1e-9:
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                     % (sx(x), sy(0) - 4, sx(x), sy(0) + 4, INK))
            s.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s" text-anchor="middle">%s</text>'
                     % (sx(x), sy(0) + 16, INK, ('%g' % x).replace('-', '−')))
        x += xschritt
    y = ymin - ymin % yschritt
    while y <= ymax:
        if abs(y) > 1e-9:
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                     % (sx(0) - 4, sy(y), sx(0) + 4, sy(y), INK))
            s.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s" text-anchor="end">%s</text>'
                     % (sx(0) - 7, sy(y) + 4, INK, ('%g' % y).replace('-', '−')))
        y += yschritt
    s.append('<text x="%.1f" y="%.1f" font-size="12" font-style="italic" fill="%s">x</text>'
             % (sx(xmax) + 2, sy(0) - 8, INK))
    s.append('<text x="%.1f" y="%.1f" font-size="12" font-style="italic" fill="%s">y</text>'
             % (sx(0) + 8, sy(ymax) - 8, INK))

    # Punkte
    for (px, py, label, farbe) in punkte:
        s.append('<circle cx="%.1f" cy="%.1f" r="4.6" fill="%s" stroke="#fff" stroke-width="1.6"/>'
                 % (sx(px), sy(py), farbe))
        if label:
            s.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="700" fill="%s" '
                     'text-anchor="middle">%s</text>' % (sx(px), sy(py) - 10, farbe, label))
    s.append(extra)
    s.append('</svg>')
    return "\n      ".join(s)


ORANGE, BLAU, GRUEN, ROT, LILA = "#c97a2e", "#2f5fa6", "#1e7d32", "#c1272d", "#7a4ea8"


def bild(svg, bu):
    return ('    <div class="kontrollbild">\n      %s\n      <span class="bu">%s</span>\n    </div>\n\n'
            % (svg, bu))
