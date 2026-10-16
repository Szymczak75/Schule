# GeoGebra Suite – geprüfte Bedienungsangaben

**Zweck:** Auf diesen Seiten wird Bedienung unterrichtet. Eine falsche Tastenfolge
oder ein erfundener Befehlsname ist deshalb kein Schönheitsfehler, sondern macht die
Seite unbrauchbar – die Kinder sitzen vor dem Gerät und bekommen es nicht hin.

**Regel:** Nur benutzen, was hier steht oder was vorher im offiziellen Handbuch
nachgeschlagen wurde (`geogebra.github.io/docs/manual/de/`). Im Zweifel den Weg
wählen, der sicher stimmt, statt den eleganteren zu raten. Neu geprüfte Angaben
kommen hier dazu, mit Quelle und Datum.

---

## Die Apps der Suite

Die Suite enthält Grafikrechner, 3D-Rechner, Geometrie, CAS und Stochastik.
Umgeschaltet wird über das Menü ☰.

| Aufgabenart | passende App |
|---|---|
| Funktionen, Graphen, Nullstellen, Extrema, Schieberegler | **Grafikrechner** |
| Parameter, die Buchstaben bleiben sollen (Steckbriefaufgaben), Gleichungssysteme mit Unbekannten | **CAS** |
| Konstruktionen mit Zirkel und Lineal, Geodreieck-Themen, Ortslinien | **Geometrie** |
| Körper, Schnitte, Vektoren im Raum | **3D-Rechner** |
| Verteilungen, Zufallsgrößen | **Stochastik** |

---

## Eingabe

| Sache | So geht es | geprüft |
|---|---|---|
| Malzeichen | `*` zwischen Zahl und Variable: `2*x`, nicht `2x` | Praxis |
| Dezimalzahl | **Punkt**, kein Komma. Ein Komma trennt Argumente: `0.5` | Handbuch |
| Hochzahl | `^` tippen, danach **Pfeiltaste nach rechts**, sonst läuft alles weiter im Exponenten | Praxis |
| Bruch | `/` springt in den Nenner und **bleibt dort** – mit der Pfeiltaste nach rechts heraus. Mehrteilige Nenner brauchen eine Klammer: `20/(4+1)` | Praxis |
| Wurzel | `sqrt(...)`, klein geschrieben, ohne Leerzeichen vor der Klammer | Handbuch |
| π | `pi` tippen (wird automatisch zu π) oder die Taste π auf der eingeblendeten Tastatur | Handbuch |
| Gradzeichen ° | iPad: Taste ° auf der GeoGebra-Tastatur. Computer: `Alt`+`O` (Windows/Linux), `Strg`+`O` (Mac); laut Handbuch geht auch `deg` | Handbuch |

---

## Bedienelemente einer Zeile

| Stelle | Wirkung |
|---|---|
| **Kreis links vor der Zeile** | blendet den Graphen nur **ein und aus**; die Funktion bleibt erhalten und kann weiter aufgerufen werden |
| **drei Punkte am rechten Zeilenrand** | Zeilenmenü: Einstellungen (Farbe, Linienstärke), **Schieberegler**, Wertetabelle, Löschen |

Das ist die am häufigsten falsch erklärte Stelle. Der Schieberegler sitzt **nicht**
am Kreis links.

**Schieberegler anlegen:** Steht in einer Zeile ein freier Buchstabe, bietet GeoGebra
beim Bestätigen an, dafür einen Schieberegler zu erzeugen. Kommt kein Angebot, erst
`a=1` in eine eigene Zeile tippen und dann über die drei Punkte den Regler
einschalten. Bereich und Schrittweite stehen im selben Menü.

**Wertetabelle:** drei Punkte am rechten Zeilenrand → „Wertetabelle" → Startwert,
Endwert und Schrittweite eintragen.

---

## Befehle

### Nullstellen und Extrema

| Befehl | Bedeutung | geprüft |
|---|---|---|
| `Nullstelle( <Polynom> )` | alle Nullstellen eines Polynoms als Punkte | Handbuch |
| `Nullstelle( <Funktion>, <Startwert> )` | eine Nullstelle über das Newton-Verfahren | Handbuch |
| `Nullstelle( <Funktion>, <Start>, <Ende> )` | Nullstelle im Intervall, Regula falsi – **nötig bei nicht-polynomialen Funktionen** wie Sinus | Handbuch |
| `Extremum( <Polynomfunktion> )` | alle lokalen Extrema als Punkte | Handbuch |
| `Extremum( <Funktion>, <Start>, <Ende> )` | numerisch im offenen Intervall | Handbuch |
| `Schneide(f, g)` | Schnittpunkte zweier Funktionen | Praxis |
| `Umfang(c)`, `Fläche(c)` | an einem mit dem Kreis-Werkzeug gezeichneten Kreis | Handbuch |

Der Zusatz mit Start und Ende ist kein Schmuck: Eine Sinuskurve hat unendlich viele
Nullstellen, GeoGebra braucht einen Suchbereich.

### Gleichungen

