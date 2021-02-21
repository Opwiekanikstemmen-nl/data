# bron: https://www.kiesraad.nl/adviezen-en-publicaties/formulieren/2016/5/kieskringen/kieskringen-en-hoofdstembureaus-tweede-kamerverkiezingen-en-europees-parlementsverkiezingen

import requests
import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://www.kiesraad.nl/adviezen-en-publicaties/formulieren/2016/5/kieskringen/kieskringen-en-hoofdstembureaus-tweede-kamerverkiezingen-en-europees-parlementsverkiezingen'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
kieskring_data = soup.find('tbody').get_text().splitlines()

kieskringen = kieskring_data[4::5]
gemeenten_raw = kieskring_data[3::5]

gemeenten = []

# Alle gemeenten per kieskring in een aparte lijst zetten en wat nutteloze
# tekst aan het begin van iedere lijst verwijderen
for el in gemeenten_raw[:-1]:
    gemeenten.append(el[12:].split(','))

# Voor overzeese gebieden in Nederlandse koninkrijk
gemeenten.append(gemeenten_raw[-1][21:][:-1].split(','))

# alle spaties voor en na gemeentenamen verwijderen
gemeenten_final = [[el.strip() for el in list] for list in gemeenten]

# Dict maken waar kieskringen de key zijn en de gemeenten per kieskring staan
result = dict(zip(kieskringen, gemeenten_final))
print(result)

# Opslaan als JSON
with open("kieskringen-gemeenten.json", "w") as outfile:
    json.dump(result, outfile)
