#!/usr/bin/python3

import os
import glob
import json
import pandas as pd

path = "data_raw/goodreads/**/*.json"

all_files = glob.glob(path, recursive=True)

dfs = []

for file in all_files:

    print(f"Processing {file}")

    df = pd.read_json(file)

    if "ISBN" in df.columns:

        df = df.rename(columns={"ISBN": "GR_isbn"})

    dfs.append(df)


df = pd.concat(dfs, ignore_index=True)

print(f"Řádků v dataframe: {len(df)}")

print("Odstraňuji řádky bez hodnocení.")

df = df.dropna(subset=["GR_isbn", "GR_ratings_count"])

print(f"Řádků v dataframe: {len(df)}")

df = df.sort_values(by="GR_date")

df['den'] = pd.to_datetime(df['GR_date'])
df['hodina'] = df['den'].dt.hour
df['den'] = df['den'].dt.day_name()

df[(df['den'] != 'Monday') | (df['hodina'] > 8)].drop(columns=['den','hodina']).to_csv(
    os.path.join("data", "goodreads-hodnoceni-extra.csv"),
    index=False,
    encoding="utf-8",
    header=True,
)

df = df[
    df["GR_published"].str.contains("2023", na=False)
    | df["GR_published"].str.contains("2024", na=False)
]

try:
    with open(os.path.join('data_raw','rucni_nesledovat.txt'), "r", encoding="utf-8") as file:
        nesledovat = [x.strip() for x in file.read().splitlines()]
        df = df[~df['GR_isbn'].isin(nesledovat)]
except:
    pass

df[(df['den'] == 'Monday') & (df['hodina'] <= 12)].drop(columns=['den','hodina']).to_csv(
    os.path.join("data", "goodreads-hodnoceni.csv"),
    index=False,
    encoding="utf-8",
    header=True,
)

print("Hotovo.")
