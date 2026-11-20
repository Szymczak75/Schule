# Anweisung EXAM – bewertete Tests auf dem iPad

Stand: 20.11.2026 · Engine `baustein_exam.html` v1.1 · gilt für das Projekt **„EXAM"**
(Sync: `_wartung/exam`, `_wartung/allgemein`).

Ein EXAM ist ein **bewerteter Test**, den die Klasse auf dem iPad schreibt. Die Seite gibt
kein Feedback, enthält keine Lösungen, sperrt sich beim Verlassen und erzeugt am Ende ein
anonymes PDF. Claude bewertet die PDFs **vor** – die endgültige Bewertung macht immer die
Lehrkraft.

**Jeder Test bekommt einen eigenen Chat im Projekt „EXAM".** In diesem Chat entstehen
Testseite und Erwartungshorizont, und dorthin kommen später die abgegebenen PDFs.

---

## 1. Der Ablauf auf einen Blick

| Phase | Wer | Was |
|---|---|---|
| **Erstellen** | Claude im Test-Chat | Testseite `thema_exam.html` aus dem Baustein + Erwartungshorizont (Abschnitt 6) |
| **Vorbereiten** | Lehrkraft | `intern/EXAM/vorbereitung.html`: Adresse der Testseite + Anzahl → alphabetisch sortierte Codes, Freischaltcode, Link und QR-Code; Liste und Zettel drucken |
| **Durchführen** | Klasse | QR-Code scannen → Seite lädt → **Flugmodus an** → Code + Initialen → Test → „Wirklich abgeben?" → PDF herunterladen → Flugmodus aus → in Teams **in der Aufgabe** hochladen |
| **Bewerten** | Claude im Test-Chat | alle PDFs einlesen, nach Erwartungshorizont vorbewerten → Excel (nach Codes) + Gesamt-PDF mit Korrekturen (Abschnitt 7) |
| **Abschließen** | Lehrkraft | Punkte prüfen und ändern, Codes in Excel durch Namen ersetzen, Noten übertragen |

---

## 2. Grundregeln (Pflicht)

1. **Nur aus dem Baustein.** Jede Testseite entsteht mit
   `python3 exam_bauen.py baustein_exam.html inhalt.js thema_exam.html titel=… klasse=… …`.
   Geschrieben wird nur der Block `var EXAM = {…};` (Abschnitt 3) und die Meta-Angaben. Die
   Engine wird nie verändert oder nachgebaut. Fehlt etwas in der Engine, wird es im
   Wartungs-Projekt ergänzt.
2. **Keine Lösungen auf der Seite.** Nicht im Text, nicht in Kennungen (`id`), nicht in der
   Reihenfolge, nicht in Kommentaren. Lösungen stehen nur im Erwartungshorizont.
3. **Erwartungshorizont nie ins Repo.** Die Website ist öffentlich – der Erwartungshorizont
   bleibt im Test-Chat bzw. im Projektwissen des Projekts „EXAM".
4. **Startreihenfolge ist nie die Lösung.** Sortierkarten und Auswahl-Optionen stehen in einer
   bewusst durcheinandergewürfelten Reihenfolge; die richtige Reihenfolge darf auch nicht
   zufällig herauskommen.
5. **Im Einleitungstext nicht die Lösung vorwegnehmen** – auch keine Fachbegriffe, die
   beschriftet werden sollen.
6. **Anrede:** Sek I `anrede: 'du'`, Oberstufe (EF/Q1/Q2) `anrede: 'sie'` – in allen Texten
   des EXAM-INHALTS durchgehend (Lernseiten-Anweisung TEIL 3.7).
7. **Abbildungen** sind eigene SVGs (keine fremden Bilder), mit `viewBox`, `role="img"` und
   `aria-label`, Farben nur aus dem Farbschema (Lernseiten-Anweisung 2.2). Nummern setzt die
   Engine selbst (`nummern`), sie gehören nicht ins SVG.
8. **Anonym.** Die Seite fragt nur Code und Initialen ab. Keine Namen, keine Klasse, keine
   Schule im Inhalt.
