#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tabula
import argparse
import re
import json
import time

# Variables

names_re = "(?P<voorletters>([A-Z.]+)) \((?P<voornaam>.+)\) \((?P<geslacht>\w)\)"
backup_names_re = "(?P<voorletters>([A-Z.]+)) \((?P<geslacht>\w)\)"
kieskring_area = (40, 30, 75, 544)
partij_area_kieskring = (90, 30, 110, 544)
partij_area_normal = (70, 30, 76, 544)
personen_area_kieskring = (100, 30, 800, 544)
personen_area_partij = (80, 30, 800, 544)
personen_area_normal = (70, 30, 800, 544)

# Passable variables

parser = argparse.ArgumentParser(
    description="Parse a procesverbaal PDF to a JSON file with all listed people")
parser.add_argument("-f", "--file", action="store",
    help="The procesverbaal PDF with just the pages with lists")
parser.add_argument("-e", "--endpage", action="store",
    help="The last page number X for the parsed page range 1-X")

args = parser.parse_args()

if args.file:
    file = args.file
else:
    file = "procesverbaal_content.pdf"

if args.endpage:
    file_end = int(args.endpage)
else:
    file_end = 681

# Performance showing

start_time = time.time()

# Fillable variables

kieskringen = {}
partijen_pages = {}
partijen = {}
partijlijsten = {}
pagina_lijsten = []
geslachten = []

laatste_kieskring = ''
laatste_partij = ''

print("🏎  start")

# Run through all pages to find the kieskringen
for page_number in range(1, file_end):
    page_kind = 3 # Kieskring
    # Try getting kieskring
    kieskring_tab = tabula.read_pdf(file, pages=page_number, area=kieskring_area, guess=True) # Kieskring
    # See if we have a kieskring
    try:
        kieskring_naam = kieskring_tab[0].columns[0]
    except IndexError:
        page_kind -= 1

    if page_kind == 3:
        # Kieskring page
        laatste_kieskring = kieskring_naam
        kieskringen[page_number] = laatste_kieskring
        party_tab = tabula.read_pdf(file, pages=page_number, area=partij_area_kieskring, guess=True)
        print("Working on {} (on page {}, after {}sec)".format(laatste_kieskring, page_number, int(time.time() - start_time)))
    else:
        # Other page: try getting party
        party_tab = tabula.read_pdf(file, pages=page_number, area=partij_area_normal, guess=True)

    # See if we have a party
    try:
        partij_naam = party_tab[0].columns[1]
        if partij_naam == 'voorletters':
            raise IndexError
    except IndexError:
        page_kind -= 1

    if page_kind == 3:
        laatste_partij = partij_naam
        partijen_pages[page_number] = partij_naam
        # check if party is already in collection; if not, add party
        if laatste_partij not in partijen:
            partijen[laatste_partij] = {}
        personen_tab = tabula.read_pdf(file, pages=page_number, area=personen_area_kieskring, guess=True)
        print("- {} (on page {}, after {}sec)".format(laatste_partij, page_number, int(time.time() - start_time)))
    elif page_kind == 2:
        laatste_partij = partij_naam
        partijen_pages[page_number] = partij_naam
        # check if party is already in collection; if not, add party
        if laatste_partij not in partijen:
            partijen[laatste_partij] = {}
        personen_tab = tabula.read_pdf(file, pages=page_number, area=personen_area_partij, guess=True)
        print("- {} (on page {}, after {}sec)".format(laatste_partij, page_number, int(time.time() - start_time)))
    else:
        personen_tab = tabula.read_pdf(file, pages=page_number, area=personen_area_normal, guess=True)

    pagina_lijsten.append({
        'kieskring': laatste_kieskring,
        'partij': laatste_partij,
        'personen': personen_tab[0]
    })
    # print('Page {} is kind {}'.format(page_number, page_kind))



print("👥 moving to creating people")

# Loop through pages
for lijst in pagina_lijsten:
    kieskring = lijst['kieskring']
    partij = lijst['partij']
    personen = lijst['personen']

    amount = personen.index.stop
    i = 0
    # loop through personen on page
    while i < amount:
        # get array from tabula entry
        persoon_array = personen.values[i]

        name_string = persoon_array[2]
        name_match = re.search(names_re, name_string)

        try:
            full_name = '{} {}'.format(name_match.group('voornaam'), persoon_array[1])
            voorletters = name_match.group('voorletters')
            voornaam = name_match.group('voornaam')
            geslacht = name_match.group('geslacht')
        except AttributeError:
            backup_name_match = re.search(backup_names_re, name_string)

            try:
                full_name = '{} {}'.format(name_match.group('voorletters'), persoon_array[1])
                voorletters = name_match.group('voorletters')
                geslacht = name_match.group('geslacht')
            except AttributeError:
                full_name = '{} {}'.format(persoon_array[2], persoon_array[1])
                voorletters = persoon_array[2]
                voornaam = ""
                geslacht = ""

        if geslacht not in geslachten:
            geslachten.append(geslacht)

        # check if person is already in party
        if full_name in partijen[partij]:
            # if so, add kiesdistrict
            partijen[partij][full_name]['kieskringen'].append(lijst['kieskring'])
        else:
            # if not,
            # - create person object
            person = {
                'lijstnummer': persoon_array[0],
                'kieskringen': [kieskring],
                'naam': full_name,
                'achternaam': persoon_array[1],
                'voorletters': voorletters,
                'voornaam': voornaam,
                'geslacht': geslacht,
                'stad': persoon_array[3],
            }
            # - append person to party object
            partijen[partij][full_name] = person

        i += 1



print("📄 storing people in json files")

partijen_json = {}

for partij in partijen:
    # Safe name for files
    illegal_chars = ['(', ')', '.', '/']
    safe_partij = partij
    for char in illegal_chars:
        safe_partij = safe_partij.replace(char, '')

    filename = '{}.json'.format(safe_partij)

    partijen_json[safe_partij] = {
        'file': filename,
        'procesverbaalnaam': partij
    }

    with open("output/{}".format(filename), 'w') as fp:
        json.dump(partijen[partij], fp)

print("📄 storing parties in json files")

with open("output/partijen.json", 'w') as fp:
    json.dump(partijen_json, fp)

print("🏳️‍🌈  geslachten: {}".format(", ".join(geslachten)))

print("✅ done")
