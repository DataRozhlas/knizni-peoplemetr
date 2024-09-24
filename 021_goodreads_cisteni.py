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

df

df.tail(60)

print(f"Řádků v dataframe: {len(df)}")


df = df.dropna(subset=["GR_isbn", "GR_ratings_count"])

print("Odstraňuji řádky bez hodnocení.")

print(f"Řádků v dataframe: {len(df)}")

df

df

df = df[
    df["GR_published"].str.contains("2023", na=False)
    | df["GR_published"].str.contains("2024", na=False)
]

df = df.sort_values(by="GR_date")

df.to_csv(
    os.path.join("data", "goodreads-hodnoceni.csv"),
    index=False,
    encoding="utf-8",
    header=True,
)

print("Hotovo.")
