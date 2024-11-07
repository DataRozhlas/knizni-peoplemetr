#!/usr/bin/python3


import os
import datetime
import re
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

gr = pd.read_csv(os.path.join("data","goodreads-hodnoceni.csv"))
gr = gr[gr['GR_ratings_count'] > 0]
isbns = [int(x) for x in gr['GR_isbn'].drop_duplicates().to_list()]
random.shuffle(isbns)

print(f"Položek ke stažení: {len(isbns)}")

def scrape_goodreads_selenium(isbn):

    def ziskej_cislo(popisek):
        try:
            return int(re.search(r"\d{1,7}",popisek.replace(",","")).group(0))
        except:
            return None

    kniha = {
        "ISBN": isbn,
        "GR_date": datetime.datetime.now()
        .replace(microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:

        display = Display(visible=0, size=(1920, 1080))
        display.start()
        driver = webdriver.Firefox()
        driver.get(f"""https://www.goodreads.com/search?q={isbn}&search_type=isbn&search%5Bfield%5D=isbn""")

        kniha["GR_title"] = driver.title.split("|")[0].strip()
        
        if ("Search results for " in kniha["GR_title"]) or (
            "request took too long" in kniha["GR_title"]
        ):
            kniha["GR_title"] = None
            return kniha

        else:

            wait = WebDriverWait(driver, 10)

            kniha['GR_currently'] = ziskej_cislo(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='currentlyReadingSignal']"))).text)
            kniha['GR_to_read'] = ziskej_cislo(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='toReadSignal']"))).text)
            kniha['GR_ratings_count'] = ziskej_cislo(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ratingsCount']"))).text)
            kniha['GR_reviews'] = ziskej_cislo(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='reviewsCount']"))).text)

            print(kniha)

            return kniha

    except Exception as E:

        print(E)

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(e)
        if display:
            try:
                display.stop()
            except Exception as e:
                print(e)


current_date = datetime.datetime.now()
date_string = current_date.strftime("%Y_%m_%d")

if not os.path.exists(f"data_raw/goodreads_selenium/{date_string}"):
    os.makedirs(f"data_raw/goodreads_selenium/{date_string}")

greads = []
count = 0
for i in isbns:
    dalsi = scrape_goodreads_selenium(i)
    if dalsi != None:
        count += 1
        greads.append(dalsi)
    if (count % 10 == 0) and (count != 0):
        pd.DataFrame(greads).to_json(
            os.path.join(
                f"data_raw/goodreads_selenium/{date_string}",
                f"goodreads_selenium_{date_string}_{(int(count/10)):04d}.json",
            )
        )
        print(f"goodreads_selenium_{date_string}_{(int(count/10)):04d}.json")
        greads = []
pd.DataFrame(greads).to_json(
    os.path.join(
        f"data_raw/goodreads_selenium/{date_string}",
        f"goodreads_selenium_{date_string}_{(int(count/10)):04d}.json",
    )
)
print("Hotovo.")