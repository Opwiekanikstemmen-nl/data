import csv
import json
import pandas as pd
import argparse


# Passable variables
parser = argparse.ArgumentParser(
    description="Add Instagram links to candidates")
parser.add_argument("-f", "--folder", action="store",
    help="the folder with the candidate json files")

args = parser.parse_args()

if args.folder:
    folder = args.folder
else:
    folder = "kandidaten_2021_kiesraad"

kandidaten_file = "{}/kandidaten.json".format(folder)
partijen_file = "{}/partijen.json".format(folder)

# Importeer gemeente-kieskring dict
with open(kandidaten_file) as json_file:
    kandidaten_dict = json.load(json_file)

# Importeer instagram links
insta_data = pd.read_csv("instagram_links.csv")

insta_data = insta_data.dropna(subset = ["firstname", "lastname", "Instagram", "livingplace"])

# Script loopt over alle rijen in instagram_links bestand, en loopt per rij
# over hele JSON kandidatenlijst totdat een match gevonden is. Eerst wordt gezocht
# op matchende achternaam, vervolgens moet woonplaats of gemeente matchen,
# daarna moet voornaam of voorletters matchen.
for i, row in insta_data.iterrows():
    partij = row["party"]
    voornaam = row["firstname"]
    for kandi in kandidaten_dict:
        if row["lastname"] == kandidaten_dict[kandi].get('achternaam'):
            #print("naam: ", voornaam, " ", row["lastname"])
            #print("woonplaats csv: ", row["livingplace"])
            #print("woonplaatsJSON: ",  kandidaten_dict[kandi].get('stad'))
            if row["livingplace"] in kandidaten_dict[kandi].get('stad') or row["livingplace"] in kandidaten_dict[kandi].get('gemeente'):
                kandi_voornaam = kandidaten_dict[kandi].get('voornaam')
                kandi_voorletters = kandidaten_dict[kandi].get('voorletters')
                if voornaam == kandi_voornaam or ("." in kandi_voorletters and voornaam[0] in kandi_voorletters):
                    kandidaten_dict[kandi].setdefault('links', []).append(row["Instagram"])
                    break

# Opslaan als JSON
with open(kandidaten_file, "w") as outfile:
    json.dump(kandidaten_dict, outfile)
