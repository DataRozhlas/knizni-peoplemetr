# Momentálně (2024-09-24) téměř nepotřebný soubor, důležitý jen pro následné extrahování ISBN nových českých beletrií. 

import os
import random
import json

kde = "data_raw/cnb"

vsechny_jsony = [f for f in os.listdir(kde)]

vzorek = []

ceska_beletrie = []
testy = []

kody = [
    "821.162.3-3",
    "821.162.3-1",
    "821.162.3-31",
    "821.162.3-32",
    "885-14-821",
    "885.0-1",
]
fkody = ["fd133974", "fd133971", "fd133958", "fd133973", "fd133969", "fd133960"]
mdt = [
    "(0:82-3)",
    "(0:82-312.6)",
    "(0:82-312.6)",
    "(0:82-312.6)",
    "(0:82-312.6)",
    "(0:82-311.8)",
    "(0:82-311.8)",
    "821-312.5",
    "(0:82-312.4)",
    "821-312.5",
    "(0:82-312.4)",
    "821-312.5",
    "(0:82-312.4)",
    "821-312.5",
    "(0:82-312.9)",
    "(0:82-311.6)",
    "(0:82-311.6)",
    "821-312.5",
    "(0:82-312.4)",
    "(0:82-313.1)",
    "(0:82-313.1)",
    "821-312.5",
    "(0:82-312.5)",
    "821-312.5",
    "(0:82-312.4)",
    "(0:82-312.4)",
    "(0:82-311.6)",
    "821-312.5",
    "(0:82-311.9)",
    "(0:82-32)",
    "(0:82-1)",
    "(0:82-32)",
]  # https://text.nkp.cz/o-knihovne/odborne-cinnosti/zpracovani-fondu/Archiv/formalnideskriptory-1
mdt = list(set([m for m in mdt if m not in kody]))
popisy = [
    "české prózy",
    "české romány",
    "české povídky",
    "české novely",
    "česká poezie",
]

celkem = 0

pocitadlo = {
    "072_a": 0,
    "080_a": 0,
    "655_a": 0,
    "072_x": 0,
    "041_h": 0,
    "041_ind1": 0,
    "fkody": 0,
    "041_h_implicitni": 0,
    "041_h_cze": 0,
    "700_a": 0,
    "245_b": 0
}

for j in vsechny_jsony:
    print(f"Filtruji soubor {j}.")
    with open(os.path.join(kde, j), "r", encoding="utf-8") as balicek:
        balicek = json.loads(balicek.read())
        do_vzorku = random.sample(balicek, 2000)
        vzorek = vzorek + do_vzorku
        for b in balicek:
            celkem += 1
            uspech = False
            if (
                ("Miluji svou babičku víc než mladé dívky" in str(b))
                or ("Němcová, Božena" in str(b))
                or ("Malířová, Helena" in str(b))
                or ("Kafka, Franz" in str(b))
                or ("Tiket na tutovku" in str(b))
                or ("Objednaná smrt" in str(b))
                or ("Příběhy detektiva Ouška" in str(b))
                or ("Dva případy třetí skupiny" in str(b))
                or ("Vlastimír Talaš" in str(b))
            ):
                testy.append(b)

            if "008" in b:
                if "cze" in str(b["008"]):
                    
                    for f in fkody:  # když je to jako česká věc vedené autoritou pro žánr či formu, je to jasné
                        if f in str(b):
                            ceska_beletrie.append(b)
                            pocitadlo["fkody"] += 1
                            uspech = True
                    
                    if uspech == False:
                        for k in kody:  # dtto
                            if k in str(b):
                                ceska_beletrie.append(b)
                                pocitadlo["072_a"] += 1
                                uspech = True
                    
                    if uspech == False:
                        if "655_a" in b:  # když je to jako česká věc popsané, je to snad safe
                            for p in popisy:
                                if p in str(b["655_a"]).lower():
                                    ceska_beletrie.append(b)
                                    pocitadlo["655_a"] += 1
                        elif "072_x" in b:  # dto
                            if ("česká próza" in str(b["072_x"]).lower()) or (
                                "česká poezie" in str(b["072_x"]).lower()
                            ):
                                ceska_beletrie.append(b)
                                pocitadlo["072_x"] += 1
                        elif "041_ind1" in b:
                            if str(b["041_ind1"]).strip() == "0":  # explicitně není překlad
                                for m in mdt:
                                    if uspech == False:
                                        if m in str(b): # str(b["080_a"]):
                                            uspech = True
                                            ceska_beletrie.append(b)
                                            pocitadlo["041_ind1"] += 1
                        elif "041_h" in b:
                            if "cze" in str(b["041_h"]):  # explicitně není překlad
                                for m in mdt:
                                    if uspech == False:
                                        if m in str(b):
                                            ceska_beletrie.append(b)
                                            pocitadlo["041_h_cze"] += 1
                                            uspech = True
                        elif "700_a" not in b: # implicitně není překlad
                            for m in mdt:
                                if uspech == False:
                                    if m in str(b):
                                        ceska_beletrie.append(b)
                                        pocitadlo["700_a"] += 1
                                        uspech = True
                        elif "041_h" not in b:  # implicitně není překlad
                            if "245_b" in b:
                                if ("román" in str(b["245_b"]).lower()) or ("novela" in str(b["245_b"]).lower()) or ("povídky" in str(b["245_b"]).lower()):
                                    ceska_beletrie.append(b)
                                    pocitadlo["245_b"] += 1
                        else:
                            for m in mdt:
                                if m in str(b):
                                    if uspech == False:
                                        ceska_beletrie.append(b)
                                        pocitadlo["041_h_implicitni"] += 1
                                        uspech = True                        

with open(
    os.path.join("data_raw", "ceska_beletrie_raw.json"), "w+", encoding="utf-8"
) as vystup:
    vystup.write(json.dumps(ceska_beletrie))

with open(os.path.join("data_raw", "testy.json"), "w+", encoding="utf-8") as vystup:
    vystup.write(json.dumps(testy))

with open(
    os.path.join("data_raw", "cnb_sample.json"), "w+", encoding="utf-8"
) as vystup:
    vystup.write(json.dumps(vzorek))

for klic, hodnota in pocitadlo.items():
    print(f"{klic}: {hodnota}")

print(
    f"Vyfiltrováno {sum(pocitadlo.values())} záznamů z celkového počtu {celkem} ({int(sum(pocitadlo.values())/celkem)} %)."
)

print("Hotovo.")