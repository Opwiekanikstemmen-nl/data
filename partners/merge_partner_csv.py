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

vinddebeta_url = "https://vinddebetaopdelijst.nl/{0}?person={1}"

with open(source, 'r') as f:
	source = csv.reader(f, delimiter=',')
	it = iter(source)
	next(it, None)
	for person in it:
		person_found = False
		for kandidaat in kandidaten:
			if kandidaat['verkiezingen']['tk2023']['lijstnummer'] == int(person[2]) and kandidaat['naam'] == person[1]:
				kandidaat['vinddebeta'] = True
				slug_name = person[1].replace(' ', '').lower()
				person_url = vinddebeta_url.format(person[0], slug_name)
				try:
					kandidaat['urls']['Vind de bèta op de lijst'] = person_url
				except KeyError:
					kandidaat['urls'] = {'Vind de bèta op de lijst': person_url}
				person_found = True

		if not person_found:
			print(person[1])

with open('../kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)

