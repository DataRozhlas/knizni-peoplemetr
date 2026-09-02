#!/usr/bin/

import os
import requests
from random import randint
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

kam = "downloads/ebooky-martinus"
os.makedirs(kam, exist_ok=True)
stazene = set([x.split(".")[0] for x in os.listdir(kam)])
print(f"{len(stazene)} knih už staženo")

df = pd.read_json(os.path.join("data_raw", "martinus_raw.json"))

driver = webdriver.Firefox()


def stahni_ebook(isbn, url):
    if isbn not in stazene:
        sleep(randint(2,7))
        driver.get(url)
        print(f"iniciována funkce stahni_ebook: {url}")
        
        try:
            # 1. WAIT FOR PAGE TO FULLY LOAD
            # This checks the browser's internal ready state
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Wait for the preview button to be clickable
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='show-m' and text()='Prohlédnout ukázku']")
                )
            )
            element.click()
            print("Klikám na Stáhnout ukázku.")
            
            # 2. WAIT FOR SPECIFIC ELEMENTS INSTEAD OF SLEEP
            # Replaces sleep(randint(4,7)) by waiting exactly until the links appear in the DOM
            links = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(@href, 'dibuk.eu')]")
                )
            )
            
            odkazy = [link.get_attribute("href") for link in links]
            
            for o in odkazy:
                filename = f"{isbn}.{o.split('/')[-1]}"
                try:
                    response = requests.get(o)
                    print("Uloveno!")
                    with open(os.path.join(kam, filename), "wb") as f:
                        f.write(response.content)
                except Exception as E:
                    print(f"Chyba při stahování: {E}")
                    
        except Exception as e:
            # Catching TimeoutExceptions so the script doesn't crash if a book is missing the button
            print(f"Prvky nenalezeny pro {isbn}: {e}")
    else:
        print("Tuto knihu jsme již stáhli.")
        pass


pocitadlo = 0

df["delka_isbn"] = df["M_isbn"].apply(lambda x: len(str(x)))
df = df[(df["M_ebook"] != False) & (df["delka_isbn"] == 13)]
df = df.sample(frac = 1)

for index, row in df[["M_isbn", "M_ebook"]].iterrows():
    pocitadlo += 1
    print(
        f"{pocitadlo}/{len(df[df['M_ebook'] != False]) - len(stazene)}: stahuji knihu s ISBN {row['M_isbn']}"
    )
    stahni_ebook(row["M_isbn"], f"""https://www.martinus.cz{row['M_ebook']}""")