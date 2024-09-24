#!/usr/bin/env python

import os
import requests
import time
import datetime
import random
import pandas as pd

kam_stahovat = "downloads/aleph"

if not os.path.exists(kam_stahovat):
    os.makedirs(kam_stahovat)

stazene = [s.split('.')[0] for s in os.listdir(kam_stahovat)]

isbns = [i for i in pd.read_json(os.path.join('data','martinus_vyslo.json'))['M_isbn'].to_list() if len(i) == 13]

print(f'{len(isbns)} ISBN ke stažení')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

for i in isbns:
    if i not in stazene:

        random_time = random.uniform(3, 15)
        time.sleep(random_time)

        try:
            print(f"Stahuji ISBN {i}")
            r = requests.get(f"https://aleph.nkp.cz/F/?func=find-b&find_code=ISN&x=0&y=0&request={i}&filter_code_1=WTP&filter_request_1=&filter_code_2=WLN&adjacent=N", headers=headers, timeout=15)
            r.encoding = r.apparent_encoding
            if "Úplné zobrazení záznamu" in r.text:
                with open(os.path.join(kam_stahovat,f'{i}.html'), "w+", encoding='utf-8') as f:
                    f.write(f"""{r.text}\n\n<!-- {datetime.datetime.now().replace(microsecond=0)} -->""")
        except Exception as E:
            print(E)
            pass
    else:
        print(f"ISBN {i} už staženo")

# for filename in os.listdir(kam_stahovat):
#    file_path = os.path.join(kam_stahovat, filename)
#    if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
#        print(f'Mažu {filename}')
#        os.remove(file_path)