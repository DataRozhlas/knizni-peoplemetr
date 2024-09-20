# Rozseká XML na menší souborry, které při manipulaci neuvaří laptop.

import os
from lxml import etree as ET

def create_new_file(records, file_number):
    # Create a new XML file
    root = ET.Element("{http://www.loc.gov/MARC21/slim}collection",
                      nsmap={None: "http://www.loc.gov/MARC21/slim",
                             "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                      attrib={"{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"})

    # Add each record to the new file
    for record in records:
        root.append(record)

    # Write the XML file
    tree = ET.ElementTree(root)
    tree.write(os.path.join("downloads/cnb.xml", f"cnb_{file_number:03}.xml"), encoding="UTF-8", xml_declaration=True)
    print(f"XML č. {file_number} uloženo.")

    # Clear the records list to free up memory
    records.clear()

# Initialize variables
records = []
file_number = 1

# Parse the XML file incrementally
for event, elem in ET.iterparse(os.path.join("downloads/cnb.xml", "cnb.xml"), events=("end",), tag="{http://www.loc.gov/MARC21/slim}record"):
    records.append(elem)

    if len(records) == 20000:
        create_new_file(records, file_number)
        elem.clear()
        records = []
        file_number += 1

# Create a file for any remaining records
if records:
    create_new_file(records, file_number)

print("Hotovo!")