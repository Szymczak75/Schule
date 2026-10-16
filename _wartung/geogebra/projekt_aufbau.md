# Das neue GeoGebra-Projekt einrichten

Kurzanleitung: was hochgeladen wird, was in die Projektanweisung kommt und was
danach mit dem alten Projekt passiert.

---

## 1. Projekt anlegen

**Name:** GeoGebra-Bedienung
**Beschreibung:** Lernseiten zur handwerklichen Nutzung der GeoGebra Suite –
Grafikrechner, CAS, Geometrie, 3D und Stochastik. Jahrgangsstufe 5 bis Q2.

---

## 2. Projektanweisung einfügen

Den Inhalt von **`anweisung_geogebra_projekt.md`** in das Feld
„Projektanweisungen" kopieren. Das ist der Text, der in jeder Unterhaltung
mitgelesen wird – deshalb ist er bewusst kurz gehalten und verweist für Details auf
die Dateien im Projektwissen.

---

## 3. Projektwissen hochladen

### Pflicht – ohne diese Dateien funktioniert es nicht

| Datei | wofür |
|---|---|
| `css.txt` | Stylesheet des Baukastens |
| `helfer.js` | JavaScript-Helfer |
| `bauer.py` | Seiten-Bauer |
| `koord.py` | Koordinatensystem-Grafiken |
| `pruefe.py` | Prüf-Brille |
| `test.js` | Browsertest |
| `LIESMICH.md` | wie der Baukasten benutzt wird |
| `baustein_navigation.html` | Navigationsleiste, die `bauer.py` in jede Seite setzt |

Diese acht gehören zusammen. Claude schreibt sie zu Beginn jeder Sitzung nach
`/tmp/gg/` und baut damit.

### Pflicht – inhaltlich

| Datei | wofür |
|---|---|
| `geogebra_befehle_geprueft.md` | jede Tastenfolge und jeder Befehl, mit Quelle. Verhindert geratene Bedienung |
| `anweisung_lernseiten.txt` | die allgemeinen Formatregeln (aktuelle Fassung aus dem Wartungs-Projekt) |
| `wiederkehrende_fehler_checkliste.md` | die Prüf-Brille in Worten (aktuelle Fassung aus dem Wartungs-Projekt) |
| `geogebra_roadmap.md` | was es schon gibt, was entschieden wurde, Statustabellen je Jahrgang |

### Pflicht – Lehrplan

Die Stoffverteilungspläne aus dem alten Projekt kopieren, mindestens:

- Klassen 5/6
- Klassen 7/8
- Klassen 9/10
- Einführungsphase
- Q-Phase GK und LK

Ohne die kann nicht geprüft werden, ob ein Thema in der Jahrgangsstufe überhaupt
vorkommen darf. Genau daran ist es schon zweimal gescheitert – Kreisberechnungen in
Klasse 8 und Wurzeln in Klasse 7.

### Freiwillig

`beispiel_bauskript.py`, `beispiel_plan.json` und `beispielseite.html` zeigen einen
vollständigen Durchlauf mit allen Bausteinen. Nützlich zum Nachschlagen, aber nicht
nötig – `LIESMICH.md` enthält dasselbe als Text.

---

## 4. Der erste Aufruf in einer neuen Unterhaltung

Es genügt ein Satz wie:

> Bau mir eine Lernseite für Klasse 9 zum Befehl Extremum, Erarbeitung, vier Karten.

Claude sollte dann von selbst: Lehrplan prüfen, Baukasten wiederherstellen,
Bauskript schreiben, bauen, Prüf-Brille und Browsertest laufen lassen und die Seite
schicken. Wenn etwas davon ausbleibt, fehlt vermutlich eine der Pflichtdateien.

---

## 5. Was mit dem alten Projekt passiert

GeoGebra bleibt dort ein Thema – als **Werkzeug in Fachaufgaben**. Was bleibt:

- die Kennzeichnungspflicht ab EF („mit GeoGebra" / „ohne Hilfsmittel",
  „rechnerisch" / „grafisch bestimmen")
- die Möglichkeit, GeoGebra-Bedienung als Inhalt der Wiederholungskarte zu nehmen
- das Verbot, GeoGebra technisch einzubinden (`deployggb.js`, `.ggb`-Dateien)

Was umzieht: die komplette Bedienungsreihe, die Roadmap und alles, was mit dem Bau
dieser Seiten zu tun hat. Der bisherige **ANHANG B** steht in `anweisung_lernseiten.txt`,
die alle Projekte gemeinsam nutzen; er ist dort im Wartungs-Projekt bereits durch die
neue Fassung („GeoGebra in diesen Projekten") ersetzt. `ANHANG_B_neu.md` wird deshalb
nicht mehr gebraucht.

So gibt es keine zwei Wahrheiten: Bedienung steht nur noch im neuen Projekt,
Fachaufgaben mit GeoGebra als Werkzeug nur noch im alten.

---

## 6. Wenn sich etwas ändert

**Allgemeine Regeln** (`anweisung_lernseiten.txt`, `wiederkehrende_fehler_checkliste.md`,
`pruefe.py`) werden nie hier, sondern nur im Wartungs-Projekt geändert und von dort in alle
Projekte verteilt.

Der Baukasten liegt als Datei im Projektwissen – eine Änderung am Layout ist deshalb
eine Änderung an **einer** Datei, nicht an dreißig Seiten. Wird `css.txt` geändert,
gilt das ab der nächsten gebauten Seite; die schon gebauten behalten ihr eigenes,
eingebettetes Stylesheet. Sollen alte Seiten mitziehen, muss das ausdrücklich gesagt
werden – dann werden sie per Skript nachgezogen.

Dasselbe gilt für `geogebra_befehle_geprueft.md`: Was am Gerät geprüft wurde, kommt
dort hinein, mit Datum. Beim nächsten Mal wird es nicht noch einmal geraten.
