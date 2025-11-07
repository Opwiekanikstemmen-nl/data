#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import csv

parser = argparse.ArgumentParser(
    description="Merge vote csv into kandidaten")
parser.add_argument("-s", "--source", action="store",
                    help="The source JSON")

args = parser.parse_args()

if args.source:
    source = args.source
else:
    print("✋ we need a source file")
    exit()

with open('./kandidaten.json', 'r') as f:
    kandidaten = json.load(f)

with open(source, 'r') as f:
    source = csv.reader(f, delimiter=',')
    it = iter(source)
    next(it, None)
    total_counted = 0
    for line in it:
        person_found = False
        if line[2] == 'candidate':
            for kandidaat in kandidaten:
                if kandidaat['verkiezingen']['tk2025']['lijstnummer'] == int(line[4]) and \
                    kandidaat['verkiezingen']['tk2025']['partij_naam'] == line[3]:

                    if 'votes' not in kandidaat:
                        kandidaat['votes'] = int(line[5])
                    else:
                        kandidaat['votes'] += int(line[5])

                    person_found = True

            if not person_found:
                print("{0}: {1}".format(line[3], line[4]))
        elif line[2] == 'total_counted':
            total_counted += int(line[5])
            print("total counted: {0}".format(total_counted))



with open('./kandidaten.json', 'w', encoding='utf8') as f:
    json.dump(kandidaten, f, ensure_ascii=False, indent=2)

