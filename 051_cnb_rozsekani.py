# Rozseká XML na menší souborry, které při manipulaci neuvaří laptop.

import os
from lxml import etree as ET

def create_new_file(file_code, records, file_number):

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
    tree.write(os.path.join(f"downloads/{file_code}", f"{file_code}_{file_number:03}.xml"), encoding="UTF-8", xml_declaration=True)
    print(f"Posekané {file_code}_{file_number:03}.xml uloženo.")

    records.clear()

kody = list(set([o.split(".xml")[0] for o in os.listdir("downloads") if len(o.split(".xml")[0]) == 3]))

print(f"Zpracuji tyto datasety NK: {', '.join(kody)}.")

for file_code in kody:

    records = []
    file_number = 1

    if not os.path.exists(f"downloads/{file_code}"):
        os.makedirs(f"downloads/{file_code}")
    
    if len(os.listdir(f"downloads/{file_code}")) > 0:
        for filename in os.listdir(f"downloads/{file_code}"):
            file_path = os.path.join(f"downloads/{file_code}", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Smazány staré soubory v adresáři.")
    else:
        print("Žádné staré soubory v cílovém adresáři.")

    for event, elem in ET.iterparse(os.path.join(f"downloads", f"{file_code}.xml"), events=("end",), tag="{http://www.loc.gov/MARC21/slim}record"):
        records.append(elem)

        if len(records) == 20000:
            create_new_file(file_code, records, file_number)
            elem.clear()
            records = []
            file_number += 1

    # Create a file for any remaining records
    if records:
        create_new_file(file_code, records, file_number)

print("Hotovo!")