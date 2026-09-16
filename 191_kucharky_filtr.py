import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl

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
        "041_h",
        "264_b",
        "490_a",
        "650_a",
        "655_a",
        "001",
        "300_a",
        "264_a",
        "264_b",
        "260_a",
        "260_b",
    ]

    pouzivane_sloupce = sorted(
        set(x[0:3] for x in pouzivane_sloupce_full if x != "001")
    )

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
    df.filter(pl.col("100_a").str.contains("Hejlík, Lu"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)gastro"))
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
        ("650_a", r"(?i)jídla"),
        ("650_a", r"(?i)meals"),
        ("650_a", r"(?i)kuchařství"),
        ("655_a", r"(?i)kuchařské recepty"),
        ("655_a", r"(?i)cookbooks"),
        ("245_a", r"(?i)recept[^á\s]"),
        ("245_a", r"(?i)kuchařk"),
        ("245_a", r"(?i)kuchařsk"),
        ("245_a", r"(?i)pečeme"),
        ("245_a", r"(?i)[^\w]pečení"),
        ("245_a", r"(?i)vaříme"),
        ("245_a", r"(?i)vaření"),
        ("245_a", r"(?i)dieta"),
        ("245_a", r"(?i)moučník"),
        ("245_a", r"(?i)dietn[ěía]"),
        ("245_a", r"(?i)obědy"),
        ("245_a", r"(?i)večeře"),
        ("245_a", r"(?i)těstovin"),
        ("245_a", r"(?i)vegetariánsk"),
        ("245_a", r"(?i)bezmas"),
        ("245_a", r"(?i)vegansk"),
        ("245_a", r"(?i)pečivo"),
        ("245_a", r"(?i)de[zs]ert[^éoa]"),
        ("245_a", r"(?i)pokrm[yů]"),
        ("245_a", r"(?i)pomazán[ek]"),
        ("245_a", r"(?i)salát"),
        ("245_a", r"(?i)v .{0,20} kuchyni"),
        ("245_a", r"(?i)z konzerv"),
        ("245_a", r"(?i)gril(ov|ujem)"),
        ("245_a", r"(?i) uzení"),
        ("245_a", r"(?i)barbecue"),
        ("245_a", r"(?i)smažíme"),
        ("245_a", r"(?i)polév"),
        ("245_a", r"(?i)kuchyně"),
        ("245_a", r"(?i)specialit[^a]"),
        ("245_a", r"(?i)zavařování"),
        ("245_a", r"(?i)nakládání"),
        ("245_a", r"(?i)cukroví"),
        ("490_a", r"(?i)dobrou chuť"),
        ("650_a", r"(?i)moučníky"),
        ("650_a", r"(?i)míšené nápoje"),
        ("650_a", r"(?i)pečivo"),
        ("650_a", r"(?i)grilov"),
        ("650_a", r"(?i)uzení"),
        ("650_a", r"(?i)zabíjačka"),
        ("650_a", r"(?i)kon[zs]ervování masa"),
        ("650_a", r"(?i)nakládání masa"),
        ("650_a", r"(?i)sušení potravin"),
        ("650_a", r"(?i)kon[sz]ervování ovoce"),
        ("650_a", r"(?i)zmrzliny"),
    ]

    filtry_pozitivni = [
        lf.with_columns(
            pl.concat_list(pl.col("245_a")).alias("245_a"),
            pl.concat_list(pl.col("008")).alias("008"),
        )
        .explode(kombo[0], empty_as_null=True)
        .filter(pl.col(kombo[0]).str.contains(kombo[1]))
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
        ("072_x", "poezie"),
        ("072_x", "drama"),
        ("072_x", "doprava"),
        ("072_x", "hudba"),
        ("260_b", "Českobratrský evang. seniorátní úřad"),
        ("490_a", "Lidové hry českého jeviště"),
        ("245_a", "Receptář pro fotoamatéry"),
        ("245_a", "100 praktických receptů pro holiče a kadeřníky"),
        ("245_a", "vévodkyně"),
        ("245_a", r"(?i)minecraft"),
        ("245_a", "Organizace evidence"),
        ("245_a", "(?i)farmakologi"),
        ("245_a", "(?i)kon[sz]ervatoř"),
        ("245_a", "(?i)kon[sz]ervativní"),
        ("245_a", "pro duši"),
        ("245_a", r"(?i)poslední večeře"),
        ("245_a", "rozvozu hotových jídel z centrálních výroben"),
        ("245_a", "aukce"),
        ("245_a", "Obsluha v restauracích"),
        ("245_b", "dějství"),
        ("650_a", "odpad"),
        ("650_a", "zbraně"),
        ("655_a", "časopis"),
        ("655_a", "hudba"),
        ("655_a", "písně"),
        ("490_a", "Švejdův divadelní sborník"),
        ("264_b", "Knihovna odborného listu Dusík"),
        ("246_b", "aktě"),
        ("260_b", "Průmyslové vydavatelství"),
        ("260_b", "Výzkumný ústav pro stavebnictví a architekturu"),
    ]

    filtry_negativni = [
        lf.with_columns(
            pl.concat_list(pl.col("245_a")).alias("245_a"),
            pl.concat_list(pl.col("245_b")).alias("245_b"),
            pl.concat_list(pl.col("008")).alias("008"),
        )
        .explode(kombo[0], empty_as_null=True)
        .filter(pl.col(kombo[0]).str.contains(kombo[1]))
        for kombo in sloupec_keyword_negativni
    ]

    for filtr in filtry_negativni:
        ids_kucharek = ids_kucharek - set(
            filtr.select(pl.col("001"))
            .collect(engine="streaming")
            .to_series()
            .to_list()
        )

    len(ids_kucharek)
    return (ids_kucharek,)


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)kuchyně"))
    return


