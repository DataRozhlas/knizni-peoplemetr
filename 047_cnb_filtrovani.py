import os
import datetime
import pandas as pd

print(datetime.datetime.now())

slozka = 'data_raw/aleph'

df = pd.DataFrame()
for f in os.listdir(slozka):
    print(f)
    df = pd.concat([df, pd.read_json(os.path.join(slozka, f), dtype='str')])

ceske_romany = df[(df['655_a'] == 'české romány') | ((df['655_a'].str.contains('román',na=False)) & (df['040_b'] == df['041_h'])) | (df['072_x'] == 'Česká próza')].reset_index(drop=True)
ceske_romany.to_json(os.path.join('data_raw','ceske_romany_raw.json'))

ceske_romany.to_json(os.path.join('data_raw','ceske_romany_raw.json'))

print(datetime.datetime.now())