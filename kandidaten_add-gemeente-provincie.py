import json

# Importeer woonplaats_data json
with open('woonplaats_data.json') as json_file:
    woonplaats_data_dict = json.load(json_file)

# Importeer kandidaten json
with open('procesverbaal_2021/kandidaten.json') as json_file:
    kandidaten_dict = json.load(json_file)

for kandi in kandidaten_dict:
    print(kandidaten_dict[kandi])

    # zoeken tussen alle woonplaatsen
    wnplts = woonplaats_data_dict.get(kandidaten_dict[kandi].get('stad'))
    print("Woonplaats;", wnplts)

    # als de woonplaats niet is gevonden, zoeken tussen alle gemeenten
    if wnplts is None:
        values_list = woonplaats_data_dict.values()
        for values in values_list:
            if values.get('gemeente') == kandidaten_dict[kandi].get('stad'):
                wnplts = values
                break
    # indien nog steeds niet gevonden, markeren als 'Overig'
    if wnplts is None:
        wnplts = {'gemeente': 'Overig', 'provincie':'Overig'}

    kandidaten_dict[kandi]['gemeente'] = wnplts['gemeente']
    kandidaten_dict[kandi]['provincie'] = wnplts['provincie']

# Opslaan als JSON
with open("procesverbaal_2021/kandidaten.json", "w") as outfile:
    json.dump(kandidaten_dict, outfile)
