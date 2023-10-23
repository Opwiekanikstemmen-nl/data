#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser(
	description="Merge two kiesraad lists")
parser.add_argument("-t", "--target", action="store",
	help="The target JSON")
parser.add_argument("-p", "--parties", action="store",
	help="The party list JSON")
parser.add_argument("-f", "--partyfiles", action="store",
	help="The party list JSON")

args = parser.parse_args()

duplicates = 0
firsttimers = 0

if args.target:
	target = args.target
else:
	print("✋ we need a target file")
	exit()

if args.parties:
	parties = args.parties
else:
	print("✋ we need a parties file")
	exit()

if args.partyfiles:
	partyfiles = args.partyfiles
else:
	print("✋ we need a partyfiles file")
	exit()

target_file = open(target, 'r')
parties_file = open(parties, 'r')

target_data = json.load(target_file)
parties_data = json.load(parties_file)

for party in parties_data:
	if 'deelname_jaren' in party and 2023 in party['deelname_jaren']:
		if 'simpele_naam' in party:
			naam = party['simpele_naam']
		else:
			naam = party['naam']
		party_file = open("{0}/{1}.json".format(partyfiles, naam))
		party_data = json.load(party_file)
		for party_candidate in party_data:
			for candidate in target_data:
				if candidate['verkiezingen']['tk2023']['lijstnummer'] == party_candidate['verkiezingen']['tk2023']['lijstnummer'] \
					and candidate['verkiezingen']['tk2023']['partij_naam'] == party['naam']:
					if candidate['voornaam'] == "" and '.' not in party_candidate['naam'].split(' ', 1)[0]:
						candidate['voornaam'] = party_candidate['naam'].split(' ', 1)[0]
						candidate['naam'] = "{0} {1}".format(party_candidate['naam'].split(' ', 1)[0], candidate['achternaam'])
						print("{0} wordt {1}".format(candidate['naam'], party_candidate['naam'].split(' ', 1)[0]))
					if 'urls' in party_candidate:
						candidate['urls'] = party_candidate['urls']
				

print("Duplicates: {}".format(duplicates))
print("First timers: {}".format(firsttimers))

with open('kandidaten.json', 'w', encoding='utf8') as fp:
	json.dump(target_data, fp, ensure_ascii=False, indent=2)
