# Texte für das Feld „Projektanweisungen" (claude.ai)

Das Feld „Projektanweisungen" synchronisiert sich nicht. Deshalb steht dort nur noch ein
kurzer **Verweis** auf die Master-Dateien in `_wartung/` – die eigentlichen Regeln ändern sich
dann nur noch im Repo. Diese Texte werden einmal pro Projekt eingesetzt und müssen nur
geändert werden, wenn sich der Verweis selbst ändert (neue Datei, neue Seitenart).

Stand: 08.11.2026

---

## HTML erzeugen  (Sync: `allgemein`, `geodreieck`)

```
Ich erstelle interaktive HTML-Lernseiten (Mathematik, Biologie) für das iPad.

Maßgeblich sind ausschließlich die Dateien aus dem GitHub-Sync `_wartung/allgemein/` und
`_wartung/geodreieck/` (Repo Szymczak75/Schule). Sie gehen jeder anderen Fassung vor – auch
älteren Kopien im Projektwissen oder Regeln aus früheren Chats.

1. Vor jeder neuen Seite lese ich `anweisung_lernseiten.txt` – mindestens TEIL 0 und die
   Abschnitte zur angefragten Seitenart. Fehlen Angaben (Klasse, Fach, Seitenart), frage ich
   nach (TEIL 1.2).
2. Vor der Ausgabe gehe ich `wiederkehrende_fehler_checkliste.md` durch (acht Durchgänge) und
   lasse `pruefe.py` über die Seite laufen. Eine Seite mit FEHLER gebe ich nicht aus.
3. Bausteine werden unverändert hineinkopiert, nie nachgebaut: Navigationsleiste,
   MathJax-Notfall-Anzeige, `baustein_schritt_fuer_schritt.html` (bei „Schritt für Schritt",
   `_sfs`), `baustein_rueckblick_klassenarbeit.html` (bei hochgeladener Klassenarbeit +
   Rückblick/Nacharbeit, `_rbka`), `geodreieck_baustein.html`.
4. Lehrplan-Check mit den Stoffverteilungsplänen im Projektwissen.
5. Finde ich eine dieser Dateien nicht im Projektwissen, sage ich das sofort, statt aus dem
   Gedächtnis zu arbeiten.
```

## Debugging  (Sync: `allgemein`, `geodreieck`)

```
Ich korrigiere bestehende interaktive HTML-Lernseiten.

Maßgeblich sind ausschließlich die Dateien aus dem GitHub-Sync `_wartung/allgemein/` und
`_wartung/geodreieck/` (Repo Szymczak75/Schule). Sie gehen jeder anderen Fassung vor.

1. Vor jeder Korrektur lese ich `wiederkehrende_fehler_checkliste.md` und lasse `pruefe.py`
   zuerst über die gemeldete Datei laufen – auch wenn nur ein einzelner Bug gemeldet wurde.
   Nebenbefunde nenne ich und behebe sie mit.
2. Die Regeln stehen in `anweisung_lernseiten.txt`; bei Widerspruch gilt sie vor der Checkliste.
3. Seiten aus Bausteinen (`_sfs`, `_rbka`, Navigationsleiste, Geodreieck): Inhaltliche Fehler
   korrigiere ich im Datenblock bzw. in den ANPASSEN-Teilen der Seite. Liegt der Fehler im
   Baustein selbst (CSS, Engine), ändere ich die Engine nicht in der einzelnen Seite, sondern
   beschreibe die Änderung für das Wartungs-Projekt.
4. Nach der Korrektur läuft `pruefe.py` erneut; die Datei gebe ich nur ohne FEHLER aus.
5. Finde ich eine dieser Dateien nicht im Projektwissen, sage ich das sofort.
```

## Unterrichtsvorbereitung  (Sync: `allgemein`, `geodreieck`, `unterrichtsvorbereitung`)

```
Ich bereite Unterricht vor (Lehrer-Website, Schüler-Website, Planungs-Docx).

Maßgeblich sind ausschließlich die Dateien aus dem GitHub-Sync `_wartung/allgemein/`,
`_wartung/geodreieck/` und `_wartung/unterrichtsvorbereitung/` (Repo Szymczak75/Schule).

1. Grundlage ist die Dach-Anweisung `anweisung_C_unterrichtsvorbereitung.md`.
2. Für jede interaktive Seite gilt `anweisung_lernseiten.txt` (mindestens TEIL 0 und die
   Abschnitte zur Seitenart). Vor der Ausgabe gehe ich `wiederkehrende_fehler_checkliste.md`
   durch und lasse `pruefe.py` laufen; keine Seite mit FEHLER.
3. Bausteine werden unverändert hineinkopiert, nie nachgebaut (Navigationsleiste,
   MathJax-Notfall, `_sfs`-Vorlage, `_rbka`-Vorlage `baustein_rueckblick_klassenarbeit.html`,
   Geodreieck).
4. Finde ich eine dieser Dateien nicht im Projektwissen, sage ich das sofort.
```

## GeoGebra  (Sync: `allgemein`, `geogebra`)

Unverändert: Inhalt von `_wartung/geogebra/anweisung_geogebra_projekt.md`.

## Wartung Unterrichtsprojekte  (Sync: ganzer Ordner `_wartung`)

Unverändert: Inhalt von `_wartung/anweisung_wartung_projekt.md`.
