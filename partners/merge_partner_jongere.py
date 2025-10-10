#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser(
	description="Merge partnerdata into kandidaten")
parser.add_argument("-s", "--source", action="store",
	help="The source JSON")

args = parser.parse_args()

if args.source:
	source = args.source
else:
	print("✋ we need a source file")
	exit()

with open('../kandidaten.json', 'r') as f:
	kandidaten = json.load(f)

with open(source, 'r') as f:
	source = json.load(f)

for key, party in source['kandidaten'].items():
	for person in party:
		found = False
		for kandidaat in kandidaten:
			if kandidaat['verkiezingen']['tk2025']['partij_naam'] == key and kandidaat['verkiezingen']['tk2025']['lijstnummer'] == int(person['plek']):
				kandidaat['leeftijd'] = person['leeftijd']
				try:
					if person['website'] and 'partijwebsite' not in kandidaat['urls']:
						kandidaat['urls']['partijwebsite'] = person['website']
				except:
					kandidaat['urls'] = { 'partijwebsite': person['website'] }
				try:
					if person['linkedin'] and 'LinkedIn' not in kandidaat['urls']:
						kandidaat['urls']['LinkedIn'] = person['linkedin']
				except:
					kandidaat['urls'] = { 'LinkedIn': person['linkedin'] }
				try:
					if person['instagram'] and 'Instagram' not in kandidaat['urls']:
						kandidaat['urls']['Instagram'] = person['instagram']
				except:
					kandidaat['urls'] = { 'Instagram': person['instagram'] }
				found = True

		if not found:
			print("{0} van {1}".format(person['naam'], key))

with open('../kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)

