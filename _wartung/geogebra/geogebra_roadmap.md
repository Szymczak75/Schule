# GeoGebra-Suite-Grafikrechner – Kompetenz-Roadmap Kl. 7–13

**Fach:** Mathematik (NRW, G9, Lambacher Schweizer / GOSt-Kernlehrplan)
**Scope:** Nur die **Grafikrechner-App** der GeoGebra Suite (Funktionen, Graphen, Analysis-Befehle, Schieberegler). Analytische Geometrie/Vektoren (3D-Rechner) und Stochastik-Rechner sind **bewusst ausgeklammert** – werden bei Bedarf später als eigener Strang geplant.
**Format:** Viele kleine Lernhappen, möglichst **unter 25 Minuten**, je **eine eigene HTML-Seite**. Aufgabentyp durchgängig **Erarbeitung mit Selbstkontroll-Abschlusskarte** ("Überprüfe dich" statt strenger Auswertung). Die Seiten verlinken sich **nicht untereinander** – Verbindung ausschließlich über eine gemeinsame Übersichtsseite (Hub). So können die Happen über die Jahrgangsstufen hinweg immer wieder eingestreut werden.

## ⚠️ GRUNDREGEL (gilt für ALLE Projekte, nicht nur diese Reihe)

**Die Arbeit findet in GeoGebra statt, nicht auf der Lernseite.**

Ziel dieser Reihe ist es, **die Bedienung von GeoGebra zu lernen** – nicht den mathematischen Inhalt (der gehört in den inhaltlichen Teil des Unterrichts). Daraus folgt:

