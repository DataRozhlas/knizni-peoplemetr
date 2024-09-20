#!/usr/bin/python3

import os
import re
import sys
import json
import pandas as pd

kody = [
    "821.162.3-3",
    "821.162.3-1",
    "821.162.3-31",
    "821.162.3-32",
    "885-14-821",
    "885.0-1",
]

def najdi_rok(pole008, c260, c264):
    if " xr" in pole008:
        try:
            vysledek = int(pole008.split(' xr')[0].strip()[-4:])
            return vysledek
        except:
            pass
    retezec = str([c260, c264])
    try:
        vysledek = int(re.search(r'\d{4}',retezec).group())
        return vysledek
    except:
        return None

df = pd.read_json(os.path.join('data_raw','ceska_beletrie_raw.json'))

df['rok'] = df.apply(lambda row: najdi_rok(row['008'], row['260_c'], row['264_c']), axis=1)

df = df[['rok','080_a','020_a','245_a']]
df = df.explode('080_a').explode('020_a').explode('245_a')

df = df[(df['rok'].isin([2024,2025,2026])) & (df['080_a'].isin(kody))]
df = df.groupby('245_a')[['080_a','020_a']].first()

isbns = df['020_a'].drop_duplicates().to_list()

print(f"Počet ISBN před čištěním: {len(isbns)}.")

isbns = list(set([i.replace("-","") for i in isbns if i != None]))
isbns = list(set([i for i in isbns if len(i) == 13]))

print(f"Počet ISBN po čištění: {len(isbns)}.")

with open(os.path.join('data_raw','cnb_sledovat.json'), 'w+', encoding='utf-8') as sledovat:
    sledovat.write(json.dumps(isbns))