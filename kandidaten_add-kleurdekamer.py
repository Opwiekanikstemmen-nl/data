#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse



# Passable variables

parser = argparse.ArgumentParser(
    description="Add missing geslachten to candidates")
parser.add_argument("-f", "--folder", action="store",
    help="the folder with the party json files")
parser.add_argument("-s", "--source", action="store",
    help="the json file with kdk urls")

args = parser.parse_args()

if args.folder:
    folder = args.folder
else:
    folder = "kandidaten_2021_kiesraad"

if args.source:
    source = args.source
else:
    print("✋ we need a file")
    exit()



kandidaten_file = "{}/kandidaten.json".format(folder)

# Importeer candidates JSON
with open(kandidaten_file, 'r', encoding='utf8') as fp:
    kandidaten_dict = json.load(fp)

# Importeer kleurdekamer JSON
with open(source, 'r', encoding='utf8') as fp:
    kleur_dict = json.load(fp)



for key, candidate in kandidaten_dict.items():
    kandidaten_dict[key]['kleurdekamer'] = False

    for kleur_key, kleur_candidate in kleur_dict.items():

        if candidate['lijstnummer'] == kleur_candidate['lijstnummer'] and \
            candidate['partij_naam'] == kleur_candidate['partij_naam']:
            print("{}: {}".format(candidate['voornaam'], kleur_candidate['link']))
            kandidaten_dict[key]['kleurdekamer'] = True
            kandidaten_dict[key]['links']['kleurdekamer'] = kleur_candidate['link']

# Opslaan als JSON
with open(kandidaten_file, 'w') as outfile:
    json.dump(kandidaten_dict, outfile, indent=2)

print("✅ Done")
