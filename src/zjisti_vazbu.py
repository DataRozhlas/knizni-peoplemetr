def zjisti_vazbu(q020):
    q020 = str(q020).lower()
    if 'váz' in q020:
        return "pevná"
    elif 'brož' in q020:
        return "brožovaná"
    else:
        return None