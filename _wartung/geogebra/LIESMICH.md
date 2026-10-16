# Baukasten für GeoGebra-Lernseiten – Bedienungsanleitung

Dieser Baukasten erzeugt fertige, selbst enthaltene HTML-Lernseiten, die alle
Pflichtregeln der Projektanweisung von sich aus einhalten. Er besteht aus sechs
Dateien, die im Projektwissen liegen:

| Datei | wofür |
|---|---|
| `css.txt` | das komplette Stylesheet mit allen Bausteinen, Farbschema über Platzhalter |
| `helfer.js` | alle JavaScript-Helfer (Karten, Mischen, Prüfen, Tipps, Timer, Formel-Notfall) |
| `bauer.py` | setzt aus Bausteinen die Seite zusammen und schreibt die HTML-Datei |
| `koord.py` | erzeugt statische Koordinatensystem-SVGs mit Achsen, Einheiten und Pfeilen |
| `pruefe.py` | Prüf-Brille: liest fertige Seiten und meldet Verstöße gegen die Regeln (projektübergreifend, wird nur im Wartungs-Projekt geändert) |
| `test.js` | Browsertest: spielt einen Bearbeitungsplan durch und meldet Fehler |

---

## Ablauf in einer neuen Sitzung

**Schritt 1 – Baukasten wiederherstellen.** Die sechs Dateien aus dem Projektwissen
lesen und unverändert nach `/tmp/gg/` schreiben. Erst danach anfangen zu bauen.

**Schritt 2 – Bauskript schreiben.** Eine Python-Datei, die `bauer` importiert und
den Seiteninhalt zusammensetzt:

```python
import sys, os
sys.path.insert(0, '/tmp/gg')
os.environ['GG_ZIEL'] = '/home/claude/seiten'
from bauer import *
from koord import koord, bild, ORANGE, BLAU

B = []
B.append(kopfzeile("Lernseite · Erarbeitung",
                   "Nullstellen finden",
                   "Der Befehl Nullstelle – und der Weg über das Werkzeug",
                   "GeoGebra-Suite · Klasse 8 · Lernhappen 4 von 6 · ca. 20 Minuten"))
B.append(tabs(["1 · Der Befehl", "2 · Ohne Befehl", "3 · Sonderfälle", "4 · Überprüfe dich"]))

B.append(karte_auf('k1', 'Der Befehl Nullstelle', aktiv=True))
B.append(merk('Wo wir gerade stehen:', 'Anknüpfung an den letzten Lernhappen …'))
B.append(merk('⚠️ Vorsicht.', 'Die typische Falle …', warnung=True))
B.append(bauen('Zwei Zeilen eingeben', [
    'Tippe <code>f(x)=x^2-4</code>.',
    'Tippe <code>Nullstelle(f)</code>.']))
B.append(bild(koord(-4, 4, -5, 5, kurven=[(lambda x: x*x-4, ORANGE, 2.8)],
                    alt="Kontrollbild: Parabel mit zwei Nullstellen"),
              "So sieht dein Fenster ungefähr aus."))
B.append(einstellung('Runden einstellen', ['Über das Menü ☰ die Nachkommastellen wählen.']))
# … Aufgabenblock, tipps(...) …
B.append(karte_zu())
B.append(ende())

baue("nullstellen_kl8_ls.html",
     titel="Nullstellen finden – Lernseite Klasse 8",
     beschreibung="Erarbeitungsseite Klasse 8: …",
     keywords="GeoGebra, Grafikrechner, Nullstelle, …",
     thema="Nullstellen", typ="Lernseite", klasse="8",
     body="".join(B), js=JS)
```

**Schritt 3 – bauen:** `python3 bauskript.py`

**Schritt 4 – prüfen:**

```
python3 /tmp/gg/pruefe.py seite.html          # Regelverstöße
node /tmp/gg/test.js seite.html plan.json     # Browsertest
```

Beide müssen sauber durchlaufen, **bevor** die Seite ausgeliefert wird. `pruefe.py`
gibt 1 zurück, wenn Fehler gefunden wurden; `test.js` gibt 1 zurück bei
JavaScript-Fehlern oder horizontalem Scrollen.

**Schritt 5 – ausliefern.** Die HTML-Datei an den Nutzer schicken.

---

## Was der Bauer automatisch erledigt

