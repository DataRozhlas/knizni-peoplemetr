#!/usr/bin/env python

import os

import re

from bs4 import BeautifulSoup

import pandas as pd

try:

    raw = pd.read_json(os.path.join("data_raw", "martinus_raw.json"))
    oscrapovane = raw["M_soubor"].to_list()
    oscrapovane = [o for o in oscrapovane if isinstance(o, str)]
    print(
        f"""Ok načteno martinus_raw.csv. {len(oscrapovane)} knih již oscrapováno.
Ukázka: {', '.join(oscrapovane[0:10])}
"""
    )

except Exception as E:

    print(E)

    raw = pd.DataFrame()
    oscrapovane = []

slozky = [item for item in os.listdir("downloads/martinus")]


def scrape_martinus(stranka):

    kniha = {}

    soup = BeautifulSoup(stranka, "html.parser")

    try:

        kniha["M_titul"] = soup.find("h1").text.strip()

    except:

        return {}

    if soup.find("h1").find("a"):

        for odkaz in soup.find("h1").find_all("a"):

            kniha["M_titul"] = kniha["M_titul"].replace(odkaz.text, "").strip()

    try:

        kniha["M_autorstvo"] = [
            odkaz.text.strip()
            for odkaz in soup.find(class_="product-detail__author").find_all("a")
            if odkaz.text.strip() != "Číst víc"
        ]

    except:

        kniha["M_autorstvo"] = soup.find(class_="product-detail__author").text.strip()

    kniha["M_anotace"] = soup.find(class_="cms-article").text.strip()

    if soup.find("h4", class_="product-detail__subtitle"):
        kniha["M_podtitul"] = soup.find(
            "h4", class_="product-detail__subtitle"
        ).text.strip()

    if soup.find(attrs={"data-datalayer-action-value": "topic_tags"}):
        kniha["M_tagy"] = [
            tag.text.strip().replace("#", "")
            for tag in soup.find_all(
                attrs={"data-datalayer-action-value": "topic_tags"}
            )
        ]

    detaily = soup.find(id="details")

    for detail in detaily.find_all("dl"):

        if "série" in detail.find("dt").text.lower():

            kniha["M_série"] = detail.find("dd").text.strip()

            kniha["M_díl"] = re.search("\d*", detail.find("dt").text).group(0)

        else:

            if detail.find("a"):

                kniha[
                    f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""
                ] = [odkaz.text.strip() for odkaz in detail.find_all("a")]

                if (
                    len(
                        kniha[
                            f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""
                        ]
                    )
                    == 1
                ):

                    kniha[
                        f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""
                    ] = kniha[
                        f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""
                    ][
                        0
                    ]

            else:

                kniha[
                    f"""M_{detail.find('dt').text.strip().replace(" ","_").lower()}"""
                ] = detail.find("dd").text.strip()

    kniha["M_cena"] = soup.find(class_="header__book").find("h3").text.strip()

    kniha["M_obálka"] = soup.find("meta", attrs={"property": "og:image"})["content"]

    kniha["M_ebook"] = False
    kniha["M_audiokniha"] = False
    for a in soup.find(class_="shell-detail__formats").find_all("a"):
        if "/e-kniha" in a["href"]:
            kniha["M_ebook"] = a["href"]
        if "/audiokniha" in a["href"]:
            kniha["M_audiokniha"] = a["href"]

    kniha["M_datum"] = (
        stranka.splitlines()[-2].split(" ")[1]
        + " "
        + stranka.splitlines()[-2].split(" ")[2]
    )

    return kniha


knihy = []

for s in slozky:

    odkud_brat = f"downloads/martinus/{s}"

    for i in os.listdir(odkud_brat):

        if i not in oscrapovane:

            print(f"Scrapuji {i}")

            with open(os.path.join(odkud_brat, i), "r", encoding="utf-8") as page:

                page = page.read()

                kniha = scrape_martinus(page)

            ## kniha['kategorie_martinus'] = s

            kniha["M_soubor"] = i

            knihy.append(kniha)

df = pd.DataFrame(knihy)

df = pd.concat([df, raw])

df.reset_index(drop=True).to_json(
    os.path.join("data_raw", "martinus_raw.json"), orient='records'
)
