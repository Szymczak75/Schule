# Bauanleitung: SchILD-3-Hilfe-Website

> Diese Datei gehört zusammen mit den Wissensdateien (z. B. `schild3_stufenleitung.md`) ins Claude-Projekt. Sie beschreibt, **wie** die Hilfe-Websites gebaut werden sollen. Die Inhalte kommen **ausschließlich** aus den Wissensdateien.

## Ziel

Eine eigenständige, gut bedienbare Hilfe-Website („SchILD-User-Hilfe“) für Lehrkräfte einer NRW-Schule, die auf SVWS-Server / SchILD-NRW 3 umstellt. Jede Rolle bekommt einen eigenen Teil. Es wird **eine einzige HTML-Datei** gebaut (HTML, CSS und JavaScript in einer Datei, ohne externe Abhängigkeiten), die offline und im Schulnetz funktioniert.

## Rollen (Reiter)

1. **Stufenleitung / Koordination** – Datei `schild3_stufenleitung.md` (vorhanden)
2. **Klassenlehrkräfte** – folgt
3. **Fachlehrkräfte** – folgt
4. **Admin** – folgt

Fehlt die Wissensdatei einer Rolle, wird der Reiter mit dem Hinweis „in Vorbereitung“ angezeigt, ohne erfundene Inhalte.

## Pflichtfunktionen

### 1. Suche
- Suchfeld oben, immer sichtbar.
- Durchsucht Titel, Schritte, Beispiele, Fallstricke **und die Suchbegriffe** jedes Eintrags.
- Tolerant gegenüber Umlauten (ue/ü), Groß-/Kleinschreibung und Teilwörtern.
- Treffer sofort beim Tippen, mit hervorgehobenen Suchwörtern.
- Optional eingrenzen nach Rolle, Bereich (Grundlagen / Sek I / Oberstufe) und Programm (SVWS-Webclient / SchILD-NRW 3).

### 2. Einträge als Karten
Jeder Eintrag (z. B. `SL-O-10`) wird als aufklappbare Karte dargestellt:
- Kopf: ID, Titel, Programm-Badge (zwei Farben: Webclient / SchILD 3), Bereich
- Inhalt: „Wann brauche ich das?“, Voraussetzungen, **nummerierte Schritte**, **Beispiel** (optisch hervorgehoben, z. B. Kasten „Beispiel aus dem Alltag“), **Fallstricke** (Warn-Kasten), Quelle als Link
- Menüpfade wie **Oberstufe → Kursplanung** als „Klickpfad“-Chips darstellen

### 3. „Frage an den Admin“
- Auf **jeder** Karte ein Button **„Frage an den Admin“**.
- Er öffnet ein kleines Formular, vorausgefüllt mit der Admin-Vorlage des Eintrags (Feld „Frage an den Admin“) und der allgemeinen Vorlage aus Teil C (Betreff mit ID und Titel, Programm, Stufe/Lernabschnitt, Was wollte ich, Was ist passiert, Was habe ich versucht).
- Die Lehrkraft ergänzt die Platzhalter in eckigen Klammern.
- Zwei Wege zum Absenden:
  - **„Per E-Mail senden“**: `mailto:` mit Betreff und Text
  - **„Text kopieren“**: in die Zwischenablage, z. B. für Messenger oder Ticketsystem
- Die Admin-Adresse steht **an einer einzigen Stelle** oben im Skript als Konstante (`ADMIN_EMAIL = "admin@schule.example"`), damit jede Schule sie leicht anpassen kann.
- Hinweis unter dem Formular: **keine Schülerdaten (Namen, Noten) per E-Mail senden**, stattdessen ID oder Kürzel verwenden.

### 4. Weitere Funktionen
- Seite **„Ablauf auf einen Blick“** pro Rolle (z. B. SL-O-00) als klickbare Schrittfolge, die zu den Karten springt.
- **Glossar** (SL-G-03) mit Tooltips: Fachbegriffe in den Karten erklären sich beim Überfahren.
- Abschnitt **„Wann frage ich den Admin?“** (Teil C) und Links zu Fachberatung und Forum.
- Druckansicht: einzelne Karte oder ganzen Bereich drucken (z. B. als Handzettel für die Stufenkonferenz).
- Hinweisleiste oben: „Stand: [Datum]. Menünamen können sich nach Updates ändern.“

## Gestaltung
- Ruhig, gut lesbar, schulgeeignet. Große Schrift für Schritte, ausreichende Kontraste, auch am Beamer lesbar.
- Funktioniert auf Desktop, Tablet und Handy.
- Barrierearm: Tastaturbedienung, sinnvolle Überschriftenstruktur, Alt-Texte.

## Regeln für Inhalte
- Nur Inhalte aus den Wissensdateien verwenden. **Keine Menüpfade erfinden.** Wo die Datei „an eurer Version prüfen“ sagt, diesen Hinweis sichtbar übernehmen.
- Beispiele dürfen ergänzt werden, müssen aber erkennbar fiktiv sein (keine echten Schülernamen).
- Neue Rollen-Dateien folgen demselben Eintragsschema (ID, Titel, Bereich, Programm, Wann, Voraussetzungen, Schritte, Beispiel, Fallstricke, Frage an den Admin, Suchbegriffe, Quelle). ID-Präfixe: `SL` Stufenleitung, `KL` Klassenlehrkraft, `FL` Fachlehrkraft, `AD` Admin.
