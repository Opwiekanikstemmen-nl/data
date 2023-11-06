# -*- coding: utf-8 -*-
# Dit script filtert alle oud-kamerleden eruit die een sterfdatum hebben, 
# en alle lege entries in de JSON.

import json
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

f = open('personen.json')
personen_json = json.load(f)

personen_filtered = []

n = 0
for person in personen_json:
    if person["Achternaam"] and person["Overlijdensdatum"] is None:
        personen_filtered.append(personen_json[n])
    n = n + 1

with open("personen_filtered.json", "w") as outfile:
    outfile.write(json.dumps(personen_filtered))