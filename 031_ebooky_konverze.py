import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import os
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup

    return BeautifulSoup, ebooklib, epub, os


@app.cell
def _():
    odkud = "downloads/ebooky-martinus"
    return (odkud,)


@app.cell
def _():
    kam = "data_raw/ebooky"
    return (kam,)


@app.cell
def _(kam, os):
    os.makedirs(kam, exist_ok=True)
    return


@app.cell
def _(BeautifulSoup, ebooklib):
    def epub_txt(surovky_ebook):
        ukazka = ""
        for item in surovky_ebook.get_items():
            try:
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    if len(soup.text) > 0:
                        ukazka += soup.text.strip().strip()
            except:
                pass
        if len(ukazka.split("ISBN")[-1]) > 9000:
            ukazka = ukazka.split("ISBN")[-1]
        try:
            ukazka = "\n".join([x for x in ukazka.splitlines()[1:] if (x.strip() != "") and (x.strip() != "Konec ukázky")])
        except:
            pass
        return ukazka

    return (epub_txt,)


@app.cell
def _():
    # sebook = epub.read_epub(os.path.join("downloads/ebooky-martinus","9788076621473.epub"))
    return


@app.cell
def _(epub, epub_txt, kam, odkud, os):
    for ipab in [x for x in os.listdir(odkud) if x.split('.')[1] == 'epub']:
        if ipab not in [x.replace('.txt','.epub') for x in os.listdir(kam)]:
            try:
                with open(os.path.join(kam, f"{ipab.split('.')[0]}.txt"), "w+", encoding="utf-8") as export:
                    print(ipab)
                    export.write(epub_txt(epub.read_epub(os.path.join(odkud,ipab))))
            except Exception as E:
                print(E)
    return


if __name__ == "__main__":
    app.run()
