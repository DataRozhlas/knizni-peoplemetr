def me_to_neurazi(image1_path, image2_path, output_path):
    
    from lxml import etree
    
    # Load both SVG files as XML
    with open(image1_path, 'r', encoding='utf-8') as f:
        svg1 = etree.parse(f)

    with open(image2_path, 'r', encoding='utf-8') as f:
        svg2 = etree.parse(f)

    # Extract root elements
    root1 = svg1.getroot()
    root2 = svg2.getroot()

    # Get width & height of both SVGs
    width1 = int(root1.get("width", "0").replace("px", ""))
    height1 = int(root1.get("height", "0").replace("px", ""))
    width2 = int(root2.get("width", "0").replace("px", ""))
    height2 = int(root2.get("height", "0").replace("px", ""))

    # Set new dimensions
    new_width = max(width1, width2)
    new_height = height1 + height2

    # Create a new SVG root element
    new_svg = etree.Element("svg", xmlns="http://www.w3.org/2000/svg",
                            width=f"{new_width}px", height=f"{new_height}px")

    # Append a white background rectangle
    background = etree.Element("rect", width=str(new_width), height=str(new_height), fill="white")
    new_svg.append(background)

    # Create a group for the first SVG (placed at (0,0))
    group1 = etree.Element("g", transform="translate(0,0)")
    for child in root1:
        group1.append(child)

    # Calculate x-offset to align the second image to the right
    x_offset = new_width - width2

    # Create a group for the second SVG (shifted down and aligned right)
    group2 = etree.Element("g", transform=f"translate({x_offset},{height1})")
    for child in root2:
        group2.append(child)

    # Append both groups
    new_svg.append(group1)
    new_svg.append(group2)

    # Write the final UTF-8 encoded SVG file
    with open(output_path, 'wb') as f:
        f.write(etree.tostring(new_svg, pretty_print=True, encoding='utf-8', xml_declaration=True))