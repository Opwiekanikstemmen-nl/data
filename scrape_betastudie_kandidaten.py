
import requests
import urllib.request
from bs4 import BeautifulSoup
import json

beta_website = 'https://vinddebetaopdelijst.nl/'
folder = "kandidaten_2021_kiesraad/"

website_partijnamen = ['vvd', 'pvv','cda', 'd66', 'groenlinks', 'sp', 'pvda', 'cu', 'pvdd', '50plus', 'denk', 'sgp', 'fvd', 'ja21', 'volt']
studies_dict = dict.fromkeys(['VVD', 'PVV Partij voor de Vrijheid', 'CDA', 'D66', 'GROENLINKS', 'SP Socialistische Partij', 'Partij van de Arbeid PvdA', 'ChristenUnie', 'Partij voor de Dieren', '50PLUS', 'DENK', 'Staatkundig Gereformeerde Partij SGP', 'Forum voor Democratie', 'JA21', 'Volt'])

for i, partij in enumerate(studies_dict):
    url = beta_website + website_partijnamen[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    scrape = soup.findAll('dd')
    lijstnummers = soup.findAll('dt')

    lijstnummers = [el.get_text() for el in lijstnummers]
    #kandidaat_namen = [el.get_text() for el in scrape[0::3]]
    studies = [el.get_text() for el in scrape[1::3]]

    studies_dict[partij] = dict(zip(lijstnummers, studies))

print(studies_dict)
print("########################################################################")
for partij in studies_dict:
    with open(folder + partij + '.json', 'r') as fp:
        partij_json = json.load(fp)
    for beta_lijstnr in studies_dict[partij]:
        for lijsttrekker in partij_json.values():
            if lijsttrekker['lijstnummer'] == int(beta_lijstnr):
                studies_list = studies_dict[partij].get(beta_lijstnr).rsplit(',', 1)
                lijsttrekker['studie'] = studies_list[0]
                lijsttrekker['onderwijsinstelling'] = studies_list[1].strip()
                break
    #print(partij_json)

    with open(folder + partij + '.json', "w") as outfile:
        json.dump(partij_json, outfile)
