#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#

import yaml
from pprint import pprint
import json


def loadyaml(filename):
    with open(filename) as _:
        return yaml.safe_load(_)

def loadjson(filename: str) -> dict:
    with open(filename) as _:
        try:
            return json.load(_)
        except json.JSONDecodeError:
            print(f"{filename} is not a valid JSON document, it could not be loaded")
            return None


def main():
    from pprint import pprint

    filename = "data.json"
    d = loadjson(filename)
    if not d:
        print(f"Could not load {filename}, probably not a valid JSON document.")
    else:
        pprint(d)


if __name__ == "__main__":
    main()
