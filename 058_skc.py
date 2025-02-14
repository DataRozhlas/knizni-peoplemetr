import duckdb
import xml.etree.ElementTree as ET
from pathlib import Path
import pyarrow as pa

# Define the namespace
NS = {'marc': 'http://www.loc.gov/MARC21/slim'}

def stream_marc_records(file_path):
    """Stream MARC records to avoid loading entire file into memory"""
    context = ET.iterparse(file_path, events=('end',))
    for event, elem in context:
        if elem.tag.endswith('record'):
            # Extract relevant fields using proper namespace
            record_data = {
                'id': next((field.text for field in elem.findall('.//marc:controlfield[@tag="008"]', NS)), None),
                'autorstvo_kod': next((subfield.text 
                             for field in elem.findall('.//marc:datafield[@tag="100"]', NS)
                             for subfield in field.findall('.//marc:subfield[@code="7"]', NS)), None),
                'autorstvo': next((subfield.text 
                             for field in elem.findall('.//marc:datafield[@tag="100"]', NS)
                             for subfield in field.findall('.//marc:subfield[@code="a"]', NS)), None),
                'titul': next((subfield.text 
                             for field in elem.findall('.//marc:datafield[@tag="245"]', NS)
                             for subfield in field.findall('.//marc:subfield[@code="a"]', NS)), None),
                
                # Add more fields as needed
            }
            yield record_data
            elem.clear()

# Create DuckDB connection
con = duckdb.connect('data/skc.db')

# Create table
con.execute("""
    CREATE TABLE IF NOT EXISTS marc_records (
        id VARCHAR,
        titul VARCHAR,
        autorstvo VARCHAR,
        autorstvo_kod VARCHAR
    )
""")

# Process in batches
batch_size = 10000
current_batch = []
pocitadlo = 0

for record in stream_marc_records('downloads/skc.xml'):
    current_batch.append(record)
    if len(current_batch) >= batch_size:
        pocitadlo += 1
        print(f"Ukládám batch {pocitadlo}.")
        # Convert batch to Arrow table and insert
        arrow_table = pa.Table.from_pylist(current_batch)
        con.execute("INSERT INTO marc_records (id, titul, autorstvo, autorstvo_kod) SELECT id, titul, autorstvo, autorstvo_kod FROM arrow_table")
        current_batch = []

# Insert remaining records
if current_batch:
    arrow_table = pa.Table.from_pylist(current_batch)
    con.execute("INSERT INTO marc_records SELECT * FROM arrow_table")