@app.cell
def _(df, ids_kucharek, pl):
    df_kucharky = df.filter(pl.col("001").is_in(ids_kucharek)).filter(
        pl.col("008").str.contains("cze")
    )
    df_kucharky.sample(len(df_kucharky))
    return (df_kucharky,)


@app.cell
def _(df_kucharky, pl):
    df_kucharky.explode("260_b").filter(pl.col("260_b").str.contains("Průmyslové"))
    return


@app.cell
def _(df_kucharky, pl):
    df_kucharky.explode("260_b").filter(pl.col("260_b").str.contains("spisovatel"))
    return


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
    df_kucharky.filter(pl.col("245_a").str.contains("sociál"))
    return


@app.cell
def _(df_kucharky, pl):
    testy = [
        "Muž v zástěře",
        "Basic cooking",
        "Kuchařka pro dceru",
        "Kluci v akci",
        "Můžu ochutnat",
        "Kniha plná jídla",
        "(?i)káva",
        # "Python",
        # "Minecraft",
        "Jaro v naší kuchyni",
        "Vaříme pro nemocné chorobami",
        "Receptury studených pokrmů",
        "Normy studené kuchyně",
        "Nová kuchyně",
        "Zavařování masa v domácnosti",
        "Domácí konservace",
        "Zmrazené potraviny",
        "Rychle a chutně z konzerv",
        "Zvěřina do naší kuchyně",
        "Kuchařský lexikon",
        "Čínská kuchyně",
        "Počítání nudliček v jarní polévce",
        "Gastronomický cestopis",
        "Exotika v družstevní kuchyni",
        "Houby v kuchyni",
        "Víkendové jídelníčky",
        "70 domácích polévek",
        "70 vaječných jídel",
        "Vaří šéfkuchař",
        "Konservování potravin v domácnostech",
        "Mléčné speciality",
        "Více sýrů na náš stůl",
        "Vydatné pokrmy",
        "Rychlé pokrmy",
        "Za pět minut dvanáct",
        "Zelenina v naší kuchyni",
        "Grilovaná jídla",
        "Skandinávská kuchyně",
        "Slavnostní příležitosti",
        "Zeleninová mísa",
        "Dneska vařím já",
        "Kuchyně labužníka",
        "Ruská kuchyně",
        "Výživa nejmenších dětí",
        "Z hotelu Ritz",
        "Retrojídlo",
        "Praktické rady pro hospodyně a matky",
        "Králičí maso v české kuchyni",
        "Kuře na sto způsobů",
        "70 bramborových jídel",
    ]

    chybi = []

    print(len(testy))

    for t in testy:
        vyfiltr = df_kucharky.filter(pl.col("245_a").str.contains(t)).select(
            pl.col(["100_a", "245_a", "246_a"])
        )
        # print("***")
        # print(t)
        # print(vyfiltr)
        if len(vyfiltr) == 0:
            chybi.append(t)

    chybi
    return (chybi,)


