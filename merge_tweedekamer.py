#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import re
import math

with open('kandidaten.json', 'r') as f:
	kandidaten = json.load(f)

with open('tweedekamer_api/combined_json.json', 'r') as f:
	tweedekamer = json.load(f)

not_found = 0
amount_found = 0
today = datetime.date.today()

for no, lid in tweedekamer.items():
	found = False
	for kandidaat in kandidaten:
		if lid['Initialen'] == kandidaat['voorletters'] and lid['Achternaam'] == kandidaat['achternaam']:

			amount_found += 1
			found = True

			# Add leeftijd if it was unknown
			if 'leeftijd' not in kandidaat:
				dob = datetime.date.fromisoformat(lid['Geboortedatum'])
				delta = today - dob
				kandidaat['leeftijd'] = math.floor(delta.days / 365.25)

			# Assign tweedekamer membership & fracties
			fractions = []
			for term in ['Fractie', 'Fractie2', 'Fractie3', 'Fractie4']:
				if lid[term] is not None:
					fraction = lid[term].split('/')
					if fraction[2] == 'None' or fraction[2] == "NaT":
						end = None
					else:
						end = datetime.datetime.fromisoformat(fraction[2]).isoformat()
					fractions.append({
						'partij': fraction[0],
						'start': datetime.datetime.fromisoformat(fraction[1]).isoformat(),
						'end': end
					})
			if lid['Functie'] == 'Tweede Kamerlid':
				kandidaat['tweedekamer'] = {
					'member': True,
					'fractions': fractions
				}
			elif lid['Functie'] == 'Eerste Kamerlid':
				kandidaat['eerstekamer'] = {
					'member': True,
					'fractions': fractions
				}
			elif lid['Functie'] == 'Oud Kamerlid':
				kandidaat['tweedekamer'] = {
					'member': True,
					'fractions': fractions
				}

			# Assign urls
			for term in ['LinkedIn', 'Website', 'Instagram', 'Facebook', 'Twitter']:
				if lid[term]:
					url = lid[term]
					if '://' not in url:
						if term == 'LinkedIn':
							url = "https://{0}.com/in/{1}".format(term.lower(), url)
						elif term in ['Instagram', 'Facebook', 'Twitter']:
							url = "https://{0}.com/{1}".format(term.lower(), url)

					try:
						if term not in kandidaat['urls']:
							kandidaat['urls'][term] = url
					except:
						kandidaat['urls'] = { term: url }

			# Assign X seperately
			try:
				if lid['X'] and 'Twitter' not in kandidaat['urls']:
					kandidaat['urls']['Twitter'] = lid['X']
			except:
				kandidaat['urls'] = { 'Twitter': lid['X'] }

			# Assign studies
			for term in ['Opleiding', 'Opleiding2', 'Opleiding3', 'Opleiding4', 'Opleiding5', \
				'Opleiding6', 'Opleiding7', 'Opleiding8', 'Opleiding9']:
				if lid[term] is not None:
					study_parts = lid[term].split('/')

					if study_parts[1] == "None":
						institution = None
					else:
						institution = study_parts[1]

					if study_parts[2] == "None":
						start = None
					else:
						start = study_parts[2]

					if study_parts[3] == "None":
						end = None
					else:
						end = study_parts[3]

					study = {
						'study': study_parts[0],
						'institution': institution,
						'start': start,
						'end': end
					}
					if 'studies' not in kandidaat:
						kandidaat['studies'] = [study]
					else:
						kandidaat['studies'].append(study)

	if not found:
		not_found += 1

print("Found {0}/not found {1}".format(amount_found, not_found))

with open('kandidaten.json', 'w', encoding='utf8') as f:
	json.dump(kandidaten, f, ensure_ascii=False, indent=2)