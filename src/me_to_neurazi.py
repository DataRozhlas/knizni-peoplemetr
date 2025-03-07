import os
from lxml import etree
import polars as pl
import altair as alt


def me_to_neurazi(
    graf: alt.vegalite.v5.api.LayerChart, kredity: str, soubor: str, slozka="grafy"
):

    def concatenate_svg_vertically(image1_path, image2_path, output_path):
        with open(image1_path, "r", encoding="utf-8") as f:
            svg1 = etree.parse(f)
        with open(image2_path, "r", encoding="utf-8") as f:
            svg2 = etree.parse(f)
        root1 = svg1.getroot()
        root2 = svg2.getroot()
        width1 = int(root1.get("width", "0").replace("px", ""))
        height1 = int(root1.get("height", "0").replace("px", ""))
        width2 = int(root2.get("width", "0").replace("px", ""))
        height2 = int(root2.get("height", "0").replace("px", ""))
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
    graf.save(f"grafy/{soubor}_temp1.svg")
    try:
        alternativni_text = f"""Graf s titulkem „{graf['title']['text']}“. Další texty by měly být čitelné ze zdrojového souboru SVG."""
    except:
        alternativni_text = "Omlouváme se, ale alternativní text se nepodařilo vygenerovat. Texty v grafu by měly být čitelné ze zdrojového souboru SVG."

    spodni = pl.DataFrame({"text": [kredity]})
    spodni = (
        alt.Chart(spodni.to_pandas(), width=300, height=30)
        .encode(x=alt.value(300), text=alt.Text("text:N"))
        .mark_text(
            fontSize=8, font="Asap", baseline="line-bottom", align="right", dx=0
        )
        .configure_view(stroke="transparent")
    )
    spodni.save(f"grafy/{soubor}_temp2.svg")

    concatenate_svg_vertically(
        f"{slozka}/{soubor}_temp1.svg", f"{slozka}/{soubor}_temp2.svg", f"{slozka}/{soubor}.svg"
    )

#    os.remove(f"{slozka}/{soubor}_temp1.svg")
#    os.remove(f"{slozka}/{soubor}_temp2.svg")

    print(f"""<figure><a href="https://data.irozhlas.cz/knihy-grafy/{soubor}.svg" target="_blank"><img src="https://data.irozhlas.cz/knihy-grafy/{soubor}.svg" width="100%" alt="{alternativni_text}" /></a></figure>""")

    print(f"""<figure><a href="https://michalkasparek.cz/sklad/{soubor}.svg" target="_blank"><img src="https://michalkasparek.cz/sklad/{soubor}.svg" width="100%" alt="{alternativni_text}" /></a></figure>""")