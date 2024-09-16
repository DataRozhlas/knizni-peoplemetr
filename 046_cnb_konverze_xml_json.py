import os
import json
import pymarc
# from pymarc import parse_xml_to_array
# import xml.etree.ElementTree as ET

def na_plochy_slovnik(xml_soubor):

    zaznamy = pymarc.marcxml.parse_xml_to_array(xml_soubor)

    hesla = []

    for zaznam in zaznamy:

        zaznam = json.loads(zaznam.as_json())['fields']

        heslo = {}
        for z in zaznam:
            for radek, hodnota in z.items():
                if isinstance(hodnota, str):
                    if radek in heslo:
                        if isinstance(heslo[radek], list):
                            heslo[radek].append(hodnota)
                        else:
                            heslo[radek] = [heslo[radek], hodnota]
                    else:
                        heslo[radek] = hodnota
                if isinstance(hodnota, dict):
                    for podradek, podhodnota in hodnota.items():
                        if isinstance(podhodnota, str):
                            if podhodnota.strip() == '':
                                pass
                            else:
                                key = f"{radek}_{podradek}"
                                if key in heslo:
                                    if isinstance(heslo[key], list):
                                        heslo[key].append(podhodnota)
                                    else:
                                        heslo[key] = [heslo[key], podhodnota]
                                else:
                                    heslo[key] = podhodnota
                        elif isinstance(podhodnota, list):
                            for posledni_uroven in podhodnota:
                                for posledni_radek, posledni_hodnota in posledni_uroven.items():
                                    key = f"{radek}_{posledni_radek}"
                                    if key in heslo:
                                        if isinstance(heslo[key], list):
                                            heslo[key].append(posledni_hodnota)
                                        else:
                                            heslo[key] = [heslo[key], posledni_hodnota]
                                    else:
                                        heslo[key] = posledni_hodnota

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
