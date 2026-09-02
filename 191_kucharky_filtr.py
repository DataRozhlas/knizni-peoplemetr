import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import altair as alt

    return (pl,)


@app.cell
def _(pl):
    pouzivane_sloupce_full = [
        "008",
        "100_a",
        "072_x",
        "245_a",
        "246_a",
        "260_b",
        "264_b",
        "490_a",
        "650_a",
        "655_a",
        "001"
    ]

    pouzivane_sloupce = sorted(set(x[0:3] for x in pouzivane_sloupce_full if x != '001'))

    print(pouzivane_sloupce)

    df = pl.read_parquet(f"data/cnb_sloupce/{pouzivane_sloupce[0]}.parquet")
    lf = pl.scan_parquet(f"data/cnb_sloupce/{pouzivane_sloupce[0]}.parquet")

    for sloupec in pouzivane_sloupce[1:]:
        df = df.join(
            pl.read_parquet(f"data/cnb_sloupce/{sloupec}.parquet"),
            how="left",
            on="001",
        )

        lf = lf.join(
            pl.scan_parquet(f"data/cnb_sloupce/{sloupec}.parquet"),
            how="left",
            on="001",
        )
    return df, lf


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)kuchař"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)kluci v akci"))
    return


@app.cell
def _(lf, pl):
    ids_kucharek = set()

    sloupec_keyword_pozitivni = [
        ("072_x", "Kuchařství. Potraviny. Vařená jídla"),
        ("246_a", "kuchařka"),
        ("650_a", "jídla"),
        ("650_a", "meals"),
        ("650_a", "kuchařství"),
        ("655_a", "kuchařské recepty"),
        ("655_a", "cookbooks"),
        ("245_a", "recept[^á]"),
        ("245_a", "kuchař"),
        ("245_a", "pečeme"),
        ("245_a", "vaříme"),
        ("245_a", "dieta"),
        ("245_a", "moučník"),
        ("245_a", "dietní"),
        ("245_a", "obědy"),
        ("245_a", "večeře"),
        ("245_a", "těstovin"),
        ("245_a", "vegetariánsk"),
        ("245_a", "bezmas"),
        ("245_a", "vegansk"),
        ("245_a", "pečivo"),
        ("245_a", "de[zs]ert[^éoa]"),
        ("245_a", "pokrm[yů]"),
        ("245_a", "pomazán[ek]"),
        ("245_a", "salát"),
        ("245_a", "gril(ov|ujem)"),
        ("245_a", " uzení"),
        ("245_a", "barbecue"),
        ("245_a", "smažíme"),
        ("245_a", "polév"),
        ("245_a", "zavařování"),
        ("245_a", "nakládání"),
        ("245_a", "cukroví"),
        ("490_a", "dobrou chuť"),
        ("650_a", "moučníky"),
        ("650_a", "míšené nápoje"),
        ("650_a", "pečivo"),
        ("650_a", "grilov"),
        ("650_a", "uzení"),
        ("650_a", "zabíjačka"),
        ("650_a", "konzervování masa"),
        ("650_a", "nakládání masa"),
        ("650_a", "sušení potravin"),
        ("650_a", "konzervování ovoce"),
        ("650_a", "zmrzliny"),
    ]

    filtry_pozitivni = [
        lf.with_columns(pl.concat_list(pl.col("245_a")).alias("245_a"))
        .explode(kombo[0], empty_as_null=True)
        .filter(pl.col(kombo[0]).str.contains(f"(?i){kombo[1]}"))
        for kombo in sloupec_keyword_pozitivni
    ]

    for filtr in filtry_pozitivni:
        ids_kucharek = ids_kucharek | set(
            filtr.select(pl.col("001")).collect().to_series().to_list()
        )

    sloupec_keyword_negativni = [
        #    ("653_a", "ekonomické předměty"),
        ("072_x", "próza"),
        ("072_x", "software"),
        ("072_x", "drama"),
        ("260_b", "Českobratrský evang. seniorátní úřad"),
        ("490_a", "Lidové hry českého jeviště"),
        ("245_a", "Receptář pro fotoamatéry"),
        ("245_a", "100 praktických receptů pro holiče a kadeřníky"),
        ("650_a", "odpad"),
        ("655_a", "časopis"),
        ("655_a", "hudba"),
        ("655_a", "písně"),
        ("490_a", "Švejdův divadelní sborník"),
        ("264_b", "Knihovna odborného listu Dusík"),
    ]

    filtry_negativni = [
        lf.with_columns(pl.concat_list(pl.col("245_a")).alias("245_a"))
        .explode(kombo[0], empty_as_null=True)
        .filter(pl.col(kombo[0]).str.contains(f"(?i){kombo[1]}"))
        for kombo in sloupec_keyword_negativni
    ]

    for filtr in filtry_negativni:
        ids_kucharek = ids_kucharek - set(
            filtr.select(pl.col("001")).collect().to_series().to_list()
        )

    len(ids_kucharek)
    return (ids_kucharek,)


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)receptář"))
    return


@app.cell
def _(df, ids_kucharek, pl):
    df_kucharky = df.filter(pl.col("001").is_in(ids_kucharek))
    df_kucharky.sample(len(df_kucharky))
    return (df_kucharky,)


@app.cell
def _(df_kucharky, pl):
    df_kucharky.with_columns(
        pl.col("245_a").str.to_lowercase().str.split(" ")
    ).explode("245_a", empty_as_null=True).group_by("245_a").len().sort(
        by="len", descending=True
    )
    return


@app.cell
def _(df_kucharky, pl):
    df_kucharky.filter(pl.col("100_a").str.contains("Rettig"))
    return


@app.cell
def _(df_kucharky, pl):
    testy = [
        "Muž v zástěře",
        "Basic cooking",
        "Kuchařka pro dceru",
        "Kluci v akci",
        "Python",
    ]

    for t in testy:
        print(
            df_kucharky.filter(pl.col("245_a").str.contains(t)).select(
                pl.col(["100_a", "245_a", "246_a"])
            )
        )
    return


@app.cell
def _(df_kucharky):
    df_kucharky.write_parquet("data/cnb_kucharky.parquet")
    return


if __name__ == "__main__":
    app.run()
