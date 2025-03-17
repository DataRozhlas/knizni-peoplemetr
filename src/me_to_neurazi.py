import os
from lxml import etree
import polars as pl
import altair as alt
from scour import scour

def me_to_neurazi(
    graf: alt.vegalite.v5.api.LayerChart, kredity: str, soubor: str, slozka="grafy", zvetseni=1.5
):

    def concatenate_svg_vertically(image1_path, image2_path, output_path):
        with open(image1_path, "r", encoding="utf-8") as f:
            svg1 = etree.parse(f)
        with open(image2_path, "r", encoding="utf-8") as f:
            svg2 = etree.parse(f)
        root1 = svg1.getroot()
        root2 = svg2.getroot()
        width1 = int(root1.get("width", "0").replace("px", "").split('.')[0])
        height1 = int(root1.get("height", "0").replace("px", "").split('.')[0])
        width2 = int(root2.get("width", "0").replace("px", "").split('.')[0])
        height2 = int(root2.get("height", "0").replace("px", "").split('.')[0])
        new_width = max(width1, width2)
        new_height = height1 + height2
        new_svg = etree.Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=f"{new_width}px",
            height=f"{new_height}px",
        )
        background = etree.Element(
            "rect", width=str(new_width), height=str(new_height), fill="white"
        )
        new_svg.append(background)
        group1 = etree.Element("g", transform="translate(0,0)")
        for child in root1:
            group1.append(child)
        x_offset = new_width - width2
        group2 = etree.Element("g", transform=f"translate({x_offset},{height1})")
        for child in root2:
            group2.append(child)
        new_svg.append(group1)
        new_svg.append(group2)
        with open(output_path, "wb") as f:
            f.write(
                etree.tostring(
                    new_svg, pretty_print=True, encoding="utf-8", xml_declaration=True
                )
            )
    
    os.makedirs(slozka, exist_ok=True)

    try:
        os.remove(f"{slozka}/{soubor}.svg")
    except Exception as e:
        pass
    
    graf.save(f"{slozka}/{soubor}_temp1.svg", scale_factor=zvetseni)
    try:
        alternativni_text = f"""Graf s titulkem „{graf['title']['text']}“. Další texty by měly být čitelné ze zdrojového souboru SVG."""
    except Exception as e:
        alternativni_text = "Omlouváme se, ale alternativní text se nepodařilo vygenerovat. Texty v grafu by měly být čitelné ze zdrojového souboru SVG."

    spodni = pl.DataFrame({"text": [kredity]})
    spodni = (
        alt.Chart(spodni.to_pandas(), width=200, height=15, padding=0)
        .encode(x=alt.value(200), text=alt.Text("text:N"))
        .mark_text(
            fontSize=8, font="Asap", color='#292829', baseline="line-top", align="right", dx=0
        )
        .configure_view(stroke="transparent")
    )
    spodni.save(f"{slozka}/{soubor}_temp2.svg", scale_factor=zvetseni)

    concatenate_svg_vertically(
        f"{slozka}/{soubor}_temp1.svg", f"{slozka}/{soubor}_temp2.svg", f"{slozka}/{soubor}.svg"
    )

    options = scour.sanitizeOptions()
    options.digits = 2
    options.strip_ids = True
    options.strip_comments = True
    options.remove_metadata = True
    options.enable_viewboxing = True

    try:
        os.remove(f"{slozka}/{soubor}_orig.svg")
    except:
        pass
    os.rename(f"{slozka}/{soubor}.svg", f"{slozka}/{soubor}_orig.svg")

    with open(f"{slozka}/{soubor}_orig.svg", 'r', encoding="utf-8") as f:
        svg_data = f.read()
    output = scour.scourString(svg_data, options)
    with open(f"{slozka}/{soubor}.svg", 'w+', encoding="utf-8") as f:
        f.write(output)

    info = f"""<figure>
    <a href="https://data.irozhlas.cz/knihy-grafy/{soubor}.svg" target="_blank">
    <img src="https://data.irozhlas.cz/knihy-grafy/{soubor}.svg" width="100%" alt="{alternativni_text}" />
    </a>
    </figure>""" 
    print(info)
    
    with open(f"{slozka}/{soubor}.txt", 'w+', encoding="utf-8") as instrukce:
        instrukce.write(info)
    
    os.remove(f"{slozka}/{soubor}_temp1.svg")
    os.remove(f"{slozka}/{soubor}_temp2.svg")