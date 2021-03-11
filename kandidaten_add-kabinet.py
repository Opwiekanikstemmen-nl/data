#! python3
'''
Scrapet https://www.rijksoverheid.nl/regering/bewindspersonen
version 1, 11/03/2021
Anna van Harmelen
'''

import json
import sys
import requests
from bs4 import BeautifulSoup

def kabinet(url=None, inputfile=None, outputfile=None):

	if inputfile is not None:
		with open(inputfile, 'r') as kandidaten:
			kandidaten = json.load(kandidaten)
	else:
		kandidaten = json.load(sys.stdin)

	response = requests.get(url)
	response.raise_for_status()

	soup = BeautifulSoup(response.text, features="html.parser")

	for bewindspersoon in soup.find_all("h3"):
		if bewindspersoon.string in kandidaten:
			kandidaten[bewindspersoon.string]['functie_2021'] = 'kabinet'
			kandidaten[bewindspersoon.string]['functieomschrijving_2021'] = bewindspersoon.next_sibling.next_sibling.string.strip()
		else:
			for kandidaat in kandidaten.values():
				if bewindspersoon.string.split()[-1] == kandidaat['achternaam'].split('-')[0] \
				and bewindspersoon.string.split()[0][0:4] == kandidaat['voornaam'][0:4]:
					kandidaten[kandidaat['naam']]['functie_2021'] = 'kabinet'
					kandidaten[kandidaat['naam']]['functieomschrijving_2021'] = bewindspersoon.next_sibling.next_sibling.string.strip()

	if outputfile is not None:
		with open(outputfile, 'w') as jsonfile:
			json.dump(kandidaten, jsonfile, indent=2)
			print(file=jsonfile) # trailing newling
	else:
		json.dump(kandidaten, sys.stdout, indent=2)
		print() # trailing newling


if __name__ == '__main__':
	ARGV_OVERRIDE = None
	ARGV_OVERRIDE = ['-i', 'kandidaten_change_functie.json', '-o', 'kandidaten_add_kabinet.json']

	from argparse import ArgumentParser, FileType
	parser = ArgumentParser(description=__doc__)
	# url, inputfile, outputfile
	KABINET_URL = 'https://www.rijksoverheid.nl/regering/bewindspersonen'
	parser.add_argument('-u', '--url', help="url of the page to scrape, defaults to: " + KABINET_URL, default=KABINET_URL)
	parser.add_argument('-i', '--inputfile', help="file to add new info to, defaults to stdin.", default=None)
	parser.add_argument('-o', '--outputfile', help="file to outputfile to, defaults to stdout.", default=None)

	kabinet(**vars(parser.parse_args(ARGV_OVERRIDE)))	