| Befehl | Bedeutung |
|---|---|
| `Löse( <Gleichung> )` | Lösungen als Gleichungen, `{x = 5}` |
| `Löse( <Gleichung>, <Variable> )` | nötig, sobald mehr als ein Buchstabe vorkommt |
| `Lösungen( <Gleichung> )` | nur die Zahlen, `{5}` – weiterverwendbar |
| `Löse( {gl1, gl2}, {a, b} )` | Gleichungssystem; Listen in geschweiften Klammern |

**Wichtiger offener Punkt:** Das Handbuch führt `Löse` als CAS-spezifischen Befehl
(„nur in der CAS-Ansicht verfügbar"). Am Gerät geprüft (Andreas, September 2026):
In der Suite funktioniert `Löse` **auch im Grafikrechner**. Die Handbuchseite ist an
dieser Stelle älter als die App. Bei Zweifeln an einer ähnlichen Angabe genauso
vorgehen: am Gerät nachsehen, Ergebnis hier eintragen.

### Logarithmus

| Eingabe | Bedeutung | geprüft |
|---|---|---|
| `ln(x)` | natürlicher Logarithmus | Handbuch |
| `lg(x)` | Logarithmus zur Basis 10 | Handbuch |
| `log(b, x)` | Logarithmus zur Basis `b` – **Basis zuerst** | Handbuch |

### Ableitung

| Eingabe | Bedeutung | geprüft |
|---|---|---|
| `Ableitung(f)` | erste Ableitung | Handbuch |
| `Ableitung(f, 2)` | zweite Ableitung | Handbuch |
| `f'(x)`, `f''(x)` | Strich-Schreibweise, ausdrücklich als Alternative genannt | Handbuch |

### Winkelfunktionen

| Eingabe | liefert | geprüft |
|---|---|---|
| `sin(x)`, `cos(x)`, `tan(x)` | rechnen im **Bogenmaß** | Handbuch |
| `sin(30°)` | 30 Grad – das Zeichen ° ist für GeoGebra die Zahl π/180 | Handbuch |

GeoGebra führt „sämtliche Berechnungen in Radiant aus"; ° ist eine Konversionshilfe.
Deshalb liefert `sin(30)` etwas ganz anderes als `sin(30°)`.

**Bewusst nicht verwendet:** die Umkehrfunktionen mit Gradausgabe (`asind` und
Verwandte). Das deutsche Handbuch schreibt dort etwas anderes als das englische;
solange das nicht am Gerät geprüft ist, läuft der Rückwärtsweg über
`Nullstelle(f, Start, Ende)` mit `f(x)=sin(x°)-Zielwert`. Das ist didaktisch ohnehin
der bessere Anschluss an Klasse 8.

---

## CAS-Ansicht

| Sache | So geht es | geprüft |
|---|---|---|
| Zuweisung | `:=` – also `f(x):=a*x+b`, `b:=5` | Handbuch |
| Gleichheitszeichen | `=` ist eine **Gleichung**. `a=2` weist nichts zu | Handbuch |
| Ableitung | `f'(x)` funktioniert auch mit Parametern im Term | Handbuch |
| Gleichungssystem | `Löse({f(1)=2, f(7)=8}, {a, b})` | Handbuch |

**Der Unterschied, auf den es ankommt:** Im Grafikrechner wird aus einem freien
Buchstaben sofort ein **Schieberegler**, also eine Zahl. Ein Aufruf wie `f(1)`
liefert dann nur noch einen Zahlenwert und keine Gleichung mehr, in der `a` und `b`
vorkommen. Im CAS bleiben die Buchstaben symbolisch. Alles, was mit Parametern
rechnet – Steckbriefaufgaben, Gleichungssysteme mit Unbekannten – gehört deshalb
ins CAS.

---

## Werkzeugleiste (Grafikrechner)

Gegen ein Handout aus Sachsen-Anhalt abgeglichen:

| Gruppe | enthält unter anderem |
|---|---|
| Einfache Werkzeuge | Bewegen, Schieberegler |
| Punkte | Punkt, Schnittpunkt, Punkt auf Objekt, Extremum, Nullstellen |
| Linien | Gerade, Strecke |
| Konstruieren | Parallele Gerade, Tangenten, Ortslinie |
| Messen | Steigung |
| Kreise | Kreis mit Mittelpunkt und Radius |
| Editieren, Medien | Löschen, Text, Bild |

**Werkzeug-Weg als didaktisches Mittel:** Zu vielen Befehlen gibt es einen Weg über
die Werkzeugleiste, der anschaulicher ist – etwa die Sekante: zwei Punkte auf die
Funktion setzen, dann *Gerade* wählen und beide Punkte antippen. Wo es so einen
schönen Weg gibt, gehört er als eigener Kasten auf die Seite (Baustein `wz(...)`),
mit einem Fazit, wann welcher Weg der bessere ist.

---

## Was in dieser Reihe nicht vorkommt

- **Kein technisches Einbinden von GeoGebra.** Kein `deployggb.js`, keine
  `.ggb`-Datei. Die Seiten erklären die Bedienung; gearbeitet wird in der echten App.
  Abbildungen werden als eigenes SVG nachgebaut.
- Erlaubt sind als externe Quellen nur Google Fonts und MathJax.

---

*Stand: September 2026. Quellen: GeoGebra-Manual (de und en), Handout
Sachsen-Anhalt, Prüfungen am Gerät durch Andreas.*
