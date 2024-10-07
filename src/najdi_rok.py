def najdi_rok(nn8):
    if nn8[6] in ['s', 't', 'd', 'm', 'e', 'c','u', 'r']:
        try:
            return int(nn8[7:11])
        except Exception as e:
            return None
        else:
            return None
    elif nn8[6] == 'q':
        try:
            rok1 = int(nn8[7:11])
            rok2 = int(nn8[11:15])
            if (len(str(rok2)) == 4) & (rok2 - rok1 <= 5):
                return int(statistics.median([rok1, rok2]))
            else:
                return None
        except:
            return None
    else:
        return None