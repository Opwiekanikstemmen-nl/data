import json

folder = "kandidaten_2021_kiesraad"
kandidaten_file = "{}/kandidaten.json".format(folder)
partijen_file = "{}/partijen.json".format(folder)
with open(partijen_file, 'r') as pf:
    partijen = json.load(pf)

def add_info(kandidaten_dict):
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
    return kandidaten_dict

# Importeer woonplaats_data json
with open('woonplaats_data.json') as json_file:
    woonplaats_data_dict = json.load(json_file)

# Importeer kandidaten json
with open(kandidaten_file, 'r') as fp:
    kandidaten_dict = json.load(fp)

kandidaten_dict = add_info(kandidaten_dict)

# Opslaan als JSON
with open(kandidaten_file, "w") as outfile:
    json.dump(kandidaten_dict, outfile)

for partij in partijen:
    print("- working on {}".format(partij))

    partij_file = "{}/{}".format(folder, partijen[partij]['file'])

    # Importeer partij json
    with open(partij_file, 'r') as fp:
        kandidaten_dict = json.load(fp)

    kandidaten_dict = add_info(kandidaten_dict)

    # Opslaan als JSON
    with open(partij_file, "w") as outfile:
        json.dump(kandidaten_dict, outfile)
