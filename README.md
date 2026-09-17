Hotel Mystery
=============

Projektbeschreibung
-------------------

Hotel Mystery ist eine rundenbasierte Webanwendung. Der Spieler leitet ein Hotel für übernatürliche Gäste.

Die Partie umfasst drei Nächte. In jeder Nacht ordnet der Spieler drei Gästen freie Hotelzimmer zu. Jeder Gast besitzt genau zwei Anforderungen. Die Bewertung hängt davon ab, wie viele Anforderungen das ausgewählte Zimmer erfüllt.

Funktionen
----------

- fünf Gasttypen
- sechs Hotelzimmer
- drei Nachtszenarien
- veränderbare Zimmerzuordnungen
- maximal ein Gast pro Zimmer
- Concierge-Empfehlung einmal pro Nacht
- Hotelbewertung und Chaoswert
- Endauswertung nach der dritten Nacht
- automatische Tests mit Pytest

Technologien
------------

- Python
- Flask
- HTML
- CSS
- Jinja
- Pytest

Projektstruktur
---------------

    hotel_mystery/
    ├── app.py
    ├── game_logic.py
    ├── requirements.txt
    ├── README.md
    ├── static/
    │   └── style.css
    ├── templates/
    │   ├── start.html
    │   ├── game.html
    │   └── result.html
    └── tests/
        └── test_game_logic.py

Installation
------------

Virtuelle Umgebung erstellen:

    python3 -m venv .venv

Virtuelle Umgebung unter macOS aktivieren:

    source .venv/bin/activate

Abhängigkeiten installieren:

    python -m pip install -r requirements.txt

Anwendung starten
-----------------

    python app.py

Danach im Browser öffnen:

    http://127.0.0.1:5000

Tests ausführen
---------------

    python -m pytest -v

Das erwartete Testergebnis lautet:

    7 passed

Punkteberechnung
----------------

- zwei erfüllte Anforderungen: Hotelbewertung +10, Chaos +0
- eine erfüllte Anforderung: Hotelbewertung +5, Chaos +5
- keine erfüllte Anforderung: Hotelbewertung +0, Chaos +10

Die Endpunktzahl berechnet sich wie folgt:

    Endpunktzahl = Hotelbewertung - Chaoswert

Negative Endpunktzahlen setzt die Anwendung auf null.

Ergebniskategorien
------------------

- 0 bis 29 Punkte: kritischer Endzustand
- 30 bis 59 Punkte: stabiler Endzustand
- 60 bis 90 Punkte: erfolgreicher Endzustand

