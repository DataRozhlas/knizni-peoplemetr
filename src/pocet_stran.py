def pocet_stran(rozsah):
    rozsah = str(rozsah)
    cisla = [x for x in re.findall(r"\d{1,4}\s{0,1}[^v]", rozsah)]
    cisla = [int(re.search(r'\d{1,4}', c).group()) for c in cisla]
    if len(cisla) > 0:
        if max(cisla) < 4000: # jak primitivní, ale jak účinné
            return max(cisla)