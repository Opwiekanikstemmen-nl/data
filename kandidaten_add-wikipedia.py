#! python3
'''
Scrapet wikipedia pagina's voor alle kandidaten
version 1, 10/03/2021
by Anna van Harmelen
'''

import requests
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
from datetime import datetime
import dateparser

def wikipedia(inputfile=None, outputfile=None):
	
	if inputfile is not None:
		with open(inputfile, 'r') as kandidaten:
			kandidaten = json.load(kandidaten)
	else:
		kandidaten = json.load(sys.stdin)

	counter = 0

	for person in tqdm(kandidaten.values()):
		
		# Add wikipedia url
		naam_zonder_spaces = person['naam'].replace(' ', '_')
		url = "https://nl.wikipedia.org/wiki/" + naam_zonder_spaces
		
		# Scrape wikipage for info
		response = requests.get(url)
		if response.status_code == 404:
			# then it doesn't exist, so:
			continue
		
		# Only add url if it actually exists
		person['links']['wikipedia'] = url
		soup = BeautifulSoup(response.text, features='html.parser')
		table = soup.find('table')
		if table is not None:
			info_table = table.get_text()
			info_table = re.sub('\n+', '\n', info_table)
			info_list = info_table.split("\n")
			birthday = get_wiki_age(info_list)
			if birthday is not None:
				counter += 1
				person['geboortedatum'] = get_wiki_age(info_list)
				# If birthday was found, remove age (because having both is redundant)
				person.pop('leeftijd', None)

	if outputfile is not None:
		with open(outputfile, 'w') as jsonfile:
			json.dump(kandidaten, jsonfile, indent=2)
			print(file=jsonfile) # trailing newling
	else:
		json.dump(kandidaten, sys.stdout, indent=2)
		print() # trailing newling

	print(counter, "birthdays successfully found!")

def get_wiki_age(info_list):
	date_present = False

	if 'Geboren' in info_list:
		date_str = info_list[info_list.index('Geboren') + 1]
		date_present = True

	if 'Geboortedatum' in info_list:
		date_str = info_list[info_list.index('Geboortedatum') + 1]
		date_present = True

	if date_present:

		# Necessary because some people add birthplace after birthdate
		if len(date_str) > 17:
			counter = 0
			for i, letter in enumerate(date_str):
				if letter.isnumeric():
					counter += 1
				elif letter.isalpha():
					counter = 0
				if counter >= 4:
					idx = i
					break
			date_str = date_str[0:idx+1]

		# Necessary because some people add birthplace before birthdate
		if ',' in date_str:
			date_list = date_str.split(", ")
			date_str = date_list[-1]

		date = dateparser.parse(date_str).date().isoformat()
		
		return date

if __name__ == '__main__':
	ARGV_OVERRIDE = None
	ARGV_OVERRIDE = ['-i', 'kandidaten.json', '-o', 'kandidaten_nieuw_wikipedia.json']

	from argparse import ArgumentParser, FileType
	parser = ArgumentParser(description=__doc__)
	# inputfile, outputfile
	parser.add_argument('-i', '--inputfile', help="file to add new info to, defaults to stdin.", default=None)
	parser.add_argument('-o', '--outputfile', help="file to outputfile to, defaults to stdout.", default=None)

	wikipedia(**vars(parser.parse_args(ARGV_OVERRIDE)))	