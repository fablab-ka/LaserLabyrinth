
## Allgemein

### Spielfiguren
Sind sechseckig, d.h. es gibt sechs Möglichkeiten, um die Figuren zu positionieren.
1. Laserstrahler (sendet Laser)
2. Laserziel (empfängt Laser)
3. Einfacher Spiegel (lenkt den Strahl um)
4. Halbdurchlässiger Spiegel als Strahlteiler (Strahl wird aufgeteilt)
5. Platzhalter (blokiert ein Spielfeld, der Laser kann darüber)
6. Richtungsblocker (nur 2 bzw. 4 der 6 Richtungen möglich)



## Vorbereitung

### Bauteile mit dem Lasercutter auschneiden

#### Das Spielfeld

Das Spielfeld ([SVG-Datei](hg_a))besteht aus 3 Schichten:
![Alle Schichten](pngs/hg_all.png){width=14cm}


Zusätzlich gibt es eine Umrandung ([SVG-Datei](hf_f)) und eine Batteriebox ([SVG-Datei](hf_bb)).


#### Die Spielfiguren

Die secheckigen Spielfiguren haben eine Boden, Deckel und sechs Seitenwände. Je nach Figur unterschieden sich die Böden/Deckel/Seiten in der Anzahl und Größe der Löcher.

Es gibt 9 verschiedene Arten von Boden-/Deckplatten:

1. Normale Platte
2. Bodenplatten mit Aussparung für Stromabnehmer
3. Deckplatten mit Aussparung für einen Button
4. Deckplatten mit Aussparung für LED oder Summer (TODO?)
5. Platte mit Spiegelschlitz (0°)
6. Platte mit Spiegelschlitz (30°)
7. Bodenplatten mit Schlitz für einen halbdurchlässigen Spiegel (0°)
8. Bodenplatten mit Schlitz für einen halbdurchlässigen Spiegel (30°)
9. Bodenplatte für einen Feldblocker

![verschiedene Platten](pngs/hf_plates.png){width=14cm}

Es gibt 4 verschiedene Arten von Seitenwänden:

1. Hohe Seiten
2. Hohe Seiten mit Loch für den Laserstrahl
3. Tiefe Seiten
4. Tiefe Seiten mit Loch für den Laserstrahl

![verschiedene Seiten](pngs/hf_sides.png){width=14cm}


###### Figuren

1. Laserstrahler ([SVG-Datei](hf_s))
2. Laserziel ([SVG-Datei](hf_t))
3. Einfacher Spiegel ([SVG-Datei](hf_m))
4. Strahlteiler ([SVG-Datei](hf_dm))
5. Feldblocker ([SVG-Datei](hf_b))
6. Richtungsblocker 2 Richtungen ([SVG-Datei](hf_rb2))
7. Richtungsblocker 4 Richtungen ([SVG-Datei](hf_rb4))


#### Kombinierte SVG-Datei aller Teile

[TODO][SVG_ALL] findet sich eine SVG-Vorlage für das gesamte Spielfeld samt Figuren.
Damit die Spielfiguren möglichst passgenau sind, werden die Ausschnitte aus dem Spielfeld für die Boden-/Deckplatten verwendet.




### PCB erstellen/fertigen lassen

Die Start- und Zielblöcke beinhalten eine einfache Schaltung,
um den Laserstrahl zu erzeugen/detektieren.

#### Startblock

Die Eagle-Design Dateien sind [hier][eagleS] zu finden.

Bauteilliste:
- ...

#### Zielblock

Die Eagle-Design Dateien sind [hier][eagleS] zu finden.

Bauteilliste:
- ...





## Workshop

## Materialien

### Holzteile mit dem Lasercutter erstellt

