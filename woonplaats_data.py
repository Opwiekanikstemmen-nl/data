import requests
import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://www.metatopos.eu/almanak.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
kieskring_data = soup.findAll('tr')

#kieskring_data = kieskring_data[1:10]
result_dict = {}

# Importeer gemeente-kieskring dict
with open('gemeente-kieskring.json') as json_file:
    gemeente_kieskring_dict = json.load(json_file)

for line in kieskring_data:
    [code, woonplaats, _, gemeente, provincie] = line.findAll('td')
    woonplaats = [el.strip() for el in woonplaats.get_text().split('/')]

    #print(code.get_text())
    #if not code.get_text():
    #    print("Geen woonplaatscode!")
    result_dict.update(dict.fromkeys(woonplaats, {'gemeente':gemeente.get_text(), 'kieskring':gemeente_kieskring_dict.get(gemeente.get_text()), 'provincie':provincie.get_text()}))


# Opslaan als JSON
with open("woonplaats_data.json", "w") as outfile:
    json.dump(result_dict, outfile)


print(result_dict.values())
