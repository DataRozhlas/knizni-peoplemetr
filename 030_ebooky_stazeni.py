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
print(f"{len(stazene)} knih už staženo.")

df = pd.read_json(os.path.join("data_raw", "martinus_raw.json"))

driver = webdriver.Firefox()


def stahni_ebook(isbn, url):
    if isbn not in stazene:
        driver.get(url)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[@class='show-m' and text()='Stáhnout ukázku']")
            )
        )
        element.click()
        sleep(randint(4,7))
        links = driver.find_elements(By.XPATH, "//a[contains(@href, 'dibuk.eu')]")
        odkazy = [link.get_attribute("href") for link in links]
        print(f"{len(odkazy)} ukázek")
        for o in odkazy:
            filename = f"""{isbn}.{o.split("/")[-1]}"""
            response = requests.get(o)
            with open(os.path.join(kam, filename), "wb") as f:
                f.write(response.content)
                print("Vpořádku staženo.")
    else:
        pass


pocitadlo = 0

df["delka_isbn"] = df["M_isbn"].apply(lambda x: len(str(x)))
df = df[(df["M_ebook"] != False) & (df["delka_isbn"] == 13)]
df = df.sample(frac = 1)

for index, row in df[["M_isbn", "M_ebook"]].iterrows():
    sleep(randint(2,7))
    pocitadlo += 1
    print(
        f"{pocitadlo}/{len(df[df['M_ebook'] != False]) - len(stazene)}: stahuji knihu s ISBN {row['M_isbn']}"
    )
    stahni_ebook(row["M_isbn"], f"""https://www.martinus.cz{row['M_ebook']}""")
