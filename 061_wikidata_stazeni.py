import os
import json
import requests
import pandas as pd
import gc

autority = pd.read_parquet(os.path.join("data","aut_vyber.parquet"))

autority = autority[autority['024_2'].notnull()]
autority = autority[autority['024_a'].notnull()]
autority = autority.explode(['024_a','024_2'])

wikids = autority[autority['024_2'] == 'wikidata']['024_a'].to_list()

aut_wikids = autority[autority['024_2'] == 'wikidata']['024_a'].drop_duplicates(keep="first")
aut_wikids = aut_wikids[~aut_wikids.index.duplicated(keep='first')]

chybejici = [f for f in os.listdir("data_raw/wikidata_doplneni")]
doplneni = []
for c in chybejici:
    if "Q" in c.split("_")[1]:
        slovnik = {}
        slovnik['001'] = c.split("_")[0] 
        slovnik['024_a'] = c.split("_")[1].split('.')[0]
        doplneni.append(slovnik)
    else:
        pass

wikiny_audiny = pd.concat([pd.DataFrame(aut_wikids), pd.DataFrame(doplneni).set_index('001')])

wikiny_audiny = wikiny_audiny[~wikiny_audiny.index.duplicated(keep='first')]

wikiny_audiny.to_json(os.path.join("data_raw","autority_wikidataids.json"))

wikids = wikiny_audiny['024_a'].drop_duplicates().to_list()

kam = 'downloads/wikidata/autority'

vsechny_jsony = set([f for f in os.listdir(kam)])

def get_wikidata_json(entity_id):
    
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        with open(os.path.join(kam, f"{entity_id}.json"), "w+", encoding="utf-8") as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        print(f"Data pro id {entity_id} stažena do {entity_id}.json")
    else:
        print(f"Nešlo stáhnout: {response.status_code}")

del autority
gc.collect()

co_stahovat = [x for x in reversed(wikids) if f"{x}.json" not in vsechny_jsony]

print(f"Stáhnu {len(co_stahovat)} jsonů s daty z Wikidat.")

for w in co_stahovat:
    get_wikidata_json(w)