#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser(
	description="Merge two kiesraad lists")
parser.add_argument("-t", "--target", action="store",
	help="The target JSON")
parser.add_argument("-s", "--source", action="store",
	help="The source JSON")

args = parser.parse_args()

duplicates = 0
firsttimers = 0

if args.target:
	target = args.target
else:
	print("✋ we need a target file")
	exit()

if args.source:
	source = args.source
else:
	print("✋ we need a source file")
	exit()

target_file = open(target, 'r')
source_file = open(source, 'r')

target_data = json.load(target_file)
source_data = json.load(source_file)

for candidate in target_data:
	old_candidate = list(filter(lambda old_candidate: old_candidate['iri'] == candidate['iri'], source_data))
	if len(old_candidate) > 0:
		duplicates += 1
		new_elections = old_candidate[0]['verkiezingen']
		for election in new_elections.keys():
			candidate['verkiezingen'][election] = new_elections[election]
	else:
		firsttimers += 1

print("Duplicates: {}".format(duplicates))
print("First timers: {}".format(firsttimers))

with open('kandidaten.json', 'w', encoding='utf8') as fp:
	json.dump(target_data, fp, ensure_ascii=False, indent=2)
