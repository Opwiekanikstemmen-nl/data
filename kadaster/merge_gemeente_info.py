#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

cbs_file = open('cbs_gemeentes.json', 'r')
cbs = json.load(cbs_file)

kadaster_file = open('gemeentes.json', 'r')
kadaster = json.load(kadaster_file)

output = {}

for kad in kadaster:
	found = False
	for gemeente in cbs:
		if gemeente['Naam_2'] == kad['name']:
			kad['stedelijkheid'] = gemeente['Omschrijving_51']
			kad['inwoners'] = gemeente['Inwonertal_52']
			kad['adressendichtheid'] = gemeente['Omgevingsadressendichtheid_53']
			output[kad['iri']] = kad
			found = True
			break
	if not found:
		print("Niet in de CBS-lijst: {0}".format(kad['name']))

with open('combi_gemeentes.json', 'w', encoding='utf8') as fp:
	json.dump(output, fp, ensure_ascii=False, indent=2)
