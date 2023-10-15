Data - Op wie kan ik stemmen
===

This repository contains data we’re collecting for [Op wie kan ik stemmen?](https://opwiekanikstemmen.nl) and the scripts used to scrape and merge the data. 

The main files are:
- `kandidaten.json`, the complete list of candidates for 2023 based on the procesverbaal, with the 2021 election info added
- `partijen.json`, the complete list of parties of the past three Tweede Kamerverkiezingen

Additionally, there are the following folders:
- `./partijwebsite-lijsten` contains a json with candidate info copied from their party websites (but not yet the info from the individual’s pages, even if the exist)
- `./kiesraad` contains kiesraad files (e.g. a procesverbaal pdf and definitive candidate list csv) and scripts to turn them into json files
