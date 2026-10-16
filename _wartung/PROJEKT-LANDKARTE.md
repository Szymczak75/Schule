# PROJEKT-LANDKARTE

Diese Übersicht zeigt, welche Referenzdatei in welches reale Projekt gehört.

**Seit 16.10.2026 liegen alle Master-Kopien im Repo `Szymczak75/Schule` im Ordner
`_wartung/`.** Die Projekte binden die passenden Unterordner über die GitHub-Synchronisation
von claude.ai ein (siehe `_wartung/LIESMICH.md`). Nach einer Änderung genügt im Projekt
„Synchronisieren" – das Hochladen von Hand entfällt.

## Die vier realen Projekte

| Reales Projekt | GitHub-Ordner | Lernseiten-Anweisung | Fehler-Checkliste | `pruefe.py` | MathJax-Notfall | Dach-Anweisung (.md) | Geodreieck-Baustein |
|---|---|---|---|---|---|---|---|
| **Unterrichtsvorbereitung** | `allgemein`, `geodreieck`, `unterrichtsvorbereitung` | ja | ja | ja | ja | ja (`anweisung_C_unterrichtsvorbereitung.md`) | ja |
| **HTML erzeugen** | `allgemein`, `geodreieck` | ja | ja | ja | ja | — (nicht nötig) | ja |
| **Debugging** | `allgemein`, `geodreieck` | ja | ja | ja | ja | — (nicht nötig) | ja |
| **GeoGebra** (Bedienungsseiten) | `allgemein`, `geogebra` | ja | ja | ja | — (steckt in `helfer.js`; liegt über `allgemein` trotzdem mit an, schadet nicht) | — | — (nicht nötig) |
| **Wartung Unterrichtsprojekte** | ganzer Ordner `_wartung` | alles | | | | | |

**Allgemeine Dateien** (`_wartung/allgemein/`: Lernseiten-Anweisung, Fehler-Checkliste,
`pruefe.py`, MathJax-Notfall) sind in allen Projekten **identisch** und werden nur hier
geändert.

## Nur im Projekt „GeoGebra" (`_wartung/geogebra/`)

Die Master-Kopie liegt hier, damit eine Änderung an allgemeinen Regeln (z. B. Farbschema,
`.frac`-CSS, Notfall-Anzeige, Speicherregel) auch im Baukasten nachgezogen werden kann.

| Datei | Zweck | Muss bei allgemeinen Änderungen mitgeprüft werden? |
|---|---|---|
| `anweisung_geogebra_projekt.md` | Text für das Feld „Projektanweisungen" | ja, wenn sie eine allgemeine Regel zusammenfasst („Die harten Formatregeln") – **Text muss von Hand ins Feld** |
| `css.txt` | Stylesheet des Baukastens | **ja** – Farben, Schriftgrößen, `.frac`, `svg`-Selektoren |
| `helfer.js` | JS-Helfer inkl. MathJax-Notfall-Anzeige | **ja** – Notfall-Anzeige muss mit `baustein_mathjax_notfall.js` übereinstimmen; Speicherregel |
| `bauer.py` | Seiten-Bauer (Meta-Tags, Farbschemata, T-Rex) | **ja** – Meta-Tags, Farbschemata |
| `koord.py` | Koordinatensystem-SVGs | ja – Regeln für Koordinatensysteme |
| `test.js` | Browsertest (Playwright) | selten |
| `LIESMICH.md` | Bedienungsanleitung des Baukastens | bei Baukasten-Änderungen |
| `geogebra_befehle_geprueft.md` | geprüfte Tastenfolgen und Befehle | nein (fachlich) – Änderungen aus dem GeoGebra-Projekt bitte melden, damit sie hier per PR landen |
| `geogebra_roadmap.md` | Stand der Reihe, Entscheidungen | nein – aber Abschnitt „Für das Wartungs-Projekt" lesen |
| `projekt_aufbau.md` | Einrichtungsanleitung des Projekts | selten |
| `beispiel_bauskript.py`, `beispiel_plan.json`, `beispielseite.html` | freiwilliges Anschauungsmaterial (liegen **nicht** in `_wartung`) | nach Baukasten-Änderung neu erzeugen |
| Stoffverteilungspläne | Lehrplan-Check (eigene Uploads im Projekt) | nein |

**Achtung Schreibrecht:** Über die GitHub-Synchronisation ist das Projektwissen
schreibgeschützt. Fachliche Funde aus dem GeoGebra-Projekt (Roadmap, geprüfte Befehle)
werden deshalb hier im Wartungs-Projekt per PR eingetragen.

**Nicht mehr gebraucht:** `ANHANG_B_neu.md` – der Text steht als ANHANG B in
`anweisung_lernseiten.txt`.

## Nur noch EINE Lernseiten-Anweisung
Alle vier Projekte nutzen dieselbe Lernseiten-Anweisung (`anweisung_lernseiten.txt`).
Sie enthält u. a. `thema_rbka.html` (Rückblick Klassenarbeit) und den ausführlichen
Koordinatensysteme-Abschnitt – das Debugging-Projekt braucht das mit, weil es auch
rbka-Seiten korrigiert. Es gibt keine abweichende Variante mehr.

