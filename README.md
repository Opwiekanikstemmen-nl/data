Data - Op wie kan ik stemmen
===

This repository contains data we’re collecting for [Op wie kan ik stemmen?](https://opwiekanikstemmen.nl) and the scripts used to scrape and merge the data. 

The main files are:
- `kandidaten.json`, the complete list of candidates for 2025 based on the procesverbaal, with the 2021 and 2023 election info added
- `partijen.json`, the complete list of parties of the past three Tweede Kamerverkiezingen

Additionally, there are the following folders:
- `./partijwebsite-lijsten` contains a json with candidate info copied from their party websites (but not yet the info from the individual’s pages, even if the exist)
- `./kiesraad` contains kiesraad files (e.g. a procesverbaal pdf and definitive candidate list csv) and scripts to turn them into json files

## Building the list

1. Switch to the kiesraad folder and activate the virtual environment `cd data && . venv/bin/activate`
2. Parse the Kiesraad CSV into our JSON format `python3 scrape_kiesraad_csv.py -f kiesraad2025.csv -e tk2025`
3. Add the previous election lists `python3 merge.py -t kandidaten.json -s definitief2021.json`
4. Copy the `kandidaten.json` to the main folder `cp kandidaten.json ../kandidaten.json`
5. Update the info in `kadaster` with the scripts there
6. Add the kadaster info from the data folder `cd ../ && python3 add_gemeente_info.py -t kandidaten.json -c kadaster/combi_gemeentes.json -g kadaster/kandidaat-gemeente.json`
7. Add party list info `python3 add_partywebsite_data.py -t kandidaten.json -p partijen.json -f partijwebsite-lijsten`

## Adding votes
Using [electiontool](https://github.com/kroncrv/electiontool?tab=readme-ov-file), create a csv-file based on the EML-files.

For example: 
1. Download the [counting files from tk2025](https://www.kiesraad.nl/adviezen-en-publicaties/publicaties/2025/11/07/digitale-tellingsbestanden-gemeentelijk---en-hoofdstembureaus) ('Digitale tellingsbestanden hoofdstembureaus')
2. Unzip the file
3. Clone the electiontool repository `git clone https://github.com/kroncrv/electiontool.git`
4. Install the dependencies (e.g. `pip install dataknead xmltodict dpath` or following their README)
5. Copy the path to the `Kieskring tellingen` folder
6. Run python3 `./electiontool.py -i <path to tellingen> -o <desired filename> --output-structure candidates --add-percentages` (e.g. `python3 ./electiontool.py -i ./tellingen -o tk2025.csv --output-structure candidates --add-percentages`)
7. Copy the output csv to this folder
8. Run `python3 merge_vote_csv.py -s tk2025.csv`