| Teil                             | Anzahl |
|:---------------------------------|:-------|
| Spielfeld Schichten 1 + 2 +3     | je 1   |
| Spielfeld Umrandung              | 6      |
| Spielfeld Batteriebox (6 teilig) | 1      |
| Figur-Platte Normal              | 2      |
| Figur-Platte Button-Aussparung   | 2      |
| Figur-Platte LED-Aussparung      | 2      |
| Figur-Platte Stromversorgung     | 4      |
| Figur-Platte Spiegel 0°          | 4      |
| Figur-Platte Spiegel 30°         | 4      |
| Figur-Platte Strahlteiler 0°     | 1      |
| Figur-Platte Strahlteiler 30°    | 1      |
| Figur-Platte Feldblocker         | 4      |
| Figur-Seite hoch                 | ?      |
| Figur-Seite hoch mit Loch        | ?      |
| Figur-Seite klein                | ?      |
| Figur-Seite klein mit Loch       | ?      |
| Feldblocker Platte 1 + 2         | je 8   |
| Feldblocker Verbindungsstift     | 4      |

### Elektronik

| Teil              | Anzahl |
|:------------------|:-------|
| PCB Laserstrahler | 2      |
| PCB Laserziel     | 2      |
| Bauteile ...      | ?      |

### Sonstiges

| Teil                               | Anzahl |
|:-----------------------------------|:-------|
| Spiegel 7cm x 7cm                  | 2      |
| Spiegel halbdurchlässig 3cm x 4 cm | 2      |
| Kabel rot/schwarz                  |        |
| Unterlegscheibe ø 1.5cm-2.5cm      | 4      |
| Batteriefederkontakt               | 4 + 2  |

### Werkzeug
- Tischkreisäge o. ä. zum schneiden der Spiegel
- Heißklebepistole
- Lötkolben und Lötzinn
- Seitenschneider, ggf. Abisolierzange
- Gummihammer (optional)
- AVR-Programmier Adapter alternativ via Raspberry Pi

## Ablauf

### Spielfeld aufbauen
- die unterste Schicht mit Kupferfolie überziehen, so dass die Löcher aus der mittleren Schicht bedeckt sind
- die mittlere Schicht mit Kupferfolie überziehen, die mittleren Löcher freilassen
- die drei Spielfeldschichten aufeinander legen und die Umrandung einsetzen
- die Batteriebox zusammenstecken, Batterien einsetzen, auf dem Spielfeld befestigen
- TODO: testen, ausarbeiten


### Spiegel/Strahlteiler zusammenbauen

#### Aluminiumspiegel vorbeiten
- aus dem 7cm x 7cm Aluspiegel  vier 2cm x 4cm Streifen auschneiden
- Kanten entgraten
- Schutzfolie abziehen

#### Spiegel einsetzen
- spiegel in korrekte platten einsetzen
- spiegel mit heißkleber in den platten verkleben
- seiten in die platten einsetzen, Seiten mit Löcher korrekt positionieren!

### Richtungsblocker zusammenbauen
- Seiten mit Löcher an den korrekten Stellen einsetzen
- 2-Wege Blocker mit 2 Löchern, 4-Wege Blocker mit 4 Löchern

### Feldblocker zusammenbauen
- Die Platten übereinander legen, (1 Bodenplatte jeweils 2 mittlere und obere Platten) und mit dem Verbindungsstift fixieren

### Laserstrahler/Laserziel

#### Stromabnehmer vorbeiten
- Kupferfolie/Unterlegscheibe? (TODO) an die Bodenplatte kleben?
- Kontaktstift in der Mitte befestigen (TODO)

#### Laserstrahler zusammenbauen
- Laserdiode im Seitenwandloch mit Heißkleber fixieren
- PCB an der "hinten" gelegenen Seitenwand mit Heißkleber befestigen
- Button im Deckel einsetzen und festkleben
- Vorbeiteten Stromabnehmerboden mit Deckel und Seitenwänden zusammenbauen
- TODO?

#### Laserziel zusammenbauen


[1]: https://raw.githubusercontent.com/fablab-ka/lasermaze/master/svg/hex_grid_layer0.svg

[hf_s]: aa
[3]: aa
[bb_svg]: aa
[SVG_ALL]: https://raw.githubusercontent.com/fablab-ka/lasermaze/master/
[eagleS]: https://raw.githubusercontent.com/fablab-ka/lasermaze/master/eagle/XY
[eagleE]:https://raw.githubusercontent.com/fablab-ka/lasermaze/master/eagle/XY
