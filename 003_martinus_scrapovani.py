#!/usr/bin/env python

import os

import re

from bs4 import BeautifulSoup

import pandas as pd

slozky = [item for item in os.listdir("downloads/martinus")]

slozky

def scrape_martinus(stranka):

    kniha = {}

    soup = BeautifulSoup(stranka, "html.parser")

    try:

        kniha['M_titul'] = soup.find('h1').text.strip()

    except:

        return {}

    if soup.find('h1').find('a'):

        for odkaz in soup.find('h1').find_all('a'):

            kniha['M_titul'] = kniha['M_titul'].replace(odkaz.text,'').strip()

    try:    

        kniha['M_autorstvo'] = [odkaz.text.strip() for odkaz in soup.find(id='author').find_all('a') if odkaz.text.strip() != 'Číst víc']

        if len(kniha['M_autorstvo']) == 1:

            kniha['M_autorstvo'] = kniha['M_autorstvo'][0]

    except:

        kniha['M_autorstvo'] = soup.find(class_='product-detail__author').text.strip()

    kniha['M_anotace'] = soup.find(class_='cms-article').text.strip()

    detaily = soup.find(id='details')

    for detail in detaily.find_all('dl'):

        if "série" in detail.find('dt').text.lower():

            kniha['M_série'] = detail.find('dd').text.strip()

            kniha['M_díl'] = re.search("\d*", detail.find('dt').text).group(0)

        else:

            if detail.find('a'):

                kniha[f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""] = [odkaz.text.strip() for odkaz in detail.find_all('a')]

                if len(kniha[f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""]) == 1:

                    kniha[f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""] = kniha[f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""][0]

            else:

                kniha[f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""] = detail.find('dd').text.strip()

    kniha['M_cena'] = soup.find(class_='header__book').find('h3').text.strip()

    kniha['M_datum'] = stranka.splitlines()[-2].split(' ')[1] + ' ' + stranka.splitlines()[-2].split(' ')[2]

    flexy = soup.find_all(class_='flex-column')

    for f in flexy:

        if f.find('h6'):

            if f.find('h6').text.strip() != 'Kniha':

                kniha[f"""M_{f.find('h6').text.strip().lower()}"""] = f.find('span').text.strip()

    return kniha

knihy = []

for s in slozky:

    odkud_brat = f'downloads/martinus/{s}'

    for i in os.listdir(odkud_brat):

        print(i)

        with open(os.path.join(odkud_brat, i), "r", encoding="utf-8") as page:

            page = page.read()

            kniha = scrape_martinus(page)

        ## kniha['kategorie_martinus'] = s

        kniha['soubor'] = i

        knihy.append(kniha)

df = pd.DataFrame(knihy)

df.columns

df

df.to_csv(os.path.join('data_raw','martinus_raw.csv'), index=False, encoding="utf-8", header=True)

