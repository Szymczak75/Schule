# Plan: Navigation, Startseite, Impressum & Datenschutz

*Stand: 16.10.2026 (aktualisiert nach Chat „Navigation Schritt 2“) – Abschnitt 7
zeigt den aktuellen Fortschritt. In einem neuen Chat dieses Wartungs-Projekts hier weitermachen.*

---

## 1. Ausgangslage

- Die Lernseiten liegen auf **GitHub Pages** (Repo `Szymczak75/Schule`, öffentlich,
  https://szymczak75.github.io/Schule/), in mehreren Ordnern (je Klasse, dazu ein eigener
  Ordner für die GeoGebra-Bedienungsseiten).
- Die Startseite (`dino_hub.html`) kennen bisher nur Kollegen.
- Die Seite ist **privat betrieben**, wird aber **dienstlich im eigenen Unterricht** genutzt.
  Zielgruppe: eigene Schüler und Schüler der Schule. Sie wird nirgends beworben, es ist aber
  wahrscheinlich, dass Kollegen sie nutzen und die Links sich verbreiten.
- Ziel des Nutzers: gute Inhalte machen, die für SuS und Kollegen **zugänglich** sind – ohne
  dass der Rahmen drumherum ständig Arbeit macht.

---

## 2. Was gebaut werden soll

### 2.1 Navigationsleiste auf jeder Seite (neuer Baustein)
- Schlichte Leiste (unten) mit:
  🏠 **Startseite** · 📚 **Alles für Klasse X** · ✉️ **Feedback zu dieser Seite** ·
  **Impressum & Datenschutz**
- Dazu ein schwebender 🏠-Knopf **unten links** (T-Rex bleibt rechts).
- „Alles für Klasse X" wird **nicht von Hand** gepflegt: Die Leiste liest das vorhandene
  Meta-Tag `klasse` und verlinkt auf `dino_hub.html?klasse=X`.
- Die Startseite wird über eine **feste (absolute) Adresse** angesprochen – dann funktioniert
  der Link aus jedem Unterordner (auch aus dem GeoGebra-Ordner).
- Kein Widerspruch zur Regel „GeoGebra-Seiten verlinken sich nicht untereinander" und kein
  „Weiter"-Button: Die Verbindung läuft weiterhin über die Startseite.
- Muss alle Pflichtregeln einhalten: Farben aus dem Schema, `font-size` ≥ 1rem, Tap-Ziele
  ≥ 44×44 px, kein `localStorage`, kein toter Link (`href="#"`), T-Rex 🦖 bleibt.
- Der Link „Impressum & Datenschutz" wird **erst freigeschaltet, wenn die Seite existiert**
  (sonst wäre er ein toter Link).

