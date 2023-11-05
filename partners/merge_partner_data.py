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

for person in source:
	for kandidaat in kandidaten:
		if kandidaat['iri'] == person['kandidaat']:
			for k, v in person.items():
				if k == 'kandidaat':
					continue
				if k == 'urls':
					try:
						kandidaat[k].update(v)
					except KeyError:
						kandidaat[k] = v
				else:
					kandidaat[k] = v

with open('../kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)

