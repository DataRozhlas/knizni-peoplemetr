#!/usr/bin/

## Najdeme nejméně vyplněné sloupce v náhodném vzorku, abychom pak tyto sloupce mohli vyhodit z datasetu pro dosažení použitelné velikosti.

import os
import warnings
import pandas as pd

## Nechceme to zatapetovat varováními:
warnings.simplefilter(action='ignore', category=FutureWarning) 
warnings.simplefilter(action='ignore', category=UserWarning)

print("Načítám vzorek.")

sample = pd.read_json(os.path.join("data_raw","cnb_sample.json"))
sample = sample.reindex(sorted(sample.columns), axis=1)

print("Počítám vyplněnost sloupců ve vzorku.")

vyplnene = {}
for c in sample.columns.to_list():
    vyplnene[c] = len(sample[~sample[c].isnull()])
vyplnene = pd.Series(vyplnene)

vyplnene.to_json(os.path.join("data_raw","cnb_vyplnenost_sloupcu.json"))

print("Hotovo, soubor cnb_vyplnenost_sloupcu.json uložen.")