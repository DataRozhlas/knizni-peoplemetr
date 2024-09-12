#!/usr/bin/env python
# coding: utf-8

import os
import json
import pandas as pd

martinus_sledovat = pd.read_json(os.path.join('data_raw','martinus_sledovat.json'), dtype={'M_isbn':str})['M_isbn'].drop_duplicates().to_list()

try:
    with open(os.path.join("data_raw", "rucni_sledovat.json"), "r") as rucni:
        rucni_sledovat = json.load(rucni)
except:
    rucni_sledovat = []

rucni_sledovat = [r.replace("-","") for r in rucni_sledovat]

sledovat = martinus_sledovat + rucni_sledovat

sledovat = [s for s in sledovat if len(s) == 13]

sledovat = list(set(sledovat))

print(f"Ukládám {len(sledovat)} ISBN.")

with open(os.path.join('data_raw','sledovat.json'), 'w+') as json_file:
    json.dump(sledovat, json_file)
