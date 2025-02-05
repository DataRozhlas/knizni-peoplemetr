#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import pandas as pd


# In[2]:


pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)


# In[3]:


df = pd.read_json(os.path.join('data_raw','wikidata_raw.json'))


# In[21]:


odkud = "downloads/wikidata/nazvy"


# In[23]:


stazene = [f for f in os.listdir(odkud)]


# In[25]:


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


# In[27]:


len(slovnik)


# In[29]:


neprekladat = ['024_a','label_cs','label_en','popis_en','popis_cs','w_narozeni','w_narozeni_presne','w_umrti','w_umrti_presne','jazykove_verze','wiki_cs','wiki_en','facebook','twitter','instagram','web']


# In[31]:


prekladat = [x for x in df.columns.to_list() if x not in neprekladat]


# In[33]:


df[prekladat]


# In[35]:


slovnik


# In[37]:


def replace_with_dict(x):
    if isinstance(x, list):
        return [slovnik.get(item, item) for item in x]
    elif isinstance(x, str):
        return slovnik.get(x, x)
    else:
        return x


# In[39]:


df_replaced = df[prekladat].map(replace_with_dict)


# In[40]:


df_result = pd.concat([df_replaced, df.drop(prekladat, axis=1)], axis=1)


# In[41]:


df_result


# In[45]:


df_result[df_result['druh_umrti'].notnull()].sample(20)


# In[47]:


df_result['w_gender'].drop_duplicates()


# In[49]:


df_result.groupby('w_gender').size()


# In[51]:


df_result = df_result.reindex(sorted(df_result.columns), axis=1)


# In[53]:


df_result.to_parquet(os.path.join('data','wikidata.parquet'))

