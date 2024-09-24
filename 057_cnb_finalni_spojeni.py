#!/usr/bin/

import os
import pandas as pd

odkud_sloupce = "data_raw/cnb_sloupce"
kam_sloupce = "data/cnb_sloupce"

filtr = True
sloupce = False

if sloupce == True:

    if not os.path.exists(kam_sloupce):
        os.makedirs(kam_sloupce)

    columns = [d for d in os.listdir(odkud_sloupce) if os.path.isdir(os.path.join(odkud_sloupce, d))]

    for c in columns:
        print(f"Spojuji sloupce začínající na {c}.")
        s = pd.DataFrame()
        for p in [d for d in os.listdir(f"{odkud_sloupce}/{c}")]:
            s = pd.concat([s, pd.read_parquet(os.path.join(f"{odkud_sloupce}/{c}",p))])
        s.to_json(os.path.join(kam_sloupce, f"{c}.json"))
        s.to_parquet(os.path.join(kam_sloupce, f"{c}.parquet"))

if filtr == True:

    odkud_vyber = "data_raw/cnb_chunks"
    kam_vyber = "data"

    chunks = [d for d in os.listdir(odkud_vyber)]

    df = pd.DataFrame()
    for c in chunks:
        print(f"Načítám chunk {c}.")
        df = pd.concat([df, pd.read_parquet(os.path.join(f"{odkud_vyber}",c)).explode('001').set_index("001", drop=True)])
    print("Ukládám spojený dataset.")
    df = df.sort_index()
    df = df.reindex(sorted(df.columns), axis=1)
    print(df.info(memory_usage="deep"))
    df = df
    df.to_json(os.path.join(kam_vyber, "cnb_vyber.json"), orient="records")
    df.to_parquet(os.path.join(kam_vyber, f"cnb_vyber.parquet"))
    print("Hotovo.")