@app.cell
def _(chybi, df, pl):
    df.filter(pl.col("245_a").str.contains_any(chybi))
    return


@app.cell
def _(df_kucharky, pl):
    nemely_by_byt = [
        "farmakolog",
        "Minecraft",
        "Python",
        "Kuřecí polévka pro duši",
        "Slepičí polévka pro duši",
        "Poslední večeře",
        "poslední večeře"
    ]

    df_kucharky.filter(pl.col("245_a").str.contains_any(nemely_by_byt))
    return


@app.cell
def _(df_kucharky, pl):
    nalezene_kucharky = df_kucharky.select(pl.col("245_a")).to_series().to_list()
    return (nalezene_kucharky,)


@app.cell
def _(df, nalezene_kucharky, pl):
    df.filter(
        pl.col("245_a").str.contains("(?i)flambo")
        & (~pl.col("245_a").str.contains_any(nalezene_kucharky))
    )
    return


@app.cell
def _(nalezene_kucharky):
    [x for x in nalezene_kucharky if "Flambo" in x]
    return


@app.cell
def _(chybi, df, pl):
    df.filter(pl.col("245_a").str.contains_any(chybi))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("100_7").str.contains("jk01023273"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains(" jídel[^e]")).select(pl.col("245_a"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("konserv")).select(pl.col("245_a"))
    return


@app.cell
def _(df, pl):
    df.explode("260_b").filter(pl.col("260_b").str.contains("Merkur"))
    return


@app.cell
def _(df_kucharky, pl):
    stats = []
    for c in df_kucharky.columns:
        stats.append(
            {
                "sloupec": c,
                "vyplnenych": len(df_kucharky.filter(pl.col(c).is_not_null())),
            }
        )

    vyhodit = (
        pl.DataFrame(stats)
        .filter(pl.col("vyplnenych") < (len(df_kucharky) / 10))
        .select(pl.col("sloupec"))
        .to_series()
        .to_list()
    )
    return (vyhodit,)


@app.cell
def _():
    import random
    import re


    def pocet_stran(rozsah):
        rozsah = str(rozsah)
        cisla = [x for x in re.findall(r"\d{1,4}\s{0,1}[^v]", rozsah)]
        cisla = [int(re.search(r"\d{1,4}", c).group()) for c in cisla]
        if len(cisla) > 0:
            if max(cisla) < 4000:  # jak primitivní, ale jak účinné
                return max(cisla)


    def najdi_rok(nulaosm):
        if "u" not in nulaosm:
            try:
                return int(nulaosm[7:11])
            except:
                return None
        else:
            try:
                return int(nulaosm[7:10] + str(random.randint(0, 9)))
            except:
                return None


    print(najdi_rok("000706s1926"))
    print(najdi_rok("000706s192u"))
    return najdi_rok, pocet_stran


@app.cell
def _(df_kucharky, najdi_rok, pl, pocet_stran, vyhodit):
    interpunkce = [",", "?", ":", "/", ".", ";", "!", '"']

    df_kucharky_final = (
        df_kucharky.drop(vyhodit)
        .with_columns(
            pl.col("008").map_elements(najdi_rok, return_dtype=int).alias("rok"),
            pl.col("300_a")
            .map_elements(pocet_stran, return_dtype=int)
            .alias("pocet_stran"),
            pl.col("245_a")
            .str.replace_many(interpunkce, ["" for x in interpunkce])
            .str.strip_chars()
            .alias("titul"),
        )
        .sort(by="rok")
    )
    return (df_kucharky_final,)


@app.cell
def _(df_kucharky_final):
    df_kucharky_final
    return


@app.cell
def _(df_kucharky_final):
    df_kucharky_final.write_parquet("data/cnb_kucharky.parquet")
    return


@app.cell
def _(df_kucharky_final, pl):
    df_kucharky_final.with_columns(pl.col("100_a").str.strip_chars(",")).rename(
        {"100_a": "autorstvo"}
    ).select(pl.col(["autorstvo", "titul", "rok", "pocet_stran"])).write_csv(
        "data/cnb_kucharky_kontrola.csv"
    )
    return


if __name__ == "__main__":
    app.run()
