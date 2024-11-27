#!/usr/bin/

## Skript zpracuje hrubé JSONy ve složce data_raw/cnb na data, která půjde v pandas otevřít na běžném stroji.
## A to dvěma různými způsoby: 1/ vypreparuje jednotlivé sloupce do samostatných souborů, 2/ profiltruje dataset do jednoho souboru.

import os
import json
import warnings
import pandas as pd

# Zde lze nastavit, co všechno se má zpracovat.

filtr = True # uložit menší vyfiltrovanou verzi cnb.xml?
rozsekani = True # uložit kompletní původní sloupce z cnb.xml?
autority = True # uložit data o autoritách?

#####################
## NEJDŘÍVE FUNKCE ##
#####################

def vyfiltruj(frame):

    global sloupce_k_zachovani

    ## Osekává jednotlivé hrubé JSONy o méně důležité řádky a sloupce. Vrací dataframe pro následné uložení.

    zmenseni = frame

    print("Vyřazuji mapy, hudebniny apod.")
    zmenseni = zmenseni[zmenseni["leader"].str[6].isin(["a", "t"])]
    ## tčko jsou rukopisy ve smyslu disertačních a diplomových prací, ALE TAKY SAMIZDATY, ALE NEJSOU V RÁMCI NÁRODNÍ BIBLIOGRAFIE
    ## SAMIZDATY JSOU V NKC!
    ## a hlavně libri prohibiti
    ## 30-60. leta a starší můžou být i mapy v monografiích

    print("Vyřazuji ryze periodické materiály.")
    zmenseni = zmenseni[~zmenseni["leader"].str[7].isin(["b", "i", "s", " "])]
    # zmenseni = zmenseni.explode("022_a")
    zmenseni = zmenseni[zmenseni["022_a"].isnull()]
    zmenseni = zmenseni.explode("008")
    zmenseni = zmenseni.explode("007")

    print("Ponechávám jen české materiály publikované na českém území.")

    zmenseni = zmenseni[
        (zmenseni["008"].str[15:17] == "xr") & (zmenseni["008"].str[35:38] == "cze")
    ]
    
    # může se stát, že někdy nám zůstalo v koedici ČR/zahraničí (ČR/Poláci např.)
    # alternativně vyplněné pole 044 a jestli v některém z výskytů je xr, to možná přihodit
    # to samé se týká jazyka, v 008 může být null a teprve v poli 041 v podpoli A můžou být různé jazyky a jedno z nich může být CZE, třeba 1/3 textu v převážně anglické publikaci 

    print("Ponechávám jen texty s rokem vydání 1900+.")
    zmenseni = zmenseni[
        zmenseni["008"].astype(str).str.contains(r"[cdemqrstu]19\d\d", na=False)
        | zmenseni["008"].astype(str).str.contains(r"[cdemqrstu]20\d\d", na=False)
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
    cisla_komplet.insert(0, "leader")

    for c in cisla_komplet:

        kam_sloupec = f"data_raw/cnb_sloupce/{c}"

        selected_columns = (
            frame.filter(regex=f"001|{c}").explode("001").set_index("001", drop=True)
        )

        selected_columns.columns = selected_columns.columns.astype(str) ## aby zůstaly nuly na začátku názvů sloupců

        if len(selected_columns.columns) > 0:
            selected_columns = selected_columns.dropna(how="all")

            if not os.path.exists(kam_sloupec):
                os.makedirs(kam_sloupec)

            selected_columns.to_parquet(
                os.path.join(kam_sloupec, f"{c}_{cislo}.parquet")
            )

############################
## ZPRACOVÁNÍ HRUBÝCH DAT ##
############################

warnings.simplefilter(
    action="ignore", category=FutureWarning
)  ## Nechceme to zatapetovat varováními.
warnings.simplefilter(action="ignore", category=UserWarning)

try:
    with open(os.path.join('data_raw','cnb_explodovatelne_sloupce.json'), 'r', encoding="utf-8") as file:
        explodovatelne = json.loads(file.read())
except:
    explodovatelne = ['008','100_a','245_a']

odkud = "data_raw/cnb"
kam_chunks = "data_raw/cnb_chunks"
kam_rozsekane_sloupce = "data_raw/cnb_sloupce"

if not os.path.exists(kam_chunks):
    os.makedirs(kam_chunks)
if not os.path.exists(kam_rozsekane_sloupce):
    os.makedirs(kam_rozsekane_sloupce)

if filtr == True:

    sloupce_k_zachovani = []
    with open("readme.md", "r", encoding="utf-8") as readme:
        readme = readme.read().split("# Klíč k")[-1].split("Databáze národních autorit")[0]
        for l in readme.splitlines():
            if (l[0:2] == "- ") and ("*" not in l):
                sloupce_k_zachovani.append(l.split("-")[1].strip())

    print(f"Začínám filtrovat data ČNB, zachovám {len(sloupce_k_zachovani)} sloupců.")

if (filtr == True) or (rozsekani == True):

    vsechny_jsony = [f for f in os.listdir(odkud)]

    df = pd.DataFrame()

    pocitadlo = 0

    for index, j in enumerate(vsechny_jsony):

        print(f"Načítám JSON č. {index + 1}.")

        df = pd.concat([df, pd.read_json(os.path.join(odkud, j))])

        if ((index + 1) % 8 == 0) or (index == len(vsechny_jsony) - 1):

            pocitadlo += 1

            print(f"Zpracovávám cnb_chunk_{pocitadlo}.")

            if filtr == True:

                vyfiltruj(df).to_parquet(
                    os.path.join(kam_chunks, f"cnb_chunk_{pocitadlo}.parquet")
                )

                print("Chunk uložen.")

            if rozsekani == True:

                print("Ukládám kompletní sloupce.")
                
                rozsekej(df, pocitadlo)

            df = pd.DataFrame()

if autority == True:

    jsony = [o for o in os.listdir("data_raw/aut")]

    sloupce_k_zachovani = []
    with open("readme.md", "r", encoding="utf-8") as readme:
        readme = readme.read().split("### Databáze národních autorit")[1]
        for l in readme.splitlines():
            if (l[0:2] == "- ") and ("*" not in l):
                sloupce_k_zachovani.append(l.split("-")[1].strip())
    sloupce_k_zachovani = list(set(sloupce_k_zachovani))

    df = pd.DataFrame()
    for j in jsony:
        print(f"Připojuji a filtruji {j}.")
        df = pd.concat([df, pd.read_json(os.path.join("data_raw/aut", j))]) 
        sloupce_k_zachovani_filtr = [s for s in sloupce_k_zachovani if s in df.columns.to_list()]
        df = df[sloupce_k_zachovani_filtr]

    df = df.explode("001").set_index("001", drop=True) 

    df = df.reindex(sorted(df.columns), axis=1)

    df.to_parquet(os.path.join("data", "aut_vyber.parquet"))
    df.to_json(os.path.join("data", "aut_vyber.json"))

    print("Hotovo!")

#############################
## SPOJENÍ DÍLKŮ DOHROMADY ##
#############################

if rozsekani == True:

    kam_spojene_sloupce = "data/cnb_sloupce" 

    if not os.path.exists(kam_spojene_sloupce):
        os.makedirs(kam_spojene_sloupce)

    columns = [
        d
        for d in os.listdir(kam_rozsekane_sloupce)
        if os.path.isdir(os.path.join(kam_rozsekane_sloupce, d))
    ]

    for c in columns:
        print(f"Spojuji sloupce začínající na {c}.")
        s = pd.DataFrame()
        for p in [d for d in os.listdir(f"{kam_rozsekane_sloupce}/{c}") if "parquet" in d]:
            s = pd.concat(
                [s, pd.read_parquet(os.path.join(f"{kam_rozsekane_sloupce}/{c}", p))]
            )

        s = s[~s.index.duplicated(keep='first')] ## PROVIZORNÍ FIX, nutno překontrolovat, proč tam jsou 2×

        for e in explodovatelne:
            if e in s.columns.to_list():
                s = s.explode(e)

        s.to_parquet(os.path.join(kam_spojene_sloupce, f"{c}.parquet"))

if filtr == True:

    odkud_vyber = "data_raw/cnb_chunks"
    kam_vyber = "data"

    chunks = [d for d in os.listdir(odkud_vyber)]

    df = pd.DataFrame()
    for c in chunks:
        print(f"Načítám chunk {c}.")
        df = pd.concat(
            [
                df,
                pd.read_parquet(os.path.join(f"{odkud_vyber}", c))
                .explode("001")
                .set_index("001", drop=True)
            ]
        )
    
    print("Ukládám spojený dataset")

    df = df.sort_index()

    for e in explodovatelne:
        if e in df.columns.to_list():
            df = df.explode(e)

    df = df[~df.index.duplicated(keep='first')] ## PROVIZORNÍ FIX, nutno překontrolovat, proč tam jsou 2×
    df = df.reindex(sorted(df.columns), axis=1)
        
    df.to_parquet(os.path.join(kam_vyber, "cnb_vyber.parquet"))
    
    print("Hotovo.")