Aufbau: TEIL 0 der Anweisung ist die Kurzfassung der härtesten Pflichtregeln, TEIL 1–10 die
Ausführung (TEIL 6: Zustand im `sessionStorage`, seit 16.10.2026), TEIL 11 das Prüfwerkzeug
`pruefe.py`, ANHANG A Geodreieck, ANHANG B „GeoGebra in diesen Projekten".

**Achtung Dateiname:** Die Anweisung heißt überall `anweisung_lernseiten.txt` (nicht `.md`).

## Fehler-Checkliste
`wiederkehrende_fehler_checkliste.md` gehört in **alle** Projekte. Sie enthält den
achtstufigen Prüf-Ablauf und die real wiederholt aufgetretenen Fehler. Sie ersetzt die
Anweisung nicht, sondern ist die Prüf-Brille davor – bei Widerspruch gilt
`anweisung_lernseiten.txt`.

Damit sie in jedem Chat auch wirklich gelesen wird, muss sie in den **Projektanweisungs-
Texten** der realen Projekte namentlich genannt werden (Textbausteine siehe unten). Das
kann nur der Nutzer selbst in den Projekteinstellungen auf claude.ai eintragen.

### Textbaustein für die Projektanweisung „Debugging"
> Vor jeder Korrektur lese ich `wiederkehrende_fehler_checkliste.md`, lasse `pruefe.py` über
> die gemeldete Datei laufen und prüfe sie gegen die dort gesammelten wiederkehrenden Fehler –
> auch wenn der Nutzer nur einen einzelnen Bug gemeldet hat.

### Textbaustein für „HTML erzeugen" und „Unterrichtsvorbereitung"
> Vor der Ausgabe jeder Seite gehe ich `wiederkehrende_fehler_checkliste.md` durch
> (Prüf-Ablauf in acht Durchgängen), lasse `pruefe.py` darüber laufen und stelle sicher, dass
> keiner der dort gelisteten wiederkehrenden Fehler in der neuen Seite steckt. Seiten mit
> Formeln bekommen am Skriptende die Notfall-Anzeige aus `baustein_mathjax_notfall.js`.

### GeoGebra
Die Projektanweisung `anweisung_geogebra_projekt.md` nennt beide Dateien und `pruefe.py`
bereits – dort ist kein zusätzlicher Textbaustein nötig.

## Prüfwerkzeug `pruefe.py`
Ein Programm, das die maschinell prüfbaren Punkte der Fehler-Checkliste über fertige Seiten
laufen lässt. **Identisch in allen Projekten**, geändert wird es nur hier. Im
GeoGebra-Projekt ist es Teil des Baukastens (`/tmp/gg/pruefe.py`), in den anderen Projekten
wird es einfach ins Arbeitsverzeichnis geschrieben (Lernseiten-Anweisung TEIL 11).

## MathJax-Notfall-Anzeige
`baustein_mathjax_notfall.js` wird in jede Seite mit Formeln **hineinkopiert** (nicht
verlinkt). Im GeoGebra-Projekt steckt derselbe Code am Ende von `helfer.js` – bei einer
Änderung **beide** Stellen nachziehen.

## Geodreieck
Der Baustein ist für die drei Unterrichts-Projekte identisch. Er heißt jetzt überall
**`geodreieck_baustein.html`** – so, wie ANHANG A der Anweisung ihn nennt (die frühere
Wartungs-Kopie hieß `baustein_geodreieck.html`; die Namensabweichung ist damit erledigt).
Das GeoGebra-Projekt braucht ihn nicht. Der Baustein hält den Zustand bewusst nur im
JS-Speicher (Entscheidung 16.10.2026).

> Offener Punkt (nicht dringend): Die Demo-Seite des Bausteins selbst hält die heutigen
> Regeln nicht ein (eigene Blautöne, `font-size` .85em/.9rem, veralteter Beschreibungstext
> „Dreh-Griff" im Abschnitt 2). Der Baustein-Code (`mountGeodreieck`, `.geo-*`) ist davon
> nur bei `.geo-hint`/`.geo-rot-hint` (Schrift unter 1rem) betroffen. Bei der nächsten
> Geodreieck-Änderung mit bereinigen.

## Dach-Anweisung (.md)
Nur das Projekt „Unterrichtsvorbereitung" hat zusätzlich die übergeordnete
Dach-Anweisung `anweisung_C_unterrichtsvorbereitung.md` (Lehrer-Website /
Schüler-Website / Planungs-Docx). Die anderen Projekte brauchen sie nicht.

## Erinnerung nach jeder Änderung
PR mergen → in den betroffenen Projekten „Synchronisieren". Geänderte
Projektanweisungs-Texte weiterhin von Hand ins Feld „Projektanweisungen" kopieren.
