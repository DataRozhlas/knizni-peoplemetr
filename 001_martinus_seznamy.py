#!/usr/bin/env python

import os



import requests

from bs4 import BeautifulSoup

if not os.path.exists('data_raw/martinus_linky'):

    os.makedirs('data_raw/martinus_linky')

seznamy = {

    'martinus-beletrie.txt': 'https://www.martinus.cz/l?categories%5B0%5D=6100&origins%5B0%5D=265851&specials%5B0%5D=available&sort=release_date+desc&page=',

    'martinus-nonfiction.txt': 'https://www.martinus.cz/l?categories%5B0%5D=6204&origins%5B0%5D=265851&specials%5B0%5D=available&sort=release_date+desc&page=',

    'martinus-ya.txt': 'https://www.martinus.cz/l?ages%5B0%5D=14..&categories%5B0%5D=6002&origins%5B0%5D=265851&sort=release_date+desc&specials%5B0%5D=available&page=',    

}

def dopln_novinky(slovnik):

    

    def knihy_do_souboru(s, sez):

        sez = list(set(sez))

        with open(os.path.join("data_raw/martinus_linky",s), "w+", encoding="utf-8") as f1:

            f1.write("\n".join(sez))

        print(f"Soubor {s} uložen.")

    

    def knihy_ze_stranky(s):

        r = requests.get(s)

        soup = BeautifulSoup(r.text, "html.parser")

        nabidka = soup.find(class_='listing')

        knihy = nabidka.find_all('a')

        knihy_na_strance = []

        for k in knihy:

            if '/kniha' in k['href']:

                knihy_na_strance.append(f"https://www.martinus.cz{k['href']}")

        return list(set(knihy_na_strance))

    

    def pavouk(s, u):

        

        nove = 0

        

        print(f"Přidávám knihy z kategorie {s.split('.')[0].split('-')[1].upper()}")

        

        try:

            with open(os.path.join("data_raw/martinus_linky",s), "r", encoding="utf-8") as f2:

                seznam_knih = f2.read().splitlines()

        except FileNotFoundError:

            seznam_knih = []

                

        print(f"Knih v seznamu: {len(seznam_knih)}")

        

        x, kontrola = 0, 0

        

        while (kontrola < 50) and (x <= 500):

            

            try:

                x += 1

                print(f"{u}{x}")

                dalsi_knihy = knihy_ze_stranky(f"{u}{x}")

                for d in dalsi_knihy:

                    if d not in seznam_knih:

                        seznam_knih.append(d)

                        nove += 1

                    else:

                        kontrola += 1 # ať to neskončí příliš brzy, kdyby se pozpřehazovalo pořadí ve výpisu

                if x % 10 == 0:

                    knihy_do_souboru(s, seznam_knih)

            except:

                break

        

        knihy_do_souboru(s, seznam_knih)

        print(f"Končím na straně {x}, {nove} nových knih, {kontrola} knih se opakovalo.")



    for soubor, url in slovnik.items():

        pavouk(soubor, url)

        

    print("Nové knihy doplněny.")

dopln_novinky(seznamy)

