# Wiederkehrende Fehler auf Lernseiten – Prüf-Ablauf & Checkliste

**Gilt für alle vier Projekte** (Unterrichtsvorbereitung, HTML erzeugen, Debugging, GeoGebra).
Ergänzt `anweisung_lernseiten.txt` – bei Widerspruch gilt die Anweisung, diese Datei
ist die Prüf-Brille davor. Das Programm `pruefe.py` prüft die maschinell prüfbaren Punkte
dieser Liste automatisch (Lernseiten-Anweisung TEIL 11); die übrigen bleiben Handarbeit.

Grundlage: Vollständigkeits-Check von 13 EF-Seiten zur Analytischen Geometrie
(`besondere_figuren_ls/_ue`, `vektoren_punkte_laenge_kollinear_ls/_ue`,
`punkt_D_eines_besonderen_Vierecks_ue`, `koordinatensystem_3d_ue`,
`parameterform_gerade_ls`, `geraden_lagebeziehung_ls/_ue`, `geraden_lage_raum_ls`,
`bewegungen_modellieren_ls/_ue`, `koordinatengeometrie_rueckblick_ls`) am 04.09.2026,
ergänzt um die Funde aus dem Aufbau der GeoGebra-Reihe (Klasse 7 bis Q1, 37 Seiten,
September 2026).
Die Punkte unter „Auf praktisch jeder Seite" waren auf mehreren Seiten gleichzeitig verletzt.

**Wann diese Datei zu lesen ist:** vor jeder Korrektur und vor jeder Abgabe einer neuen
Seite – auch dann, wenn nur ein einzelner Bug gemeldet wurde.

---

## TEIL 1 – Prüf-Ablauf (in dieser Reihenfolge durchgehen)

**Schritt 0:** `python3 pruefe.py seite.html` laufen lassen. Alles, was als FEHLER kommt,
landet direkt auf der Korrekturliste. Danach die acht Durchgänge von Hand – das Programm
ersetzt sie nicht.

Jede Seite wird in acht Durchgängen geprüft. Erst wenn ein Durchgang sauber ist, kommt
der nächste. Gefundene Fehler werden gesammelt und am Ende gemeinsam korrigiert – nicht
nach jedem Fund einzeln umgebaut.

**1. Kopf & Meta**
Alle sieben Pflicht-Meta-Tags gesetzt und gefüllt (`description`, `keywords`, `typ`,
`klasse`, `fach`, `oberthema`, `thema`)? Passt `typ` zum Dateinamen-Suffix? Passt `klasse`
zur restlichen Reihe? MathJax-Block exakt wie vorgeschrieben eingebunden? Keine weitere
externe Ressource außer MathJax – auch kein Google Fonts (Links `<a href>` zählen nicht)?

**2. Farbschema & Typografie**
Sind exakt die verbindlichen Hex-Werte verwendet (kein eigener Orange-/Blauton)? Passt das
Farbschema zum Aufgabentyp (Erarbeitung orange, Übung blau, Wissenstest grau/dunkelblauer
Rand)? Sind Tipps und Musterlösungen in Amber? Gibt es irgendwo eine `font-size` unter
`1rem` – auch in Tabs, Tipp-Boxen, MC-Buttons, Feedback-Zeilen und Badges?

**3. Kartengerüst**
Sind die Aufgabentypen auf getrennten, umschaltbaren Karten? Hat die Übung/der Wissenstest
eine Auswertungskarte **und** eine Wiederholungskarte (vorletzte Karte)? Hat jede
Oberstufen-Aufgabenkarte unter dem Titel die `.op-tags`-Zeile mit Hilfsmittel- und
Lösungsart-Kennzeichnung? Gibt es einen „Weiter"-Button – und wenn ja, mit echtem Ziel?
Beginnt jede Karte, die auf der vorigen aufbaut, mit „Wo wir gerade stehen"? Sind alle
Aufgaben ausformuliert (keine Tabellen-Stichworte)? Steht die Navigationsleiste
(`baustein_navigation.html`) unverändert vor dem T-Rex, außerhalb von `<main>`?