9. **Prüfen vor der Ausgabe:** `pruefe.py` ohne FEHLER und ein Durchlauf im Browser
   (Abschnitt 8). Danach gilt TEIL 0 Nr. 26 der Lernseiten-Anweisung: erst im Chat zeigen,
   nach dem OK per Pull Request nach `intern/EXAM/`.

---

## 3. Der EXAM-INHALT

```js
var EXAM = {
  thema: 'Neurobiologie',                 // Dateiname EXAM_<thema>_<Code>.pdf, PDF-Kopf
  titel: '🧠 EXAM · Neurobiologie',       // Seitenkopf
  untertitel: 'Neuron, Synapse und Signalübertragung',
  anrede: 'sie',                          // 'du' (Sek I) oder 'sie' (Oberstufe)
  zeit: 30,                               // Richtzeit in Minuten (nur Orientierung)
  flugmodus: true,                        // Standard: Test nur im Flugmodus (false = ohne Netzprüfung)
  speicher: 'aszym:neurobiologie_exam:v1',// eindeutig je Seite; bei Inhaltsänderung hochzählen
  aufgaben: [
    { titel: 'Aufgabe 1 · Bau einer Nervenzelle', kurz: 'Neuron',
      einleitung: '<p>…</p>',             // HTML, darf leer sein
      teile: [ { id: '1', typ: 'beschriften', auftrag: '…', svg: '<svg …>…</svg>',
                 nummern: [ {nr:1, x:60, y:40, zx:105, zy:88}, … ] } ] },
    …
  ]
};
```

- **Aufgabe** = ein Reiter und eine Spalte in Excel. **Teil** = Teilaufgabe (a, b, …).
- **`id`** des Teils: `'1'`, `'3a'`, `'3b'` … – eindeutig, sie verbindet Seite, PDF und
  Erwartungshorizont.
- **`auftrag`** ist der Arbeitsauftrag mit Operator; bei mehreren Teilen mit „a)", „b)".

### Teil-Typen

| `typ` | Felder | Was die Klasse tut | Im PDF |
|---|---|---|---|
| `beschriften` | `svg`, `nummern` `[{nr, x, y, zx, zy}]` (Kreis bei x/y, Zielpunkt zx/zy) | trägt zu jeder Nummer einen Begriff ein | Abbildung + Liste „Nr: Begriff" |
| `sortieren` | `karten` `[{id, t}]`, optional **eine** Karte `{id, t:'❓ Fehlender Schritt', fehlt:true}` | legt die Karten per Antippen auf nummerierte Plätze | gelegte Reihenfolge, nicht gelegte Karten |
| `auswahl` | `optionen` `[{id, t}]`, `mehrfach: true/false` | tippt eine (bzw. mehrere) Optionen an | alle Optionen mit [X] / [ ] |
| `freitext` | – | schreibt einen Text | Text genau so, wie eingegeben |

**Kennungen** (`id` der Karten und Optionen) sind neutral und ohne Muster (`'kq'`, `'kd'`,
`'oa'` …) – nie `'schritt1'`, `'richtig'` oder alphabetisch in Lösungsreihenfolge.

**Formeln:** möglichst als Unicode (Ca²⁺, Na⁺, ½). Braucht ein Test echte Formeln, kommt der
MathJax-Block der Lernseiten-Anweisung (7.4) in den `<head>`; im PDF erscheinen sie dann als
TeX-Quelltext.

---

## 4. Vorbereitung (Lehrkraft)

`https://szymczak75.github.io/Schule/intern/EXAM/vorbereitung.html` – eine Seite für alle Tests:

1. Adresse der Testseite und Anzahl der Codes eintragen → **Test vorbereiten**.
2. Es entstehen: **alphabetisch sortierte Codes** (4 Buchstaben + Prüfbuchstabe, z. B. `HKWP-Z` – nur Buchstaben, ohne I, L, O),
   ein **Freischaltcode** (entsperrt ein gesperrtes iPad), der **Link für die Klasse**
   (`…_exam.html?l=<Hash des Freischaltcodes>`) und ein **QR-Code** (groß für den Beamer).
3. **Drucken:** Liste für die Lehrkraft (Freischaltcode, Link, Code + Namenszeile) und Zettel
   zum Ausschneiden. Codes in der Reihenfolge der Klassenliste vergeben – dann stimmt die
   alphabetische Reihenfolge der Codes später mit der Namensliste in Excel überein.

