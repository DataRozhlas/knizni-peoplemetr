#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import json
import requests
import pandas as pd


# In[2]:


pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)


# In[3]:


df = pd.read_json(os.path.join('data_raw','wikidata_raw.json'))


# In[4]:


vsechny_hodnoty = []
for sloupec in df.columns.to_list():
    sl = df.explode(sloupec)[sloupec].drop_duplicates().to_list()
    for s in sl:
        if re.findall(r'^Q\d\d', str(s)):
            vsechny_hodnoty.append(str(s))
vsechny_hodnoty = list(set(vsechny_hodnoty))


# In[5]:


len(vsechny_hodnoty)


# In[6]:


kam = 'downloads/wikidata/nazvy'


# In[7]:


if not os.path.exists(kam):
    os.makedirs(kam)


# In[8]:


nestahovat = []
for f in os.listdir(kam):
    with open(os.path.join(kam, f), "r", encoding="utf-8") as soubor:
        slovnik = json.loads(soubor.read())
    try:
        for q in list(slovnik['entities'].keys()):
            nestahovat.append(q)
    except:
        print(f)
        os.remove(os.path.join(kam, f))


# In[9]:


len(nestahovat)


# In[10]:


nestahovat = set(nestahovat)


# In[11]:


def get_labels(ktere):
    seznam = '|'.join(ktere)
    nazev = '-'.join(ktere[0:3])
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids={seznam}&languages=cs|en|sk|de|fr|es|ru&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(kam, f"{nazev}.json"), "w+", encoding="utf-8") as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        print(f"Data has been saved to {nazev}.json")
    else:
        print(f"Failed to retrieve data: {response.status_code}")


# In[12]:


stahnout = [x for x in vsechny_hodnoty if x not in nestahovat]


# In[13]:


len(stahnout)


# In[14]:


pracovni = []
pocitadlo = 0
for v in stahnout:
    pocitadlo += 1
    pracovni.append(v)
    if pocitadlo % 50 == 0:
        get_labels(pracovni)
        print(f'{pocitadlo:6}/{len(stahnout)}')
        pracovni = []
get_labels(pracovni)
print('Hotovo!')

