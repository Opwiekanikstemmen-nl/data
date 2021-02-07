#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
from decouple import config
from slugify import slugify
from graphqlclient import GraphQLClient



# Environment variables

api_token = "Bearer {}".format(config('GRAPH_API'))
client = GraphQLClient(config('GRAPH_URL'))
client.inject_token(api_token)



# Tool functions

# Turn array into a string which is acceptable for GraphQL
def array_to_string(array):
    string = '["'
    for item in array:
        string += item
        string += '", "'
    string = string + '"]'
    # Remove empty items
    string = string.replace(', ""', '')
    string = string.replace('""', '')
    return string



# Passable variables

parser = argparse.ArgumentParser(
    description="Parse JSON and mutate the people into GraphCMS")
parser.add_argument("-f", "--folder", action="store",
    help="the folder with the party json files")
parser.add_argument("-p", "--onlypartij", action="store",
    help="limits to certain party name")
parser.add_argument("-d", "--dryrun", action="store_true",
    help="only does a dry run, so it doesn’t connect to GraphCMSs")
args = parser.parse_args()

if args.folder:
    folder = args.folder
else:
    folder = "output"

if args.onlypartij:
    onlypartij = args.onlypartij
else:
    onlypartij = False

if args.dryrun:
    print("🚧 dry run")



# Query

request = '''
mutation CreatePersoon {{
  __typename
  createPersoon(data: {{
    naam: "{naam}",
    achternaam: "{achternaam}",
    geslacht: "{geslacht}",
    kieskringen: {kieskringen},
    lijstnummer: {lijstnummer},
    slug: "{slug}",
    voornaam: "{voornaam}",
    voorletters: "{voorletters}",
    woonplaats: "{woonplaats}",
    partij: {{connect: {{id: "{partij_id}"}}}}
  }}) {{
    naam
  }}
}}
'''



print("🗄 reading partijen file")

partijen_file = "{}/partijen.json".format(folder)
with open(partijen_file, 'r') as pf:
    partijen = json.load(pf)



# Loop through all parties

for partij in partijen:
    print("- working on {}".format(partij))

    if onlypartij:
        if partij != onlypartij:
            print('skip')
            continue

    partij_id = partijen[partij]['id']
    partij_file = "{}/{}".format(folder, partijen[partij]['file'])

    with open(partij_file, 'r') as fp:
        people = json.load(fp)

    for key in people:

        person = people[key]

        slug = slugify(key)

        if '(' in person['naam']:
            print("{} van {}".format(person['naam'], partij))

        filled_request = request.format(
            naam = person['naam'],
            achternaam = person['achternaam'],
            geslacht = person['geslacht'],
            kieskringen = array_to_string(person['kieskringen']),
            lijstnummer = person['lijstnummer'],
            slug = slug,
            voornaam = person['voornaam'],
            voorletters = person['voorletters'],
            woonplaats = person['stad'],
            partij_id = partij_id
        )

        if args.dryrun:

            if person['lijstnummer'] == 1:
                print(filled_request)
                # client.execute(filled_request)
                laatste_partij = partij

        else:
            try:
                client.execute(filled_request)
            except:
                print("⚠️ ignored")
                print(filled_request)



print("✅ done")
