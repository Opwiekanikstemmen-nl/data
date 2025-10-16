#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import csv

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
	source = csv.reader(f, delimiter=',')
	it = iter(source)
	next(it, None)
	for person in it:
		person_found = False
		for kandidaat in kandidaten:
			if kandidaat['verkiezingen']['tk2025']['lijstnummer'] == int(person[2]) and kandidaat['naam'] == person[1]:
				kandidaat['vinddebeta'] = True
				kandidaat['studies'] = [{
					'study': person[3],
					'institute': person[4]
				}]

				try:
					if person[5] and 'partijwebsite' not in kandidaat['urls']:
						kandidaat['urls']['partijwebsite'] = person[5]
				except:
					kandidaat['urls'] = { 'partijwebsite': person[5] }

				try:
					if person[6] and 'LinkedIn' not in kandidaat['urls']:
						kandidaat['urls']['LinkedIn'] = person[6]
				except:
					kandidaat['urls'] = { 'LinkedIn': person[6] }

				person_found = True

		if not person_found:
			print(person[1])

with open('../kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)

