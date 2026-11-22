# Ideenliste – zurückgestellte Vorhaben

Hier landen Ideen, die (noch) nicht umgesetzt werden. Claude fragt im Wartungs-Projekt
gelegentlich nach, ob eine davon jetzt dran ist – umgesetzt wird erst nach ausdrücklichem OK.

Status: `zurückgestellt` · `als Nächstes` · `verworfen` · `erledigt`

---

## 1. Bruch-Eingabefeld (Klasse 6–10)
- **Status:** erledigt (22.11.2026) – umgesetzt als `allgemein/baustein_formeltool.html` (v1,
  einfache Form: Bruch, gemischte Zahl, Hochzahl, Index, Quadratwurzel, n-te Wurzel) plus
  getrennte Zähler/Nenner-Felder; Regel in `anweisung_lernseiten.txt` TEIL 4.7. Offen: Einbau in
  die Engines `_rbka`, `_sfs`, EXAM (auf Wunsch); später evtl. Verschachtelung (Bruch im Bruch).
- **Idee:** Kleiner eigener Baustein: Taste „Bruch" fügt ein Eingabefeld mit Zähler/Nenner ein,
  zusätzlich **gemischte Zahlen** (Ganzes + Zähler/Nenner). Evtl. später Potenz/Wurzel.
- **Warum gut:** auswertbar (Zähler/Nenner liegen getrennt vor → Kürzen/Gleichwertigkeit prüfbar),
  passt zur Regel „div-basierte Brüche auf Websites".
- **Bewusst NICHT:** externe Formel-Bibliothek (MathLive o. ä.) – lädt ~1 MB von außen,
  schwer auszuwerten, zweites Darstellungssystem neben MathJax.
- **Didaktik:** Lineare Eingabe bleibt Standard; das Bruchfeld nur dort, wo die Schreibweise
  nicht selbst geübt werden soll.
- **Umsetzung später:** als Baustein in `_wartung/allgemein/` (wie Geodreieck), mit Testseite,
  Regel in `anweisung_lernseiten.txt`, Checkliste und `pruefe.py` nachziehen.

## 2. Zeichen-/Schreibfläche für den Stift
- **Status:** zurückgestellt – derzeit nicht nötig (nicht auswertbar). Nur auf Nachfrage der
  Lehrkraft wieder aufgreifen, nicht von selbst vorschlagen.
- **Machbarkeit (geklärt):** Canvas + Pointer-Events mit `setPointerCapture`; nur Stift zeichnet,
  Finger scrollt (Handballen-Erkennung); Striche als Punktlisten im `sessionStorage`, nicht als Bild.