Der Freischaltcode wird nirgends gespeichert außer auf dem Ausdruck (und solange der Tab offen
ist). Ohne `?l=` im Link startet die Testseite nicht.

---

## 5. Durchführung (Klasse)

- **Ohne Apple Classroom, mit Flugmodus** (Entscheidung 20.11.2026). Classroom und Flugmodus
  schließen sich aus: Im Flugmodus ist das iPad für Classroom offline, und während einer
  Classroom-App-Sperre kommt man nicht ins Kontrollzentrum.
- QR-Code zeigen oder Link verteilen → die Seite lädt → **Flugmodus einschalten** (WLAN aus).
  Erst offline lassen sich Code und Initialen eingeben. Nach dem Laden braucht die Seite kein
  Netz mehr; auch das PDF entsteht offline.
- Start: **Code** (wird über das Prüfzeichen geprüft) und **Initialen** (2–3 Buchstaben). Erst
  dann erscheinen die Aufgaben, die Orientierungsuhr läuft.
- Wird während des Tests das Netz eingeschaltet (Flugmodus aus oder WLAN im Flugmodus an),
  **sperrt** sich der Test. Entsperren geht nur offline.
- Zwischen den Aufgaben frei wechseln. Rechtschreibhilfen sind aus (`spellcheck`,
  `autocorrect`); Text kann außerhalb der Felder nicht markiert/nachgeschlagen werden.
- Verlassen (Tab, App, Neuladen) **sperrt** den Test; Entsperren mit dem Freischaltcode.
  Jede Sperre und jeder falsche Freischaltcode steht mit Uhrzeit im PDF.
- **Abgeben** → „Wirklich abgeben?" → Felder werden gesperrt → **PDF herunterladen**
  (`EXAM_<thema>_<Code>.pdf`) → Flugmodus aus → in Teams in der **Aufgabe** hochladen (nicht im
  Kanal).
- Grenzen: Wird der Tab geschlossen, sind die Antworten weg (nur `sessionStorage`). Neu laden
  im Flugmodus scheitert (keine Verbindung): Flugmodus kurz aus, Seite lädt gesperrt mit allen
  Antworten, Flugmodus wieder an, Lehrkraft entsperrt. Andere Apps lassen sich öffnen – das
  sperrt die Seite und steht im PDF; ein Zweitgerät bemerkt die Seite nicht. Aufsicht bleibt
  nötig.

### Das Abgabe-PDF
Kopf mit Code, Initialen, Start, Abgabe, Dauer und Sperrprotokoll; danach jede Aufgabe mit
Auftrag, Abbildung und Antwort. Zusätzlich steckt im PDF die Datei **`abgabe.json`** mit allen
Antworten maschinenlesbar (Format `exam-abgabe-1`) – daraus liest Claude bei der Bewertung.

---

## 6. Erwartungshorizont (entsteht mit der Testseite)

