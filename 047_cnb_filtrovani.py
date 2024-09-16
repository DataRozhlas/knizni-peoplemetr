import os
import json

kde = 'data_raw/cnb'

vsechny_jsony = [f for f in os.listdir(kde)]

ceska_beletrie = []

for j in vsechny_jsony:
    print(f'Filtruji soubor {j}.')
    with open(os.path.join(kde, j), 'r', encoding='utf-8') as balicek:
        balicek = json.loads(balicek.read())
        for b in balicek:
            if '072_a' in b and b['072_a']:
                if '821.162.3-3' in b['072_a']:
                    ceska_beletrie.append(b)

with open(os.path.join('data','ceska_beletrie.json'), 'w+', encoding='utf-8') as vystup:
    vystup.write(json.dumps(ceska_beletrie))

print('Hotovo.')

# ceske_romany = df[(df['655_a'] == 'české romány') | ((df['655_a'].str.contains('román',na=False)) & (df['040_b'] == df['041_h'])) | (df['072_x'] == 'Česká próza')].reset_index(drop=True)
# ceske_romany[['020_c','020_q','100_a','100_d','040_b','041_h','245_a','245_b','250_a','260_a','260_b','260_c','964_a','300_c','500_a','550_a','655_a','830_a','072_x']].to_json(os.path.join('data_raw','ceske_romany_raw.json'))