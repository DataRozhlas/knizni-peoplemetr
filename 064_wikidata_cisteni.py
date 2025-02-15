# Čištění wikidat, zejména výměna kryptických entit za popisky srozumitelné člověku.

import os
import json
import pandas as pd

df = pd.read_json(os.path.join('data_raw','wikidata_raw.json'))

odkud = "downloads/wikidata/nazvy"

stazene = [f for f in os.listdir(odkud)]

slovnik = {}
jazyky = 'cs|en|sk|de|fr|es|ru'.split('|')
for f in stazene:
    with open(os.path.join(odkud, f), 'r', encoding='utf-8') as soubor:
        minislovnik = json.loads(soubor.read())
        try:
            for entita in minislovnik['entities']:
                labels = minislovnik['entities'][entita].get('labels')
                value = None
                for j in jazyky:
                    if value == None:
                        try:
                            value = labels[j]['value']
                        except:
                            pass
                slovnik[entita] = value
        except:
            pass

print(f"{len(slovnik)} kódů k nahrazení textem")

neprekladat = ['024_a','label_cs','label_en','popis_en','popis_cs','w_narozeni','w_narozeni_presne','w_umrti','w_umrti_presne','jazykove_verze','wiki_cs','wiki_en','facebook','twitter','instagram','web']

prekladat = [x for x in df.columns.to_list() if x not in neprekladat]

def replace_with_dict(x):
    if isinstance(x, list):
        return [slovnik.get(item, item) for item in x]
    elif isinstance(x, str):
        return slovnik.get(x, x)
    else:
        return x

df_replaced = df[prekladat].map(replace_with_dict)

df_result = pd.concat([df_replaced, df.drop(prekladat, axis=1)], axis=1)

df_result.groupby('w_gender').size()

df_result = df_result.reindex(sorted(df_result.columns), axis=1)

print("Ukázka výsledku:")

print(df_result[['skoly','w_misto_narozeni','w_gender']].sample(20))

df_result.to_parquet(os.path.join('data','wikidata.parquet'))

print("wikidata.parquet uložen")