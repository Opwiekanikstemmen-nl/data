#! /usr/bin/env python3
"""
Find the IRIs for the "woonplaats" of each "kandidaat" in procesverbaal2023.json

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


def woonplaatsen_json():
    for p in [
        "./woonplaatsen.json",
        "./kadaster/woonplaatsen.json",
        "../kiesraad/woonplaatsen.json",
    ]:
        if path.exists(p):
            return p
    raise Exception("I'm too stupid to find woonplaatsen.json.")


def prepare_woonplaatsen(woonplaatsen):
    """Load a { name: IRI } structure while deleting duplicate names"""

    """{ name: IRI }"""
    curated = {}

    """{ name }"""
    deleted = set()

    for wp in woonplaatsen:
        if wp["naam"] == "Hengelo":
            wp["naam"] = "Hengelo (O)"
        if wp["naam"] in deleted:
            continue
        if wp["naam"] in curated:
            del curated[wp["naam"]]
            deleted.add(wp["naam"])
        else:
            curated[wp["naam"]] = wp["woonplaats"]
    return curated


def kandidaat_woonplaats(procesverbaal, woonplaatsen):
    for kandidaat in procesverbaal:
        wp = kandidaat["verkiezingen"]["tk2023"]["woonplaats"]
        if wp not in woonplaatsen:
            print(
                f"{kandidaat['iri']} has ambiguous or unknown woonplaats {wp}",
                file=stderr,
            )
            continue
        yield {
            "kandidaat": kandidaat["iri"],
            "woonplaats": woonplaatsen[wp],
        }


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.parse_args()

    with open(woonplaatsen_json()) as fd:
        woonplaatsen = prepare_woonplaatsen(json.load(fd))

    with open(procesverbaal2023_json()) as fd:
        procesverbaal = json.load(fd)

    print(json.dumps(list(kandidaat_woonplaats(procesverbaal, woonplaatsen))))
