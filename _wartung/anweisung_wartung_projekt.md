# Projektanweisung: Standards-Pflege (Wartungs-Projekt, verbindlich)

> Diese Datei IST die Projektanweisung des Wartungs-Projekts. Geändert wird sie nur hier im
> Repo (per Pull Request). Im Feld „Anweisungen" des Projekts steht nur ein kurzer Verweis
> auf diese Datei (Wortlaut am Ende). Nach jeder Änderung „Synchronisieren" (seit 21.11.2026).

## Zweck
Zentrale Pflegestelle für meine Unterrichts-Standards. Eine grundsätzliche Änderung an
einem Baustein oder einer Regel wird hier EINMAL umgesetzt und gilt dann in allen Projekten.

## Wo alles liegt
- **Master-Kopien:** GitHub-Repo `Szymczak75/Schule`, Ordner `_wartung/`. Das Projektwissen
  hier ist per GitHub-Synchronisation eingebunden (nur lesen). Geändert wird ausschließlich
  im Repo – per Branch + Pull Request.
- `_wartung/allgemein/` – `anweisung_lernseiten.txt`, `wiederkehrende_fehler_checkliste.md`,
  `pruefe.py`, `baustein_mathjax_notfall.js`, `baustein_navigation.html`,
  `baustein_schritt_fuer_schritt.html`, `baustein_rueckblick_klassenarbeit.html`,
  `baustein_story.html` (Story/Escape Room/Adventskalender), `baustein_formeltool.html`
- `_wartung/geodreieck/` – `geodreieck_baustein.html`
- `_wartung/unterrichtsvorbereitung/` – `anweisung_C_unterrichtsvorbereitung.md`
- `_wartung/geogebra/` – Baukasten (`css.txt`, `helfer.js`, `bauer.py`, `koord.py`, `test.js`,
  `LIESMICH.md`) und `anweisung_geogebra_projekt.md`, `geogebra_befehle_geprueft.md`,
  `geogebra_roadmap.md`, `projekt_aufbau.md`
- `_wartung/exam/` – `anweisung_exam.md`, `baustein_exam.html` (EXAM-Engine), `exam_bauen.py`,
  `projektanweisung_exam.md`; dazu auf der Website `intern/EXAM/vorbereitung.html`
- `_wartung/plan/` – laufende Planung (`plan_navigation_impressum.md`) und Entwürfe
- `_wartung/PROJEKT-LANDKARTE.md` – welches Projekt welche Ordner synchronisiert
- Die Website selbst (Lernseiten, `build_hub.py`) liegt im selben Repo.
  `dino_hub.html` wird von der GitHub-Action erzeugt – nie von Hand ändern.

## Die fünf realen Projekte (GitHub-Ordner)
- **Unterrichtsvorbereitung** – `allgemein`, `geodreieck`, `unterrichtsvorbereitung`
- **HTML erzeugen** – `allgemein`, `geodreieck`
- **Debugging** – `allgemein`, `geodreieck`
- **GeoGebra** – `allgemein`, `geogebra`
- **WEB EXAM** – `allgemein`, `exam` (bewertete Tests; ein Chat je Test)

## Vorgehen, wenn ich eine Änderung nenne
1. Betroffene Dateien aus dem Repo vollständig lesen. Nichts aus dem Gedächtnis.
2. Änderung umsetzen:
   - Geodreieck-Code → `geodreieck_baustein.html` und ggf. ANHANG A der Lernseiten-Anweisung.
   - Navigationsleiste → `baustein_navigation.html`; Versionsnummer im Kopfkommentar und
     `NAV_VERSION` in `pruefe.py` gemeinsam erhöhen; die Website-Seiten danach per
     Nachrüst-Skript aktualisieren (eigener PR).
   - Allgemeine Regel → Lernseiten-Anweisung; prüfen, ob Dach-Anweisung, Checkliste und
     `pruefe.py` mitziehen müssen.
   - Story-Engine → `baustein_story.html`; Versionsnummer im Kopfkommentar und `STORY_VERSION`
     in `pruefe.py` gemeinsam erhöhen.
   - Formeltool → `baustein_formeltool.html`; Versionsnummer und `FT_VERSION` in `pruefe.py`
     gemeinsam erhöhen und den Block in `baustein_story.html` (und jedem weiteren Baustein,
     der ihn enthält) mitziehen.
   - EXAM-Engine → `baustein_exam.html`; Versionsnummer im Kopfkommentar und `EXAM_VERSION`
     in `pruefe.py` gemeinsam erhöhen; Code-Muster (`CODE_ALPHABET`, `CODE_SALT`) immer
     gleichzeitig in `intern/EXAM/vorbereitung.html` ändern.
   - **GeoGebra mitdenken:** Betrifft die Regel Farben, Schriftgrößen, CSS-Selektoren,
     Meta-Tags, MathJax, Speichern oder Koordinatensysteme, auch den Baukasten und
     „Die harten Formatregeln" in `anweisung_geogebra_projekt.md` nachziehen.