### 2.2 Startseite mit Filter
- `dino_hub.html` versteht den Parameter `?klasse=…` und zeigt dann nur die Seiten dieser
  Jahrgangsstufe (ggf. später auch `?oberthema=…`, z. B. „GeoGebra Suite").
- Kleiner Umbau, kein Neubau. Grundlage sind die Meta-Tags, die jede Seite schon trägt.

### 2.3 Nachrüsten der bestehenden Seiten
- Die Leiste wird **per Skript einmal in alle vorhandenen Seiten eingesetzt** – nicht Seite
  für Seite von Hand.
- Danach `pruefe.py` über alle Seiten laufen lassen.
- Bei der Gelegenheit mit erledigen (aus dem GeoGebra-Projekt offen):
  - 37 GeoGebra-Seiten: `oberthema="GeoGebra Grafikrechner"` → `"GeoGebra Suite"`
  - `geogebra_start_ef_rb.html`: `typ="Übung"` → `typ="Rückblick"`
  - Seiten, die mit dem alten `helfer.js` gebaut wurden, enthalten doppelt definierte
    Funktionen (`pruefe.py` meldet `DOPPELT`) → bereinigen

### 2.4 Regeln & Bausteine nachziehen (Wartungs-Standard)
- Neuer Baustein `baustein_navigation.html` (v3, liegt in `_wartung/allgemein/`).
- `anweisung_lernseiten.txt`: neue Pflichtregel „Navigationsleiste auf jeder Seite".
- `pruefe.py`: Prüfung, ob die Leiste vorhanden ist.
- GeoGebra-Baukasten (`bauer.py`) setzt die Leiste automatisch.
- `PROJEKT-LANDKARTE.md`: neuen Baustein eintragen.
- **Google Fonts aus der Liste erlaubter externer Quellen streichen** (der Baukasten nutzt
  ohnehin Systemschriften; dynamisch geladene Google Fonts wurden vom LG München 2022 als
  Datenschutzverstoß gewertet). Betrifft Lernseiten-Anweisung, Dach-Anweisung (.md),
  `geogebra_befehle_geprueft.md`.

### 2.5 Seite „Impressum & Datenschutz" (eine gemeinsame Seite neben der Startseite)
- **Impressum (einfach, § 18 Abs. 1 MStV):** Vor- und Nachname + ladungsfähige Anschrift.
  E-Mail ist hier nicht Pflicht.
- **Datenschutzhinweis:** Die Seiten speichern nichts auf einem Server (kein Login, kein
  `localStorage`; der Bearbeitungsstand liegt nur im `sessionStorage` des eigenen Tabs);
  GitHub Pages protokolliert IP-Adressen; MathJax wird vom CDN (jsDelivr) geladen;
  Feedback geht nur per E-Mail aus dem eigenen Mailprogramm.
- **Kontakt für Feedback/Anregungen:** nicht als klickbarer `mailto:`-Link ausgeschrieben
  (Spam).
- **Lizenzhinweis (optional, empfohlen wegen Weitergabe an Kollegen):** z. B. „CC BY-SA 4.0"
  – erlaubt Weitergeben und Anpassen mit Namensnennung.
- Kein Disclaimer/Haftungsausschluss nötig (rechtlich nahezu wirkungslos); stattdessen ein
  Satz „Fehler gefunden? Schreib mir."

---

## 3. Rechtliche Einordnung (Stand der Überlegungen, keine Rechtsberatung)

- **§ 5 DDG** (großes Impressum) gilt nur für geschäftsmäßige, in der Regel entgeltliche
  Angebote → bei kostenlosem Material ohne Werbung eher **nicht**.
- **§ 18 Abs. 1 MStV** (einfaches Impressum) gilt für jedes Angebot, das **nicht
  ausschließlich persönlichen oder familiären Zwecken** dient → bei SuS und Kollegen als
  Zielgruppe **wahrscheinlich ja**. Die Landesmedienanstalt empfiehlt im Zweifel ein
  einfaches Impressum.
- **Postfach oder Drittanschrift reicht nicht.**
- **Datenschutz (DSGVO)** greift, sobald die Seite öffentlich ist – unabhängig vom Impressum.
- Weil die Seiten mit Minderjährigen im Unterricht eingesetzt werden: **Schulleitung
  informieren**, auch wenn die Seite privat bleibt.

---

## 4. Offene Entscheidungen (vom Nutzer zu treffen)

1. ~~Adresse ins Impressum~~ → entschieden: Privatadresse (siehe 7).
2. **Lizenz** ja/nein, und welche (Vorschlag: CC BY-SA 4.0).
3. ~~Feedback-Adresse~~ → entschieden: vorerst Schuladresse, Betreff `[Dino-Feedback]`.
   Kein Zugriff von Claude auf das Schulpostfach (dort laufen sensible Mails).
4. ~~Leiste nur unten oder oben und unten~~ → entschieden: nur unten.

---

## 5. Vorgeschlagene Reihenfolge

1. Startseiten-Filter + Navigationsleiste bauen und testen (Impressum-Link noch aus)
2. Regeln, `pruefe.py`, `bauer.py`, Landkarte nachziehen
3. Nachrüst-Skript für alle bestehenden Seiten (inkl. der offenen GeoGebra-Korrekturen)
4. Seite „Impressum & Datenschutz" + Link freischalten

---

## 6. Startsatz für den neuen Chat

> Lies `_wartung/plan/plan_navigation_impressum.md` (besonders Abschnitt 7) und die
> Referenzdateien. Das Repo `Szymczak75/Schule` ist über GitHub verbunden. Wir machen beim
> nächsten offenen Punkt aus Abschnitt 7 weiter.

---

## 7. Fortschritt & Entscheidungen (16.10.2026)

**Arbeitsweise:** Claude arbeitet direkt im GitHub-Repo `Szymczak75/Schule`
(Claude GitHub App installiert). Jeder Schritt = eigener Branch + Pull Request; der Nutzer
merged in der GitHub-App/im Browser. Große Dateien gehen nicht mehr durch den Chat.

**Master-Kopien im Repo (neu):** Alle Referenzdateien liegen in `_wartung/` (Aufbau siehe
`_wartung/LIESMICH.md`). Die claude.ai-Projekte holen sie über die GitHub-Synchronisation
(Projektwissen → „+" → GitHub → Ordner wählen → bei Änderungen „Synchronisieren").
Änderungen an Regeln = Änderungen an `_wartung/` per PR.

**Wichtig:** `dino_hub.html` wird **nicht von Hand** gepflegt. Die GitHub-Action
`.github/workflows/hub.yml` erzeugt sie bei jedem Push aus `build_hub.py` neu (dito die
Ordner-Übersichten `_*.html` über `linking.txt`). Änderungen an der Startseite also immer in
`build_hub.py`. Ordner-Übersichten tragen `<meta name="hubignore">`.

**Entscheidungen:**
- Leiste: nur **unten**, Systemschrift, Startseite absolut:
  `https://szymczak75.github.io/Schule/dino_hub.html`. Zusätzlich schwebender
  **🏠-Knopf unten links**.
- Impressum: **Andreas Szymczak, Frankenweg 249, 45665 Recklinghausen**,
  Kontakt aszymczak@my-mcg.de (als Text, kein `mailto:`-Link). Lizenz: noch offen.
- **Feedback-Knopf „✉️ Feedback zu dieser Seite"** (Variante 1): Popup mit Fehler/Idee/Lob
  und Textfeld → öffnet Mailprogramm. Seitentitel und Seitenadresse automatisch in
  Betreff/Text, Betreff beginnt mit `[Dino-Feedback]`. Adresse per JS zusammengesetzt,
  Fallback „Text kopieren". Kein fremder Dienst.
- **Sichtbarkeit:** `intern/` = erreichbar, aber nicht auf der Startseite und `noindex`
  (Tests, Kollegen-Formulare, Generatoren); `_privat/` = gar nicht hochgeladen
  (`.gitignore`). Alle 11 bisherigen Test-/Kollegen-Dateien liegen in `intern/`, an den
  alten Pfaden stehen Weiterleitungen (`hubignore`).
- **Neues optionales Meta-Tag `anzeigename`:** ersetzt auf der Startseite den Titel/Dateinamen.
- **Neue Zustandsregel sessionStorage** (Stand übersteht Neuladen, Schlüssel
  `aszym:<datei>:v1`, nur Daten, try/catch, Leeren-Button löscht mit). In Anweisung,
  Checkliste und `pruefe.py` eingearbeitet. Gilt für neue und überarbeitete Seiten.
- Geodreieck bleibt beim JS-Speicher (bewusst, „passt so").

**Erledigt:**
- Schritt 1a: Filter `?klasse=…` in `build_hub.py`, `intern/`/`_privat/`, `anzeigename`
  → **PR #1** (Branch `navigation-filter`).
- Schritt 1b: `baustein_navigation.html` v2 (mit Feedback und 🏠-Knopf) als Entwurf.
- **Schritt 2** → **PR #__PR__** (Branch `navigation-regeln`):
  - Baustein als **v3** nach `_wartung/allgemein/baustein_navigation.html` (Farbe
    `#f2f3f5` → `#eef0f3` aus dem Schema, `width:auto` gegen fremde Button-Regeln).
  - Lernseiten-Anweisung: TEIL 0 Nr. 23 + neuer **TEIL 3.6 Navigationsleiste**, Hinweise in
    3.3, 3.4, 7.6 (Systemschrift), 8.1 (nur MathJax; `<a href>` ist keine Ressource),
    8.3, TEIL 10, ANHANG B. Checkliste und Dach-Anweisung nachgezogen.
  - `pruefe.py`: Regel `NAV` (fehlt / verändert / mehrfach / in `<main>`), Hinweis `NAVALT`
    (alte Fassung, `NAV_VERSION`); Google Fonts → `EXTERN`; `<a href>`-Links (Videos,
    Quellen) kein Fehlalarm mehr; Leisten-Block zählt nicht für `DOPPELT`/`NEULADEN`.
  - `bauer.py` setzt die Leiste vor den T-Rex (bricht ab, wenn der Baustein fehlt);
    Baukasten-Doku (sieben Dateien), „Die harten Formatregeln", `projekt_aufbau.md`,
    Landkarte, `_wartung/LIESMICH.md`, Wartungs-Projektanweisung.
  - Getestet: Testseite mit `bauer.py` gebaut, `pruefe.py` 0 Befunde, `test.js` sauber;
    Leiste im Browser: Klassen-Link `?klasse=8`, Feedback-Fenster, Mail-Betreff
    `[Dino-Feedback] Idee: …`, keine Überlappung mit dem T-Rex, nichts im Speicher.
- sessionStorage-Regel in `anweisung_lernseiten.txt`, Checkliste, `pruefe.py`.
- Master-Kopien in `_wartung/` → **PR #2** (Branch `wartung-sync`).
- GeoGebra-Baukasten auf sessionStorage umgestellt (`helfer.js`, `bauer.py` setzt
  `SPEICHER`, `mische(liste, schlüssel)`, `LIESMICH.md`, „Die harten Formatregeln" in
  `anweisung_geogebra_projekt.md`; `test.js` startet Chromium im neuen Headless-Modus)
  → ebenfalls PR #2. Im echten Browser mit Neuladen getestet.

**Als Nächstes:**
1. Schritt 3 (Nachrüst-Skript, PR mit Prüfbericht). **Befund aus Schritt 2 (Lauf über
   442 Seiten):** 421 ohne Leiste (`NAV`); **183 Seiten binden Google Fonts ein** → das
   Skript entfernt den `<link>` (und `preconnect`/`@import`) – die `font-family`-Angaben
   fallen dann auf ihre Ersatzschrift zurück, Stichprobe im Browser ansehen. **Auch die
   Startseite** lädt Google Fonts (`build_hub.py`, Playfair Display/Source Sans 3) → dort
   von Hand auf Systemschriften umstellen. **6 Seiten sind nicht UTF-8** (`blutzucker_kl9_
   erarbeitung`, fünf Winkel-Seiten Klasse 7) → Skript muss die Kodierung erkennen und
   als UTF-8 zurückschreiben, sonst überspringen und melden. Leiste immer vor dem T-Rex
   einsetzen, nie in `<main>`. **Neu (Entscheidung 16.10.2026):** Das
   Skript setzt zusätzlich einen einheitlichen **Neulade-Schutz Stufe 1** in alle bestehenden
   Seiten (ca. 344 interaktive von 430): Feldwerte, Auswahllisten, Häkchen und die offene Karte
   im `sessionStorage`, Schlüssel `aszym:<datei>:v1`, try/catch. Prüfergebnisse,
   MC-Markierungen und Zuordnungen kommen damit nicht zurück (dann erneut „Prüfen"). Seiten,
   die schon `sessionStorage` nutzen (2), werden übersprungen. Leeren-Knöpfe der Seiten
   müssen das Feld auch im Speicher leeren (Baustein hört auf Eingabe-Ereignisse; Leeren per
   Skript setzt nur `value` → Baustein speichert zusätzlich bei jedem Klick).
   **Stufe 2** (voller Schutz wie im Baukasten) nach und nach für die Seiten, die gerade im
   Unterricht laufen, bzw. beim nächsten Überarbeiten (Debugging-Regel).
2. Schritt 4 (Impressum-Seite, Lizenz klären).

---

## Quellen
- NLM – Leitfaden zur Impressumspflicht: https://www.nlm.de/fileadmin/dateien/infothek/pdf/leitfaden_impressumspflicht_NLM.pdf
- § 18 MStV: https://lxgesetze.de/mstv/18
- IT-Recht Kanzlei – Impressumspflicht nach DDG: https://www.it-recht-kanzlei.de/website-impressumspflicht-digitale-dienste-gesetz.html
- Kanzlei Plutte – LG München zu Google Fonts: https://www.ra-plutte.de/lg-muenchen-dynamische-einbindung-google-web-fonts-ist-dsgvo/
- adsimple – GitHub Pages Datenschutzerklärung: https://www.adsimple.de/datenschutzerklaerung/github-pages-datenschutzerklaerung/
- claude.ai – GitHub-Integration verwenden: https://support.claude.com/de/articles/10167454-github-integration-verwenden