- **Keine interaktiven Widgets, die die Aufgabe ersetzen.** Ein Schieberegler oder ziehbarer Punkt *auf der HTML-Seite* verführt dazu, alles dort zu erledigen und GeoGebra nie zu öffnen. Genau das ist zu vermeiden.
- **Stattdessen: Bauanleitung + Zielvorgabe.** Die Seite sagt konkret, was in GeoGebra einzugeben/einzustellen ist („Lege `a=1`, `c=0`, `d=0` als Regler an, Schrittweite 0.5, gib `f(x)=a*(x-c)^2+d` ein"). Danach werden **Ziele** vorgegeben, die durch Einstellen in GeoGebra erreicht werden müssen: „Stelle c = 3 und verändere d so, dass die Nullstellen bei x = 1 und x = 5 liegen. Welchen Wert hat d?" – abgefragt wird dann der eingestellte Wert.
- **Erlaubt und sinnvoll: statische Kontrollbilder.** Ein unbewegliches Vergleichsbild („So muss es bei dir aussehen, wenn a = 1, c = 0, d = 0") hilft beim Selbstlernen, ohne die Arbeit abzunehmen.
- **Kontrolle über GeoGebra-Befehle einfordern:** „Prüfe mit `Nullstelle(f)`" bzw. „Tippe `f(0)` ein" – so wird nebenbei der Befehlsumgang geübt.
- Gute Zielvorgaben sind z. B.: bestimmte Nullstellen treffen, einen vorgegebenen Punkt treffen, einen bestimmten y-Achsenabschnitt erzeugen, genau eine/keine Nullstelle erzeugen.

*(Seite 4 wurde nach dieser Regel umgebaut: ursprünglich enthielt sie einen ziehbaren Scheitelpunkt und einen Regler auf der HTML-Seite – beides entfernt, weil die SuS damit GeoGebra gar nicht gebraucht hätten.)*

---

**Wichtiges Design-Prinzip (gilt für alle Seiten der Reihe, Rückmeldung nach Seite 1):**
- **Erst erklären, dann üben.** Jede Themenkarte zeigt zuerst ein oder mehrere **vorgerechnete Beispiele** ("Du tippst … → das erscheint …"), bevor die Lernenden selbst etwas eingeben müssen. Keine kalte Abfrage ohne vorherige Erklärung – das ist eine **Lernoberfläche**, kein Test.
- **Physische Tastatur maximal nutzen.** Zeigen, wie möglichst viel über die normale (Bluetooth-)Tastatur eingegeben wird (Tricks: `^` für Exponenten, `sqrt(...)` für Wurzeln, `/` für Brüche, `*` für Malnehmen). Die Mathe-Bildschirmtastatur nur als Fallback für echte Sonderfälle erwähnen, nicht als Standardweg.
- **Gemischte Zahlen/Brüche:** Werden im Grafikrechner als Rechnung eingegeben, z. B. \(4\tfrac34\) → `4+3/4` (ergibt 4.75). Ausführlich Thema von Seite 2 ("Klammern, Brüche & Exponenten"); auf Seite 1 nur als kurzer Ausblick.
- **Testkarte nur am Schluss.** Die eigentliche Selbstkontrolle/Testkarte kommt erst als letzte Karte der Seite; die Themenkarten davor sind zum Lernen da, nicht zum Prüfen.
- **Numerische Antworten: Dezimalzahl UND Bruch akzeptieren.** Bei „Jetzt rechnen"-Aufgaben mit freiem Zahlenergebnis (z. B. 17.25) muss die Prüf-Logik auch eine gleichwertige Bruch-Eingabe (z. B. 69/4) als richtig werten, nicht nur die Dezimalform.
- **Hochzahl-Ausstieg thematisieren.** Beim Trick mit `^` immer mit erklären, dass man nach der Hochzahl mit der Pfeiltaste → wieder auf die normale Zeile zurückspringen muss (sonst wird `x^23` zu \(x^{23}\) statt \(x^2+3\)).
- **⚠️ Nie die Lösung vorwegnehmen – auch nicht im Beispiel (wiederholte Rückmeldung).**
  Typische Fallen, die alle schon einmal passiert sind:
  - Ein **Eingabe-Beispiel**, das zufällig das Ergebnis der danebenstehenden Aufgabe ist
    („Tippe dein Ergebnis ein, z. B. `h(x)=3x^2-10x+2`" bei genau dieser Aufgabe) →
    stattdessen `h(x)=` … „dein eigener Term".
  - Ein **Formathinweis** mit der Lösung als Beispielwert („Ein Bruch wie `5/3` wird auch
    akzeptiert", und 5/3 *ist* die Lösung) → Format abstrakt angeben: „auch als Bruch in der
    Form `a/b`".
  - Eine **Rechenregel-Erklärung** am Term der aktuellen Aufgabe → neutrales Beispiel wählen
    (\(x^5 \to 5x^4\) statt des Terms, der gerade abgeleitet werden soll).
  - Ein **Rückverweis**, der das Ergebnis einer früheren Karte im Klartext nennt → auf die
    eigene Notiz verweisen („nimm deine erste Ableitung von Karte 2").

  Faustregel vor Abgabe: Jedes „z. B." und jeden Beispielwert daraufhin prüfen, ob er zufällig
  eine Antwort auf der Seite ist. Nur die **gestuften Tipps** dürfen Lösungen enthalten – und
  erst in der letzten Stufe.
- **Karten müssen den roten Faden mittragen (Rückmeldung Extrempunkte-Seite).** Karten sind
  frei umschaltbar, also darf keine Karte voraussetzen, dass man die vorige noch im Kopf hat.
  Baut eine Karte auf Zwischenergebnissen der vorigen auf, beginnt sie mit einem kurzen Kasten
  **„Wo wir gerade stehen"**: Funktion, Zwischenschritt, Ergebnis – als knappe Liste, plus einem
  Satz dazu, was jetzt noch offen ist. Ebenso nennt jede Bauanleitung die **Ausgangsfunktion**
  ausdrücklich, statt nur mit der Ableitung zu starten. Eingesetzte Zahlen werden benannt
  („setze die *erste Kandidatenstelle* ein: `f''(-1)`"), nie kommentarlos hingeschrieben.
- **Begriffe konsistent halten – besonders bei notwendig/hinreichend.** Was aus \(f'(x)=0\)
  kommt, heißt durchgängig **Kandidatenstelle**, nie „Extremstelle". Sonst widersprechen sich
  Antwortoptionen und Warnbox auf derselben Seite (passiert auf der Extrempunkte-Seite: eine
  MC-Option sprach von „allen Extrempunkten", während zwei Fragen weiter richtig stand, dass es
  nur Kandidaten sind). Gilt analog für Wendepunkte.
- **Brüche: keine Doppelbrüche stapeln, und `.frac` muss Kind-Selektoren nutzen.** Zwei Dinge,
  die zusammen einen unlesbaren Kasten erzeugt hatten:
  - **CSS-Bug (in allen Dateien behoben):** Die Regeln lauteten `.frac span{…}` und
    `.frac span:first-child{border-bottom:…}` – als **Nachfahren**-Selektoren. Steckt ein Bruch
    in einem Bruch, bekommen dadurch auch die inneren Spans `display:block` und einen
    Bruchstrich → mehrere übereinanderliegende Linien, nichts mehr zu entziffern. Richtig sind
    **Kind-Selektoren**: `.frac > span`, `.frac > span:first-child`, `.frac > span:last-child`.
    Diese Form ist ab jetzt verbindlich, damit Verschachtelung nie wieder das Layout zerlegt.
  - **Didaktisch:** Auch korrekt gerendert ist ein gestapelter Doppelbruch (gemischte Zahl über
    gemischter Zahl) auf dem iPad zu gedrängt. Division zweier gemischter Zahlen deshalb
    **einzeilig mit Doppelpunkt** schreiben: \(7\tfrac12 : 1\tfrac14\). Die Lernwirkung bleibt
    identisch – beide Operanden brauchen in GeoGebra ihre eigene Klammer: `(7+1/2)/(1+1/4)`.
- **Aufgabenstellungen ausformulieren – keine Tabellen-Stichworte.** Eine Tabellenzeile wie
  „Zurück auf 1200 €: nach 3 Jahren" ist für die Lehrkraft verständlich, für die SuS nicht:
  Sie enthält Arbeitsanweisung, Kontext und Frage in vier Wörtern. Regel: Jede Aufgabe bekommt
  einen **eigenen `.aufgabe`-Block** mit Überschrift („Aufgabe 3: Drei Jahre liegen lassen"),
  einem oder zwei Sätzen Kontext, der nötigen Arbeitsanweisung als eigener Satz – und erst dann
  das Eingabefeld mit einer **vollständig formulierten Frage** („Wie viel Geld hat Lena nach
  drei Jahren?"). In der Tabelle steht nur noch die Frage, nie die Vorbereitung dazu.
- **⚠️ Lehrplan-Check vor Abgabe – nicht aus dem Gedächtnis planen.** Auf der Klasse-8-Seite 6
  standen zunächst **Kreisumfang, Kreisfläche und Zylindervolumen** – die gehören laut NRW-G9-Plan
  aber erst in **Klasse 9** (UV III „Kreise, Prismen und Zylinder"). Der Fehler entstand, weil
  „Formeln eingeben" naheliegend mit dem Kreis besetzt wurde, statt nachzusehen. Merkposten:

  | Inhalt | frühestens |
  |---|---|
  | Umfang/Flächeninhalt **Rechteck, rechtwinkliges Dreieck**, Volumen Quader | Kl. 5/6 |
  | Umfang/Flächeninhalt **Dreieck, Viereck, zusammengesetzte Figuren** (UV IV) | **Kl. 8** |
  | **Terme mit mehreren Variablen**, binomische Formeln (UV III) | **Kl. 8** |
  | Kreise und Dreiecke = Thaleskreis, In-/Umkreis – **keine** Berechnungen (UV VI) | Kl. 8 |
  | **Kreis**umfang/-fläche, Zylinder, Prisma (UV III) | Kl. 9 |
  | Wurzeln, Potenzgesetze, Pythagoras, quadratische Funktionen | Kl. 9 |
  | Sinus/Kosinus/Tangens, Exponentialfunktionen | Kl. 10 |

  Ein automatischer Scan über alle Seiten (Regex auf die verbotenen Begriffe je Jahrgangsstufe,
  CSS und Skript ausgeblendet) läuft in Sekunden und sollte vor jeder Abgabe einmal drüber.
  Er hat zusätzlich einen Restsatz auf Klasse-7-Seite 1 gefunden („…Sonderzeichen wie Brüche
  oder **Wurzeln** schreibst") – Wurzeln sind Klasse 9, und die Seite behandelt sie gar nicht.
- **Formeln mit mehreren Variablen sind der ideale Klasse-8-Formelinhalt (Idee der Lehrkraft).**
  `A(g,h)=g*h/2` und `T(a,c,h)=(a+c)/2*h` treffen gleich zwei Unterrichtsvorhaben: UV III
  („Terme mit mehreren Variablen") und UV IV („Flächen: Dreieck, Viereck, Höhe und Grundseite").
  Drei didaktische Gewinne, die sonst nirgends so klar herauskommen:
  - **Die Reihenfolge in der Klammer zählt.** Kontrastaufgabe auf der Seite: `T(10,6,3)` gegen
    `T(3,6,10)` – dieselben drei Zahlen, völlig verschiedene Ergebnisse.
  - **Kein Graph bei mehreren Variablen.** Der Grafikrechner zeichnet nur Funktionen *einer*
    Variablen; bei zwei müsste eine Fläche im Raum entstehen. Das ist kein Fehler, sondern eine
    Bedieninformation – und hält man eine Größe fest, ist der Graph wieder da.
  - **Große Buchstaben als Funktionsnamen** sind erlaubt, sobald eine Klammer mit Platzhaltern
    folgt (sonst sind sie Punktnamen). So darf \(A\) im Programm heißen wie im Heft.
- **⚠️ Schieberegler: über die DREI PUNKTE am rechten Rand der Zeile einschalten** (von der
  Lehrkraft am Gerät geprüft). In vier Dateien stand fälschlich „den kleinen **Kreis links** vor
  der Zeile antippen" – das ist falsch und hätte die SuS beim ersten Schritt hängen lassen.
  Sauber getrennt gehören zwei verschiedene Bedienelemente:

  | Element | Wo | Wofür |
  |---|---|---|
  | **Kreis links** vor der Zeile | linker Zeilenrand | Objekt (z. B. einen **Graphen**) ein-/ausblenden |
  | **Drei Punkte** am rechten Rand | rechtes Zeilenende | Zeilenmenü: **Schieberegler einschalten**, Einstellungen, Farbe, Beschriftung, Wertetabelle |

  Der Kreis darf also weiterhin genannt werden – aber nur zum **Ein- und Ausblenden**
  (so auf der Klasse-8-Seite 3 korrekt verwendet). Für Regler immer das **Zeilenmenü**.
  Korrigiert in: `geogebra_regler_gerade_kl8_ls.html`, `geogebra_parameter_ef_ls.html`,
  `geogebra_sekante_ef_ls.html`, `geogebra_tangente_ef_ls.html`.
- **Gestufte Tipps bei Freitexteingaben (Projektanweisung).** Nach einer falschen Freitext-/Zahleneingabe erscheint eine aufklappbare Tipp-Treppe: Tipp 1 = Hinweis zum Start, Tipp 2 = typische Stolperstellen, Tipp 3 = vollständige Lösung. Umgesetzt als `.stufen-tipps` (erscheint nur nach einem Fehler, verschwindet wieder, sobald alles stimmt).
- **Der Werkzeug-Weg gehört dazu (Rückmeldung nach den EF-Seiten).** Nicht alles läuft über die
  Eingabezeile: Der Reiter **Werkzeuge** (neben *Algebra*) bietet für viele Aufgaben einen
  intuitiven, antippbaren Weg – zwei Punkte auf den Graphen setzen, *Gerade* wählen, beide
  Punkte antippen, fertig ist die Sekante. Wo es einen solchen schönen Weg gibt, wird er als
  eigener Kasten `.werkzeug` (blau gestrichelt, 👆-Überschrift) **zusätzlich** zum Befehl gezeigt.
  Aufbau immer gleich: kurze Einleitung → nummerierte Tipp-Schritte (mit Werkzeuggruppe:
  *Punkte*, *Linien*, *Messen*, *Einfache Werkzeuge*) → Abschlusszeile **„Wann welcher Weg?"**.
  - Der Befehl bleibt der Kern der Reihe – der Werkzeug-Kasten ersetzt ihn nie, sondern stellt
    ihn gegenüber. Ehrliche Abwägung in der Fazit-Zeile: Werkzeug = schnell, anschaulich,
    gut zum **Erkunden** und zum Operator *„lies ab"*; Befehl = bleibt als Zeile stehen
    (**dokumentiert den Weg**), rechnet bei Änderungen automatisch neu, ist
    **weiterverwendbar** und passt zu *„bestimme"/„berechne"*.
  - **Didaktische Brücke, die überall gilt:** Beide Wege erzeugen **dasselbe Objekt**. Nach dem
    Antippen steht das Ergebnis mit seiner Definition in der Algebra-Ansicht – man kann also mit
    dem Werkzeug anfangen und den Befehl dort **nachlesen**. Das ist der beste Einstieg für SuS,
    die vor der Eingabezeile zurückschrecken.
  - Praktischer Pflicht-Hinweis in jedem Kasten: **danach wieder auf *Bewegen* umschalten**,
    sonst setzt jeder weitere Tipp ein neues Objekt.
  - **Umgesetzt in 10 Seiten** (Werkzeugnamen und Gruppen gegen die Handreichung „GeoGebra
    Werkzeuge Grafikrechner", Digitalassistenz Sachsen-Anhalt, geprüft):

    | Seite | Werkzeug-Weg |
    |---|---|
    | EF 1 Funktionen/Fenster | *Punkte → Punkt auf Objekt* – Punkt am Graphen entlangziehen |
    | EF 2 Nullstellen | *Punkte → Nullstellen* – einmal auf den Graphen tippen |
    | EF 3 Schnittpunkte | *Punkte → Schnittpunkt* – beide Graphen bzw. eine Kreuzungsstelle antippen |
    | EF 4 Parameter | *Einfache Werkzeuge → Schieberegler* – Name/Min/Max/Schrittweite gleich im Dialog |
    | EF 5 Sekante | *Punkt auf Objekt* (K1) sowie *Linien → Gerade* + *Messen → Steigung* (K2) |
    | EF 6 Tangente | *Konstruieren → Tangenten* + *Messen → Steigung* mit Steigungsdreieck |
    | EF 7 Ableitungsfunktion | **kein Werkzeug für die Ableitung** – dafür die Ortslinien-Konstruktion (s. u.) |
    | EF 8 Extrempunkte | *Punkte → Extremum* – einmal auf den Graphen tippen |
    | EF 9 Wendepunkte | **kein Wendepunkt-Werkzeug** – stattdessen *Extremum* auf \(f'\) anwenden |
    | Kl. 7 Seite 6 Terme grafisch | *Punkte → Punkt auf Objekt* – Graph abfahren und Werte ablesen |

  - **Nüchtern formulieren.** Keine Superlative („wunderschön", „unschlagbar"). Ein Weg ist
    *schön*, *anschaulich* oder *schnell* – mehr Werbung braucht er nicht.
  - **Inhaltliches gehört nicht in den Bedienungs-Kasten.** Wo eine Konstruktion eher den
    mathematischen Inhalt erklärt als die Bedienung, kommt sie als **aufklappbarer, freiwilliger
    Kasten** (`.werkzeug.wz-fak` mit `.wz-kopf` / `.wz-inhalt`, `toggleWz(id)`) – standardmäßig
    eingeklappt, mit dem Hinweis „Für diese Seite brauchst du das nicht". Die Reihe lehrt die
    **Bedienung**; Inhaltliches ist Zugabe, nicht Pflichtstoff.
  - **Zwei Seiten ohne eigenes Werkzeug – bewusst als Chance genutzt:**
    - *Ableitungsfunktion:* Punkt auf Objekt → Tangenten → Steigung (\(m\)) → getippt
      `S=(x(A),m)` → bei \(S\) über **Einstellungen** die **Spur** einschalten → \(A\) ziehen,
      \(S\) hinterlässt den Graphen der Ableitung. **Spur statt Ortslinie** (Vorgabe der
      Lehrkraft): Die Spur zeigt unmittelbar, was passiert; die Ortslinie müsste erst als
      Objekt erklärt werden. Steht als **freiwilliger Aufklapp-Kasten** auf der Seite.
    - *Wendepunkte* (ebenfalls als **aufklappbarer** Kasten, s. o.): Wendepunkt von \(f\) = **Extremum von \(f'\)**. Also `g(x)=f'(x)` eingeben
      und das *Extremum*-Werkzeug auf \(g\) anwenden. Begründet nebenbei, **warum** \(f''(x)=0\)
      der richtige Ansatz ist. Wichtige Warnung im Kasten: Der \(y\)-Wert des Extremums von \(g\)
      ist die **Steigung**, nicht der \(y\)-Wert des Wendepunkts.
  - **Bewusst ohne Werkzeug-Kasten:** Klasse 7 Seiten 1–5 (Erste Schritte, Klammern/Brüche,
    Vorzeichen, ANS/Variablen, Wertetabelle). Das sind reine Eingabe- und Rechenseiten – dort
    gibt es keinen Werkzeug-Weg, der etwas besser oder anschaulicher machen würde. Ein Kasten
    „der Vollständigkeit halber" wäre nur Ballast. Der Grundsatz lautet: **Hinweis nur, wo der
    Weg wirklich schön ist.**
  - **Klasse-7-Sonderregel:** Auf Kl. 7 Seite 6 wird das *Schnittpunkt*-Werkzeug **nicht**
    genannt. Es würde den didaktischen Kern der Seite aushebeln (den Kreuzungspunkt selbst
    ablesen) und liefe der Festlegung „keine Lösebefehle in Klasse 7" zuwider. Angeboten wird
    nur *Punkt auf Objekt* – mit dem ehrlichen Hinweis, dass man \(x=3\) mit dem Finger nie
    genau trifft und deshalb mit `f(3)` kontrolliert.
- **Paare verbinden: Zugehörigkeit sichtbar machen.** Bei „Paare verbinden"-Aufgaben (unabhängig gemischte linke/rechte Spalte) bekommt jedes linke Element eine feste Nummer (Position in der Spalte); sobald verbunden, zeigt das rechte Element dieselbe Nummer. So sieht man auch nach der Auswahl noch, was zusammengehört – nicht nur eine grüne Markierung ohne Zuordnung.

---

## Klasse 7 – Grundsätzlicher Umgang mit GeoGebra
*(in Bearbeitung – siehe Seiten-Liste unten)*
- Eingabe mit Punkt statt Komma
- Klammern – Hinweis zu Rechenregeln
- Eingabe von Brüchen und gemischten Zahlen
- Verwendung von ANS und von zugewiesenen Variablen
- Rechnungen im Verlauf stehen lassen (nicht löschen)
- Terme mit x eingeben und grafisch darstellen, Wertetabelle
- Exponenten schreiben
- Tastatur vs. Bildschirmtastatur

**Geplante Lernhappen (6 Seiten, je ~25 Min) – Planung abgestimmt:**

| # | Titel | GeoGebra-Kern | Lehrplan-Anker Kl. 7 |
|---|---|---|---|
| 1 | Erste Schritte & Bedienung | Oberfläche, Tastatur-Tricks `^`/`/`/`*`, Punkt statt Komma, Verlauf, Vorschau auf Variablen | – (Bedienung) |
| 2 | Klammern & Brüche | Wann muss geklammert werden? Bruchstrich als unsichtbare Klammer, verschachtelte Klammern, gemischte Zahlen in größeren Rechnungen | Kap. I Rationale Zahlen |
| 3 | Vorzeichen & negative Zahlen | Minuszeichen vs. Subtraktion, `(-3)^2` vs. `-3^2`, negative Werte einsetzen, `5-(-3)` | Kap. I Rationale Zahlen |
| 4 | Weiterrechnen: ANS & Variablen | automatische Namen (a, b, c …) nutzen, eigene Namen vergeben, mehrschrittig rechnen ohne Zwischenergebnisse abzutippen | UV III Prozent-/Zinsrechnung |
| 5 | Terme mit x & Wertetabelle | Term mit x eingeben, Wertetabelle anlegen (Startwert/Endwert/Schrittweite), Werte ablesen | UV II Zuordnungen, UV IV Terme |
| 6 | Terme grafisch darstellen | Graph zum Term, Sichtfenster, zwei Terme in einem System, **Schnittpunkt ablesen = grafisches Lösen** | UV II Zuordnungen, UV IV grafische Lösungsverfahren |

**Wichtige Festlegungen für Klasse 7:**
- **Keine Befehle zum Gleichungslösen** (kein `Löse`, kein `Lösungen`, kein `Schneide`, kein `Nullstelle`). Auf Seite 6 wird der Schnittpunkt **rein visuell abgelesen** – das ist laut Lehrplan (UV IV: „algebraische und grafische Lösungsverfahren") korrekt und bereitet Klasse 8 vor, ohne ihr vorzugreifen.
- **Malzeichen explizit:** In Klasse 5–7 gilt `5·x` statt `5x` und `8·(7·x+2)`. In den GeoGebra-Eingaben also konsequent `5*x` schreiben.
- **Rationale Zahlen sind verfügbar** (Kap. I), negative Zahlen dürfen und sollen vorkommen – Seite 3 macht die Vorzeichenfallen zum eigenen Thema.
- Die **Wertetabelle** wird erst auf Seite 5 eingeführt (Menü der Funktionszeile → Wertetabelle → Startwert / Endwert / Schrittweite), nicht schon früher.

**Hinweis zu Seite 1 (Rückmeldung nach erstem Entwurf):** Wurzeln (`sqrt(...)`) sind in Klasse 7 noch nicht nötig und wurden aus Seite 1 entfernt – stattdessen liegt der Fokus auf gemischten Zahlen/Brüchen als Rechnung. Seite 1 erwähnt ANS/Variablen bereits kurz (Karte „Verlauf"), Seite 3 vertieft das Thema. **Wichtig für Seite 3:** GeoGebra weist jeder Rechnung automatisch selbst einen Variablennamen zu (z. B. `a`, `b`, `c`, …) – man tippt NICHT selbst `a=13*6`, sondern einfach `13*6`, und GeoGebra zeigt von sich aus `a = 78`. Die Testkarte enthält neben Verständnisfragen auch mehrere **nicht im Kopf lösbare Rechenaufgaben**, die die SuS tatsächlich mit dem Grafikrechner lösen müssen. Seite 1 weist außerdem schon darauf hin, dass eine gemischte Zahl (`4+3/4`) in einer größeren Rechnung **geklammert** werden muss (`2*(4+3/4)`, sonst Punkt-vor-Strich-Fehler) – Seite 2 („Klammern, Brüche & Exponenten") kann darauf aufbauen statt bei null anzufangen.

## Klasse 8
- Lineare Funktionen/Geraden eingeben – Einsatz von Schiebereglern
- Mehrere Funktionen/Geraden in einem Koordinatensystem – Lagebeziehung
- Schnittpunkte (Nullstelle, y-Achse, von Funktionen; gezielt Werte oder Stellen bestimmen)
- Formeln eingeben
- **Ausdrücklich noch NICHT:** Lösen von Gleichungen mit den eingebauten Löse-Funktionen

**Befehlsumfang Klasse 8 (mit der Lehrkraft abgestimmt):** `Nullstelle(f)`, `Schneide(f,g)` und
`f(0)` werden eingeführt – `Löse`/`Lösungen` bleiben für Klasse 9 reserviert. Auf Seite 5 steht
dazu ein aufklappbarer Hinweis („Kann GeoGebra das nicht direkt ausrechnen?"), der die
Verschiebung begründet, statt sie zu verschweigen: Über den Schnittpunkt sieht man, **was** die
Lösung ist – Voraussetzung dafür, später die Fälle ohne bzw. mit unendlich vielen Lösungen zu
verstehen.

**Lehrplan-Anker:** UV *Lineare Funktionen* und UV *Lineare Gleichungssysteme* (Gleichsetzungs-,
Einsetzungs- und Additionsverfahren) aus Lambacher Schweizer 8 – G9. Seite 5 ist die
GeoGebra-Entsprechung zum grafischen Lösungsverfahren; die rechnerischen Verfahren aus dem
Unterricht bleiben davon unberührt (GeoGebra = Kontrolle, nicht Ersatz).

**Geplante und umgesetzte Lernhappen Klasse 8 (6 Seiten, je ~25 Min):**

| # | Titel | Datei | GeoGebra-Kern |
|---|---|---|---|
| 1 | Geraden eingeben und lesen | geogebra_geraden_eingeben_kl8_ls.html | `f(x)=…` mit Namen, `f(1)-f(0)` als Steigungstrick, Sichtfenster |
| 2 | m und b am Schieberegler | geogebra_regler_gerade_kl8_ls.html | Regler anlegen, Zielvorgaben treffen (Grundregel) |
| 3 | Mehrere Geraden in einem Bild | geogebra_geraden_lage_kl8_ls.html | Farben/Ausblenden, parallel–identisch–schneidend |
| 4 | Nullstelle und y-Achsenabschnitt | geogebra_nullstelle_achse_kl8_ls.html | **erster Befehl** `Nullstelle(f)`, Stelle/Wert/Punkt |
| 5 | Schnittpunkt zweier Geraden | geogebra_schnittpunkt_lgs_kl8_ls.html | `Schneide(f,g)`, LGS grafisch, Sonderfälle |
| 6 | Formeln mit mehreren Variablen | geogebra_formeln_tarife_kl8_ls.html | `A(g,h)` und `T(a,c,h)`, Tarifvergleich |

**Didaktische Festlegungen, die sich durch die Klasse-8-Reihe ziehen:**
- **Der Steigungstrick `f(1)-f(0)`** (Seite 1) liefert \(m\), ohne den Term zu kennen – und trägt
  gleich die Bedeutung mit: ein Schritt nach rechts, dann \(m\) nach oben.
- **`f(0)` statt „die letzte Zahl im Term"** (Seite 4). Gegenbeispiel \(h(x)=5-2x\): Dort ist der
  y-Achsenabschnitt die *vordere* Zahl. Diese Falle steht bewusst als Warnbox auf der Seite.
- **Stelle – Wert – Punkt** (Seite 4, Karte 3) als eigene Tabelle. Führt die Unterscheidung ein,
  die ab EF unter „Operator beachten" wieder auftaucht.
- **GeoGebra vereinfacht Terme selbst** (Seiten 3 und 6): `k(x)=(4*x+6)/2` erscheint in der
  Algebra-Ansicht als \(2x+3\). Das ist der schnellste Weg, „identisch" zu erkennen – und ein
  echter Bedienvorteil, für den man sonst per Hand umformen müsste.
- **Geradengleichungen direkt eingeben** (Seite 5): `2*x+y=5` wird ohne Umstellen als Gerade
  angenommen. Das spart bei LGS-Aufgaben den kompletten Umformschritt.
- **„undefiniert" ist die Antwort, keine Fehlermeldung** (Seite 5, Karte 3) – bei parallelen
  Geraden. Wird ausdrücklich als Warnbox behandelt, weil SuS es sonst als Bedienfehler deuten.
- **Werkzeug-Kästen** auf den Seiten 2 (*Schieberegler*), 3 (*Parallele Gerade*), 4
  (*Nullstellen*) und 5 (*Schnittpunkt*) – nach der auf S. 1–9 EF etablierten Form.
- **Kontrollbilder ohne Lösungspunkte:** Die Bilder zeigen die Geraden, markieren aber **nicht**
  die Punkte, die auf derselben Karte abgefragt werden. Sonst wäre die Aufgabe durch Ablesen im
  Bild erledigt (siehe Regel „nie die Lösung vorwegnehmen").

**Wiederverwendbarer Baustein:** `/tmp/koord.py` erzeugt statische Koordinatensystem-SVGs
(Achsen mit Pfeilen, beschriftete Einheiten, Gitter, an den Fenstergrenzen geclippte Geraden,
optionale Punkte). Parameter: Fenstergrenzen, Geradenliste `(m, b, Farbe, Breite, gestrichelt)`,
Punktliste, Achsenschrittweiten. Damit sind alle Bilder dieser Reihe entstanden.

## Klasse 9
- Wie Klasse 8, zusätzlich:
- Lösen von Gleichungen mit den "rechnerischen" Lösungswegen des Grafikrechners – nicht mehr nur ablesen
- Abwägen verschiedener Lösungswege (ablesen vs. rechnerisch bestimmen)
- Wurzeln exakt eingeben (`sqrt`) und Anzeige-Rundung von echter Genauigkeit unterscheiden
- `Extremum(f)` für den Scheitelpunkt; Scheitelpunktform mit drei Schiebereglern
- Kreis und Zylinder als reine Formelrechnung (Funktionen mit zwei Variablen, `Löse` rückwärts)
- **Umgesetzt:** 6 Seiten, siehe „Status Seiten-Serie Klasse 9".

## Klasse 9/10
- Sinus mithilfe des Einheitskreises entwickeln
- Einsatz zum Lösen jeder Form quadratischer Gleichung – beide Wege: pq-Formel **und** direkt mit Lösungsfunktion

## Klasse 10
- Vertiefender Einsatz zum Lösen von Gleichungen
- Darstellung vieler Funktionen gleichzeitig
- Unterschied klar herausstellen: **rechnerisches Lösen** (Gleichung notieren, dann GTR-Funktion nutzen) vs. **Bestimmen** (am Graphen ablesen – besondere Punkte)
- Exponentielles Wachstum: `a*q^x`, Prozent → Faktor, Wertetabelle, Verdopplungs-/Halbwertszeit
- Logarithmus eintippen: `ln`, `lg`, `log(b, x)`
- Winkel: Gradzeichen ° gegen Bogenmaß, eigene Umrechnungsfunktionen
- Sinusfunktion `a*sin(b*x)` mit zwei Schiebereglern; `Nullstelle`/`Extremum` **mit Suchbereich**
- **Umgesetzt:** 6 Seiten, siehe „Status Seiten-Serie Klasse 10".

## EF (Einführungsphase)
- Wie Kl. 10, zusätzlich:
- Ableitung und zweite Ableitung: Hinweise auf Nutzung, Hilfestellung beim manuellen Ableiten, korrekte Ableitung wird vom Grafikrechner zur Kontrolle angezeigt
- **Zusätzlich (Vorgabe):** Extrempunkte und Wendepunkte *berechnen* – also über Ableitungen Gleichungen aufstellen (\(f'(x)=0\), \(f''(x)=0\)), die dann in GeoGebra gelöst werden. Gern auch Funktionen höheren Grades.
- **Pflicht ab EF (Projektanweisung):** Jede Aufgabe kennzeichnet sichtbar (1) Hilfsmittel – *mit GeoGebra/GTR* vs. *ohne Hilfsmittel* – und (2) Lösungsart – *rechnerisch* vs. *grafisch bestimmen/ablesen*. Umgesetzt als Chip-Zeile (`.kennz` mit `.chip-hm` / `.chip-frei` / `.chip-art`) direkt über der Aufgabe.

**Geplante Lernhappen EF (9 Seiten, je ~25 Min):**
1. **Funktionen eingeben & Sichtfenster** – `f(x)=…` mit Namen, warum der Name Voraussetzung für `f(2)`/`f'(x)` ist, Fenster einstellen, „der Graph kann täuschen", Funktionswerte exakt bestimmen *(fertig)*
2. **Nullstellen bestimmen** – ablesen vs. rechnerisch mit Löse-Befehl; Genauigkeit und Grenzen des Ablesens
3. **Schnittpunkte zweier Funktionen** – `Schneide(f,g)`, Gleichung \(f(x)=g(x)\) aufstellen und lösen lassen
4. **Parameter & Transformationen mit Schiebereglern** (E-A2) – Einfluss von Parametern systematisch erkunden
5. **Durchschnittliche Änderungsrate – die Sekante** (E-A3) – Differenzenquotient, Sekante durch zwei Punkte
6. **Lokale Änderungsrate – Tangente & Ableitung an einer Stelle** (E-A3) – Grenzprozess sichtbar machen, Tangentensteigung
7. **Die Ableitungsfunktion** (E-A4) – `f'(x)` erzeugen, eigenes händisches Ableiten damit kontrollieren (Grafikrechner als Korrekturhilfe, nicht als Ersatz)
8. **Extrempunkte berechnen** (E-A4) – \(f'(x)=0\) als Gleichung aufstellen und in GeoGebra lösen, hinreichendes Kriterium mit \(f''\) prüfen; auch Funktionen höheren Grades
9. **Wendepunkte & Krümmung** (E-A4) – \(f''(x)=0\) lösen, Krümmungsverhalten begründen, höhere Grade

**Noch einzuplanen (Wunsch, Zeitpunkt offen – im Verlauf der Häppchen einstreuen):** *Mehrere Werte auf einmal einsetzen* über eine **Liste in geschweiften Klammern**, Trennzeichen Komma: `g({4.5, 0})` liefert direkt `{47.5, -11}`. Praktisch, um mehrere Funktionswerte in einem Schritt zu bekommen (auch als Ergebnis einer Liste `l1` weiterverwendbar). Passt gut als Erweiterung in einen Happen ab Nr. 2 oder als Wiederholungsbaustein. Achtung beim Erklären: **innerhalb der Liste trennt das Komma**, die Dezimaltrennung bleibt der **Punkt** (`4.5`) – genau der Kontrast, der in Klasse 7 als „Punkt statt Komma" eingeführt wurde.

**Noch zu prüfen (Lehrkraft):** Die Intervall-Varianten der Suchbefehle – auf Seite 2 steht `Nullstelle(f, -5, 5)` als Möglichkeit, im Bereich von −5 bis 5 zu suchen. Diese Syntax konnte nicht gegen das offizielle GeoGebra-Handbuch verifiziert werden (wiki.geogebra.org und geogebra.org/manual blockieren automatisches Abrufen). Vor dem Einsatz im Unterricht einmal in der App gegenprüfen. Auf Seite 3 ist die entsprechende Stelle bewusst offen formuliert („GeoGebra blendet dir beim Tippen die möglichen Varianten ein") und nennt keine ungeprüfte Signatur.

**Roter Faden Seiten 2 und 3 (Begriffsunterschied bewusst herausgearbeitet):**
- Nullstelle = **x-Wert** (der y-Wert ist ja 0) → `Nullstelle(f)` gibt trotzdem Punkte aus, x-Koordinate ablesen
- Schnittpunkt = **Punkt mit zwei Koordinaten** → `Schneide(f,g)` liefert sie fertig, `Löse(f(x)=g(x))` liefert nur die x-Werte, y muss eingesetzt werden
Diese Gegenüberstellung ist der didaktische Kern von Seite 3 und sollte in späteren Seiten (Extrempunkte, Wendepunkte – ebenfalls Punkte!) wieder aufgegriffen werden.

**`Löse` vs. `Lösungen` – ab EF immer gegenüberstellen (Vorgabe):**

| Befehl | Ausgabe | Vorteil | Nachteil |
|---|---|---|---|
| `Löse(...)` | Liste von **Gleichungen**, z. B. `{x = -√2, x = √2}` | Variable darf **beliebig heißen** (a, t, k …); liest sich wie eine Lösungsmenge | Ergebnisse **nicht direkt weiterverwendbar** |
| `Lösungen(...)` | Liste von **Zahlen**, z. B. `{-√2, √2}` | direkt **in Funktionen einsetzbar**, auch als ganze Liste auf einmal | Variable muss **x** heißen |

Faustregel für die SuS: Lösungsmenge nur hinschreiben → `Löse`. Mit den Werten weiterrechnen → `Lösungen`.

**Killer-Anwendung (auf Seite 3 umgesetzt):** `q(Lösungen(p(x)=q(x)))` liefert **alle y-Werte der Schnittpunkte auf einen Schlag** – löst genau das Problem, dass `Löse` nur x-Werte liefert. Das Einsetzen derselben Liste in die *andere* Funktion ist zugleich die Probe. Das ist auch die praktische Einlösung des früher notierten Listen-Wunsches (`g({4.5, 0})` → `{47.5, -11}`): `Lösungen` erzeugt genau so eine Liste. In späteren Seiten (Extrempunkte, Wendepunkte) analog nutzen: `f(Lösungen(f'(x)=0))` gibt die y-Werte der Extrempunkte.

**Wiederverwendbarer Baustein: statisches Koordinatensystem (SVG, ohne Bibliothek).**
In `geogebra_parameter_ef_ls.html` steckt ein kleines Zeichenmodul für **Kontroll- und Illustrationsbilder** (nicht interaktiv, siehe Grundregel oben):
- `GEO`-Objekt (Fenstergrenzen), `sx()`/`sy()` (Mathe → Pixel)
- `zeichneAchsen(svg)` – Gitter, Achsen mit Pfeilen, Einheiten und x/y-Beschriftung (erfüllt die Projektvorgabe für Koordinatensysteme)
- `zeichneKurve(svg, fn, farbe, breite, gestrichelt)` – zeichnet beliebige Funktionen, am Fenster geclippt und in Teilstücken (also auch für Polstellen geeignet)

**Bauanleitungs-Baustein:** CSS-Klasse `.bauen` (blau umrandeter Kasten mit 🔧-Überschrift und nummerierter Liste) für „Das gibst du in GeoGebra ein". CSS-Klasse `.einstellung` für vorgegebene Reglerwerte, `.aufgabe` für einen Aufgabenblock mit Zielvorgabe. Diese drei Klassen sind der Standard für alle weiteren Seiten.

**Die Sekanten-Konstruktion aus Seite 5 (wird auf Seite 6 zur Tangente weitergebaut):**
```
f(x)=x^2
u=1        v=3          (beide als Regler einblenden, Schrittweite 0.5)
A=(u,f(u)) B=(v,f(v))   (Punkte kleben am Graphen – y-Wert aus f berechnen lassen)
s=Gerade(A,B)
m=Steigung(s)
```
Kernidee: `A=(u,f(u))` statt fester Zahlen – dann bleibt der Punkt auf dem Graphen, auch wenn die Funktion später ausgetauscht wird. Genau das nutzt die Testkarte: `f(x)=x^3-4x` neu eintippen, die ganze Konstruktion rechnet sich neu.
Alternativer Weg ohne Konstruktion, ebenfalls gezeigt: Differenzenquotient direkt eintippen, z. B. `(f(3)-f(1))/(3-1)`.

**Seite 6 baut das fort (umgesetzt):** \(v\) gegen \(u\) laufen lassen (Wertetabelle 2 / 1,5 / 1,1 / 1,01 → m nähert sich 2), dann `t=Tangente(A,f)` und `k=Steigung(t)`. Nebenbei geübte GeoGebra-Fähigkeit: **Schrittweite auf 0.01 stellen** bzw. den Wert direkt eintippen (`v=1.01`), weil man ihn sonst nie trifft. Bewusst thematisiert: Bei \(v=u\) bricht die Sekante zusammen – das ist kein Bedienfehler, sondern der Grund für den Grenzwert.

**Vorbereitung auf Seiten 8/9 (bereits auf Seite 6 angelegt):** Die Zielaufgabe „stelle \(u\) so ein, dass \(k=0\)" führt direkt auf den Scheitelpunkt; die Testkarte lässt beide Stellen mit waagerechter Tangente von \(x^3-3x\) suchen (\(x=\pm1\), Hoch- und Tiefpunkt). Der Zusammenhang **waagerechte Tangente ↔ Extrempunkt** ist damit vorbereitet und muss auf Seite 8 nur noch formalisiert werden (\(f'(x)=0\)).

**Seite 7 (umgesetzt):** Knüpft an die Beobachtung \(k=2u\) von Seite 6 an. Befehle: `g(x)=f'(x)` bzw. `Ableitung(f)`, zweite Ableitung `f''(x)` bzw. `Ableitung(f,2)`.

**Der Kontroll-Trick von Seite 7 (in späteren Seiten wiederverwendbar):** Eigene händische Ableitung als `h(x)=...` eingeben, dann `d(x)=f'(x)-h(x)` bilden. **Ist d überall 0, war die Ableitung richtig.** Besser als Termvergleich per Auge, weil unterschiedlich aussehende Terme gleich sein können – und ein Restterm zeigt sogar, *wo* der Fehler steckt.
**Klausurregel – korrekt formulieren (Korrektur der Lehrkraft):** Die Klausur hat einen
**hilfsmittelfreien Teil** (dort muss selbst abgeleitet werden) und einen **Teil mit
Hilfsmitteln** (dort darf GeoGebra auch zum *Ableiten* genutzt werden, nicht nur zur
Kontrolle). Nicht „GeoGebra darf nie ableiten" schreiben – das ist falsch. Die Begründung für
den Kontroll-Trick lautet: erst selbst ableiten, dann prüfen lassen – so wird für den
hilfsmittelfreien Teil geübt und im anderen Teil trotzdem schnell gearbeitet. Chip-Kombination
„✏️ zuerst ohne Hilfsmittel ableiten" + „🖩 danach mit GeoGebra kontrollieren" bleibt als
**Arbeitsauftrag** richtig und wird für alle Ableitungsaufgaben verwendet.

**Bedienhinweis, der Zeit spart:** `f''(x)` sind **zwei einzelne Apostrophe**, kein Anführungszeichen – häufiger Stolperstein auf dem iPad.

**Brücke zu Seite 9:** Die Aufgabe „finde die Stelle mit \(f''(x)=0\)" (dort \(x=5/3\)) ist bereits gestellt und als Wendepunkt benannt.

**Seiten 8 und 9 (umgesetzt) – der gemeinsame Dreischritt:**
Beide Seiten folgen exakt demselben Muster, das sich durch die ganze Reihe zieht:

| | Nullstellen (S. 2) | Extrempunkte (S. 8) | Wendepunkte (S. 9) |
|---|---|---|---|
| Befehl | `Nullstelle(f)` | `Extremum(f)` | `Wendepunkt(f)` |
| Ansatz | `f(x)=0` | `f'(x)=0` | `f''(x)=0` |
| y-Werte auf einen Schlag | – | `f(Lösungen(f'(x)=0))` | `f(Lösungen(f''(x)=0))` |

Alle drei Befehle geben **Punkte** zurück – die Unterscheidung Stelle/Punkt aus Seite 3 wird konsequent durchgehalten.

**Notwendig vs. hinreichend – auf beiden Seiten als rote Warnbox:**
- S. 8: `f'(x)=0` liefert nur *Kandidaten* (Gegenbeispiel \(x^3\)); Entscheidung über \(f''\): negativ → Hochpunkt, positiv → Tiefpunkt. Abkürzung für alle Stellen auf einmal: `f''(Lösungen(f'(x)=0))`.
- S. 9: `f''(x)=0` reicht nicht, die Krümmung muss *wechseln* (Gegenbeispiel \(x^4\)).

**Hinreichendes Kriterium bei Wendepunkten – beide Wege anbieten (Vorgabe der Lehrkraft):**
Nicht nur den Vorzeichenwechsel nennen, sondern auch die **dritte Ableitung**. Auf S. 9 als
Vergleichstabelle umgesetzt:

| | Weg A: Vorzeichenwechsel von \(f''\) | Weg B: dritte Ableitung |
|---|---|---|
| Bedingung | \(f''\) wechselt dort das Vorzeichen | \(f'''(x_0) \neq 0\) |
| in GeoGebra | zweimal `f''(…)`, links und rechts von \(x_0\) | einmal `f'''(…)` |
| Vorteil | funktioniert immer | ein Tastendruck |
| Haken | zwei Werte nötig, nah genug an \(x_0\) | bei \(f'''(x_0)=0\) keine Entscheidung |

Bedienwissen dazu: `f'''(x)` sind **drei einzelne Apostrophe** – bequemer ist `Ableitung(f,3)`.
Listen-Trick auch hier: `f'''(Lösungen(f''(x)=0))` prüft alle Kandidatenstellen auf einen
Schlag – ist keine Null dabei, sind alle echte Wendestellen. Das \(x^4\)-Gegenbeispiel dient
zugleich als Beleg für den Haken bei Weg B (\(f'''(0)=0\)).

**Funktionen höheren Grades (Vorgabe erfüllt):** Testkarte S. 8 nutzt \(g(x)=x^4-8x^2+3\) mit drei Extrempunkten, Testkarte S. 9 nutzt \(h(x)=x^4-6x^2+5\) mit zwei Wendepunkten – beide zusätzlich mit dem Hinweis, dass ohne passendes Sichtfenster Punkte übersehen werden.

**Operator-Regel (gilt ab EF für alle Seiten):** Die Unterscheidung explizit thematisieren und bei jeder Aufgabe kennzeichnen:
- „lies ab" / „schätze ab" → Näherungswert vom Graphen genügt
- „bestimme" → GeoGebra-Funktionen erlaubt (z. B. `f(2)`, `Nullstelle(f)`), Ergebnis exakt, kein Rechenweg nötig
- „berechne" → nachvollziehbarer Rechenweg/Ansatz verlangt, GeoGebra höchstens zum Lösen

Roter Faden der Reihe: In den Seiten 8 und 9 wird durchgehend betont, dass die **Gleichung von Hand aufgestellt** wird (rechnerischer Weg) und GeoGebra nur das **Lösen** übernimmt – im Gegensatz zum bloßen Ablesen eines Extrempunkts am Graphen. Genau diese Unterscheidung verlangt die Kennzeichnungspflicht ab EF.

## Q1 / Q2
- Noch offen / vorläufig – wird auf Basis von EF weitergedacht
- Es kommt voraussichtlich noch Stochastik-Bezug hinzu (später gesondert klären, da eigentlich andere App-Funktion)

---

## Orientierung aus dem Kernlehrplan (zur Einordnung, nicht Teil des Grafikrechner-Strangs)
- EF: E-A1–E-A4 (Funktionseigenschaften, Transformationen/Parameter, Änderungsrate, Untersuchungskriterien), E-G1/E-G2 (Vektoren/Geraden im Raum – separater Strang)
- GK Q1: Optimierung, Modellieren mit ganzrationalen Funktionen, Änderungsrate→Bestand, Hauptsatz, Skalarprodukt, Ebenen, Wahrscheinlichkeitsrechnung
- LK Q1: zusätzlich Funktionenscharen, natürliche Exponentialfunktion, komplexere Extremwertprobleme mit Parametern, Ebenen/Abstände, Binomialverteilung
- Q2 GK/LK: Wachstumsprozesse, Binomialverteilung/Konfidenzintervalle (LK)

---

## Status Seiten-Serie EF
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Funktionen eingeben & Sichtfenster | geogebra_funktionen_fenster_ef_ls.html | fertig |
| 2 | Nullstellen bestimmen | geogebra_nullstellen_ef_ls.html | fertig |
| 3 | Schnittpunkte zweier Funktionen | geogebra_schnittpunkte_ef_ls.html | fertig |
| 4 | Parameter & Transformationen (Schieberegler) | geogebra_parameter_ef_ls.html | fertig |
| 5 | Durchschnittliche Änderungsrate – Sekante | geogebra_sekante_ef_ls.html | fertig |
| 6 | Lokale Änderungsrate – Tangente | geogebra_tangente_ef_ls.html | fertig |
| 7 | Die Ableitungsfunktion | geogebra_ableitungsfunktion_ef_ls.html | fertig |
| 8 | Extrempunkte berechnen | geogebra_extrempunkte_ef_ls.html | fertig |
| 9 | Wendepunkte & Krümmung | geogebra_wendepunkte_ef_ls.html | fertig |

## Status Seiten-Serie Klasse 7
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Erste Schritte & Bedienung | geogebra_erste_schritte_kl7_ls.html | fertig |
| 2 | Klammern & Brüche | geogebra_klammern_brueche_kl7_ls.html | fertig |
| 3 | Vorzeichen & negative Zahlen | geogebra_vorzeichen_kl7_ls.html | fertig |
| 4 | ANS & Variablen | geogebra_ans_variablen_kl7_ls.html | fertig |
| 5 | Terme mit x & Wertetabelle | geogebra_wertetabelle_kl7_ls.html | fertig |
| 6 | Terme grafisch darstellen | geogebra_terme_grafisch_kl7_ls.html | fertig |

**Klasse-7-Serie ist damit komplett (6/6).** Umsetzungsnotizen zu den Seiten 2–6:

- **Seite 2 – Gemischte Zahlen mit Klammer (ausdrückliche Vorgabe der Lehrkraft).** Eigene
  Themenkarte „Gemischte Zahlen – hier ist die Klammer Pflicht" mit Falsch/Richtig-Paaren:
  `2*4+3/4` → 8.75 (falsch) gegen `2*(4+3/4)` → 9.5 (richtig); `5-2+1/2` → 3.5 gegen
  `5-(2+1/2)` → 2.5. **Faustregel für die SuS:** Sobald vor oder hinter der gemischten Zahl
  noch etwas steht, kommt sie in eine Klammer. Davor die Karten „Punkt vor Strich" und
  „Der Bruchstrich ist eine unsichtbare Klammer" (`(3+5)/2` statt `3+5/2`).
- **Seite 3 – Vorzeichen.** Rechenzeichen vs. Vorzeichen (`8-(-3)` = 11), Klammerpflicht bei
  Mal/Geteilt mit negativen Zahlen, und als Kernfalle die Hochzahl: `(-3)^2` = 9 gegen
  `-3^2` = −9.
- **Seite 4 – ANS & Variablen.** GeoGebra vergibt die Namen `a`, `b`, `c` … selbst – man
  tippt **nicht** `a=13*6`. Eigene Namen (`preis=250`) nur, wo sie das Weiterrechnen lesbar
  machen. Anwendungskontext: mehrschrittige Prozent-/Zinsaufgaben (UV III).
- **Seite 5 – Wertetabelle.** Genauer Bedienweg nach offiziellem Handbuch: Menü-Symbol der
  Funktionszeile → Wertetabelle → Startwert / Endwert / Schrittweite → OK; späteres Ändern
  über das Menü neben der x-Spalte → Bearbeiten. Vorher `f(4)` als Einzelwert.
- **Seite 6 – Grafisches Lösen.** Zwei Terme in einem System, Schnittpunkt (2|5) **rein
  visuell abgelesen** – bewusst ohne `Schneide`/`Löse` (siehe Festlegung oben). Zwei statische
  Kontroll-SVGs (Achsen mit Pfeilen, beschrifteten Einheiten) als Vergleichsbild.

Alle fünf Seiten wurden headless (Playwright) durchgetestet: jede Karte erreichbar, jeder
Prüfen-Button mit korrekten Antworten grün, gestufte Tipps erscheinen nach Fehler und
verschwinden nach Korrektur, Zustand überlebt den Kartenwechsel, keine JS-Fehler.
**MathJax-Absicherung** (aus Seite 1 übernommen und in allen Seiten drin): `typesetPromise`
nur in `if(window.MathJax && …)` + `try/catch` aufrufen – sonst reißt ein blockiertes CDN
(Schul-WLAN!) das ganze Skript mit und die Karten funktionieren nicht mehr.

Verlinkung: gemeinsame Übersichtsseite (Hub) für die GeoGebra-Grafikrechner-Reihe – Details bei Bau der Serie klären (eigener Hub vs. bestehendes dino_hub.html).

## Status Seiten-Serie Klasse 8
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Geraden eingeben und lesen | geogebra_geraden_eingeben_kl8_ls.html | fertig |
| 2 | m und b am Schieberegler | geogebra_regler_gerade_kl8_ls.html | fertig |
| 3 | Mehrere Geraden in einem Bild | geogebra_geraden_lage_kl8_ls.html | fertig |
| 4 | Nullstelle und y-Achsenabschnitt | geogebra_nullstelle_achse_kl8_ls.html | fertig |
| 5 | Schnittpunkt zweier Geraden | geogebra_schnittpunkt_lgs_kl8_ls.html | fertig |
| 6 | Formeln mit mehreren Variablen | geogebra_formeln_tarife_kl8_ls.html | fertig |

## Status Seiten-Serie Klasse 9
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Wurzeln – exakt oder gerundet | geogebra_wurzeln_kl9_ls.html | fertig |
| 2 | Parabeln lesen: Nullstelle und Extremum | geogebra_parabel_lesen_kl9_ls.html | fertig |
| 3 | Scheitelpunktform mit drei Schiebereglern | geogebra_parabel_regler_kl9_ls.html | fertig |
| 4 | Gleichungen lösen: `Löse` und `Lösungen` | geogebra_loesen_kl9_ls.html | fertig |
| 5 | Ablesen, bestimmen oder berechnen? | geogebra_wege_kl9_ls.html | fertig |
| 6 | Kreis und Zylinder als Formelrechner | geogebra_kreis_zylinder_kl9_ls.html | fertig |

### Klasse 9 – inhaltliche Festlegungen
- **Neue Befehle in dieser Stufe:** `sqrt(...)`, `Extremum(f)`, `Löse(...)`, `Lösungen(...)`.
  Alles aus Klasse 7/8 (`Nullstelle`, `Schneide`, `f(0)`, Schieberegler, Fenster) bleibt gültig.
- **Kein mathematisches Verfahren wird hergeleitet** (Vorgabe Andreas): pq-Formel, quadratische
  Ergänzung usw. werden im Unterricht selbst erarbeitet. Diese Seiten zeigen ausschließlich,
  **wie man das Gerät bedient**. Deshalb steht auf Seite 4 „berechnen" für *Gleichung als Ansatz
  aufschreiben, Auflösen dem Rechner überlassen" – nicht für „Verfahren von Hand vorführen".
- **Löse vs. Lösungen:** `Löse` gibt Gleichungen der Form `{x = …}` aus, `Lösungen` nur die
  reinen Zahlen `{…}` – Letzteres ist weiterverwendbar (z. B. `g(Lösungen(f(x)=g(x)))`).
  Bei mehr als einem Buchstaben in der Gleichung ist die gesuchte Variable als zweites
  Argument Pflicht: `Löse(4*t-6=18, t)`.
- **Operator-Regel (Seite 5):** *lies ab* → Näherung vom Graphen; *bestimme* → exaktes Ergebnis,
  Befehl erlaubt, kein Rechenweg; *berechne* → Gleichung als Ansatz ins Heft, Auflösen darf der
  Rechner. Diese Tabelle ist der rote Faden der Klasse-9-Serie und wird in Klasse 10 wieder
  aufgegriffen.
- **Seite 6 bewusst nur Kreis und Zylinder** (Vorgabe Andreas). Der Grafikrechner zeichnet keine
  Körper – er wird hier als **Formelrechner** benutzt: π exakt (`pi`, nie 3,14), Formeln als
  Funktionen speichern (`u(r)`, `a(r)`, `V(r,h)`, `O(r,h)`), Rückwärtsfragen über `Löse`.
  Die Reihenfolge der Argumente bei zwei Variablen wird ausdrücklich als Fehlerquelle geübt
  (`V(2,10)` gegen `V(10,2)`).
- **Werkzeug-Weg auf Seite 6:** Gruppe *Kreise* → *Kreis mit Mittelpunkt und Radius*, danach
  `Umfang(c)` und `Fläche(c)`. Anschaulich für einen einzelnen Kreis; für viele Radien sind die
  Funktionen schneller.
- **Einheiten:** Der Grafikrechner rechnet einheitenlos. Auf Seite 6 wird das explizit gesagt
  und es werden nur Zahlen eingetragen; die Einheitenfrage läuft über eine MC-Frage der
  Auswertungskarte statt über Dropdowns (die Dropdown-Regel greift, wo *die Einheit selbst*
  der Lerngegenstand ist – hier ist es die Bedienung).
- **Lehrplan-Grenze eingehalten:** keine Ableitung, keine Trigonometrie, kein Logarithmus,
  keine Vektoren, kein Begriff „pq-Formel" (Klasse 10) – auch nicht als Distraktor.

## Status Seiten-Serie Q1 – Steckbriefaufgaben (CAS-Ansicht)
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Funktionen aus Bedingungen bestimmen | geogebra_steckbrief_q1_ls.html | fertig |
| 2 | Steckbriefaufgaben dritten Grades (weiterführend) | geogebra_steckbrief_grad3_q1_ls.html | fertig |

### Der entscheidende Punkt: Grafikrechner gegen CAS
Für Steckbriefaufgaben braucht man Parameter, die **symbolisch bleiben**. Im **Grafikrechner**
wird aus einem freien Buchstaben sofort ein **Schieberegler**, also eine Zahl – `f(1)` liefert
dann nur einen Zahlenwert und keine Gleichung in `a` und `b`. Deshalb laufen diese beiden
Seiten in der **CAS-Ansicht** der Suite.

| Angabe | Beleg |
|---|---|
| `Löse( <Liste von Gleichungen>, <Liste von Variablen> )` löst Systeme, ausdrücklich auch mit Parametern | GeoGebra-Manual „Löse (Befehl)" |
| In der CAS-Ansicht ist `:=` die **Zuweisung**; `=` ist ein Gleichheitszeichen in einer Gleichung. `a=2` weist nichts zu. | GeoGebra-Manual „CAS-Ansicht" |
| Strich-Schreibweise `f'(x)` / `f''(x)` statt `Ableitung(f)` erlaubt | GeoGebra-Manual „Ableitung (Befehl)" |

**Offener Punkt aus dem Handbuch, am Gerät geklärt:** Das Manual führt `Löse` als
CAS-spezifischen Befehl („nur in der CAS-Ansicht verfügbar"). Andreas hat am Gerät geprüft,
dass `Löse` in der Suite **auch im Grafikrechner-Modus** funktioniert – die Klasse-9- und
Klasse-10-Seiten bleiben deshalb unverändert. Das Handbuch ist an dieser Stelle älter als die
Suite.

### Inhaltliche Festlegungen
- **Seite 1** baut das Prinzip auf: CAS öffnen, `:=` gegen `=`, Ansatz mit Parametern,
  Bedingungen als Liste, Ergebnis einsetzen und prüfen. Dazu die Ableitungsbedingungen
  (`f'(2)=3`, waagerechte Tangente, Extrempunkt) mit der Übersetzungstabelle.
- **Seite 2** ist die weiterführende Seite (Vorgabe Andreas): Ansatz dritten Grades, vier
  Bedingungen, vollständige Übersetzungstabelle inklusive Wendepunkt, Symmetrie als
  Abkürzung, Rückkehr in den Grafikrechner zur Kontrolle.
- **Die Abzählregel** ist der rote Faden beider Seiten: so viele Bedingungen wie Parameter.
  Die wichtigste Fehlerquelle bekommt eine eigene Warnbox – **Stelle** („bei \(x=1\) ein
  Hochpunkt") liefert eine Gleichung, **Punkt** („der Hochpunkt \(H(1|4)\)") zwei.
- **Kennzeichnung nach TEIL 3.2** (Pflicht ab EF) ist auf beiden Seiten an jeder Aufgabe
  gesetzt: Chip-Zeile mit Hilfsmittel und Lösungsart.
- **Neuer Baukasten:** `/tmp/bauer_q1.py` (wie bauer10, aber `klasse="Q1"`, `.kennz`-CSS,
  `.uebers`-Tabelle und `kennz()`-Helfer). Bauskripte `/tmp/q1_s1.py`, `/tmp/q1_s2.py`.

## Status Seiten-Serie Klasse 10
| # | Titel | Datei | Status |
|---|---|---|---|
| 1 | Quadratische Gleichungen in jeder Form | geogebra_quadratisch_loesen_kl10_ls.html | fertig |
| 2 | Viele Funktionen gleichzeitig | geogebra_viele_funktionen_kl10_ls.html | fertig |
| 3 | Exponentielles Wachstum eingeben | geogebra_exp_wachstum_kl10_ls.html | fertig |
| 4 | Exponentialgleichungen lösen | geogebra_exp_gleichungen_kl10_ls.html | fertig |
| 5 | Winkel: Grad und Bogenmaß | geogebra_winkel_bogenmass_kl10_ls.html | fertig |
| 6 | Die Sinusfunktion mit Schiebereglern | geogebra_sinusfunktion_kl10_ls.html | fertig |

### Klasse 10 – inhaltliche Festlegungen
Grundlage ist der Stoffverteilungsplan Lambacher Schweizer 10 – G9 (UV II Quadratische
Gleichungen, UV IV Exponentielles Wachstum, UV V Trigonometrie, UV VI Trigonometrische
Funktionen). **Ähnlichkeit/Strahlensätze (UV III) und Stochastik (UV I) bleiben außen vor** –
das eine gehört in die Geometrie-App, das andere in den Stochastik-Rechner; beide sind für
diese Reihe ausdrücklich ausgeklammert.

- **Neu in dieser Stufe:** `log(b, x)`, `lg`, `ln`, das Gradzeichen °, `sin`/`cos`/`tan`,
  `Nullstelle(f, Start, Ende)` und `Extremum(f, Start, Ende)` mit Suchbereich.
- **Seite 1** greift die Operator-Regel aus Klasse 9 auf: `Löse` braucht **keine** Normalform,
  aber bei „berechne" gehört die Gleichung als Ansatz ins Heft. Zusätzlich: drei Schreibweisen
  derselben Funktion (Normalform, Scheitelpunktform, faktorisiert) liegen als Graphen exakt
  aufeinander; Anzahl der Lösungen (keine/eine/zwei) an der Lage der Parabel.
- **Seite 2** löst den Roadmap-Punkt „Darstellung vieler Funktionen gleichzeitig" ein und
  schärft ein drittes Mal die Bedienungsregel: **Kreis links = ein-/ausblenden**, **drei Punkte
  rechts = Zeilenmenü** (Farbe, Linienstärke, Schieberegler, Löschen). Schar über einen freien
  Buchstaben; beim Bestätigen bietet GeoGebra selbst an, einen Schieberegler zu erzeugen.
- **Seite 3** übersetzt Prozent in Wachstumsfaktoren, warnt vor der Exponenten-Falle
  (Pfeiltaste nach `1.05^x`) und grenzt mit der **Wertetabelle** ein – bewusst nur auf ganze
  Schritte genau, damit Seite 4 den genauen Wert nachliefert.
- **Seite 4** bringt den Logarithmus als zweiten Weg neben `Löse` und zeigt, dass
  Verdopplungs- und Halbwertszeit **nicht vom Startwert abhängen**.
- **Seiten 5 und 6** trennen sauber: Auf Seite 5 sind Winkel **Zahlen** (mit °), auf Seite 6 ist
  der Winkel die **Variable** (ohne °, im Bogenmaß).

### Gegen das offizielle Handbuch geprüft (nicht aus dem Gedächtnis)
| Angabe | Beleg |
|---|---|
| GeoGebra rechnet intern **in Radiant**; ° ist der Faktor \(\pi/180\) | GeoGebra-Manual „Zahlen und Winkel" |
| Gradzeichen: `Alt`+`O` (Windows/Linux), `Strg`+`O` (Mac), alternativ `deg` | GeoGebra-Manual „Vordefinierte Funktionen und Operatoren" |
| `log(b, x)` = Logarithmus zur Basis b; `lg` = Basis 10; `ln` = Basis e | ebenda |
| `Nullstelle( <Funktion>, <Startwert>, <Endwert> )` für nicht-polynomiale Funktionen (Regula falsi) | GeoGebra-Manual „Nullstelle (Befehl)" |
| `Extremum( <Funktion>, <Startwert>, <Endwert> )` numerisch im offenen Intervall | GeoGebra-Manual „Extremum (Befehl)" |

**Bewusst weggelassen:** die Umkehrfunktionen in Grad (`asind` u. Ä.). Das deutsche Handbuch
schreibt an dieser Stelle etwas anderes als das englische; solange das nicht am Gerät geprüft
ist, läuft der Rückwärtsweg auf Seite 5 stattdessen über `Nullstelle(f, Start, Ende)` mit
`f(x)=sin(x°)-Zielwert` – didaktisch ohnehin der bessere Anschluss an Klasse 8.

## Einstieg EF: Rückblick + Wissenstest (zwei neue Seitentypen)

Für die Kinder, die gerade mit der EF beginnen – prüft die **Bedienung des Grafikrechners
aus Klasse 7 bis 10**, nicht neuen Stoff (Festlegung Andreas).

| Seite | Datei | Typ | Status |
|---|---|---|---|
| Rückblick (Übung, blau, drei Niveaustufen) | geogebra_start_ef_rb.html | Übung | fertig |
| Wissenstest (hellgrau, dunkelblauer Rand, Timer) | geogebra_start_ef_test.html | Test | fertig |

**Karten (beide Seiten parallel aufgebaut):** 1 Eingeben und anzeigen · 2 Besondere Punkte
finden · 3 Gleichungen lösen · 4 Wiederholung (Klammern und Brüche eintippen, Klasse 7) ·
5 Auswertung. Die Wiederholungskarte steht damit als **vorletzte** Karte, wie vorgeschrieben.

**Inhaltliche Abdeckung:** Terme und Hochzahlen eintippen (Pfeiltaste), Dezimalpunkt statt
Komma, Sichtfenster, Funktionen über ihre Namen weiterverwenden (`r(x)=p(x)+q(x)`,
`p(q(2))`), `Nullstelle`, `Schneide`, `Extremum`, `Löse` mit gesuchter Variable,
exponentielles Wachstum als Kl.-10-Thema, Gradmaß-Falle bei `sin(30)` (ohne ° rechnet
GeoGebra im Bogenmaß).

**Neuer Baukasten:** `/tmp/efbau.py` – eine CSS-Vorlage mit austauschbarem Akzent
(`THEMA_UEBUNG` blau, `THEMA_TEST` hellgrau/dunkelblau), gemeinsame Helfer, Timer-CSS,
Chip-Zeile (`kennz()`), Niveaustufen. Bauskripte: `/tmp/ef_rb.py`, `/tmp/ef_test.py`.

**Niveaustufen (nur Übung):** Jede Stufe ist ein eigener `.stufe-block` mit **eigenen**
Feldern, eigenem MC, eigenem Prüfen-/Leeren-Knopf und eigenem Eintrag im `state`. Umschalten
blendet nur um – dadurch bleibt der Stand jeder Stufe automatisch erhalten, ohne Neuaufbau.
Eine Karte gilt als geschafft, sobald **eine** Stufe vollständig richtig war.

**Wissenstest:** `TESTZEIT_MIN` steht als benannte Konstante oben im Skript (aktuell 32).
Countdown startet nur per Tap, ist pausier- und rücksetzbar, bei 0 passiert nichts (nur
Farbwechsel), daneben die aufklappbare Amber-Box mit der Erläuterung. „Antworten speichern"
sperrt eine Karte ohne Rückmeldung (Marker ● = gespeichert, nicht bewertet), „Antworten
ändern" gibt sie bis zur Auswertung wieder frei. „Test auswerten" ist einmalig: markiert
jede Zeile grün/rot, zählt Teilaufgaben und blendet die aufklappbaren **Lösungswege** genau
für die Karten ein, auf denen ein Fehler war.

**Geklärt (Wartung, 25.09.2026):** `typ="Rückblick"` ist in der Lernseiten-Anweisung
(TEIL 3.4/9) ein gültiger Wert und gehört zum Suffix `_rb`. `geogebra_start_ef_rb.html`
trägt noch `typ="Übung"` – `pruefe.py` meldet das als `TYP`-Fehler. Beim nächsten Anfassen
auf `typ="Rückblick"` umstellen (Farbschema bleibt blau).

## Notfall-Anzeige für Formeln (MathJax-Fallback) – in allen Seiten

**Problem (von Andreas gemeldet):** Auf dem Gerät standen Formeln als Rohtext da –
`\(c(3,4)\)` statt der gesetzten Formel. Ursache ist **nicht** die Datei: MathJax kommt
vom CDN (`cdn.jsdelivr.net`). Kommt das Skript nicht an – Schul-WLAN, Vorschau-Ansicht,
Offline-Kopie –, bleiben die TeX-Trennzeichen sichtbar stehen.

**Lösung:** Am Ende jeder Seite steht der Block `MATHJAX-FALLBACK`. 3,5 Sekunden nach dem
Laden prüft er, ob MathJax da ist. Wenn ja, passiert nichts. Wenn nein, werden alle
`\( … \)`-Ausdrücke in lesbares HTML umgeschrieben:

| TeX | Notfall-Anzeige |
|---|---|
| `\sqrt{50}` / `\sqrt{a^2+b^2}` | √50 / √(a²+b²) – Klammer, damit die Wurzel den ganzen Term überspannt |
| `\dfrac{a}{b}` | echtes `.frac`-Konstrukt mit waagerechtem Strich – **nie** ein Schrägstrich |
| `x^2`, `S_g`, `f_{\min}` | `<sup>` / `<sub>` |
| `\cdot \approx \le \ge \neq \pm \ldots \rightarrow \pi \alpha …` | · ≈ ≤ ≥ ≠ ± … → π α … |
| `\left\{ … \right\}`, `3{,}61` | { … }, 3,61 |

Der Block ist idempotent (bei Neuaufbau einer Seite einfach wieder anhängen) und ersetzt
nur Textknoten – Event-Listener an bestehenden Elementen bleiben unangetastet.
Vier EF-Seiten hatten kein `.frac`-CSS; das ist dort ergänzt worden.

**Merkregel für neue Seiten:** Etwas, das man in GeoGebra **eintippt** (`c(3,4)`, `sqrt(20)`,
`Löse(...)`), gehört in `<code>`, nicht in MathJax. MathJax nur für echte Mathematik
(Wurzelzeichen, Brüche, Indizes).

## Nächste Schritte
1. Q1/Q2 weiter ausbauen (bisher nur die beiden Steckbrief-Seiten)
2. Hub-Anbindung aller 37 bisherigen Seiten. **Entscheidung 25.09.2026:** verbindlich ist
   `oberthema="GeoGebra Suite"`. Die 37 fertigen Seiten tragen noch `"GeoGebra Grafikrechner"`
   und werden per Skript umgestellt (nur dieses Meta-Tag, sonst nichts).
3. Alle bisherigen Seiten einmal mit dem aktuellen `pruefe.py` prüfen – neu sind die
   Prüfungen `DOPPELT` (doppelt definierte Funktionen), `TYPESET` und `NOTFALL`. Seiten, die
   mit dem alten `helfer.js` gebaut wurden, haben die doppelten Funktionen eingebettet.

## Für das Wartungs-Projekt
Hier sammeln, was unterwegs an **allgemein gültigen** Regeln oder Fehlern auffällt. Diese
Punkte werden im Wartungs-Projekt in `anweisung_lernseiten.txt` / Fehler-Checkliste /
`pruefe.py` übernommen und dann hier gelöscht.

- *(zurzeit leer – Stand 25.09.2026 übernommen)*
