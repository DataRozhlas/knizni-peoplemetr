import re

def zjisti_cenu(c020):
    
    c020 = str(c020)
    cena = None
    if 'K' in c020:
        ceny = re.findall(r'\d{1,5},{0,1}\d{0,2}',c020)
        if len(ceny) > 0:
            ceny = [float(c.replace(',','.')) for c in ceny]
            cena = min(ceny)
    if 'hal' in c020:
        ceny = re.findall(r'\d{1,5},{0,1}\d{0,2}',c020)
        if len(ceny) > 0:
            ceny = [float(c.replace(',','.')) for c in ceny]
            cena = max(ceny)
            if cena > 1:
                cena = cena / 100
    return cena