Claude liefert ihn als Datei `erwartungshorizont_<thema>.md` im Test-Chat (und legt ihn, wenn
möglich, ins Projektwissen von „EXAM"). **Nie ins Repo.** Aufbau:

```markdown
# Erwartungshorizont – EXAM Neurobiologie (Q1)
Testseite: intern/EXAM/neurobiologie_exam.html · speicher: aszym:neurobiologie_exam:v1
Höchstpunkte gesamt: 34

## Aufgabe 1 · Bau einer Nervenzelle – 8 P.
### Teil 1 (beschriften) – 8 P., je Nummer 1 P.
| Nr | erwartet | auch richtig | Hinweis |
|---|---|---|---|
| 1 | Dendrit | Dendriten | |
…
## Aufgabe 3 · … – 10 P.
### Teil 3a (sortieren) – 6 P.
Richtige Reihenfolge (Karten-id): kb, kw, kr, kq, kx, km, kd
Punkte: Standardregel Sortieren (längste richtige Kette − 1, max. 6 P.)
### Teil 3b (freitext) – 4 P.
Erwartete Inhalte (je 1 P.): …
Fachbegriffe, die richtig geschrieben sein müssen: …
```

- Punkte **je Aufgabe** müssen zu den Spalten der Excel-Vorlage passen (max. 20 Aufgaben).
- Für geschlossene Teile (beschriften, sortieren, auswahl) eine **eindeutige Regel**, damit die
  Vorbewertung nachvollziehbar ist.
- **Standardregel Sortieren** (seit 20.11.2026, Erprobung): Gezählt wird die **längste Kette
  von Karten, die untereinander in richtiger Reihenfolge liegen** – egal, an welchen Plätzen
  (längste Teilfolge in richtiger Reihenfolge; leere Plätze werden übersprungen, die Karte
  „❓ Fehlender Schritt" zählt wie jede andere Karte). **Punkte = Länge der Kette − 1**,
  höchstens Kartenzahl − 1. Ein falsch gelegter Fehler kostet so genau einen Punkt, egal wo er
  liegt; eine völlig verdrehte Reihenfolge gibt 0 Punkte.
  Beispiele bei 5 Karten (max. 4 P.): `1 2 3 4 5` → 4 · `2 3 4 5 1` → 3 · `1 3 2 4 5` → 3 ·
  `3 1 4 5 2` → 2 · `5 4 3 2 1` → 0.
  Nicht „je Karte am richtigen Platz": Dort kostet ein einziger verschobener Fehler alle Punkte
  (`2 3 4 5 1` → 0). Eine abweichende Regel steht ausdrücklich im Erwartungshorizont.
- Für Freitext: erwartete Inhalte mit Teilpunkten, typische Fehlvorstellungen, Umgang mit
  Rechtschreibung und Fachbegriffen.
- Die Lehrkraft prüft den Erwartungshorizont, **bevor** der Test geschrieben wird.

---

## 7. Bewertung (im Test-Chat)

*Wird im zweiten Ausbauschritt festgelegt (Auswertungs-Skript, Excel-Vorlage,
Gesamt-PDF).* Grundsätze, die schon gelten:

- Claude bewertet **vor**, die Lehrkraft entscheidet. Jede Punktvergabe ist begründet.
- Grundlage sind `abgabe.json` aus jedem PDF und der Erwartungshorizont.
- Excel: eine Zeile je Code, **alphabetisch nach Code**, eine Spalte je Aufgabe.
- Gesamt-PDF: alle Abgaben mit Korrekturen (Rechtschreibung, Fachbegriffe, geschlossene Teile
  mit Punkten); Freitext-Punkte stehen nur in Excel.

---

## 8. Prüfen vor der Ausgabe

1. `python3 exam_bauen.py …` meldet keine WARNUNG.
2. `python3 pruefe.py thema_exam.html` – kein FEHLER (Regeln `EXAM`, `ANREDE`, `TYP`, `META`).
3. Browser-Durchlauf (Playwright): ohne `?l=` gesperrt; online sind Code-Felder zu, offline
   (`context.setOffline(true)`) offen; Netz an während des Tests → Sperre, Entsperren nur
   offline; mit Link Code + Initialen → Start;
   jede Aufgabe bearbeiten; Sperre auslösen und mit Freischaltcode lösen; neu laden (bleibt
   gesperrt, Antworten erhalten); abgeben; PDF herunterladen. Das PDF öffnen: Abbildungen da,
   Umlaute richtig, `abgabe.json` als Anhang vorhanden (`pypdf`: `reader.attachments`).
4. Lösungs-Check von Hand: Verrät eine Kennung, eine Startreihenfolge oder ein
   Einleitungssatz die Lösung?

---

## 9. Dateien

| Datei | Ort | Zweck |
|---|---|---|
| `baustein_exam.html` | `_wartung/exam/` | Engine + Beispiel-Inhalt mit allen Teil-Typen |
| `exam_bauen.py` | `_wartung/exam/` | setzt EXAM-INHALT und Meta-Angaben in den Baustein |
| `anweisung_exam.md` | `_wartung/exam/` | diese Anweisung |
| `projektanweisung_exam.md` | `_wartung/exam/` | Text für das Feld „Anweisungen" des Projekts „EXAM" |
| `vorbereitung.html` | `intern/EXAM/` | Codes, Freischaltcode, Link, QR-Code |
| `thema_exam.html` | `intern/EXAM/` | die einzelnen Testseiten |
| `pruefe.py` | `_wartung/allgemein/` | kennt `typ="Exam"` (Regel `EXAM`) |
