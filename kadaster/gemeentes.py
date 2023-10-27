#! /usr/bin/env python3
"""
Find the IRIs for the "gemeente" of each "kandidaat" in procesverbaal2023.json

No need to specify arguments: I'm smart! (and will make some informed guesses)
"""
from os import path
import json
from sys import stderr


def procesverbaal2023_json():
    for p in [
        "./procesverbaal2023.json",
        "./kiesraad/procesverbaal2023.json",
        "../kiesraad/procesverbaal2023.json",
    ]:
        if path.exists(p):
            return p
    raise Exception("I'm too stupid to find procesverbaal2023.json.")


def gemeentes_json():
    for p in [
        "./gemeentes.json",
        "./kadaster/gemeentes.json",
        "../kiesraad/gemeentes.json",
    ]:
        if path.exists(p):
            return p
    raise Exception("I'm too stupid to find gemeentes.json.")

def woonplaats_json():
    for p in [
        "./cbs_woonplaats_gemeente.json",
        "./kadaster/cbs_woonplaats_gemeente.json",
    ]:
        if path.exists(p):
            return p
    raise Exception("I'm too stupid to find cbs_woonplaats_gemeente.json.")

def prepare_gemeentes(gemeentes):
    """Load a { name: IRI } structure from a { iri: string, name: string } structure"""

    """{ name: IRI }"""
    curated = {}

    for gemeente in gemeentes:
        curated[gemeente["name"]] = gemeente["iri"]

    return curated


def kandidaat_gemeente(procesverbaal, gemeentes, woonplaatsen):
    for kandidaat in procesverbaal:
        wp = kandidaat["verkiezingen"]["tk2023"]["woonplaats"]  # this name is a lie
        if wp not in gemeentes:
            if wp not in woonplaatsen:
                print(
                    f"{kandidaat['iri']} has unknown gemeente {wp}",
                    file=stderr,
                )
                continue
            if woonplaatsen[wp]['gemeente'] not in gemeentes:
                print(
                    f"{kandidaat['iri']} has unknown woonplaats {wp}",
                    file=stderr,
                )
                continue
            else:
                gemeente = gemeentes[woonplaatsen[wp]['gemeente']]
        else:
            gemeente = gemeentes[wp]
        yield {
            "kandidaat": kandidaat["iri"],
            "gemeente": gemeente,
        }


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.parse_args()

    with open(gemeentes_json()) as fd:
        gemeentes = prepare_gemeentes(json.load(fd))

    with open(woonplaats_json()) as fd:
        woonplaatsen = json.load(fd)

    with open(procesverbaal2023_json()) as fd:
        procesverbaal = json.load(fd)

    print(json.dumps(list(kandidaat_gemeente(procesverbaal, gemeentes, woonplaatsen))))
