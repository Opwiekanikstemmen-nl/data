#! python3
"""
version 1 - 7/3/2021
adds data from tweedekamer.nl to kandidaten.json
"""

import json

def add_info(new_info, old_dataset=None, outputfile=None):

	if old_dataset is not None:
		with open(old_dataset, 'r') as kandidaten_large:
			kandidaten_large = json.load(kandidaten_large)
	else:
		kandidaten_large = json.load(sys.stdin)


	with open(new_info, 'r') as kandidaten_klein:
		kandidaten_klein = json.load(kandidaten_klein)

	voorletters_naam = {
		naam_from_kandidaat(kandidaat): naam
		for naam, kandidaat in kandidaten_large.items()
	}

	for oude_kandidaat in kandidaten_large.values():
		oude_kandidaat['kamerlid_2021'] = False
		oude_kandidaat['fotos'] = []
		oude_kandidaat['socials'] = {}

		if len(oude_kandidaat['links']) == 1:
			oude_kandidaat['links'] = {'instagram': oude_kandidaat['links'][0]}
			almost_handle = oude_kandidaat['links']['instagram'].split("/")
			oude_kandidaat['socials']['instagram'] = almost_handle[-1] if almost_handle[-1] else almost_handle[-2]

		elif len(oude_kandidaat['links']) > 1:
			raise Exception("WTF didn't expect more than one existing link!!!!!!!!!")
		else:
			oude_kandidaat['links'] = {}

	for nieuwe_kandidaat in kandidaten_klein:
		naam = nieuwe_kandidaat['name']
		if naam not in voorletters_naam:
			print("Skipping:", naam)
			continue

		oude_kandidaat = kandidaten_large[voorletters_naam[naam]]

		oude_kandidaat['kamerlid_2021'] = True
		
		oude_kandidaat['leeftijd'] = nieuwe_kandidaat['age']
		
		oude_kandidaat['ancienniteit'] = nieuwe_kandidaat['ancienniteit']

		oude_kandidaat['fotos'].append(nieuwe_kandidaat['image'])

		for network, (handle, link) in nieuwe_kandidaat['socials'].items():
			if link[-1] != '/':
				link += '/'
			if network == 'instagram' and oude_kandidaat['links'].get('instagram', link).lower() != link.lower():
				print(f"Wow {oude_kandidaat['naam']} heeft twee insta accounts :O oud: {oude_kandidaat['links']['instagram']}, nieuw: {link}")
				oude_kandidaat['links']['instagram2'] = oude_kandidaat['links']['instagram']
				oude_kandidaat['socials']['instagram2'] = oude_kandidaat['socials']['instagram']
			oude_kandidaat['links'][network] = link
			oude_kandidaat['socials'][network] = handle

		oude_kandidaat['links']['tweedekamer'] = nieuwe_kandidaat['url']

	if outputfile is not None:
		with open(outputfile, 'w') as jsonfile:
			json.dump(kandidaten_large, jsonfile, indent=2)
			print(file=jsonfile) # trailing newling
	else:
		json.dump(kandidaten_large, sys.stdout, indent=2)
		print() # trailing newling


def naam_from_kandidaat(kandidaat):
	return kandidaat['voorletters'] + \
		(' ' + kandidaat['tussenvoegsel'] if kandidaat['tussenvoegsel'] else '') + \
		' ' + kandidaat['achternaam']


if __name__ == '__main__':
	ARGV_OVERRIDE = None
	# ARGV_OVERRIDE = ['tweedekamer.json', '-od', 'kandidaten_original.json', '-o', 'kandidaten_nieuw.json']

	from argparse import ArgumentParser, FileType
	parser = ArgumentParser(description=__doc__)
	# old_dataset, new_info, outputfile
	parser.add_argument('new_info', help="new info to add to old dataset.")
	parser.add_argument('-od', '--old-dataset', help="file to add new info to, defaults to stdin.", default=None)
	parser.add_argument('-o', '--outputfile', help="file to outputfile to, defaults to stdout.", default=None)

	add_info(**vars(parser.parse_args(ARGV_OVERRIDE)))	
