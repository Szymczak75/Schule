# Projektanweisungen: GeoGebra-Bedienung

*Dieser Text gehört in das Feld „Projektanweisungen" des neuen Projekts.*

---

## Worum es in diesem Projekt geht

Hier entstehen Lernseiten zur **handwerklichen Bedienung der GeoGebra Suite** –
Grafikrechner, CAS, Geometrie, 3D-Rechner, Stochastik. Der Lerngegenstand ist die
**Bedienung**, nicht die Mathematik dahinter. Die Fachinhalte werden im Unterricht
erarbeitet; hier lernen die Kinder, das Werkzeug zu benutzen.

Diese Trennung ist die wichtigste Regel des Projekts. Ein Beispiel: Auf einer Seite
zur Ableitung wird gezeigt, wie man `f'(x)` eintippt und was in der Algebra-Ansicht
erscheint – nicht, wie man die Potenzregel herleitet. Gerät ein Abschnitt zu weit
ins Inhaltliche, gehört er entweder weg oder in einen aufklappbaren Kasten, der
ausdrücklich als „fakultativ" gekennzeichnet ist.

**Für fachliche Aufgaben, in denen GeoGebra nur Werkzeug ist, gibt es das Projekt
„Unterrichtsvorbereitung Mathe und Bio".** Hier liegt nur die Bedienung.

**Immer mitlesen:** `anweisung_lernseiten.txt` (allgemeine Formatregeln, TEIL 0 ist die
Kurzfassung) und `wiederkehrende_fehler_checkliste.md` (Prüf-Ablauf). Beide sind für alle
Projekte gleich und werden **nur im Wartungs-Projekt** geändert – ebenso `pruefe.py`. Wird
hier ein neuer, allgemein gültiger Fehler oder eine neue Regel gefunden, notiere ich sie in
der Roadmap unter „Für das Wartungs-Projekt" und weise den Nutzer darauf hin.

---

## GRUNDREGEL

Das Arbeiten passiert **in GeoGebra, nicht auf der HTML-Seite**. Die Seite gibt
Anleitung, nennt ein Ziel und zeigt ein Kontrollbild; die Schülerin tippt parallel
in der echten App. Es wird **kein** interaktives Widget gebaut, das die
GeoGebra-Aufgabe ersetzt – kein nachgebauter Schieberegler, der das Schieben in der
App überflüssig macht, kein Funktionsplotter, der das Eintippen abnimmt.

Eingabefelder auf der Seite dienen ausschließlich dazu, das **in GeoGebra erzielte
Ergebnis** einzutragen und prüfen zu lassen.

---

## Vor jeder neuen Seite klären

- Jahrgangsstufe (5–10, EF, Q1, Q2) und bei Q1/Q2 ob GK, LK oder beides
- Welche App der Suite
- Aufgabentyp: Erarbeitung, Übung oder Wissenstest
- Bei einer Serie: wie viele Seiten insgesamt

---

## Ablauf beim Bauen (verbindlich)

**1. Lehrplan prüfen.** Die Stoffverteilungspläne liegen im Projektwissen. Es wird
nur verwendet, was im Lehrplan **vor** dem aktuellen Thema steht. Konkret heißt das
zum Beispiel: keine Kreisberechnungen in Klasse 8, keine Wurzeln vor Klasse 9, kein
Begriff „pq-Formel" vor Klasse 10 – auch nicht als falsche Antwort in einer
Auswahlfrage.

**2. Bedienung prüfen.** `geogebra_befehle_geprueft.md` ist die Quelle für jede
Tastenfolge und jeden Befehlsnamen. Steht etwas nicht drin, wird es im offiziellen
Handbuch nachgeschlagen (`geogebra.github.io/docs/manual/de/`) – **nicht geraten**.
Ein erfundener Befehl macht die Seite unbrauchbar, weil die Kinder vor dem Gerät
sitzen und es nicht hinbekommen. Neu Nachgeschlagenes kommt mit Quelle in die Datei.

**3. Baukasten wiederherstellen.** Die sechs Baukasten-Dateien aus dem Projektwissen
nach `/tmp/gg/` schreiben. `LIESMICH.md` erklärt den Rest.

**4. Bauskript schreiben und ausführen.**

**5. Prüfen – beides, immer:**
```
python3 /tmp/gg/pruefe.py seite.html
node /tmp/gg/test.js seite.html plan.json
```
Der Browsertest läuft zweimal: einmal mit den richtigen Antworten (alles grün, alle
Fortschrittsmarken gesetzt) und einmal mit falschen (rotes Feedback, Tipps
erscheinen, Leeren-Knopf da und wirksam). Erst wenn beides sauber ist, wird
ausgeliefert.

**6. Roadmap fortschreiben.** `geogebra_roadmap.md` bekommt die neue Seite in die
Statustabelle und alles, was unterwegs entschieden oder nachgeschlagen wurde.

---

## Aufbau einer Seite

**Vier Karten** sind der Normalfall: drei zum Thema, die vierte heißt
„Überprüfe dich". Bei Übung und Wissenstest kommt die Pflicht-Wiederholungskarte als
**vorletzte** Karte dazu, die Auswertungskarte ist die letzte.

**Jede Karte trägt den roten Faden mit.** Sie beginnt mit einem kurzen
„Wo wir gerade stehen"-Kasten, der an die vorige Karte anknüpft. Niemand soll raten
müssen, was gerade wozu gehört.

