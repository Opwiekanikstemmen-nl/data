# Met dit script is de Tweede Kamer API gescrapet. Hieronder staan de links die
# je kan invoeren in de "url" variabele om te scrapen.
# Voor meer info: https://opendata.tweedekamer.nl/documentatie/informatiemodel

# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/PersoonContactinformatie?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/PersoonOnderwijs?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/PersoonLoopbaan?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/PersoonNevenfunctie?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/FractieZetelPersoon?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Fractiezetel?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Fractie?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/CommissieZetelVastPersoon?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/CommissieZetelVervangerPersoon?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/CommissieZetel?$skip="
# "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Commissie?$skip="

import urllib, json
import os
from random import randint
from time import sleep

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

data_list = []

entries_n = 250
n = 0
while entries_n >= 250:
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Commissie?$skip=" + str(n);
    print(url)
    with urllib.request.urlopen(url) as response:
        s = response.read()
    data = json.loads(s)["value"]
    entries_n = len(data)
    n = n + 250
    data_list.extend(data)
    sleep(randint(3,10))

data_json = json.dumps(data_list)

with open("commissie.json", "w") as outfile:
    outfile.write(data_json)
    
print("Success!")