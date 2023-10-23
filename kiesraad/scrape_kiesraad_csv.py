#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import argparse
import os
import json
import re
import sys
import urllib



# CSV context

columns = {
	'Kieskring': 0,
	'Lijstnummer': 1,
	'Politieke Groepering': 2,
	'Type': 3,
	'Publiceer geslacht': 4,
	'Taal': 5,
	'Nr.': 6,
	'Tussenvoegsel': 7,
	'Achternaam': 8,
	'Voorletters': 9,
	'Roepnaam': 10,
	'Geslacht': 11,
	'Woonplaats': 12,
	'Land': 13
}

kieskringen = [
	"Groningen", # 1
	"Leeuwarden", # 2
	"Assen", # 3
	"Zwolle", # 4
	"Lelystad", # 5
	"Nijmegen", # 6
	"Arnhem", # 7
	"Utrecht", # 8
	"Amsterdam", # 9
	"Haarlem", # 10
	"Den Helder", # 11
	"'s-Gravenhage", # 12
	"Rotterdam", # 13
	"Dordrecht", # 14
	"Leiden", # 15
	"Middelburg", # 16
	"Tilburg", # 17
	"'s-Hertogenbosch", # 18
	"Maastricht", # 19
	"Bonaire" # 20
]



# Passable variables

parser = argparse.ArgumentParser(
	description="Parse a kiesraad CSV to a JSON file with all listed people")
parser.add_argument("-f", "--file", action="store",
	help="The csv")
parser.add_argument("-e", "--election", action="store",
	help="The slug-like name of these elections of which it is the procesverbaal (e.g. tk2023)")

args = parser.parse_args()

if args.file:
	file = args.file
else:
	print("✋ we need a file")
	exit()

if args.election:
	election = args.election
else:
	print("Please provide an election shorthand with the -e argument")
	sys.exit()



# Tool functions
def safe_filename(filename):
	# Safe name for files
	illegal_chars = ['(', ')', '.', '/', ',']
	for char in illegal_chars:
		filename = filename.replace(char, '')
	return filename



# Fillable variables

partijen = []
partijlijsten = {}
kandidaten = []
geslachten = []
uniques = []

# Status variables

prev_party_number = 0
kieskring_number = 0

print("🏎  start")



print("📁 creating output folder if it doesn’t exist")

output_dir = file[:-4]

if not os.path.exists(output_dir):
	os.mkdir(output_dir)



# Function to save a candidate

def save_candidate(unique, lijstnummer, kieskring, full_name, achternaam, voorletters, voornaam, tussenvoegsel, geslacht, woonplaats, partij):
	# check if person is already in party
	if full_name in partijlijsten[partij]:
		# if so, add kieskring
		partijlijsten[partij][full_name]['verkiezingen'][election]['kieskringen'].append(kieskring)
	else:
		iri = "https://opwiekanikstemmen.nl/id/person/{0}".format(unique.replace(" ", "%20"))
		# - create person object
		person = {
			'iri': iri,
			'id': unique,
			'naam': full_name,
			'voornaam': voornaam,
			'achternaam': achternaam,
			'voorletters': voorletters,
			'tussenvoegsel': tussenvoegsel,
			'geslacht': geslacht,
			'verkiezingen': {
				election: {
					'lijstnummer': lijstnummer,
					'kieskringen': [kieskring],
					'woonplaats': woonplaats,
					'partij_naam': partij
				}
			}
		}

		if unique in uniques:
			if partij not in ["Vrij en Sociaal Nederland", "Blanco (Zeven, A.J.L.B.)"]:
				raise Exception("{0} already exists".format(unique))

		uniques.append(unique)


		# - append person to party object
		partijlijsten[partij][full_name] = person
		kandidaten.append(person)



# Looping through all lines of csv file

csvfile = open(file, 'r')
reader = csv.reader(csvfile, delimiter=';')

i = 0

for row in reader:

	# Ignore the first four rows
	i += 1
	if i < 5:
		continue

	# Update current kieskring
	party_number = int(row[columns['Lijstnummer']])
	if party_number != prev_party_number:
		if party_number < prev_party_number:
			kieskring_number += 1
		prev_party_number = party_number

	partij = row[columns['Politieke Groepering']]
	lijstnummer = int(row[columns['Nr.']])
	kieskring = kieskringen[kieskring_number]
	achternaam = row[columns['Achternaam']]
	voorletters = row[columns['Voorletters']]
	voornaam = row[columns['Roepnaam']]
	tussenvoegsel = row[columns['Tussenvoegsel']]

	if voornaam:
		full_name = "{} {} {}".format(voornaam, tussenvoegsel, achternaam)
	else:
		full_name = "{} {} {}".format(voorletters, tussenvoegsel, achternaam)

	full_name = re.sub("\s\s+" , " ", full_name)

	if row[columns['Publiceer geslacht']] == 'ja':
		geslacht = row[columns['Geslacht']]
	else:
		geslacht = None

	if geslacht not in geslachten:
		geslachten.append(geslacht)

	woonplaats = row[columns['Woonplaats']]
	if row[columns['Land']] != 'NL':
		woonplaats = "{} ({})".format(woonplaats, row[columns['Land']])


	partij = row[columns['Politieke Groepering']]

	if partij not in partijen:
		partijen.append(partij)
		partijlijsten[partij] = {}

	unique = "{0} {1} {2}".format(voornaam, voorletters, achternaam).strip()

	save_candidate(unique, lijstnummer, kieskring, full_name, achternaam, voorletters, voornaam, tussenvoegsel, geslacht, woonplaats, partij)



print("📄 storing people in json files")

partijen_json = {}

for partij in partijen:
	safe_partij = safe_filename(partij)
	filename = '{}.json'.format(safe_partij)

	partijen_json[safe_partij] = {
		'file': filename,
		'procesverbaalnaam': partij
	}

	with open("{}/{}".format(output_dir, filename), 'w', encoding='utf8') as fp:
		json.dump(partijlijsten[partij], fp, ensure_ascii=False, indent=2)

print("📄 storing parties and all candidates in json files")

with open("{}/partijen.json".format(output_dir), 'w', encoding='utf8') as fp:
	json.dump(partijen_json, fp, ensure_ascii=False, indent=2)

output = file.replace("csv", "json")

with open(output, 'w', encoding='utf8') as fp:
	json.dump(kandidaten, fp, ensure_ascii=False, indent=2)


print("🏳️‍🌈  geslachten: {}".format(", ".join(filter(None, geslachten))))
print("🎉 partijen: {}".format(", ".join(partijen)))

print("✅ done")
