#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

wikidata_api = "https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/{0}"
male = 'Q6581097'
female = 'Q6581072'

with open('kandidaten.json', 'r') as f:
	kandidaten = json.load(f)

dob_count = 0
gender_count = 0
website_count = 0

count = 0

for kandidaat in kandidaten:
	print(count)
	count += 1
	try:
		if kandidaat['urls']['wikidata']:
			qid = kandidaat['urls']['wikidata'].replace("http://www.wikidata.org/entity/", "")
			response = requests.get(wikidata_api.format(qid))
			data = response.json()
			
			try:
				dob = data['statements']['P569'][0]['value']['content']['time']
				kandidaat['geboortedatum'] = dob
				if dob:
					dob_count += 1
			except:
				pass

			try:
				sex_or_gender = data['statements']['P21'][0]['value']['content']
				if kandidaat['geslacht'] == None:
					if sex_or_gender:
						gender_count += 1
					if sex_or_gender == male:
						kandidaat['geslacht'] = "m"
					elif sex_or_gender == female:
						kandidaat['geslacht'] = "v"
			except:
				pass


			try:
				official_website = data['statements']['P856'][0]['value']['content']
				kandidaat['urls']['eigen website'] = official_website
				if official_website:
					website_count += 1
			except:
				pass
	except Exception as e:
		print(kandidaat['id'])
		print(e)


with open('tmp.json', 'w', encoding='utf8') as fp:
	json.dump(kandidaten, fp, ensure_ascii=False, indent=2)

print([dob_count, gender_count, website_count])