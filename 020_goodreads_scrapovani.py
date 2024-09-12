#!/usr/bin/python3


import os
import time
import datetime
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


with open(os.path.join("data_raw", "sledovat.json"), "r") as json_file:
    isbns = json.load(json_file)

print(f"Položek ke stažení: {len(isbns)}")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


def scrape_goodreads(isbn):

    kniha = {
        "ISBN": isbn,
        "GR_date": datetime.datetime.now()
        .replace(microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        r = requests.get(
            f"""https://www.goodreads.com/search?q={isbn}&search_type=isbn&search%5Bfield%5D=isbn""",
            timeout=15,
            headers=headers,
        )
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(e)
        try:
            time.sleep(120)
            r = requests.get(
                f"""https://www.goodreads.com/search?q={isbn}&search_type=isbn&search%5Bfield%5D=isbn""",
                timeout=15,
                headers=headers,
            )
            soup = BeautifulSoup(r.text, "html.parser")
        except:
            return {}

    try:
        kniha["GR_title"] = soup.find("title").text.split("|")[0].strip()
    except:
        return kniha

    if ("Search results for " in kniha["GR_title"]) or (
        "request took too long" in kniha["GR_title"]
    ):
        kniha["GR_title"] = None
        return kniha

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
    return kniha


current_date = datetime.datetime.now()
date_string = current_date.strftime("%Y_%m_%d")
print(date_string)


if not os.path.exists(f"data_raw/goodreads/{date_string}"):
    os.makedirs(f"data_raw/goodreads/{date_string}")


greads = []
count = 0
for i in isbns:
    count += 1
    greads.append(scrape_goodreads(i))
    if count % 20 == 0:
        pd.DataFrame(greads).to_json(
            os.path.join(
                f"data_raw/goodreads/{date_string}",
                f"goodreads_{date_string}_{(int(count/20)):04d}.json",
            )
        )
        print(f"goodreads_{date_string}_{(int(count/20)):04d}.json")
        greads = []
