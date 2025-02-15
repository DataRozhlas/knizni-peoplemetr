# Postahujeme labels pro kryptické entity ve wikidata_raw.json.

import os
import re
import json
import requests
import pandas as pd
from multiprocessing import Pool, cpu_count
from functools import partial
from itertools import islice

def chunk_list(lst, chunk_size):
    """Split list into chunks of specified size"""
    iterator = iter(lst)
    return list(iter(lambda: list(islice(iterator, chunk_size)), []))

def get_labels(ktere, kam):
    """Download and save labels for a chunk of Q-values"""
    seznam = '|'.join(ktere)
    nazev = '-'.join(ktere[0:3])
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&ids={seznam}&languages=cs|en|sk|de|fr|es|ru&format=json"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            output_path = os.path.join(kam, f"{nazev}.json")
            with open(output_path, "w+", encoding="utf-8") as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)
            return f"Success: Data saved to {nazev}.json"
        else:
            return f"Failed: HTTP {response.status_code} for chunk starting with {nazev}"
    except Exception as e:
        return f"Error: {str(e)} for chunk starting with {nazev}"

def main():
    # Create output directory
    kam = 'downloads/wikidata/nazvy'
    if not os.path.exists(kam):
        os.makedirs(kam)

    # Read and process input data
    df = pd.read_json(os.path.join('data_raw', 'wikidata_raw.json'))
    
    print(df)

    vsechny_hodnoty = []
    for sloupec in df.columns.to_list():
        sl = df.explode(sloupec)[sloupec].drop_duplicates().to_list()
        for s in sl:
            if re.findall(r'^Q\d\d', str(s)):
                vsechny_hodnoty.append(str(s))
    vsechny_hodnoty = list(set(vsechny_hodnoty))
    
    print(f"{len(vsechny_hodnoty)} different values in wikidata_raw.json")

    # Get already downloaded items
    nestahovat = set()
    for f in os.listdir(kam):
        try:
            with open(os.path.join(kam, f), "r", encoding="utf-8") as soubor:
                slovnik = json.loads(soubor.read())
                nestahovat.update(slovnik['entities'].keys())
        except Exception as e:
            print(f"Error reading {f}: {str(e)}")
            os.remove(os.path.join(kam, f))

    print(f"{len(nestahovat)} already downloaded")

    # Get items to download
    stahnout = [x for x in vsechny_hodnoty if x not in nestahovat]
    print(f"{len(stahnout)} remaining to download")

    # Split into chunks of 50 items
    chunks = chunk_list(stahnout, 50)
    
    # Determine number of processes
    num_processes = min(cpu_count(), len(chunks))
    print(f"Using {num_processes} processes")

    # Create partial function with fixed kam parameter
    get_labels_with_path = partial(get_labels, kam=kam)

    # Process chunks in parallel
    with Pool(processes=num_processes) as pool:
        results = []
        for i, result in enumerate(pool.imap_unordered(get_labels_with_path, chunks)):
            results.append(result)
            print(f"Progress: {i+1}/{len(chunks)} chunks processed")
            print(result)

    # Print summary
    successes = sum(1 for r in results if r.startswith("Success"))
    failures = sum(1 for r in results if r.startswith("Failed"))
    errors = sum(1 for r in results if r.startswith("Error"))
    
    print("\nDownload Complete!")
    print(f"Successful downloads: {successes}")
    print(f"Failed requests: {failures}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()