#!/usr/bin/python3


import os
import sys
import time
import datetime
import re
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

if len(sys.argv) == 2:

    with open(os.path.join("data_raw", sys.argv[-1]), "r") as json_file:
        isbns = json.load(json_file)    
    pripona = sys.argv[-1].split(".")[0]

if len(sys.argv) == 1:

    with open(os.path.join("data_raw", "sledovat.json"), "r") as json_file:
        isbns = json.load(json_file)
    pripona = "pravidelne"

isbns = list(set([x for x in isbns if x != None]))

print(f"Položek ke stažení: {len(isbns)}")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


def scrape_goodreads(isbn):

    if len(isbn) == 13:
        url = f"""https://www.goodreads.com/search?q={isbn}&search_type=isbn&search%5Bfield%5D=isbn"""
    elif "goodreads.com/" in isbn:
        url = isbn
    else:
        return None

    kniha = {
        "ISBN": isbn,
        "GR_date": datetime.datetime.now()
        .replace(microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        r = requests.get(
            url,
            timeout=15,
            headers=headers,
        )
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(e)
        try:
            time.sleep(120)
            r = requests.get(
                url,
                timeout=15,
                headers=headers,
            )
            soup = BeautifulSoup(r.text, "html.parser")
        except:
            return None

    try:
        kniha["GR_title"] = soup.find("title").text.split("|")[0].strip()
    except:
        return None

    if ("Search results for " in kniha["GR_title"]) or (
        "request took too long" in kniha["GR_title"]
    ):
        kniha["GR_title"] = None
        return None

    try:
        kniha["GR_rating"] = float(
            soup.find(class_="RatingStatistics__rating").text.strip()
        )
    except:
        pass
    try:
        kniha["GR_ratings_count"] = int(
            soup.find("span", {"data-testid": "ratingsCount"})
            .text.split("\xa0")[0]
            .strip()
            .replace(",", "")
        )
    except:
        pass
    try:
        kniha["GR_pages"] = int(
            soup.find("p", {"data-testid": "pagesFormat"})
            .text.split(",")[0]
            .replace("pages","")
            .strip()
        )
    except Exception as E:
        print(E)
        pass

    try:
        format = soup.find("p", {"data-testid": "pagesFormat"}).text.lower()
        if "paperback" in format:
            kniha['GR_format'] = "paperback"
        elif "hardcover" in format:
            kniha['GR_format'] = "hardcover"
    except:
        pass

    try:
        kniha["GR_reviews"] = int(
            soup.find("span", {"data-testid": "reviewsCount"})
            .text.split("\xa0")[0]
            .strip()
            .replace(",", "")
        )
    except:
        pass
    try:
        kniha["GR_published"] = (
            soup.find("p", {"data-testid": "publicationInfo"})
            .text.split("lished")[1]
            .strip()
        )
    except:
        pass
    for i in range(1, 6):
        try:
            starcount = soup.find("div", attrs={"data-testid": f"labelTotal-{i}"})
            kniha[f"GR_{i}_stars"] = int(re.search(r"\d{1,10}", starcount.text).group())
        except:
            pass

    return kniha


current_date = datetime.datetime.now()
date_string = current_date.strftime("%Y_%m_%d")
print(date_string)

if not os.path.exists(f"data_raw/goodreads/{date_string}"):
    os.makedirs(f"data_raw/goodreads/{date_string}")

greads = []
count = 0
pribylo = False
for i in isbns:
    prirustek = scrape_goodreads(i)
    print(prirustek)
    if prirustek != None:
        count += 1
        pribylo = True
        greads.append(prirustek)
    if count % 50 == 0:
        if pribylo == True:
            try:
                pd.DataFrame(greads).to_json(
                    os.path.join(
                        f"data_raw/goodreads/{date_string}",
                        f"goodreads_{date_string}_{pripona}_{(int(count/50)):04d}.json",
                    )
                )
                print(f"goodreads_{date_string}_{pripona}_{(int(count/50)):04d}.json")
                greads = []
                pribylo = False
            except: 
                pass
pd.DataFrame(greads).to_json(
    os.path.join(
        f"data_raw/goodreads/{date_string}",
        f"goodreads_{date_string}_{(int(count/50)):04d}.json",
    )
)
print("Hotovo.")
