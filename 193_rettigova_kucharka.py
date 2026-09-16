import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import re
    import marimo as mo
    import polars as pl
    import simplemma

    return mo, pl, re, simplemma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Domácí kuchařka_ ručně stažena odtud: https://www.mlp.cz/katalog/titul/domaci-kucharka/3369879
    """)
    return


@app.cell
def _():
    with open(
        "downloads/rettigova/domaci_kucharka.txt", "r", encoding="utf-16"
    ) as f:
        rettigova = f.read().split("Polívky masité")[1].split("Dodatek.")[0]
    return (rettigova,)


@app.cell
def _(rettigova):
    print(rettigova)
    return


@app.cell
def _(rettigova):
    byl_recept = False
    recepty = []  # Změněno na seznam (list)

    for radek in rettigova.splitlines():
        if radek[0:1].isdigit():
            # Uložíme očištěný název a rovnou přidáme nový slovník do seznamu
            nazev = radek.strip().strip(".")
            recepty.append({"nazev": nazev, "recept": ""})
            byl_recept = True

        elif byl_recept:
            # Přesunul jsem kontrolu prázdného řádku sem, aby se na konec receptu
            # nepřidávala zbytečná mezera předtím, než se čtení receptu ukončí.
            if radek == "":
                byl_recept = False
            else:
                # Upravujeme hodnotu "recept" u POSLEDNÍHO slovníku v seznamu
                if recepty[-1]["recept"]:
                    recepty[-1]["recept"] += " " + radek.strip()
                else:
                    recepty[-1]["recept"] = radek.strip()
    return (recepty,)


@app.cell
def _(recepty):
    recepty
    return


@app.cell
def _(recepty):
    len(recepty)
    return


@app.cell
def _(re, simplemma):
    def lematizuj(retezec):
        try:
            return list(
                set(
                    [
                        simplemma.lemmatize(
                            re.sub(r"[.,\:?!„“()]", "", slovo.strip()), lang="cs"
                        ).lower()
                        for slovo in retezec.split(" ")
                        if len(slovo) > 1
                    ]
                )
            )
        except Exception as e:
            print(f"{retezec}: {e}")
            return None

    return (lematizuj,)


@app.cell
def _(lematizuj, pl, recepty):
    df = pl.DataFrame(recepty).with_columns(
        pl.col("recept")
        .str.to_lowercase()
        .map_elements(lematizuj, return_dtype=pl.List(inner=pl.String))
        .alias("recept_lemma"),
        pl.col("nazev")
        .str.to_lowercase()
        .map_elements(lematizuj, return_dtype=pl.List(inner=pl.String))
        .alias("nazev_lemma"),
    )

    df
    return (df,)


@app.cell
def _(df, pl):
    df.with_columns(
        pl.col("nazev").str.extract(r"pro\s+(.*?)\s+osob").alias("osob")
    ).filter(pl.col("osob").is_not_null())
    return


@app.cell
def _(df, pl):
    df.explode("recept_lemma").group_by("recept_lemma").len().filter(
        pl.col("recept_lemma").str.len_chars() >= 3
    ).sort(by="len", descending=True)
    return


@app.cell
def _():
    return


@app.cell
def _(df, pl):
    ", ".join(
        df.explode("nazev_lemma")
        .group_by("nazev_lemma")
        .len()
        .filter((pl.col("nazev_lemma").str.len_chars() >= 3) & (pl.col("len") > 5))
        .sort(by="len", descending=True)
        .select(pl.col("nazev_lemma"))
        .to_series()
        .to_list()
    )
    return


@app.cell
def _(df, pl):
    ", ".join(
        df.explode("nazev_lemma")
        .group_by("nazev_lemma")
        .len()
        .filter((pl.col("nazev_lemma").str.len_chars() >= 3) & (pl.col("len") < 3))
        .sort(by="len", descending=True)
        .select(pl.col("nazev_lemma"))
        .to_series()
        .to_list()
    )
    return


@app.cell
def _():
    kuriozity = [
        "vemeno",
        "vemínko",
        "mozek",
        "mozeček",
        "rak",
        "škeble",
        "mušle",
        "šnek",
        "žába",
        "žabí",
        "kvíčala",
        "tetřev",
        "sluka",
        "slučí",
        "indigo",
        "fialkový",
        "dřišťál",
        "kdoule",
        "lanýž",
        "smrž",
        "želva",
        "želví",
        "mník",
        "lastura",
        "vydra",
        "skřiv",
        "piskoř"
    ]
    return (kuriozity,)


@app.cell
def _(df, kuriozity, pl):
    df.explode("nazev_lemma").group_by("nazev_lemma").len().filter(
        (pl.col("nazev_lemma").str.len_chars() >= 3)
        & (pl.col("nazev_lemma").str.contains_any(kuriozity))
    ).sort(by="len", descending=True)
    return


@app.cell
def _(df, pl):
    df.explode("nazev_lemma").group_by("nazev_lemma").len().filter(
        pl.col("nazev_lemma").str.len_chars() >= 3
    ).sort(by="len", descending=True)
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)hňup"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)sardel"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)kapr[^l]"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)špargl"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)karfio"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("nazev").str.contains("(?i)neprav"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("nazev").str.contains("(?i)šne[kčc]"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept").str.contains("(?i)olej"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("recept_lemma").list.contains("sádlo"))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
