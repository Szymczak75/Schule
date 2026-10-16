# _wartung – Master-Kopien aller Unterrichts-Standards

Dieser Ordner ist die **eine Quelle** für alle Regeln, Bausteine und Werkzeuge der vier
claude.ai-Projekte. Geändert wird nur hier (per Pull Request aus dem Wartungs-Projekt).
Die Projekte holen sich die Dateien über die GitHub-Synchronisation von claude.ai.

> Der Ordner ist öffentlich abrufbar (GitHub Pages mit `.nojekyll`), erscheint aber nicht
> auf der Startseite. Er enthält nur Anweisungen und Werkzeuge – keine Schülerdaten,
> keine Passwörter.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `allgemein/` | `anweisung_lernseiten.txt`, `wiederkehrende_fehler_checkliste.md`, `pruefe.py`, `baustein_mathjax_notfall.js` |
| `geodreieck/` | `geodreieck_baustein.html` |
| `unterrichtsvorbereitung/` | `anweisung_C_unterrichtsvorbereitung.md` |
| `geogebra/` | Baukasten (`css.txt`, `helfer.js`, `bauer.py`, `koord.py`, `test.js`, `LIESMICH.md`) und `anweisung_geogebra_projekt.md`, `geogebra_befehle_geprueft.md`, `geogebra_roadmap.md`, `projekt_aufbau.md` |
| `plan/` | laufende Planung (`plan_navigation_impressum.md`) und Entwürfe |
| `PROJEKT-LANDKARTE.md` | welche Datei in welches Projekt gehört |

## Welches Projekt synchronisiert welche Ordner?

| claude.ai-Projekt | Ordner auswählen |
|---|---|
| **Unterrichtsvorbereitung** | `allgemein`, `geodreieck`, `unterrichtsvorbereitung` |
| **HTML erzeugen** | `allgemein`, `geodreieck` |
| **Debugging** | `allgemein`, `geodreieck` |
| **GeoGebra** | `allgemein`, `geogebra` |
| **Wartung Unterrichtsprojekte** | ganzer Ordner `_wartung` |

Stoffverteilungspläne und Lehrpläne liegen **nicht** hier – sie bleiben als eigene Uploads
in den Projekten.

## Einrichten (einmal pro Projekt)

1. Im Projekt die alten, von Hand hochgeladenen Kopien dieser Dateien löschen
   (sonst gibt es zwei Fassungen nebeneinander).
2. Projektwissen → „+" → **GitHub** → Repo `Szymczak75/Schule` → die Ordner aus der Tabelle
   oben anhaken → hinzufügen.

## Nach jeder Änderung

Pull Request mergen → in jedem betroffenen Projekt im Projektwissen auf
**„Synchronisieren"** tippen. Welche Projekte betroffen sind, steht in der Abschluss-
Checkliste jeder Änderung.

Die **Projektanweisungs-Texte** (das Feld „Projektanweisungen") synchronisieren sich nicht –
wenn sich `anweisung_geogebra_projekt.md` oder ein Textbaustein aus der Landkarte ändert,
muss der Text weiterhin von Hand eingesetzt werden.
