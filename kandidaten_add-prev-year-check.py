#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import json
import argparse



# Passable variables

parser = argparse.ArgumentParser(
    description="Add missing geslachten to candidates")
parser.add_argument("-f", "--folder", action="store",
    help="the folder with the party json files")
parser.add_argument("-p", "--previous", action="store",
    help="the old file")

args = parser.parse_args()

if args.folder:
    folder = args.folder
else:
    folder = "kandidaten_2021_kiesraad"

if args.previous:
    previous = args.previous
else:
    print("✋ we need a file")
    exit()

kandidaten_file = "{}/kandidaten.json".format(folder)
partijen_file = "{}/partijen.json".format(folder)

with open(partijen_file, 'r', encoding='utf8') as pf:
    partijen = json.load(pf)

# Tool functions
def safe_filename(filename):
    # Safe name for files
    illegal_chars = ['(', ')', '.', '/', ',']
    for char in illegal_chars:
        filename = filename.replace(char, '')
    return filename

# Importeer candidates JSON
with open(kandidaten_file, 'r', encoding='utf8') as fp:
    kandidaten_dict = json.load(fp)

def further_comparison(kandidaat, name):
    # Store that it’s their second run
    kandidaat['tweede_poging'] = True
    # Open previous partij file
    safe_partij = safe_filename(kandidaat['partij_naam'])
    prev_file = "{}/{}.json".format(previous, safe_partij)
    # If the party existed
    if os.path.isfile(prev_file):
        with open(prev_file, 'r') as fp:
            prev_partij = json.load(fp)
        # If they switched, save party name
        if name not in prev_partij:
            print("➕ from {} to {}, same {}".format(prev_lijst[name]['partij_naam'], kandidaat['partij_naam'], name))
            kandidaat['vorige_partij'] = prev_lijst[name]['partij_naam']
    # If the party is new and they switched
    else:
        print("➕ new {}, same {}".format(kandidaat['partij_naam'], name))
        kandidaat['vorige_partij'] = prev_lijst[name]['partij_naam']

    # If the candidate moved to another city
    if kandidaat['stad'] != prev_lijst[name]['stad']:
        kandidaat['vorige_woonplaats'] = prev_lijst[name]['stad']
        print("➕ moved to {}, same {}".format(kandidaat['stad'], name))

print("🗄 opening previous year")

if previous:
    prev_kandidaten_file = "{}/kandidaten.json".format(previous)
    with open(prev_kandidaten_file, 'r') as pf:
        prev_lijst = json.load(pf)

for kandidaat in kandidaten_dict.values():

    # - check if they’ve tried before, assume they didn’t
    kandidaat['tweede_poging'] = False
    kandidaat['vorige_partij'] = ""
    kandidaat['vorige_woonplaats'] = ""

    name = "{} {}".format(kandidaat['voornaam'], kandidaat['achternaam'])
    full_name = "{} {} {}".format(kandidaat['voornaam'], kandidaat['tussenvoegsel'], kandidaat['achternaam'])
    alt_name = "{} {}".format(kandidaat['voorletters'], kandidaat['achternaam'])
    alt_full_name = "{} {} {}".format(kandidaat['voorletters'], kandidaat['tussenvoegsel'], kandidaat['achternaam'])
    # If the candidate participated last year
    if alt_full_name in prev_lijst:
        further_comparison(kandidaat, alt_full_name)
    if name in prev_lijst:
        further_comparison(kandidaat, name)
    if full_name in prev_lijst:
        further_comparison(kandidaat, full_name)
    if alt_name in prev_lijst:
        further_comparison(kandidaat, alt_name)



# Opslaan als JSON
with open(kandidaten_file, 'w') as outfile:
    json.dump(kandidaten_dict, outfile, indent=2)
