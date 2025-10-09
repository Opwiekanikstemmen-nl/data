#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import csv

parser = argparse.ArgumentParser(
	description="Merge partnerdata into kandidaten")
parser.add_argument("-s", "--source", action="store",
	help="The source CSV")

args = parser.parse_args()

if args.source:
	source = args.source
else:
	print("✋ we need a source file")
	exit()

with open('../kandidaten.json', 'r') as f:
	kandidaten = json.load(f)

with open(source, 'r') as f:
	source = csv.reader(f, delimiter=',')
	it = iter(source)
	for person in it:
		person_found = False
		for kandidaat in kandidaten:
			if kandidaat['verkiezingen']['tk2025']['partij_naam'] == person[0] and kandidaat['verkiezingen']['tk2025']['lijstnummer'] == int(person[1]):
				if kandidaat['geslacht'] == None:
					if person[3] == 'M':
						kandidaat['geslacht'] = 'm'
					elif person[3] == 'V':
						kandidaat['geslacht'] = 'v'
					elif person[3] == 'X':
						kandidaat['geslacht'] = 'x'
					else:
						print(person[3])
					
					if kandidaat['voornaam'] == '':
						kandidaat['voornaam'] = person[1]
					
					try:
						if person[4] and 'partijwebsite' not in kandidaat['urls']:
							kandidaat['urls']['partijwebsite'] = person[4]
					except:
						kandidaat['urls'] = { 'partijwebsite': person[4] }
					try:
						if person[5] and 'LinkedIn' not in kandidaat['urls']:
							kandidaat['urls']['LinkedIn'] = person[5]
					except:
						kandidaat['urls'] = { 'LinkedIn': person[5] }
					try:
						if person[6] and 'Twitter' not in kandidaat['urls']:
							kandidaat['urls']['Twitter'] = person[6]
					except:
						kandidaat['urls'] = { 'Twitter': person[6] }
					try:
						if person[7] and 'Instagram' not in kandidaat['urls']:
							kandidaat['urls']['Instagram'] = person[7]
					except:
						kandidaat['urls'] = { 'Instagram': person[7] }
					try:
						if person[8] and 'Facebook' not in kandidaat['urls']:
							kandidaat['urls']['Facebook'] = person[8]
					except:
						kandidaat['urls'] = { 'Facebook': person[8] }
					try:
						if person[9] and 'BlueSky' not in kandidaat['urls']:
							kandidaat['urls']['BlueSky'] = person[9]
					except:
						kandidaat['urls'] = { 'BlueSky': person[9] }
				person_found = True

		if not person_found:
			print("{0} {1} van {2}".format(person[1], person[2], person[0]))

with open('../kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)

