#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


isbns = pd.read_json(os.path.join('data','sledovat.json'), dtype={'M_isbn':str})['M_isbn'].drop_duplicates().to_list()
print(f"Položek ke stažení: {len(isbns)}")


# In[3]:


def scrape_dk(isbn):
    
    kniha = {
        'ISBN': isbn,
        'DK_date': datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        r = requests.get(f"""https://www.databazeknih.cz/search?q={isbn}""")
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(e)
        try:
            time.sleep(120)
            r = requests.get(f"""https://www.databazeknih.cz/search?q={isbn}""")
            soup = BeautifulSoup(r.text, "html.parser")
        except:
            return {}
        
    kniha['DK_titul'] = soup.find("title").text.split("-")[0].strip()
    if kniha['DK_titul'] == 'Vyhledávání | Databáze knih':
        kniha['DK_titul'] = None
        return kniha
    
    try:
        kniha['DK_rating'] = int(soup.find(class_=lambda c: c and c.startswith("hodnoceni")).text.split(' ')[0].strip())
    except:
        pass
    try:
        kniha['DK_ratings_count'] = int(soup.find(class_="ratingDetail").text.replace('hodnocení','').replace(' ',''))
    except:
        pass
    
    kniha['DK_tags'] = [s.text for s in soup.find_all(class_="tag")]
    
    try:
        tabulka = soup.find(class_="morePadding")
        for tr in tabulka.find_all('tr'):
            try:
                kniha[f"""DK_{tr.find_all('td')[0].text.strip().replace(" ","_")}"""] = int(tr.find_all('td')[1].text.replace("x","").replace(" ","").strip())
            except:
                pass
    except:
        pass
    
    return kniha


# In[4]:


scrape_dk('978-80-257-0493-6')


# In[5]:


current_date = datetime.datetime.now()
date_string = current_date.strftime("%Y_%m_%d")
print(date_string)


# In[6]:


if not os.path.exists(f'data_raw/databazeknih/{date_string}'):
    os.makedirs(f'data_raw/databazeknih/{date_string}')


# In[7]:


dknih = []
count = 0
for i in isbns:
    count += 1
    dknih.append(scrape_dk(i))
    if count % 20 == 0:
        pd.DataFrame(dknih).to_json(os.path.join(f'data_raw/databazeknih/{date_string}',f'databazeknih_{date_string}_{(int(count/20)):04d}.json'))
        print(f'databazeknih_{date_string}_{(int(count/20)):04d}.json')
        dknih = []

