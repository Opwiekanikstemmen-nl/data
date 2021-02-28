#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import argparse



# Passable variables

parser = argparse.ArgumentParser(
    description="Add missing geslachten to candidates")
parser.add_argument("-f", "--folder", action="store",
    help="the folder with the party json files")
parser.add_argument("-s", "--source", action="store",
    help="the csv file with instagram urls")
parser.add_argument("-p", "--onlypartij", action="store",
    help="limits to certain party name")

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

if args.onlypartij:
    onlypartij = args.onlypartij
else:
    print("✋ we need a specific party")
    exit()



kandidaten_file = "{}/kandidaten.json".format(folder)
partijen_file = "{}/partijen.json".format(folder)

with open(partijen_file, 'r', encoding='utf8') as pf:
    partijen = json.load(pf)

# Importeer candidates JSON
with open(kandidaten_file, 'r', encoding='utf8') as fp:
    kandidaten_dict = json.load(fp)

csvfile = open(source, 'r', encoding='utf8')
reader = csv.reader(csvfile, delimiter=';')





for partij in partijen:

    if onlypartij:
        if partij != onlypartij:
            continue

    print("📋 Checking list")

    # Open partij file

    partij_file = "{}/{}".format(folder, partijen[partij]['file'])
    with open(partij_file, 'r') as fp:
        partij_dict = json.load(fp)

    for key, candidate in partij_dict.items():
        print(key)

        csvfile.seek(0)
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:

            try:
                lijstnummer = int(row[0])
            except ValueError:
                continue

            if lijstnummer == candidate['lijstnummer']:
                if row[2] == 'v':
                    partij_dict[key]['geslacht'] = row[2]
                    kandidaten_dict[key]['geslacht'] = row[2]
                else:
                    partij_dict[key]['geslacht'] = 'm'
                    kandidaten_dict[key]['geslacht'] = 'm'
                print(partij_dict[key]['geslacht'])

    with open(partij_file, 'w', encoding='utf8') as outfile:
        json.dump(partij_dict, outfile)

# Opslaan als JSON
with open(kandidaten_file, 'w', encoding='utf8') as outfile:
    json.dump(kandidaten_dict, outfile)

print("✅ Done")
