def hezke_jmeno(sto):
    if not sto[-1].isalnum():
        sto = sto[:-1]
    if "," in sto:
        sto = sto.split(",")
        sto = sto[1].strip() + " " + sto[0].strip()
    return sto    