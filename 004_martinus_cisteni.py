#!/usr/bin/env python
# coding: utf-8

# In[14]:


import os
import json
import pandas as pd


# In[15]:


df = pd.read_csv(os.path.join('data_raw','martinus_raw.csv'))


# In[16]:


df.columns


# In[17]:


df = df.drop(columns=['M_naše_katalogové_číslo','soubor','M_filmové_zpracování'])


# In[19]:


df[df['M_kategorizace'].notnull()]['M_kategorizace']


# In[20]:


kategorizace = df.explode('M_kategorizace')
kategorizace.groupby('M_kategorizace').size().nlargest(20)


# In[21]:


df['M_ostatní'].drop_duplicates()


# In[22]:


df


# In[23]:


df['M_isbn'] = df['M_isbn'].apply(lambda x: str(x).split(".")[0]).astype(str)


# In[25]:


df['M_věkové_doporučení'] = df['M_věkové_doporučení'].apply(lambda x: str(x).replace("+","") if x else None)


# In[26]:


df


# In[27]:


na_int = ['M_počet_stran','M_rok_vydání','M_díl','M_věkové_doporučení']
for i in na_int:
    df[i] = pd.to_numeric(df[i], errors='coerce', downcast='integer')


# In[28]:


df


# In[29]:


if not os.path.exists('data'):
    os.makedirs('data')


# In[30]:


df[df['M_předběžné_datum_vydání'].notnull()].to_json(os.path.join('data','martinus_vyjde.json'))
df[df['M_rok_vydání'].notnull()].to_json(os.path.join('data','martinus_vyslo.json'))


# In[31]:


puvod = df.explode("M_původ")
puvod.size


# In[32]:


puvod[puvod['M_původ'] == "Česko"].drop_duplicates(subset=['M_isbn']).size


# In[33]:


puvod[puvod['M_původ'] == "Česko"]


# In[34]:


with open(os.path.join("data","nesledovat.json")) as nesledovat:
    nesledovat = json.load(nesledovat)


# In[35]:


puvod[(~puvod['M_isbn'].isin(nesledovat)) & (puvod['M_rok_vydání'].isin([2023,2024])) & (puvod['M_vydání'].isnull()) & (puvod['M_originální_název'].isnull()) & (puvod['M_překlad'].isnull())][['M_titul','M_isbn']].reset_index().to_json(os.path.join('data','sledovat.json'))