- alle sieben Pflicht-Meta-Tags
- MathJax-Einbindung exakt nach Vorgabe
- Farbschema **passend zum `typ`**: Lernseite orange, Übung und Rückblick blau,
  Test grau mit dunkelblauem Rand – kein eigener Ton möglich
- Schriftgrößen durchgehend mindestens 1 rem
- T-Rex 🦖 mit „Made by ASzym"
- Notfall-Anzeige für Formeln, falls MathJax nicht geladen werden kann (derselbe Code wie
  `baustein_mathjax_notfall.js` der anderen Projekte)
- Fortschrittsmarken über den Reitern (✅, beim Wissenstest ●)
- **Zustand im `sessionStorage`** (TEIL 6): Eingaben, Auswertungen, gewählte Karte und
  Niveaustufe, offene Tipps, MC-Reihenfolgen und Timer überstehen das Neuladen; nach dem
  Schließen des Tabs startet die Seite leer. Schlüssel `aszym:<datei>:v1` – bei einem
  Umbau einer schon veröffentlichten Seite `baue(..., version=2)` setzen
- keine globale `svg`-Regel; eigene Grafiken werden über `.kontrollbild > svg`
  angesprochen, damit MathJax-Formeln nicht mit aufgeblasen werden

**Was der Bauer nicht kann** und was deshalb beim Schreiben zu beachten bleibt:
die fachliche Richtigkeit der Werte, dass Tipps die Rechnung nicht vorwegnehmen,
dass kein Kontrollbild die gesuchte Lösung zeigt, und die Lehrplan-Einordnung.

---

## Bausteine im Überblick

### Gerüst
| Aufruf | erzeugt |
|---|---|
| `kopfzeile(typtext, h1, unter, serie)` | farbiger Seitenkopf |
| `tabs([...])` | Reiterleiste, merkt sich die Kartenzahl |
| `karte_auf(id, titel, aktiv=False, unter='')` / `karte_zu()` | eine Karte |
| `ende()` | schließt `<main>` |

### Text
| Aufruf | erzeugt |
|---|---|
| `merk(fett, text)` | farbiger Merkkasten |
| `merk(fett, text, warnung=True)` | roter Warnkasten |
| `bauen(titel, [schritte])` | blauer Kasten „🔧 …" mit nummerierten Schritten |
| `einstellung(titel, [absätze])` | Kasten „⚙️ …" für eine App-Einstellung |
| `wz(titel, intro, [schritte], fazit)` | Werkzeug-Weg (derselbe Zweck ohne Befehl) |
| `wz(..., fak=True, wid='wz2')` | derselbe Kasten zum Aufklappen |
| `tipps(id, [(titel, inhalt), …])` | gestufte Hilfen, erst nach dem Prüfen sichtbar |
| `kennz('gg'\|'cas'\|'frei', art)` | Kennzeichnung Hilfsmittel + Lösungsart (Pflicht ab EF) |

### Niveaustufen (Übung)
`stufenwahl(kid)` setzt die drei Knöpfe, `stufe(kid, 'g'\|'f'\|'p', inhalt)` je einen
Block. Jede Stufe führt automatisch ihren eigenen Stand – Umschalten blendet nur um.

### Wissenstest
`timer(32)` setzt den Pflicht-Orientierungstimer **über** die Reiterleiste,
`TIMER_JS % 32` liefert den zugehörigen Code. Die Richtzeit steht damit als
benannte Konstante oben im Skript.

### Grafiken
`koord(xmin, xmax, ymin, ymax, geraden=(), punkte=(), kurven=(), xschritt=1,
yschritt=1, alt="…")` erzeugt ein Koordinatensystem mit Achsen, Pfeilen und
beschrifteten Einheiten. `bild(svg, bildunterschrift)` rahmt es als Kontrollbild.

- `geraden`: Liste von `(m, b, farbe, breite, gestrichelt)`
- `punkte`: Liste von `(x, y, beschriftung, farbe)`
- `kurven`: Liste von `(funktion, farbe, breite)` – die Funktion ist ein normales
  Python-Lambda, z. B. `lambda x: x*x - 4`
- Farben: `ORANGE, BLAU, GRUEN, ROT, LILA`

---

## JavaScript-Helfer

Im Seitenskript steht ein `state`-Objekt je Karte; alles Weitere kommt aus
`helfer.js` und ist ohne Import verfügbar.