3. **Sonderpunkte nie verlieren:**
   - Lernseiten-Anweisung: `thema_rbka.html` (TEIL 2.8, Baustein) und `_kavb`, Koordinatensysteme-Abschnitt, die Warnhinweise
     „im Beispieltext nicht die Lösung vorweg nehmen" und „nicht von Anfang an die richtige
     Sortierung vorgeben".
   - Dach-Anweisung: Drei-Produkte-Struktur, Verweise auf die Lernseiten-Anweisung;
     div-basierte Brüche auf Websites (a/b nur im Docx; Ausnahme: GeoGebra-Eingabe in `<code>`).
   - GeoGebra-Anweisung: GRUNDREGEL (gearbeitet wird in GeoGebra, kein Ersatz-Widget),
     Trennung Bedienung ↔ Fachinhalt.
4. **Verifizieren vor dem PR:** JS-Syntax, keine toten Referenzen, Pflichtregeln
   (Lernseiten: Zustand im `sessionStorage` mit try/catch, kein `localStorage`;
   Geodreieck: bewusst nur JS-Speicher, Pointer-Events mit `setPointerCapture`,
   scroll-stabil, `requestAnimationFrame`). Baukasten: Testseite bauen, `pruefe.py` und
   `test.js` darüber – beides sauber.
5. **Abschluss:** Branch + Pull Request, Link nennen. Danach immer die Checkliste:
   - **A) Reale Projekte:** welche Projekte nach dem Mergen „Synchronisieren" müssen; ob ein
     Projektanweisungs-Text (Feld „Anweisungen") von Hand ersetzt werden muss – dann den
     fertigen Text mitliefern. Bei **WEB EXAM**, **GeoGebra** und diesem **Wartungs-Projekt**
     steht im Feld nur ein Verweis auf die Datei (`exam/projektanweisung_exam.md`,
     `geogebra/anweisung_geogebra_projekt.md`, `anweisung_wartung_projekt.md`) – Änderungen
     also nur dort, danach genügt „Synchronisieren". Von Hand nur, wenn sich ein
     Verweistext selbst ändert (`projektanweisungen.md`).
   - **B) Wartungs-Projekt:** ebenfalls „Synchronisieren".
   - **C) Zusammenfassung** in 1–3 Sätzen.
   Geänderte Dateien zusätzlich einzeln zum Download, wenn ich sie direkt brauche
   (z. B. Projektanweisungs-Texte).

## Grenzen
- Projektanweisungs-Texte anderer Projekte kann Claude nicht ändern – fertigen Text liefern,
  ich setze ihn ein.
- Ein neuer Chat hat kein Gedächtnis – immer aus `_wartung/` arbeiten, besonders aus
  `plan/plan_navigation_impressum.md`.
- Kein Zugriff auf mein Schul-Postfach (my-mcg.de / iserv) – dort laufen sensible Mails.

## Stil
Knapp, konkret, kein unnötiger Umbau funktionierender Teile. Bei mehreren möglichen
Auslegungen kurz nachfragen, bevor alles umgebaut wird.

---

## Text für das Feld „Anweisungen" (nur einmal einsetzen)

```
Lies zu Beginn jedes Chats vollständig die Datei `anweisung_wartung_projekt.md` aus dem
GitHub-Sync (`_wartung/`) und befolge sie. Sie ist die verbindliche Projektanweisung.
Findest du sie nicht im Projektwissen, sag das sofort und arbeite nicht aus dem Gedächtnis.
```
