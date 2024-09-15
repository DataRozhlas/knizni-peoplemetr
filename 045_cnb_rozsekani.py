import xml.etree.ElementTree as ET

ET.register_namespace('', "http://www.loc.gov/MARC21/slim")

def create_new_file(records, file_number):
  # Create a new XML file
  root = ET.Element("{http://www.loc.gov/MARC21/slim}collection",
                     # xmlns="http://www.loc.gov/MARC21/slim",
                      xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                      xsi_schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd")

  # Add each record to the new file
  for record in records:
    root.append(record)  # Append the element directly to the root
    
  # Write the XML file
  tree = ET.ElementTree(root)  
  tree.write(f"cnb_{file_number}.xml", encoding="UTF-8", xml_declaration=True)

  # Clear the records list to free up memory
  records.clear()

# Initialize variables
records = []
file_number = 1

# Parse the XML file incrementally
for event, elem in ET.iterparse(os.path.join("downloads/cnb.xml","cnb.xml"), events=("end",)):
  if elem.tag == "{http://www.loc.gov/MARC21/slim}record":
    records.append(elem)

  if len(records) == 10000:
    create_new_file(records, file_number)
    records = []
    file_number += 1

# Create a file for any remaining records
if records:
  create_new_file(records, file_number)
