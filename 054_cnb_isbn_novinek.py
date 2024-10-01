#!/usr/bin/

import os
import re
import json
import pandas as pd

print("Vybírám ze souboru cnb_vyber.parquet novinky pro sledování na Goodreads a Databázi knih.")

df = pd.read_parquet(os.path.join("data","cnb_vyber.parquet"))

def najdi_rok(nn8):
    try:
        if nn8[6] in 'stdemcur':
            return int(nn8[7:11])
    except (ValueError, IndexError):
        pass  # Handle invalid input gracefully
    return None
        
df['rok'] = df['008'].apply(lambda x: najdi_rok(x))

df = df[df['rok'] >= 2023]

def vydani(o_vydani):
    vsechny_udaje = []
    slova = {'první':1,'prvé':1,'druhé':2,'třetí':3,'čtvrté': 4, 'páté': 5, 'šesté': 6, 'sedmé': 7, 'osmé': 8, 'deváté': 9, 'desáté': 10, 'jedenácté': 11, 'dvanácté': 12, 'třinácté': 13, 'čtrnácté': 14, 'patnácté': 15, 'šestnácté': 16, 'sedmnácté': 17, 'osmnácté': 18, 'devatenácté': 19, 'dvacáté': 20, 'třicáté': 30}
    rimske = {'i.': 1, 'ii.' : 2, 'iii.': 3, 'iv.': 4, 'v.': 5, 'vi.': 6, 'vii.': 7, 'viii.': 8, 'ix.': 9}
    o_vydani = str(o_vydani).lower().replace('IQ 147','').replace('68 Publishers','').replace('65. poli','').split('zákon')[0].split('narozen')[0]
    o_vydani = re.sub(r'\d{1,5}\s{0,2}(obr|výt|let)','',o_vydani)
    cifry = re.findall(r'\d{1,6}',o_vydani)
    if cifry:
        cifry = [int(c) for c in cifry if int(c) < 1000]
        vsechny_udaje += cifry
    for slovo, cislo in slova.items():
        if slovo in o_vydani:
            vsechny_udaje.append(cislo)
    for pismena, cislo in rimske.items():
        if pismena in o_vydani:
            vsechny_udaje.append(cislo)
    if len(vsechny_udaje) > 0:
        return max(vsechny_udaje)
    else:
        return None

df['vydani'] = df['250_a'].apply(lambda x: vydani(x))

df = df[df['vydani'] == 1]

df = df.explode('072_a')
df = df[df['072_a'] == '821.162.3-3']

isbns = df['020_a'].explode().drop_duplicates().to_list()
isbns = [str(i).replace("-","") for i in isbns]
isbns = [i for i in isbns if len(i) == 13]
print(f'Ukázka: {", ".join(isbns[0:5])}')

print(f"Počet ISBN po čištění: {len(isbns)}.")

with open(os.path.join('data_raw','cnb_sledovat.json'), 'w+', encoding='utf-8') as sledovat:
    sledovat.write(json.dumps(isbns))