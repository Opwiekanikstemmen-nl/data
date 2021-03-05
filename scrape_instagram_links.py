import csv
import json
import pandas as pd
import argparse
import ast

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

# Script loopt over alle rijen in instagram_links bestand, en loopt per rij
# over hele JSON kandidatenlijst totdat een match gevonden is. Eerst wordt gezocht
# op matchende achternaam, vervolgens moet woonplaats of gemeente matchen,
# daarna moet voornaam of voorletters matchen.
def add_insta_links(kandidaten_dict):
    i_list = []
    insta_data_filtered = insta_data.dropna(subset = ["firstname", "lastname", "Instagram", "livingplace"])
    for i, row in insta_data_filtered.iterrows():
        partij = row["party"]
        voornaam = row["firstname"]
        for kandi in kandidaten_dict:
            if row["lastname"] == kandidaten_dict[kandi].get('achternaam'):
                #print("naam: ", voornaam, " ", row["lastname"])
                #print("woonplaats csv: ", row["livingplace"])
                #print("woonplaatsJSON: ",  kandidaten_dict[kandi].get('stad'))
                #print(row["livingplace"])
                if row["livingplace"] in kandidaten_dict[kandi].get('stad') or row["livingplace"] in kandidaten_dict[kandi].get('gemeente'):
                    kandi_voornaam = kandidaten_dict[kandi].get('voornaam')
                    kandi_voorletters = kandidaten_dict[kandi].get('voorletters')
                    if voornaam == kandi_voornaam or ("." in kandi_voorletters and voornaam[0] in kandi_voorletters):
                        kandidaten_dict[kandi].setdefault('links', []).append(row["Instagram"])
                        #insta_data = insta_data.drop(insta_data.index[i])
                        i_list.append(i)
                        break
    return(kandidaten_dict, i_list)



print("🌐 Reading Instagram data")

# Importeer instagram links
insta_data = pd.read_csv("instagram_links.csv")

print("👪 Working on candidates file")

# Importeer kandidaten JSON
with open(kandidaten_file, 'r') as fp:
    kandidaten_dict = json.load(fp)

kandidaten_dict, insta_remove = add_insta_links(kandidaten_dict)


# Opslaan als JSON
with open(kandidaten_file, "w") as outfile:
    json.dump(kandidaten_dict, outfile)

print("👥 Moving on to parties")

# Import party list
# json.load vervangen, dit werkte niet voor de partijen.json
file = open(partijen_file, 'r')
contents = file.read()
partijen = ast.literal_eval(contents)

# Cycle through parties
for partij in partijen:
    print("- working on {}".format(partij))

    partij_file = "{}/{}".format(folder, partijen[partij]['file'])

    # Importeer partij JSON
    with open(partij_file, 'r') as fp:
        kandidaten_dict = json.load(fp)

    kandidaten_dict, _ = add_insta_links(kandidaten_dict)

    # Opslaan als JSON
    with open(partij_file, "w") as outfile:
        json.dump(kandidaten_dict, outfile)

print("🌐 Writing Instagram data")

insta_data = insta_data.drop(insta_data.index[insta_remove])
insta_data.to_csv('instagram_links_test.csv', index=False)

print("✅ Done")