**4. Aufgaben- und Antwortlogik**
Hat jede Eingabe einen erreichbaren Prüfen-Button? Werden MC-Optionen beim Laden einmal
gemischt, und zwar **vor** den Klick-Bindungen? Sind `data-ok`/`data-c` wahrheitsgemäß
gesetzt (nie invertiert und im Prüf-Code kompensiert)? Hängt keine Auswertung an einem
festen Index? Bleiben Zuordnungen nach dem Prüfen sichtbar und gesperrt? Werden Dezimalzahl
und gleichwertiger Bruch akzeptiert, haben gerundete Werte eine Toleranz? Ist keine
JS-Funktion doppelt definiert?

**5. Feedback, Tipps, Musterlösung**
Sattes Grün/Rot mit weißer Schrift statt Pastell? Verrät die Rückmeldung nicht sofort die
Lösung? Ist der Tipp-/Musterlösungs-Block vor dem ersten Prüfen `display:none`? Nehmen die
gestuften Tipps die Rechnung nicht vorweg? Gibt es nach einem Fehler einen Leeren-Button –
bleibt keine Aufgabe dauerhaft gesperrt? Verrät kein Beispiel, kein Platzhalter und kein
Kontrollbild die Lösung (die vier Varianten, Teil 2 Nr. 14)?

**6. Formeln & Rendering**
Wird Feedback mit Formeln per `innerHTML` **plus** `MathJax.typesetPromise()` gesetzt (nie
`textContent`), und ist der Aufruf abgesichert (`if (window.MathJax && …)` + `try/catch`)?
Ist die Notfall-Anzeige (`MATHJAX-FALLBACK`) am Skriptende? Stehen keine literalen
LaTeX-Reste (`\;`, `\quad`, `\\`) außerhalb von `\(…\)`? Kein `\color{…}` in Formeln? Keine
globale `svg`-Regel, keine Nachfahren-Regel `.xyz svg`, keine Größenregel auf
`mjx-container`, keine `em`-Ketten? `.frac` nur mit Kind-Selektoren?

**7. Grafiken**
Ist jede Grafik ein eigenes SVG, angesprochen über den Kind-Selektor (`.kos > svg`,
`.figur > svg`)? Haben Koordinatensysteme Achsenbeschriftung, mindestens eine Einheit je
Achse und Pfeilspitzen? Werden keine externen Dateien referenziert, die neben der HTML gar
nicht existieren?

**8. Layout & Abschluss**
Bei 768px kein horizontales Scrollen, keine Überläufe? Flip-Cards mit `min-height` an der
längeren Seite? Zustand in einem Status-Objekt und per `sessionStorage` mit eigenem
Seitenschlüssel gesichert? Nach Neuladen vollständig wiederhergestellt (inkl.
MC-Reihenfolge und Timer)? Zugriffe in `try/catch`? Kein `localStorage`? T-Rex 🦖
vorhanden? Lehrplan-Check gemacht – auch für falsche Antwortoptionen? Zum Schluss die
Fehlerliste in Teil 2 einmal komplett gegenlesen.

---

## TEIL 2 – Fehlerliste

### Auf praktisch jeder Seite verletzt

**1. MC-Optionen nicht gemischt.** Die richtige Antwort stand fast immer an erster Stelle.
Lösung: Fisher-Yates einmal beim Laden – und zwar **vor** allen Klick-Bindungen –,
Reihenfolge danach stabil halten; die Auswertung nie an einem festen Index festmachen,
sondern am `data-ok`/`data-c`-Attribut bzw. am Wahrheitswert im `onclick`.

**2. Schriftgrößen unter 16px** (0.72–0.95rem in Tabs, Tipps, MC-Buttons, Feedback).
Faustregel: keine `font-size` unter `1rem`.

**3. Kennzeichnung „mit/ohne Hilfsmittel" und „rechnerisch/grafisch" fehlte** auf allen
EF-Seiten komplett. Umgesetzt als `.op-tags`-Zeile unter jedem Aufgaben-Kartentitel.

**4. Amber-Farben für Tipps und Musterlösungen** (`#b8860b` / `#fdf3d9` / `#96690a`) wurden
nirgends verwendet – stattdessen Orange, Blau oder Grau.

