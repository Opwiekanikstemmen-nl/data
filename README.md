# Data stemlijsten TK 2017/2021

Deze repository bevat de kandidatenlijsten van de Tweede Kamerverkiezingen van 2017 en 2021 in een aantal formaten en scripts om zelf een procesverbaal om te zetten in JSON.
- de PDF van het procesverbaal van de Kiesraad
- een tekstversie daarvan
- een map per procesverbaal met:
  - JSON-bestanden per partij
  - een JSON-bestand met alle kandidaten
  - een JSON-bestand met alle partijen
  - een JSON-bestand met alle partijen + de IDs in een specifieke GraphQL database (alleen 2021)

## Zelf scrapen

Om zelf de PDF om te zetten in deze bestanden moet je Python 3, `pip` en `virtualenv` geïnstalleerd hebben en:
1. deze repo clonen
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python scrape_procesverbaal.py -f procesverbaal_2021.pdf -p procesverbaal_2017`

De flags met uitleg kun je zien via `python scrape_procesverbaal.py -h`

## Zelf uploaden naar GraphCMS

1. `cp env.sample .env`
2. de twee variabelen invullen in `.env`
3. optioneel: een dryrun doen om te kijken of de queries er goed uit zien: `python store_kandidaten.py -d -u -f procesverbaal_2021`
4. `python store_kandidaten.py -u -f procesverbaal_2021`

De flags met uitleg kun je zien via `python store_kandidaten.py -h`
