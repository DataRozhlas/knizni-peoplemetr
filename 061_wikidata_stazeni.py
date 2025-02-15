# Skript stáhne JSONy s daty z Wikidat. Při prvním běhu jich
# bude přes 100 tisíc.

import os
import json
import requests
import pandas as pd
import gc
from multiprocessing import Pool, cpu_count
from functools import partial
import time
from typing import List, Set
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('data_raw','wikidata_download.log')),
        logging.StreamHandler()
    ]
)

def get_wikidata_json(entity_id: str, kam: str, retries: int = 3, initial_delay: int = 5) -> bool:
    """
    Download Wikidata JSON with adaptive retries and specific error handling.
    """
    for attempt in range(retries):
        try:
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
            response = requests.get(url, timeout=(30, 45))
            
            if response.status_code == 200:
                output_path = os.path.join(kam, f"{entity_id}.json")
                try:
                    with open(output_path, "w+", encoding="utf-8") as file:
                        json.dump(response.json(), file, ensure_ascii=False, indent=4)
                    logging.info(f"Data for id {entity_id} downloaded successfully")
                    return True
                except IOError as e:
                    logging.error(f"Failed to write file for {entity_id}: {str(e)}")
                    time.sleep(2)
                    continue
                    
            elif response.status_code == 429:
                delay = initial_delay * (2 ** attempt)
                logging.warning(f"Rate limit hit for {entity_id}, waiting {delay}s")
                time.sleep(delay)
                continue
            else:
                logging.warning(f"Failed to download {entity_id}: Status {response.status_code}")
                time.sleep(initial_delay)
                continue
                
        except requests.exceptions.RequestException as e:
            delay = initial_delay * (2 ** attempt)
            logging.warning(f"Request error for {entity_id}: {str(e)}")
            time.sleep(delay)
            continue
            
        except Exception as e:
            logging.error(f"Unexpected error downloading {entity_id}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(initial_delay * (attempt + 1))
                continue
            
    return False

def load_existing_downloads(kam: str) -> Set[str]:
    """Safely load existing downloads."""
    try:
        return set(f.replace('.json', '') for f in os.listdir(kam) if f.endswith('.json'))
    except OSError as e:
        logging.error(f"Error reading directory {kam}: {str(e)}")
        return set()

def process_batch(entities: List[str], kam: str, batch_size: int = 100) -> None:
    """Process a batch of entities with proper error handling and adaptive batch sizing."""
    num_processes = min(cpu_count(), 4)
    current_batch_size = batch_size
    
    for i in range(0, len(entities), current_batch_size):
        batch = entities[i:i + current_batch_size]
        logging.info(f"Processing batch {i//current_batch_size + 1}, size: {current_batch_size}")
        
        try:
            with Pool(num_processes) as pool:
                get_wikidata_partial = partial(get_wikidata_json, kam=kam)
                results = pool.map(get_wikidata_partial, batch)
                
            successful = sum(1 for r in results if r)
            failure_rate = (len(batch) - successful) / len(batch)
            
            if failure_rate > 0.5:
                current_batch_size = max(10, current_batch_size // 2)
                logging.info(f"High failure rate detected, reducing batch size to {current_batch_size}")
                time.sleep(30)
            elif current_batch_size < batch_size:
                current_batch_size = min(batch_size, current_batch_size * 2)
                logging.info(f"Success rate improved, increasing batch size to {current_batch_size}")
            
            logging.info(f"Batch complete: {successful}/{len(batch)} successful")
            
        except Exception as e:
            logging.error(f"Batch processing error: {str(e)}")
            current_batch_size = max(10, current_batch_size // 2)
            time.sleep(60)
            continue

def process_wikidata_ids(autority: pd.DataFrame) -> List[str]:
    """Process and deduplicate Wikidata IDs."""
    try:
        aut_wikids = autority[autority["024_2"] == "wikidata"]["024_a"].drop_duplicates(keep="first")
        aut_wikids = aut_wikids[~aut_wikids.index.duplicated(keep="first")]
        
        try:
            chybejici = [f for f in os.listdir("data_raw/wikidata_doplneni")]
            print(f"V předchozím kroku doplněno extra {len(chybejici)} ids přes hledání na https://query.wikidata.org/sparql")
        except OSError:
            chybejici = []
            
        doplneni = []
        for c in chybejici:
            if "Q" in c.split("_")[1]:
                doplneni.append({
                    "001": c.split("_")[0],
                    "024_a": c.split("_")[1].split(".")[0]
                })
        
        wikiny_audiny = pd.concat([
            pd.DataFrame(aut_wikids),
            pd.DataFrame(doplneni).set_index("001")
        ])
        wikiny_audiny = wikiny_audiny[~wikiny_audiny.index.duplicated(keep="first")]
        
        wikiny_audiny.to_json(os.path.join("data_raw", "autority_wikidataids.json"))
        
        finalni_seznam = wikiny_audiny["024_a"].drop_duplicates().tolist()
        
#        finalni_seznam = [w.replace(')','').replace('(','').replace('-','').replace('0000000','').replace('|','') for w in finalni_seznam]
#        finalni_seznam = ['Q' + w for w in finalni_seznam if 'Q' not in w]

        return finalni_seznam

    except Exception as e:
        logging.error(f"Error processing Wikidata IDs: {str(e)}")
        raise

def main():
    try:
        kam = "downloads/wikidata/autority"
        os.makedirs(kam, exist_ok=True)
        
        # Load and prepare data
        autority = pd.read_parquet(os.path.join("data", "aut_vyber.parquet"))
        autority = autority[autority["024_2"].notnull() & autority["024_a"].notnull()]
        autority = autority.explode(["024_a", "024_2"])
        
        # Process Wikidata IDs
        wikids = process_wikidata_ids(autority)
        
        # Get existing downloads
        downloaded = load_existing_downloads(kam)
        logging.info(f"{len(downloaded)} JSON files already downloaded")
        
        # Determine what needs to be downloaded
        to_download = [x for x in reversed(wikids) if x not in downloaded]
        logging.info(f"{len(to_download)} JSON files remaining to download")
        
        # Process in batches
        process_batch(to_download, kam)
        
        # Final verification
        final_downloaded = load_existing_downloads(kam)
        success_rate = len(final_downloaded) / len(wikids) * 100
        logging.info(f"Download complete. Success rate: {success_rate:.2f}%")
        
    except Exception as e:
        logging.error(f"Critical error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()