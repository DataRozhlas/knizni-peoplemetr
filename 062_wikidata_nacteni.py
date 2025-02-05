#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import json
import pandas as pd


# In[2]:


pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)


# In[3]:


odkud = 'downloads/wikidata/autority'


# In[4]:


def najdi_letopocet(x):
    try:
        return int(re.search(r"\d{4}",x).group())
    except:
        return None


# In[5]:


len([f for f in os.listdir("downloads/wikidata/autority")])


# In[6]:


medailony = []
pocitadlo = 0

for f in [f for f in os.listdir("downloads/wikidata/autority")]:

    pocitadlo += 1
    if pocitadlo % 1000 == 0:
        print(f"{pocitadlo:006}: {f}")
    
    medailon = {}
    with open(os.path.join('downloads/wikidata/autority', f), 'r', encoding='utf-8') as file:
        
        wd = json.loads(file.read())
        q = f[:-5]
        medailon['024_a'] = q

        try:
            medailon['label_cs'] = wd['entities'][q]['labels']['cs']['value']
        except:
            pass
        try:
            medailon['label_en'] = wd['entities'][q]['labels']['en']['value']
        except:
            pass
        try:
            medailon['popis_cs'] = wd['entities'][q]['descriptions']['cs']['value']
        except:
            pass
        try:
            medailon['popis_en'] = wd['entities'][q]['descriptions']['en']['value']
        except:
            pass

        try:
            medailon['w_narozeni_presne'] = wd['entities'][q]['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
        except:
            pass
        try:
            medailon['w_umrti_presne'] = wd['entities'][q]['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
        except:
            pass
        
        try:
            medailon['w_narozeni'] = najdi_letopocet(medailon['w_narozeni_presne'])
        except:
            pass
        try:
            medailon['w_umrti'] = najdi_letopocet(medailon['w_umrti_presne'])
        except:
            pass
        
        try:
            medailon['w_gender'] = wd['entities'][q]['claims']['P21'][0]['mainsnak']['datavalue']['value']['id']
        except:
            pass
        try:
            medailon['obcanstvi'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P27']]
        except:
            pass
        try:
            medailon['w_misto_narozeni'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P19']]
        except:
            pass
        try:
            medailon['w_misto_umrti'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P20']]
        except:
            pass
        try:
            medailon['druh_umrti'] = wd['entities'][q]['claims']['P1196'][0]['mainsnak']['datavalue']['value']['id']
        except:
            pass
        try:
            medailon['pricina_umrti'] = wd['entities'][q]['claims']['P509'][0]['mainsnak']['datavalue']['value']['id']
        except:
            pass      
        try:
            medailon['vezeni'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P2632']]
        except:
            pass
        try:
            medailon['profese'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P106']]
        except:
            pass
        try:
            medailon['strany'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P102']]
        except:
            pass
        try:
            medailon['skoly'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P69']]
        except:
            pass
        try:
            medailon['udalosti'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P793']]
        except:
            pass
        try:
            medailon['role'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P2868']]
        except:
            pass
        try:
            medailon['ceny'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P166']]
        except:
            pass
        try:
            medailon['manzelstvo'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P26']]
        except:
            pass
        try:
            medailon['partnerstvo'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P451']]
        except:
            pass
        try:
            medailon['sourozenectvo'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P3373']]
        except:
            pass
        try:
            medailon['potomstvo'] = [x['mainsnak']['datavalue']['value']['id'] for x in  wd['entities'][q]['claims']['P40']]
        except:
            pass       

        try:
            medailon['facebook'] = wd['entities'][q]['claims']['P2013'][0]['mainsnak']['datavalue']['value']
        except:
            pass
        try:
            medailon['twitter'] = wd['entities'][q]['claims']['P2002'][0]['mainsnak']['datavalue']['value']
        except:
            pass
        try:
            medailon['instagram'] = wd['entities'][q]['claims']['P2003'][0]['mainsnak']['datavalue']['value']
        except:
            pass
        try:
            medailon['web'] = wd['entities'][q]['claims']['P856'][0]['mainsnak']['datavalue']['value']
        except:
            pass
        try:
            medailon['wiki_cs'] = wd['entities'][q]['sitelinks']['cswiki']['url']
        except:
            pass
        try:
            medailon['wiki_en'] = wd['entities'][q]['sitelinks']['enwiki']['url']
        except:
            pass
        
        try:
            medailon['jazykove_verze'] = [z.split(".wikipedia")[0].split("//")[1] for z in set(list([x for x in [hodnoty['url'] for popisky, hodnoty in wd['entities'][q]['sitelinks'].items()]])) if "wikipedia" in z]
        except:
            pass
    
    medailony.append(medailon)


# In[7]:


medailony[5:100]


# In[8]:


import sys
sys.getsizeof(medailony)


# In[9]:


text = "text"
sys.getsizeof(text)


# In[10]:


df = pd.read_json(os.path.join("data_raw","autority_wikidataids.json")).reset_index(drop=False)


# In[11]:


df


# In[12]:


df = df.merge(pd.DataFrame(medailony), on='024_a').set_index('index')


# In[13]:


df.sample(20)


# In[14]:


df[df.index == 'Q93240837']


# In[15]:


df[df['024_a'] == 'Q571203']


# In[16]:


df[df['024_a'] == 'Q16861736']


# In[17]:


df[df.index == 'jx20100301005']


# In[18]:


df.sample(10)


# In[19]:


df.to_json(os.path.join('data_raw','wikidata_raw.json'))


# In[20]:


df.info(memory_usage="deep")


# In[21]:


df.columns


# In[22]:


for sloupec in df.columns.to_list():
    print(f"{sloupec}: {int(len(df[df[sloupec].notnull()])/len(df)*100)} %")

