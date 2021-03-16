#! python3
'''
version 1 - 5/3/2021
scrapes directly from website
'''

import requests
import sys
from bs4 import BeautifulSoup
import json
import math
from tqdm import tqdm
from datetime import datetime, timedelta

def html_scrape(url, outputfile=None):
	response = requests.get(url)
	response.raise_for_status()

	soup = BeautifulSoup(response.text, features="html.parser")
	members = [
		{
			'name': get_member_name(member),
			'url': get_member_url(member),
			'image': get_member_image(member),
			'age': get_member_age(member),
			'ancienniteit': get_member_ancienniteit(member)
		}
		for member in filter(
			lambda member: not member.find('template'),
			soup.find_all('div', class_='member')
		)
	]
	members = [m for m in members if m['name'] is not None]
	
	for member in tqdm(members):
		response_kandidaat = requests.get(member['url'])
		response_kandidaat.raise_for_status()
		tinysoup = BeautifulSoup(response_kandidaat.text, features="html.parser")
		member['socials'] = get_member_socials(tinysoup)
			
	if outputfile is not None:
		with open(outputfile, 'w') as jsonfile:
			json.dump(members, jsonfile, indent=2)
			print(file=jsonfile) # trailing newling
	else:
		json.dump(members, sys.stdout, indent=2)
		print() # trailing newling


def get_member_socials(tinysoup):
	socials = tinysoup.find('div', class_='list-social')
	poss_socials = ['email', 'twitter', 'facebook', 'instagram', 'web']

	social_dict = {}
	for social in poss_socials:
		social_account = socials.find('a', class_='___'+social)
		if social_account is not None:
			social_dict[social] = (social_account.contents[0], social_account.get('href'))

	return social_dict


def get_member_name(member):
	name = member.find('a', class_='member__name')
	if name is not None:
		name = (map(str.strip, reversed(name.contents[0].split(', '))))
		name = " ".join(name)
		return name


# deze is niet helemaal geoptimaliseerd, want pakt van hetzelfde object als de functie hierboven
def get_member_url(member):
	url = member.find('a', class_='member__name')
	if url is not None:
		url = url.get('href')
		if url is not None:
			return 'https://www.tweedekamer.nl' + url


def get_member_image(member):
	image = member.find('img', class_='member__image')
	if image is not None:
		return image.get('src')


def get_member_age(member):
	age = member.find('table', class_='member__info-table')
	if age is not None:
		age = age.contents[3].contents[3].contents[0]
		age = int(age[0:-5])
		return age


def get_member_ancienniteit(member):
	anc = member.find('table', class_='member__info-table')
	if anc is not None:
		anc = int(anc.contents[5].contents[3].contents[0][0:-6])
		anc = datetime.today() - timedelta(days=anc)
		anc = anc.date().isoformat()
		return anc


if __name__ == '__main__':
	ARGV_OVERRIDE = None
	# ARGV_OVERRIDE = ['-o', 'tweedekamer.json']

	from argparse import ArgumentParser, FileType
	parser = ArgumentParser(description=__doc__)
	TWEEDEKAMER_URL = 'https://www.tweedekamer.nl/kamerleden_en_commissies/alle_kamerleden'
	parser.add_argument('-o', '--outputfile', help="file to output to, defaults to stdout.", default=None)
	parser.add_argument('-u', '--url', help="url of the page to scrape, defaults to: " + TWEEDEKAMER_URL, default=TWEEDEKAMER_URL)

	html_scrape(**vars(parser.parse_args(ARGV_OVERRIDE)))	