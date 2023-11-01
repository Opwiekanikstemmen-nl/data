import json

provincies = {
    'Groningen': [],
    'Fryslân': [],
    'Drenthe': [],
    'Overijssel': [],
    'Flevoland': [],
    'Gelderland': [],
    'Utrecht': [],
    'Noord-Holland': [],
    'Zuid-Holland': [],
    'Zeeland': [],
    'Noord-Brabant': [],
    'Limburg': [],
    'Overig': []
}

with open('../kadaster/cbs_gemeentes.json') as fs:
    cbs = json.load(fs)
with open('../kandidaten.json') as fs:
    kandidaten = json.load(fs)
with open('../kadaster/cbs_woonplaats_gemeente.json') as fs:
    woonplaatsen = json.load(fs)

used_woonplaatsen = []

for kandidaat in kandidaten:
    woonplaats = kandidaat['verkiezingen']['tk2023']['woonplaats']
    if woonplaats not in used_woonplaatsen:
        used_woonplaatsen.append(woonplaats)

def append_to_province(woonplaats, key):
    found = False
    for option in cbs:
        if option['Naam_2'] == key:
            try:
                provincies[option['Naam_27']].append(woonplaats)
                found = True
            except KeyError:
                print("{0}/{1} has no province or something; {2}".format(woonplaats, key, option['Naam_27']))
    return found

for woonplaats in used_woonplaatsen:
    if not append_to_province(woonplaats, woonplaats):
        try:
            new_try = woonplaatsen[woonplaats]['gemeente']
            append_to_province(woonplaats, new_try)
        except KeyError:
            provincies['Overig'].append(woonplaats)

with open('provincies.json', 'w', encoding='utf8') as fp:
	json.dump(provincies, fp, ensure_ascii=False, indent=2)
