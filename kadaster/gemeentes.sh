curl https://data.labs.kadaster.nl/_api/datasets/cbs/wbk/services/wbk/sparql --data query=PREFIX%20wbk%3A%20%3Chttps%3A%2F%2Fdata.labs.kadaster.nl%2Fcbs%2Fwbk%2Fvocab%2F%3E%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0ASELECT%20%2A%20WHERE%20%7B%0A%20%20%3Firi%20a%20wbk%3AGemeente%20%3B%0A%20%20%20%20%20%20%20rdfs%3Alabel%20%3Fname%20.%0A%7D -X POST > gemeentes.json
echo >> gemeentes.json