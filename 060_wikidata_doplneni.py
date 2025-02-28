import gc
import os
import json
import requests
import pandas as pd
import concurrent.futures
import time
from tqdm import tqdm  # For progress tracking

# Configuration
MAX_WORKERS = 10  # Adjust based on your system and API rate limits
BATCH_SIZE = 100  # Process data in batches to manage memory
RATE_LIMIT_DELAY = 0.1  # Delay between requests to avoid hitting rate limits

kam = 'data_raw/wikidata_doplneni'
if not os.path.exists(kam):
    os.makedirs(kam)

vsechny_jsony = [f for f in os.listdir(kam)]
vyhledane = set([x.split("_")[0] for x in vsechny_jsony])

# Load and process data
print("Načítám data...")
df = pd.read_parquet(os.path.join("data/cnb_sloupce","100.parquet"))
df = df.explode('100_7')

print(f"Unikátních kódů personálních autorit 100_7: {df['100_7'].nunique()}")

# Get authors with at least one book
opakovane = df.groupby('100_7').size()
opakovane = opakovane.sort_values(ascending=False)
opakovane = opakovane[opakovane > 0].index.to_list()

# Load authorities with existing Wikidata IDs
print("Načítám existující autority...")
autority = pd.read_parquet(os.path.join("data","aut_vyber.parquet"))
autority = autority[autority['024_2'].notnull()]
autority = autority[autority['024_a'].notnull()]
autority = autority.explode(['024_a','024_2'])
autority_s_wikidaty = set(autority[autority['024_2'] == 'wikidata']['024_a'].index.to_list())

# Find authorities that need Wikidata IDs
chybi = [x for x in opakovane if x not in autority_s_wikidaty]

# Free memory
del df
del autority
gc.collect()

# Wikidata SPARQL endpoint
sparql_endpoint = "https://query.wikidata.org/sparql"

# Function to get Wikidata ID from NL CR AUT ID with retry mechanism
def get_wikidata_id(nl_cr_aut_id):
    max_retries = 3
    retry_delay = 2
    
    query = f"""
    SELECT ?item WHERE {{
      ?item wdt:P691 "{nl_cr_aut_id}".
    }}
    """
    
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                sparql_endpoint, 
                params={"query": query}, 
                headers=headers,
                timeout=10  # Set timeout to avoid hanging
            )
            
            if response.status_code == 429:  # Too Many Requests
                wait_time = retry_delay * (2 ** attempt)
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()

            if "results" in data and "bindings" in data["results"]:
                bindings = data["results"]["bindings"]
                if bindings:
                    return bindings[0]["item"]["value"].split("/")[-1]
            return None
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                time.sleep(wait_time)
            else:
                print(f"Error querying Wikidata for {nl_cr_aut_id}: {e}")
                return None
    
    return None

# Process a single authority and save result
def process_authority(nl_cr_aut_id):
    # Skip if already processed
    if nl_cr_aut_id in vyhledane:
        return None
        
    slovnik = {}
    slovnik['100_7'] = nl_cr_aut_id
    
    # Add slight delay to avoid overwhelming the API
    time.sleep(RATE_LIMIT_DELAY)
    
    wikidata_id = get_wikidata_id(nl_cr_aut_id)
    slovnik['024_a'] = wikidata_id if wikidata_id else ""
    
    # Save the result
    with open(os.path.join(kam, f"{nl_cr_aut_id}_{slovnik['024_a']}.json"), "w", encoding="utf-8") as file:
        file.write(json.dumps(slovnik))
    
    return nl_cr_aut_id, wikidata_id

# Filter out already processed authorities
co_stahovat = [x for x in chybi if x not in vyhledane]
total_to_process = len(co_stahovat)

print(f"Zjistím Wikidata IDs pro {total_to_process} personálních autorit pomocí paralelního zpracování.")

# Process in batches to manage memory
results = []
for i in range(0, total_to_process, BATCH_SIZE):
    batch = co_stahovat[i:i+BATCH_SIZE]
    print(f"Zpracovávám dávku {i//BATCH_SIZE + 1}/{(total_to_process+BATCH_SIZE-1)//BATCH_SIZE}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Use tqdm for progress tracking
        future_to_auth = {executor.submit(process_authority, auth_id): auth_id for auth_id in batch}
        
        for future in tqdm(concurrent.futures.as_completed(future_to_auth), total=len(batch)):
            auth_id = future_to_auth[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Chyba při zpracování {auth_id}: {e}")

print(f"Dokončeno. Zpracováno {len(results)} personálních autorit.")

# Print statistics
found_count = sum(1 for _, wikidata_id in results if wikidata_id)
print(f"Nalezeno Wikidata ID: {found_count}")
print(f"Nenalezeno Wikidata ID: {len(results) - found_count}")