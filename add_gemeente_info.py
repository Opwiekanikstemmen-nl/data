#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser(
	description="Merge gemeentedata into kandidaten")
parser.add_argument("-t", "--target", action="store",
	help="The target JSON")
parser.add_argument("-c", "--combi", action="store",
	help="The combined municipality info JSON")
parser.add_argument("-g", "--gemeente", action="store",
	help="The candidate x gemeente coupling")

args = parser.parse_args()

if args.target:
	target = args.target
else:
	print("✋ we need a target file")
	exit()

if args.combi:
	combi = args.combi
else:
	print("✋ we need a combi file")
	exit()

if args.gemeente:
	gemeente = args.gemeente
else:
	print("✋ we need a gemeente file")
	exit()

target_file = open(target, 'r')
combi_file = open(combi, 'r')
gemeente_file = open(gemeente, 'r')

target_data = json.load(target_file)
combi_data = json.load(combi_file)
gemeente_data = json.load(gemeente_file)

for coupling in gemeente_data:
	coupled = False
	for candidate in target_data:
		if candidate['iri'] == coupling['kandidaat']:
			coupled = True
			candidate['verkiezingen']['tk2023']['gemeente'] = combi_data[coupling['gemeente']]
			break
	if not coupled:
		print("{0} van {1}".format(candidate['naam'], candidate['verkiezingen']['tk2023']['partij_naam']))

with open(target, 'w', encoding='utf8') as fp:
	json.dump(target_data, fp, ensure_ascii=False, indent=2)