**5. Freie Farbwahl statt der verbindlichen Hex-Werte.** Jede Seite hatte einen eigenen
Orange- bzw. Blauton (z. B. `#e07b1a`, `#d98324`, `#e8943c`, `#1565c0`, `#1976d2`).
Verbindlich sind Erarbeitung `#c97a2e`/`#a5611e`/`#fbeee0` und Übung
`#2f5fa6`/`#1f4680`/`#e6eefb`; dazu `--ink:#22303f`, Grün `#1e7d32`, Rot `#c1272d`.

### Häufig

**6. Toter „Weiter"-Button** (`href="#"`, `location.href='#'`) – auf neun Seiten. Entweder
ganz weglassen oder auf ein echtes Ziel legen (z. B. die Auswertungskarte).

**7. Pastellfeedback** statt sattem Grün/Rot mit weißer Schrift.

**8. Rückmeldung verrät die Lösung sofort** statt gestufter Tipps. Bewährtes Muster: kurzer
Hinweis im roten Feld + aufklappbare Musterlösung mit nachvollziehbarem Lösungsweg, die
erst nach einem Fehler erscheint.

**9. Musterlösung schon vor dem ersten Versuch aufklappbar** (Tipp-Block ohne
`display:none`). Immer erst nach dem Prüfen freigeben.

**10. Kein Leeren-Button**, Aufgaben nach einer falschen Antwort dauerhaft gesperrt.

**11. Aufklappbare Tipps nehmen die Rechnung vorweg** (z. B. bereits ausgerechnete
Teilvektoren, oder das Ergebnis des vorherigen Schritts im Tipp des nächsten).

**12. Literale LaTeX-Reste** wie `\;` oder `\quad` zwischen zwei `\(…\)`-Blöcken – stehen
außerhalb des Mathe-Modus und erscheinen als Text.

**13. Feedback per `textContent`** statt `innerHTML` + `MathJax.typesetPromise` – Formeln
bleiben ungerendert.

### Aus der GeoGebra-Reihe (September 2026) – gilt für alle Projekte

