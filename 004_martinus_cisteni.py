#!/usr/bin/env python
# coding: utf-8

import os
import json
import pandas as pd

df = pd.read_csv(os.path.join("data_raw", "martinus_raw.csv"))

vyhodit = ["M_naše_katalogové_číslo", "soubor", "M_filmové_zpracování"]
for v in vyhodit:
    if v in df.columns.to_list():
        df = df.drop(columns=[v])

kategorizace = df.explode("M_kategorizace")
kategorizace.groupby("M_kategorizace").size().nlargest(20)

df["M_isbn"] = df["M_isbn"].apply(lambda x: str(x).split(".")[0]).astype(str)

df["M_věkové_doporučení"] = df["M_věkové_doporučení"].apply(
    lambda x: str(x).replace("+", "") if x else None
)

na_int = ["M_počet_stran", "M_rok_vydání", "M_díl", "M_věkové_doporučení"]
for i in na_int:
    df[i] = pd.to_numeric(df[i], errors="coerce", downcast="integer")

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data_raw"):
    os.makedirs("data_raw")

df[df["M_předběžné_datum_vydání"].notnull()].to_json(
    os.path.join("data", "martinus_vyjde.json")
)

smazat = df[df["M_předběžné_datum_vydání"].notnull()]['M_isbn'].drop_duplicates().to_list()
with open(os.path.join("data_raw", "smazat.json"), "w+") as smaz:
    json.dump(smazat, smaz)

df[df["M_rok_vydání"].notnull()].to_json(os.path.join("data", "martinus_vyslo.json"))

puvod = df.explode("M_původ")

puvod[puvod["M_původ"] == "Česko"].drop_duplicates(subset=["M_isbn"]).size

puvod[puvod["M_původ"] == "Česko"]

try:

    with open(os.path.join("data_raw", "nesledovat.json")) as nesledovat:
        nesledovat = json.load(nesledovat)

except:

    nesledovat = []

puvod[
    (~puvod["M_isbn"].isin(nesledovat))
    & (puvod["M_rok_vydání"].isin([2023, 2024, 2025, 2026, 2027]))
    & (puvod["M_vydání"].isnull())
    & (puvod["M_originální_název"].isnull())
    & (puvod["M_překlad"].isnull())
][["M_titul", "M_autorstvo", "M_isbn"]].reset_index().to_json(
    os.path.join("data_raw", "martinus_sledovat.json")
)
