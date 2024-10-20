#!/usr/bin/

import os
import requests
import pandas as pd

df = pd.read_json(os.path.join("data_raw","martinus_raw.json"))
df = df[df['M_obálka'].notnull()]

kam = "downloads/obalky-martinus"
os.makedirs(kam, exist_ok=True)
stazene = [x.replace('.jpg','') for x in os.listdir(kam)]
df = df[~df['M_isbn'].isin(stazene)]

pocitadlo = 0
for index, row in df.iterrows():
    try:
        soubor = row['M_isbn'] + ".jpg"
        pocitadlo += 1
        print(f'{pocitadlo:5}/{len(df['M_obálka'].drop_duplicates().to_list()):5} ISBN {row['M_isbn']}')
        response = requests.get(row['M_obálka'])
        with open(os.path.join(kam, soubor), "wb") as f:
            f.write(response.content)
    except:
        pass