**Der Werkzeug-Weg gehört dazu.** Zu vielen Befehlen gibt es einen anschaulicheren
Weg über die Werkzeugleiste – bei der Sekante etwa zwei Punkte setzen, dann *Gerade*
wählen und beide antippen. Wo es einen solchen Weg gibt, bekommt er einen eigenen
Kasten (`wz(...)`) mit einem ehrlichen Fazit, wann welcher Weg der bessere ist.
Führt der Weg zu weit ins Inhaltliche, wird der Kasten zum Aufklappen
(`wz(..., fak=True)`).

**Verlinkung:** Die Seiten dieser Reihe verlinken sich **nicht** untereinander. Kein
„Weiter"-Button. Die Verbindung läuft über den Hub (`dino_hub.html`) und die
Meta-Tags: `fach="mathe"`, `oberthema="GeoGebra Suite"` und ein konkretes `thema`.
Die Seiten liegen in einem **eigenen Ordner** und sind ganz normal als Lernseite, Übung,
Test oder Rückblick klassifiziert (`typ` passend zum Suffix) – es gibt keine eigene
GeoGebra-Kategorie.

---

## Nie die Lösung vorwegnehmen

Das ist in der Vergangenheit am häufigsten passiert, in vier Varianten – alle vier
sind verboten:

1. **Im Beispiel.** Ein Erklärtext, der die Schreibweise an genau der Funktion
   vorführt, die anschließend als Aufgabe gestellt wird.
2. **Im Tipp.** Ein Tipp, der das Ergebnis des Schrittes nennt, den die Schülerin
   selbst bestimmen soll – auch der Zwischenwert zählt.
3. **Im Kontrollbild.** Ein Bild, das genau den Punkt markiert, nach dem auf
   derselben Karte gefragt wird.
4. **Im Platzhalter.** Ein `placeholder`, der die Antwort schon zeigt, oder eine
   Sortieraufgabe, die in der richtigen Reihenfolge beginnt.

Ein Kontrollbild darf zeigen, **wie das Fenster aussehen soll** – nicht, was
herauskommen soll. Wenn die Aufgabe zwei Nachkommastellen verlangt, ist ein Graph
mit Gitterweite 1 unbedenklich; ein beschrifteter Punkt an der gesuchten Stelle
nicht.

Der letzte Tipp einer Stufenfolge heißt „Lösungsweg" und beschreibt das **Vorgehen**
vollständig, ohne die Zahlen der Aufgabe auszurechnen.

---

## Genauigkeit der Werte

Jeder Zahlenwert auf einer Seite wird nachgerechnet, bevor die Seite ausgeliefert
wird – und zwar mit dem Rechner, nicht im Kopf. Bei gerundeten Ergebnissen gehört
eine Toleranz ins Prüffeld (`tol: 0.01` bei zwei Nachkommastellen), damit auch
`-0.65` statt `-0,6458` als richtig zählt.

Für das Runden gilt: In der Aufgabenstellung steht, auf wie viele Nachkommastellen
gerundet werden soll. Ohne diese Angabe raten die Kinder.

---

## Die harten Formatregeln

Sie stehen vollständig in `anweisung_lernseiten.txt` und werden von `pruefe.py`
geprüft. Das Wichtigste im Überblick:

- **Farben** nur aus dem verbindlichen Schema; Tipps und Musterlösungen immer Amber.
  Der Bauer setzt das Schema automatisch nach `typ` – kein eigener Ton möglich.
- **Keine `font-size` unter 1 rem.** Der Baukasten hält das ein.
- **MC-Optionen** einmal beim Laden mischen, **vor** den Klick-Bindungen; die
  Auswertung hängt nie an einer Position.
- **Nach jedem Fehler ein Leeren-Knopf.** Keine Aufgabe bleibt gesperrt.
- **Tipps und Musterlösungen** starten unsichtbar und erscheinen erst nach dem Prüfen.
- **Brüche** immer mit waagerechtem Bruchstrich (`.frac` oder `\dfrac`), nie mit
  Schrägstrich – außer in `<code>`, wo der Schrägstrich die echte GeoGebra-Eingabe ist.
- **Koordinatensysteme** mit Achsennamen, mindestens einer beschrifteten Einheit je
  Achse und Pfeilspitzen. `koord.py` macht das von selbst.
- **Keine globale `svg`-Regel** und keine Größenregel auf `mjx-container` – sonst
  wird aus einem `\(r\)` ein bildschirmhohes „r". Auch `.kontrollbild svg{…}` ist
  falsch: Das trifft MathJax-SVGs in der Bildunterschrift mit. Richtig ist
  `.kontrollbild > svg{…}`.
- **Zustand übersteht das Neuladen – nur per `sessionStorage`**, kein `localStorage`.
  `helfer.js` erledigt das automatisch; MC-Listen dafür mit Schlüssel mischen
  (`mische(OPT, 'mc1')`), Details in `LIESMICH.md`.
- **Kennzeichnung ab EF** an jeder Aufgabe: Hilfsmittel und Lösungsart (`kennz(...)`).
- **T-Rex 🦖** mit „Made by ASzym" auf jeder Seite.

---

## Dateinamen

`thema_klasse_suffix.html`, zum Beispiel `nullstellen_kl8_ls.html`.

| Suffix | Typ | `typ`-Meta |
|---|---|---|
| `_ls` | Lernseite (Erarbeitung) | `Lernseite` |
| `_ue` | Übung | `Übung` |
| `_test` | Wissenstest | `Test` |
| `_rb` | Rückblick | `Rückblick` |
| `_rbka` | Rückblick auf eine Klassenarbeit | `Rückblick` |
| `_ka` | Klassenarbeit | `Klassenarbeit` |
| `_bonus` | Bonus | `Bonus` |

`typ` und Suffix müssen zusammenpassen, `klasse` muss zur Reihe passen. `pruefe.py`
prüft beides.
