#!/usr/bin/python3

import os

import glob

import json

import re

import pandas as pd

path = 'data_raw/databazeknih/**/*.json'



all_files = glob.glob(path, recursive=True)


def letopocet_pryc(x):
    try:
        return re.sub('.\(\d\d\d\d\)...Databáze knih', "", x)
    except:
        return x

dfs = []


for file in all_files:

    print(f'Processing {file}')

    df = pd.read_json(file)

    if "ISBN" in df.columns:

        df = df.rename(columns={'ISBN':'DK_isbn'})

    df['DK_titul'] = df['DK_titul'].apply(lambda x: letopocet_pryc(x))

    df = df.rename(columns=lambda x: x.replace('_v_', '_').replace('_ve_','_'))

    dfs.append(df)


df = pd.concat(dfs, ignore_index=True)

print(f"Řádků v dataframe: {len(df)}")

print("Odstraňuji řádky bez hodnocení.")

df = df.dropna(subset=['DK_isbn','DK_ratings_count'])

print(f"Řádků v dataframe: {len(df)}")

print("Odstraňuji knihy, které se nemají sledovat.")

with open(os.path.join("data","nesledovat.json")) as nesledovat:

    nesledovat = json.load(nesledovat)

df = df[~df['DK_isbn'].isin(nesledovat)]

print(f"Řádků v dataframe: {len(df)}")

df = df.sort_values(by='DK_date')

df.to_csv(os.path.join("data","databazeknih-hodnoceni.csv"), index=False, encoding="utf-8", header=True)

print("Hotovo.")

