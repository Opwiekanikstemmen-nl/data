#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fitz
import argparse
import re
import os
import json
import sys
import urllib



# Regexes

voorletters_re = "(?P<voorletters>([A-Z.]+))"
voornaam_re = "\((?P<voornaam>\w{2,})\)"
geslacht_re = "\((?P<geslacht>\w)\)"
hash_re = "(([A-Z1-9]{4})(\s{,1})){16}"



# Passable variables

parser = argparse.ArgumentParser(
	description="Parse a procesverbaal PDF to a JSON file with all listed people")
parser.add_argument("-f", "--file", action="store",
	help="The procesverbaal PDF with just the pages with lists")
parser.add_argument("-e", "--election", action="store",
	help="The slug-like name of these elections of which it is the procesverbaal (e.g. tk2023)")

args = parser.parse_args()

if args.file:
	file = args.file
else:
	file = "procesverbaal_content.pdf"

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

kieskringen = []
partijen = []
partijlijsten = {}
kandidaten = []
geslachten = []
uniques = []

# Status variables

next_is_party = False
next_is_last_name = False
next_is_initials = False
next_is_location = False
partij = None

print("🏎  start")



print("📁 creating output folder if it doesn’t exist")

output_dir = file[:-4]

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

# Create file name for the plain text output
output_txt = "{}.txt".format(file)

# Open text file to store procesverbaal in plain text
procesverbaal_txt = open(output_txt, 'w')

# Open PDF
with fitz.open(file) as doc:
	# Flip through pages
	for page in doc:
		# Extracting text
		text = page.get_text()
		# Store text in plain text file
		procesverbaal_txt.write(text)

# Close and save plain text procesverbaal
procesverbaal_txt.close()

print("💾 the procesverbaal is now plain text")



# Open plain text procesverbaal again for processing
procesverbaal_txt = open(output_txt, 'r')
# Create a list of all the lines in the procesverbaal
lines = procesverbaal_txt.read().splitlines()



# Function to save a candidate

def save_candidate(unique, lijstnummer, kieskring, full_name, achternaam, voorletters, voornaam, geslacht, woonplaats, partij):
	# check if person is already in party
	if full_name in partijlijsten[partij]:
		# if so, add kieskring
		partijlijsten[partij][full_name]['verkiezingen'][election]['kieskringen'].append(kieskring)
	else:
		iri = "https://opwiekanikstemmen.nl/id/{0}".format(unique.replace(" ", "%20"))
		# - create person object
		person = {
			'iri': iri,
			'naam': full_name,
			'voornaam': voornaam,
			'achternaam': achternaam,
			'voorletters': voorletters,
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
			raise Exception("{0} already exists".format(unique))

		uniques.append(unique)

		# - append person to party object
		partijlijsten[partij][full_name] = person
		kandidaten.append(person)


# Looping through all lines of procesverbaal

for line in lines:

	# Remove (trailing) spaces
	line = line.strip()

	if "naam kandidaat" in line:
		# Store it
		if partij not in partijen:
			partijen.append(partij)
			partijlijsten[partij] = {}
		# Make sure not to treat the next line as the party name
		next_is_party = False

		continue


	# If the line contains a lot of underscores, one of these strings or nothing
	if "___" in line or \
	   "pagina" in line or \
	   "voorletters" in line or \
	   "woonplaats" in line or \
	   re.match(hash_re, line) is not None or \
	   "Datum:" in line or \
	   not line:
		# it’s at the page break or table heading and we can ignore it
		continue


	# If, according to the previous line, this should be a party name
	if next_is_party:
		# Memorize it for later use
		if partij is None:
			partij = line
		else:
			partij += " " + line

		continue

	# If, according to the previous line, this should be a last name
	if next_is_last_name:
		# Memorize it for later use
		achternaam = line
		# Make sure to treat the next line as initials and such
		next_is_initials = True
		next_is_last_name = False

		continue

	# If, according to the previous line, this should be initials and such
	if next_is_initials:

		# Try if there’s initials
		voorletter_match = re.search(voorletters_re, line)
		try:
			voorletters = voorletter_match.group('voorletters')
		except AttributeError:
			print("voorletters not found in {}".format(line))

		# Try if there’s a first name
		voornaam_match = re.search(voornaam_re, line)
		try:
			voornaam = voornaam_match.group('voornaam')
		except AttributeError:
			voornaam = ""

		# Try if there’s a sex
		geslacht_match = re.search(geslacht_re, line)
		try:
			geslacht = geslacht_match.group('geslacht')
		except AttributeError:
			geslacht = None

		# Make sure we have list of all sexes to print
		if geslacht not in geslachten:
			geslachten.append(geslacht)

		# Make sure to treat the next line as their location
		next_is_initials = False
		next_is_location = True

		continue

	# If the kieskring is announced
	if "Kieskring" in line:
		# Find just that name
		kieskring_match = re.search("Kieskring (?P<kieskring>[A-Za-z-\'\s]+)", line)
		# Memorize it for later use
		kieskring = kieskring_match.group('kieskring')
		# Store it
		kieskringen.append(kieskring)

		continue

	# If, according to the previous line, this should be their location
	if next_is_location:
		# Memorize
		woonplaats = line
		# Store candidate in party
		if voornaam:
			full_name = "{} {}".format(voornaam, achternaam)
		else:
			full_name = "{} {}".format(voorletters, achternaam)

		unique = "{0} {1} {2}".format(voornaam, voorletters, achternaam).strip()

		save_candidate(unique, lijstnummer, kieskring, full_name, achternaam, voorletters, voornaam, geslacht, woonplaats, partij)

		# Make sure not to treat the next line as the party name
		next_is_location = False

		continue

	# If it’s the one line before a party name
	if re.match("[A-Z][0-9]?$", line) != None:
		# Make sure to treat the next line as the party name
		next_is_party = True
		partij = None

		continue

	# If it’s a lijstnummer
	if line.isdigit():
		# Memorize it for later use
		lijstnummer = int(line)
		# Make sure to treat the next line as a last name
		next_is_last_name = True

		continue

	if partij is not None:
		print("{} is a problematic line in {}".format(line, partij))
	else:
		print("{} is a problematic line".format(line))




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
		json.dump(partijlijsten[partij], fp, ensure_ascii=False)

print("📄 storing parties and all candidates in json files")

with open("{}/partijen.json".format(output_dir), 'w', encoding='utf8') as fp:
	json.dump(partijen_json, fp, ensure_ascii=False)

output = file.replace("pdf", "json")

with open(output, 'w', encoding='utf8') as fp:
	json.dump(kandidaten, fp, ensure_ascii=False)


print("🏳️‍🌈  geslachten: {}".format(", ".join(filter(None, geslachten))))
print("🎉 partijen: {}".format(", ".join(partijen)))
print("⭕️ kieskringen: {}".format(", ".join(kieskringen)))

print("✅ done")