| Helfer | Zweck |
|---|---|
| `mische(liste, 'mc1')` | Fisher-Yates, einmal beim Laden aufrufen – **mit Schlüssel**, dann bleibt die Reihenfolge auch nach dem Neuladen gleich |
| `baueMC(wrapId, optionen, karte, feld)` | MC-Knöpfe bauen und binden |
| `mcAuswerten(wrapId, optionen, wahl)` | grün/rot markieren, gibt richtig/falsch zurück |
| `baueWF(karte, scope)` / `wfAuswerten(karte, scope, fbId)` | Wahr/Falsch-Block |
| `pruefeGruppen(gruppen)` | Zahlenfelder prüfen und mit ✅/❌ markieren |
| `leereGruppen(gruppen)` | Felder und Marken zurücksetzen |
| `mitMC(karte, gruppen, opt, wrapId, ids, okText, fehlerText)` | Karte mit Zahlen **und** einer MC-Frage |
| `karteAuswerten(karte, gruppen, ids, okText, fehlerText)` | Karte nur mit Zahlen |
| `checkAuswerten(fragen, 'zsf')` | MC-Block der Abschlusskarte |
| `rechnenAuswerten(gruppen, okText, fehlerText)` | Rechenteil der Abschlusskarte |
| `toggleWz(id)`, `toggleStufe(btn)`, `toggleTipp(id)` | Aufklappen |

Eine Feldgruppe sieht so aus:

```javascript
const G1 = [
  {statusId:'s1', felder:[{id:'z1', erwartet:-2}]},
  {statusId:'s2', felder:[{id:'z2', erwartet:3.14, tol:0.01}]}
];
```

### Zustand übersteht das Neuladen – was dafür zu beachten ist

`helfer.js` speichert nach jedem Tippen und Antippen automatisch und stellt beim Laden alles
wieder her. Ausgewertete Karten werden dabei **durch dieselben Helfer neu ausgewertet**
(`karteAuswerten`, `mitMC`, `wfAuswerten`, `checkAuswerten`, `rechnenAuswerten`) – es wird
kein HTML gespeichert. Damit das klappt:

- Das `state`-Objekt enthält **nur Daten** (Zahlen, Texte, `wahlen`, `geprueft`, `erledigt`).
- Jede MC-Liste wird mit **eigenem Schlüssel** gemischt: `const OPT1 = mische(OPTIONEN1, 'mc1');`
- Eingabefelder haben eine `id`.
- Leeren immer über die Leeren-Helfer (`karteLeeren`, `mitMCleeren`, `rechnenLeeren`) – sie
  löschen die Aufgabe auch im gespeicherten Stand. Eigene Leeren-Funktionen rufen am Ende
  `_vergiss('k3'); speichere();` auf.
- Macht eine **seiteneigene** Prüffunktion mehr als die Helfer (eigene Anzeige, eigene
  Sperre), stellt die Seite das in `function nachWiederherstellen(g){ … }` wieder her –
  `helfer.js` ruft sie nach dem Wiederherstellen auf.

Der Browsertest sollte einmal **neu laden** und prüfen, dass der Stand noch da ist.

`tol` ist die erlaubte Abweichung; ohne Angabe wird exakt verglichen. Eingaben mit
Komma und Brüche wie `-1/3` werden automatisch erkannt.

---

## Testplan für `test.js`

```json
[
 {"karte":"k1",
  "felder":{"z1":"-2","z2":"2"},
  "mc":{"mc1-wahl":"Nullstelle mit dem Funktionsnamen"},
  "klick":["button[onclick=\"pruefeK1()\"]"],
  "zeige":["#fb1"]},
 {"karte":"k3","stufe":"p"},
 {"karte":"k4","felder":{"r1":"7"},"mc":{"c1-wahl":"Richtig"},
  "klick":["button[onclick=\"pruefeCheck()\"]"],"zeige":["#zsf"]}
]
```

Der Text bei `mc` muss die Option **eindeutig** treffen. Weil die Optionen gemischt
werden, niemals über die Position auswählen – und bei ähnlichen Optionen
(`f'(3) = 0` gegen `f''(3) = 0`) den vollständigen Text angeben.

Mindestens zwei Durchläufe gehören zu jeder neuen Seite: einer mit den richtigen
Antworten (alles grün, alle Marken gesetzt) und einer mit falschen Antworten
(rotes Feedback, Tipps erscheinen, Leeren-Knopf da, Leeren gibt wieder frei).
