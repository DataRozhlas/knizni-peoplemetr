#!/usr/bin/env python

import os

import time

import re

import requests

import datetime

import pandas as pd

slozky = [item.split(".")[0] for item in os.listdir("data_raw/martinus_linky")]

slozky

smazat = pd.read_json(os.path.join("data_raw","smazat.json"))

smazat = smazat['soubor'].to_list()

smazat

def prosekej(x):

    patterns = [

        r'<style.*?</style>',

        r'<script.*?</script>'

    ]

    for pattern in patterns:

        x = re.sub(pattern, '', x, flags=re.DOTALL)

    return x

for s in slozky:

    kam_stahovat = f'downloads/martinus/{s}'

    print(kam_stahovat)

    if not os.path.exists(kam_stahovat):

        os.makedirs(kam_stahovat)

    for filename in smazat:

        file_path = os.path.join(kam_stahovat, filename)

        if os.path.exists(file_path):

            os.remove(file_path)

            print(f"Smazáno: {filename}")

    stazene = os.listdir(kam_stahovat)

    with open(os.path.join("data_raw/martinus_linky",f'{s}.txt')) as linky:

        linky = [l.strip() for l in linky.readlines()]

        for l in linky:

            nazev_souboru = f"""{l.split("/")[-2]}-{l.split("/")[-1]}.html"""

            if nazev_souboru not in stazene:

                print(f"Stahuji {nazev_souboru}")

                try:

                    r = requests.get(l)

                    with open(os.path.join(kam_stahovat, nazev_souboru), 'w+', encoding='utf-8') as f:

                        f.write(f"""{prosekej(r.text)}\n\n<!-- {datetime.datetime.now().replace(microsecond=0)} -->\n<!-- {l} -->""")

                except:

                    print("Nastal problém, počkám 5 minut.")

                    time.sleep(300)

                    r = requests.get(l)

                    with open(os.path.join(kam_stahovat, nazev_souboru), 'w+', encoding='utf-8') as f:

                        f.write(f"""{prosekej(r.text)}\n\n<!-- {datetime.datetime.now().replace(microsecond=0)} -->\n<!-- {l} -->""")

            else:

                print(f"Už staženo {nazev_souboru}")

