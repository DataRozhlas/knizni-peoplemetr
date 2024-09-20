# Převede rozsekané XML s Českou národní bibliografií na JSONy, se kterými se už dá pracovat např. v pandas.

import os
import json
from collections import defaultdict
import pymarc

def slovnik_opakovanych(seznam): 
    
    # Aby byly na každém řádku stejně dlouhé seznamy vícenásobných záznamů a šlo např. explodovat jména a role autorstva současně.
    # Ano, každý řádek to prochází třikrát, šlo by to zefektivnit na dva průchody, serepes.

    slovnik = {}
    klice = []
    opakovane_klice = []
    
    for p in seznam:
        if list(p.keys())[0] not in klice:
            klice.append(list(p.keys())[0])
        else:
            opakovane_klice.append(list(p.keys())[0])
    opakovane_klice = list(set(opakovane_klice))
    for p in seznam:
        if list(p.keys())[0] in opakovane_klice:
            pismenka = []
            if 'subfields' in p[list(p.keys())[0]]:
                for o in p[list(p.keys())[0]]['subfields']:
                    pismenka.append(list(o.keys())[0])
            if len(pismenka) > 1:
                if list(p.keys())[0] not in slovnik:                
                    slovnik[list(p.keys())[0]].update(pismenka)
    return slovnik

def na_plochy_slovnik(xml_soubor):

    zaznamy = pymarc.marcxml.parse_xml_to_array(xml_soubor)

    hesla = []

    for zaznam in zaznamy:

        zaznam = json.loads(zaznam.as_json())['fields']

        heslo = defaultdict(list)

        doplneni = slovnik_opakovanych(zaznam)

        for z in zaznam:
            
            for radek, hodnota in z.items():
                if isinstance(hodnota, str):
                    heslo[radek].append(hodnota)
                elif isinstance(hodnota, dict):
                    for podradek, podhodnota in hodnota.items():
                        if isinstance(podhodnota, str) and podhodnota.strip():
                            heslo[f"{radek}_{podradek}"].append(podhodnota)
                        elif isinstance(podhodnota, list):
                            for posledni_uroven in podhodnota:
                                for posledni_radek, posledni_hodnota in posledni_uroven.items():
                                    heslo[f"{radek}_{posledni_radek}"].append(posledni_hodnota)
                            if radek in list(doplneni.keys()):
                                cotuje = [list(podhodnoty.keys())[0] for podhodnoty in podhodnota]
                                for pismenecko in doplneni[radek]:
                                    if pismenecko not in cotuje:
                                        heslo[f"{radek}_{pismenecko}"].append(None)

        hesla.append(heslo)

    return hesla

vsechna_xml = [f for f in os.listdir('downloads/cnb.xml') if (f[0:3] == 'cnb') and ('_' in f)]

print(f"""{len(vsechna_xml)} souborů XML ve složce. (Počítáme jen ty s podtržítkem.)""")

kam_s_tim = "data_raw/cnb"

if not os.path.exists(kam_s_tim):
    os.makedirs(kam_s_tim)

for v in vsechna_xml:
    print(f"Konvertuji {v}.")
    prectene = na_plochy_slovnik(os.path.join('downloads/cnb.xml', v))
    with open(os.path.join(kam_s_tim,v.replace('.xml','.json')), 'w+', encoding='utf-8') as vystup:
        vystup.write(json.dumps(prectene))

print("Hotovo!")
