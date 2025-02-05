import gc
import os
import json
import requests
import pandas as pd

kam = 'data_raw/wikidata_doplneni'
if not os.path.exists(kam):
    os.makedirs(kam)

vsechny_jsony = [f for f in os.listdir(kam)]
vyhledane = set([x.split("_")[0] for x in vsechny_jsony])
df = pd.read_parquet(os.path.join("data/cnb_sloupce","100.parquet"))
df = df.explode('100_7')

print(f"Unikátních kódů personálních autorit 100_7: {len(df['100_7'].nunique())}")

opakovane = df.groupby('100_7').size()
opakovane = opakovane.sort_values(ascending=False)
opakovane = opakovane[opakovane > 1].index.to_list()

print(f"Kódů personálních autorit opakujících se alespoň 2×: {len(opakovane)}")

autority = pd.read_parquet(os.path.join("data","aut_vyber.parquet"))

autority = autority[autority['024_2'].notnull()]
autority = autority[autority['024_a'].notnull()]

autority = autority.explode(['024_a','024_2'])

autority_s_wikidaty = set(autority[autority['024_2'] == 'wikidata']['024_a'].index.to_list())

chybi = [x for x in opakovane if x not in autority_s_wikidaty]

del df
del autority
gc.collect()

# Wikidata SPARQL endpoint
sparql_endpoint = "https://query.wikidata.org/sparql"

# Function to get Wikidata ID from NL CR AUT ID
def get_wikidata_id(nl_cr_aut_id):
    query = f"""
    SELECT ?item WHERE {{
      ?item wdt:P691 "{nl_cr_aut_id}".
    }}
    """
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(sparql_endpoint, params={"query": query}, headers=headers)
    data = response.json()

    if "results" in data and "bindings" in data["results"]:
        bindings = data["results"]["bindings"]
        if bindings:
            return bindings[0]["item"]["value"].split("/")[-1]
    return None

vyhledane = set(vyhledane)

co_stahovat = [x for x in chybi if x not in vyhledane]

print(f"Zjistím Wikidata IDs pro {len(co_stahovat)} personálních autorit.")

pocitadlo = 0
for nl_cr_aut_id in co_stahovat:
    pocitadlo += 1
    print(f"{pocitadlo:005}: {nl_cr_aut_id}")
    slovnik = {}
    slovnik['100_7'] = nl_cr_aut_id
    wikidata_id = get_wikidata_id(nl_cr_aut_id)
    if wikidata_id:
        slovnik['024_a'] = wikidata_id
    else:
        slovnik['024_a'] = ""
    with open(os.path.join(kam, f"{nl_cr_aut_id}_{slovnik['024_a']}.json"), "w+", encoding="utf-8") as file:
        file.write(json.dumps(slovnik))