**14. Lösung im Beispiel, im Platzhalter oder im Kontrollbild verraten** – die häufigste
Rückmeldung der ganzen Reihe, in vier Varianten:
- **Beispiel:** Ein Eingabebeispiel war genau das Ergebnis der danebenstehenden Aufgabe
  („Tippe dein Ergebnis ein, z. B. `h(x)=3x^2-10x+2`" – bei genau dieser Aufgabe).
- **Formathinweis/Platzhalter:** „Ein Bruch wie 5/3 wird auch akzeptiert" – und 5/3 *war*
  die Lösung. Format abstrakt angeben („in der Form a/b").
- **Rechenregel-Erklärung** am Term der aktuellen Aufgabe statt an einem neutralen Beispiel.
- **Rückverweis** („mit \(f'(x)=3x^2\) von Karte 2 …") nennt das Ergebnis einer früheren
  Karte im Klartext. Stattdessen „nimm deine Ableitung von Karte 2".
- **Kontrollbild** markiert den Punkt, nach dem auf derselben Karte gefragt wird.

Faustregel: Jedes „z. B.", jeden Beispielwert, jeden Platzhalter und jedes Kontrollbild vor
der Abgabe darauf prüfen, ob es zufällig eine Antwort auf der Seite ist.

**15. `.kontrollbild svg{…}` / `.kos svg{…}` als Nachfahren-Selektor.** Traf die
MathJax-Formel in der Bildunterschrift mit – aus `\(r\)` wurde ein bildschirmhohes „r".
Richtig: `.kontrollbild > svg{…}`. (Die alte Anweisung schrieb `.kos svg` sogar vor – seit
September 2026 korrigiert.)

**16. `.frac span{…}` als Nachfahren-Selektor.** Bei verschachtelten Brüchen bekamen auch die
inneren Spans einen Bruchstrich – mehrere Linien übereinander, unlesbar. Richtig:
`.frac > span`, `.frac > span:first-child`, `.frac > span:last-child`. Dazu: keine
gestapelten Doppelbrüche, sondern einzeilig mit Doppelpunkt.

**17. Formeln standen auf dem Gerät als Rohtext** (`\(c(3,4)\)`). Ursache war nicht die
Datei, sondern ein im Schul-WLAN blockiertes MathJax-CDN. Abhilfe: Notfall-Anzeige
(`baustein_mathjax_notfall.js`) ans Skriptende, und `typesetPromise` nur abgesichert
aufrufen – ein ungeschützter Aufruf riss das ganze Skript mit, sodass auch Karten und
Prüfen-Buttons tot waren.

**18. Lehrplan-Verstoß durch Planen aus dem Gedächtnis.** Kreisumfang/-fläche und Zylinder
auf einer Klasse-8-Seite (gehört in Klasse 9), „Wurzeln" als Nebensatz auf einer
Klasse-7-Seite. Stoffverteilungsplan aufschlagen; auch falsche Antwortoptionen prüfen; ein
kurzer Begriffs-Scan über den sichtbaren Text findet solche Reste in Sekunden.

**19. Richtige Bruch-Eingabe als falsch gewertet.** Das Ergebnis 17,25 wurde nur dezimal
akzeptiert, `69/4` galt als falsch. Dezimal und Bruch gleichwertig prüfen; bei gerundeten
Werten Toleranz; Rundung in der Aufgabe nennen.

**20. Begriffe auf derselben Seite widersprüchlich.** Eine MC-Option sprach von „allen
Extrempunkten", zwei Fragen weiter stand richtig, dass es nur Kandidaten sind. Einen Begriff
wählen und durchhalten.

**21. Aufgaben als Tabellen-Stichworte.** „Zurück auf 1200 €: nach 3 Jahren" – für die
Lehrkraft klar, für die SuS nicht. Jede Aufgabe als eigener Block mit Überschrift, Kontext,
Arbeitsanweisung und vollständig formulierter Frage.

**22. Karte setzt die vorige voraus.** Karten sind frei umschaltbar; ohne „Wo wir gerade
stehen"-Kasten wusste niemand, woher die eingesetzte Zahl kam.

**23. Paare verbinden ohne sichtbare Zugehörigkeit.** Nach der Auswahl war nur eine
Markierung zu sehen, nicht, was mit was verbunden ist. Linke Elemente nummerieren,
verbundene rechte zeigen dieselbe Nummer.

**24. JS-Funktion doppelt definiert.** Im GeoGebra-Baukasten standen `pruefeFortschritt`,
`toggleStufe` und `toggleTipp` zwei- bzw. dreimal im Skript. Die letzte, fest verdrahtete
Fassung gewann stillschweigend – Wissenstests zeigten ✅ statt ●, eine fünfte Karte bekam nie
eine Marke. `pruefe.py` meldet das seitdem als `DOPPELT`.

**25. Bedienangabe falsch** (nur Seiten, die GeoGebra-Bedienung nennen): „Schieberegler über
den Kreis links vor der Zeile" – falsch, der Kreis blendet nur ein/aus. Richtig sind die
**drei Punkte am rechten Zeilenrand**. Bedienangaben nicht raten, sondern nachschlagen.

### Einzelfälle mit Signalwirkung

- **Externe Bibliothek eingebunden** (GeoGebra `deployggb.js`) und dazu eine `.ggb`-Datei
  referenziert, die neben der HTML gar nicht existiert. Erlaubt ist nur MathJax; Grafiken als eigenes SVG bauen, angesprochen über den Kind-Selektor
  (`.kos > svg`, nie global `svg`, nie `.kos svg`).
- **Zuordnung wurde nach dem Prüfen zurückgesetzt.** Pflicht ist das Gegenteil: gesetzte
  Paare bleiben sichtbar, werden grün/rot markiert und gesperrt; nur der Leeren-Button gibt
  sie wieder frei. Beim Prüfen nur Statusklassen setzen, nie neu rendern.
- **Übung ohne Auswertungskarte** (`punkt_D`) und **Übung ohne Wiederholungskarte**
  (`bewegungen_modellieren_ue`) – beides ist bei Übung und Wissenstest Pflicht.
- **Erarbeitung im falschen Farbschema** (dunkelblauer Kopf statt Orange).
- **Koordinatensystem ohne Achsenbeschriftung, Einheiten und Pfeile**
  (`parameterform_gerade_ls`). Pflicht sind Achsennamen, mindestens eine Einheit je Achse
  und Pfeilspitzen.
- **`data-ok` invertiert gesetzt** und im Prüf-Code mit `dataset.ok==='0'` kompensiert
  (`geraden_lage_raum_ls`). Das bricht jede spätere Mischlogik – Attribute immer
  wahrheitsgemäß setzen.
- **`\color{…}` in MathJax** zieht eine zusätzliche Extension vom CDN nach. Farbe besser
  außerhalb der Formel über CSS-Klassen setzen.
- **Flip-Cards mit absolut positionierten Seiten und zu kleiner `min-height`**
  (`koordinatengeometrie_rueckblick_ls`: 120px bei zweizeiligen Rückseiten).
- **Interaktives Widget ersetzte die Arbeit in GeoGebra** (ziehbarer Scheitelpunkt und
  Regler auf einer Bedienungsseite – die SuS hätten die App nie geöffnet). Wo „mit GeoGebra"
  gearbeitet wird: Anleitung + Zielvorgabe + statisches Kontrollbild, kein Ersatz-Widget.

---

## TEIL 3 – Geklärte Grundsatzfragen

Diese Punkte standen offen und sind inzwischen als Regel in
`anweisung_lernseiten.txt` festgeschrieben:

- **Einstufige geführte Aufgabenkarten sind erlaubt.** Wenn sich Grundlagen /
  Fortgeschritten / Profi bei einer geführten Aufgabe nicht sinnvoll unterscheiden lassen,
  werden dort keine Stufen angeboten; die Niveaustufen liegen dann in der
  Wiederholungskarte bzw. den freien Übungskarten (Fall `punkt_D_eines_besonderen_Vierecks_ue`).
- **Rückblick-Seiten heißen `_rb`** und tragen `typ="Rückblick"`. Bestandsdateien mit
  falschem Suffix werden nur umbenannt, wenn gleichzeitig alle Seiten mitgezogen werden,
  die darauf verlinken (Fall `koordinatengeometrie_rueckblick_ls`).
- **`klasse` muss zur Reihe passen.** Eine EF-Reihe trägt durchgehend `klasse="EF"`; eine
  abweichende Angabe ist ein Fehler, kein Sonderfall (Fall `koordinatensystem_3d_ue` mit
  `klasse="10"`).
- **Schrägstrich in `<code>` ist kein Bruch.** Wörtlicher Eingabetext für GeoGebra
  (`20/(4+1)`) steht in `<code>` und darf den Schrägstrich enthalten; außerhalb von `<code>`
  bleibt die div-basierte Bruchdarstellung ohne Ausnahme Pflicht.
- **GeoGebra-Bedienungsseiten** sind normale Lernseiten/Übungen/Tests, liegen in einem
  eigenen Ordner und tragen `oberthema="GeoGebra Suite"`.
- **Der Stand übersteht ein Neuladen** (Oktober 2026). Der Zustand liegt in einem
  Status-Objekt und wird per `sessionStorage` unter einem eigenen Seitenschlüssel gesichert;
  nach dem Schließen des Tabs startet die Seite leer. `localStorage`, Cookies und
  serverseitige Speicherung bleiben verboten. Ein Zurücksetzen-Knopf ist nicht nötig, weil
  jeder Schüler an einem eigenen iPad arbeitet.
- **Navigationsleiste auf jeder Seite** (Oktober 2026). `baustein_navigation.html` wird
  unverändert vor dem T-Rex eingefügt: 🏠 Startseite, 📚 Alles für Klasse X (aus dem
  Meta-Tag `klasse`), ✉️ Feedback, schwebender 🏠-Knopf unten links. `pruefe.py` meldet eine
  fehlende oder veränderte Leiste als `NAV`.
- **Keine Google Fonts mehr** (Oktober 2026, Datenschutz). Einzige erlaubte externe Quelle
  ist MathJax; Schrift kommt aus dem System.

---

*Stand: 16.10.2026 (Navigationsleiste, keine Google Fonts) – gepflegt im Wartungs-Projekt „Wartung Unterrichtsprojekte".*
