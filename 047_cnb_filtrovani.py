import os
import json

kde = 'data_raw/cnb'

vsechny_jsony = [f for f in os.listdir(kde)]

ceska_beletrie = []
klasici = []
testy = []

kody = ['821.162.3-3', '821.162.3-1', '821.162.3-31','821.162.3-32', '885-14-821']
popisy = ['české prózy','české romány','české povídky','české novely','česká poezie']

pocitadlo = {'072_a': 0, '080_a': 0, '655_a': 0, '072_x': 0, '245_b': 0, 'fd133974': 0}

for j in vsechny_jsony:
    print(f'Filtruji soubor {j}.')
    with open(os.path.join(kde, j), 'r', encoding='utf-8') as balicek:
        balicek = json.loads(balicek.read())
        for b in balicek:
            if ("Hrabal, Bohumil" in str(b)) or ("Čapek, Karel" in str(b)) or ("Mikulášek, Oldřich" in str(b)) or ("Malířová, Helena" in str(b)) or ("Němcová, Božena" in str(b)):
                klasici.append(b)
            if ('Miluji svou babičku víc než mladé dívky' in str(b)) or ('Šokovaná růže' in str(b)) or ('K čemu jste na světě' in str(b)) or ('Clarissa a jiné texty' in str(b)):
                testy.append(b)
            if 'fd133974' in str(b):
                ceska_beletrie.append(b)
                pocitadlo['fd133974'] += 1
            if '072_a' in b and b['072_a']:
                for k in kody:
                    if k in str(b['072_a']):
                        ceska_beletrie.append(b)
                        pocitadlo['072_a'] += 1
            if '080_a' in b and b['080_a']:
                for k in kody:
                    if k in str(b['080_a']):
                        ceska_beletrie.append(b)
                        pocitadlo['080_a'] += 1
            elif '655_a' in b and b['655_a']:
                for p in popisy:
                    if p in str(b['655_a']).lower():
                        ceska_beletrie.append(b)
                        pocitadlo['655_a'] += 1
                        pass
            elif '072_x' in b and b['072_x']:
                if ('česká próza' in str(b['072_x']).lower()) or ('česká poezie' in str(b['072_x']).lower()):
                    ceska_beletrie.append(b)
                    pocitadlo['072_x'] += 1
            elif '245_b' in b and b['245_b']:
                if 'román' in b['245_b'].lower():
                    if '041_ind1' in b and b['041_ind1']:
                        if str(b['041_ind1']) == '0':
                            ceska_beletrie.append(b)
                            pocitadlo['245_b'] += 1
                    if '240_l' not in b:
                            ceska_beletrie.append(b)
                            pocitadlo['245_b'] += 1

with open(os.path.join('data_raw','ceska_beletrie_raw.json'), 'w+', encoding='utf-8') as vystup:
    vystup.write(json.dumps(ceska_beletrie))

with open(os.path.join('data_raw','klasici.json'), 'w+', encoding='utf-8') as vystup:
    vystup.write(json.dumps(klasici))

with open(os.path.join('data_raw','testy.json'), 'w+', encoding='utf-8') as vystup:
    vystup.write(json.dumps(testy))

for klic, hodnota in pocitadlo.items():
    print(f"{klic}: {hodnota}")

print('Hotovo.')

# ceske_romany = df[(df['655_a'] == 'české romány') | ((df['655_a'].str.contains('román',na=False)) & (df['040_b'] == df['041_h'])) | (df['072_x'] == 'Česká próza')].reset_index(drop=True)
# ceske_romany[['020_c','020_q','100_a','100_d','040_b','041_h','245_a','245_b','250_a','260_a','260_b','260_c','964_a','300_c','500_a','550_a','655_a','830_a','072_x']].to_json(os.path.join('data_raw','ceske_romany_raw.json'))