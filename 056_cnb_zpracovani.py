#!/usr/bin/

## Skript zpracuje hrubé JSONy ve složce data_raw/cnb na data, která půjde v pandas otevřít na běžném stroji.
## A to dvěma různými způsoby: 1/ vypreparuje jednotlivé sloupce do samostatných souborů, 2/ profiltruje dataset do jednoho souboru.

import os
import json
import warnings
import pandas as pd

filtr = True
rozsekani = False


def vyfiltruj(frame):

    global sloupce_k_zachovani

    ## Osekává jednotlivé hrubé JSONy o méně důležité řádky a sloupce. Vrací dataframe pro následné uložení.

    zmenseni = frame

    print("Zahazuji řádky s vyplněným ISSN.")
    zmenseni = zmenseni.explode("022_a")
    zmenseni = zmenseni[zmenseni["022_a"].isnull()]

    print("Ponechávám jen české materiály publikované na českém území.")
    zmenseni = zmenseni.explode("008")
    zmenseni = zmenseni[
        zmenseni["008"].str.contains("xr", na=False)
        & zmenseni["008"].str.contains("cze", na=False)
    ]

    print("Ponechávám jen texty.")
    zmenseni = zmenseni.explode("007")
    zmenseni = zmenseni[zmenseni["007"].str[0:1] == "t"]

    print("Ponechávám jen texty vázané a brožované publikace.")
    zmenseni = zmenseni[
        zmenseni["020_q"]
        .astype("str")
        .str.lower()
        .str.contains(r"(brož|váz|vaz)", na=False)
    ]

    print("Ponechávám jen texty s rokem vydání 1900+.")
    zmenseni = zmenseni[
        zmenseni["008"].astype(str).str.contains(r"19\d\d", na=False)
        | zmenseni["008"].astype(str).str.contains(r"20\d\d", na=False)
    ]

    print("Zahazuji nepotřebné sloupce.")
    zdejsi_sloupce_k_zachovani = [
        x for x in sloupce_k_zachovani if x in zmenseni.columns.to_list()
    ]
    zdejsi_sloupce_k_zachovani = list(set(zdejsi_sloupce_k_zachovani))
    zmenseni = zmenseni[zdejsi_sloupce_k_zachovani]

    return zmenseni


def rozsekej(frame, cislo):

    ## Rozsekává jednotlivé hrubé JSONy na sloupce začínající stejnou cifrou. Ponechává všechny řádky.

    cisla_komplet = [f"{i:003}" for i in range(2, 1000)]
    cisla_komplet

    for c in cisla_komplet:

        kam_sloupec = f"data/cnb_sloupce/{c}"

        selected_columns = (
            frame.filter(regex=f"001|{c}").explode("001").set_index("001", drop=True)
        )
        selected_columns.columns = selected_columns.columns.astype(str)

        if len(selected_columns.columns) > 0:
            selected_columns = selected_columns.dropna(how="all")
            #        for col in selected_columns.columns.to_list():
            #            if len(selected_columns.explode(col)) == len(selected_columns):
            #                selected_columns = selected_columns.explode(col)
            #                print(f"Exploduji sloupec {col}, počet řádků zůstává stejný.")
            #            else:
            #                print(f"Sloupec {col} nelze explodovat, počet řádků se zvýší {len(selected_columns.explode(col)) / len(selected_columns)}×.")

            if not os.path.exists(kam_sloupec):
                os.makedirs(kam_sloupec)

            selected_columns.to_parquet(
                os.path.join(kam_sloupec, f"{c}_{cislo}.parquet")
            )


## Následuje lineární skript pro zpracování hrubých dat na data použitelnější.

warnings.simplefilter(
    action="ignore", category=FutureWarning
)  ## Nechceme to zatapetovat varováními.
warnings.simplefilter(action="ignore", category=UserWarning)

odkud = "data_raw/cnb"
kam_chunks = "data_raw/cnb_chunks"
kam_sloupce = "data_raw/cnb_sloupce"

if not os.path.exists(kam_chunks):
    os.makedirs(kam_chunks)
if not os.path.exists(kam_sloupce):
    os.makedirs(kam_sloupce)

with open(
    os.path.join("data_raw", "cnb_vsechny_sloupce.json"), "r", encoding="utf-8"
) as soubor_sloupce:
    vsechny_sloupce = json.loads(soubor_sloupce.read())

if filtr == True:

    sloupce_k_zachovani = []
    with open("readme.md", "r", encoding="utf-8") as readme:
        readme = readme.read().split("# Klí")[-1]
        for l in readme.splitlines():
            if (l[0:2] == "- ") and ("*" not in l):
                sloupce_k_zachovani.append(l.split("-")[1].strip())

    print(f"Zachovám {len(sloupce_k_zachovani)} sloupců.")

vsechny_jsony = [f for f in os.listdir(odkud)]

df = pd.DataFrame()

vsechny_jsony = vsechny_jsony

pocitadlo = 0

for index, j in enumerate(vsechny_jsony):

    print(f"Načítám JSON č. {index + 1}")

    df = pd.concat([df, pd.read_json(os.path.join(odkud, j))])

    if ((index + 1) % 8 == 0) or (index == len(vsechny_jsony) - 1):

        pocitadlo += 1

        print(f"Zpracovávám cnb_chunk_{pocitadlo}")

        if filtr == True:

            vyfiltruj(df).to_parquet(
                os.path.join(kam_chunks, f"cnb_chunk_{pocitadlo}.parquet")
            )

            print("Chunk uložen.")

        if rozsekani == True:

            rozsekej(df, pocitadlo)

        df = pd.DataFrame()
