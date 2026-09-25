import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import altair as alt
    import simplemma
    import re
    import marimo as mo

    return alt, mo, pl, re, simplemma


@app.cell
def _(pl):
    df = pl.read_parquet("data/cnb_kucharky.parquet")
    return (df,)


@app.cell
def _():
    minimum = ["100_a", "titul", "rok", "pocet_stran"]
    return (minimum,)


@app.cell
def _(df):
    df.sample(100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Produkce podle let
    """)
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("rok") <= 1826)
    return


@app.cell
def _(df):
    len(df.unique(subset=["100_a", "titul"], keep="first"))
    return


@app.cell
def _(df):
    len(df)
    return


@app.cell
def _(df, pl):
    len(
        df.filter(pl.col("rok") > 1826).unique(
            subset=["100_a", "titul"], keep="first"
        )
    )
    return


@app.cell
def _(df, pl):
    len(df.filter(pl.col("rok") > 1826))
    return


@app.cell
def _(alt, df):
    alt.Chart(
        df.unique(subset=["100_a", "titul"], keep="first").group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("rok").is_between(1980, 2000)).unique(
        subset=["100_a", "titul"], keep="first"
    ).group_by("rok").len().sort(by="rok")
    return


@app.cell
def _(alt, df):
    alt.Chart(
        df.explode("041_h").group_by(["041_h", "rok"]).len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"), alt.Color("041_h:N"))
    return


@app.cell
def _(df, pl):
    df_jazyky = (
        df.explode("041_h")
        .filter(pl.col("041_h").is_not_null())
        .group_by(["rok", "041_h"])
        .len()
        .join(
            df.explode("041_h")
            .filter(pl.col("041_h").is_not_null())
            .group_by(["rok"])
            .len(),
            how="left",
            on="rok",
        )
        .with_columns(
            (pl.col("len") / pl.col("len_right")).alias("podil_z_prekladu")
        )
    )

    df_jazyky
    return (df_jazyky,)


@app.cell
def _(df_jazyky, pl):
    df_jazyky.filter(pl.col("rok") >= 1901).sort(
        by=["rok", "len"], descending=[False, True]
    ).unique(subset="rok", keep="first")
    return


@app.cell
def _(alt, df_jazyky, pl):
    alt.Chart(
        df_jazyky.filter(pl.col("rok") > 1900).filter(pl.col("041_h") == "eng")
    ).mark_line().encode(alt.X("rok:Q"), alt.Y("podil_z_prekladu:Q"))
    return


@app.cell
def _(alt, df_jazyky, pl):
    alt.Chart(
        df_jazyky.filter(pl.col("rok") > 1900).filter(pl.col("041_h") == "ger")
    ).mark_line().encode(alt.X("rok:Q"), alt.Y("podil_z_prekladu:Q"))
    return


@app.cell
def _(alt, df_jazyky, pl):
    alt.Chart(
        df_jazyky.filter(pl.col("rok") > 1900).filter(pl.col("041_h") == "rus")
    ).mark_line().encode(alt.X("rok:Q"), alt.Y("podil_z_prekladu:Q"))
    return


@app.cell
def _(alt, df_jazyky, pl):
    alt.Chart(
        df_jazyky.filter(pl.col("rok") > 1900).filter(pl.col("041_h") == "fre")
    ).mark_line().encode(alt.X("rok:Q"), alt.Y("podil_z_prekladu:Q"))
    return


@app.cell
def _(alt, df_jazyky, pl):
    alt.Chart(
        df_jazyky.filter(pl.col("rok") > 1900).filter(pl.col("041_h") == "spa")
    ).mark_line().encode(alt.X("rok:Q"), alt.Y("podil_z_prekladu:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.unique(subset=["100_a", "titul"], keep="first")
        .group_by("rok")
        .len()
        .filter(pl.col("rok") > 1980),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df):
    alt.Chart(df.group_by("rok").len(), width=800).mark_bar().encode(
        alt.X("rok:Q"), alt.Y("len:Q")
    )
    return


@app.cell
def _(df):
    df.group_by("rok").len().sort(by="len", descending=True)
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.group_by("rok").agg(pl.col("pocet_stran").sum()), width=800
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("pocet_stran:Q"))
    return


@app.cell
def _(df, pl):
    df.group_by("rok").agg(pl.col("pocet_stran").sum()).sort(
        by="pocet_stran", descending=True
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Opakovaná vydání
    """)
    return


@app.cell
def _(df):
    df.group_by(["100_a", "titul"]).len().sort(by="len", descending=True)
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("Hrníčková")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df):
    df.group_by("100_a").len().sort(by="len", descending=True)
    return


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Vlachová, Libu")
    ).select(pl.col(minimum)).sort(by="rok")
    return


@app.cell
def _(df):
    df.unique(subset=["100_a", "titul"]).group_by("100_a").len().sort(
        by="len", descending=True
    )
    return


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Poláček, Jiř")
    ).select(pl.col(minimum)).sort(by="rok")
    return


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Vašák, Jaro")
    ).select(pl.col(minimum)).sort(by="rok")
    return


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Hejlík, Lu")
    ).select(pl.col(minimum)).sort(by="rok")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motivy / témata
    """)
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)salát"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)kalor"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)gril"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)gril")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)diet")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)diet")).select(
        pl.col(minimum)
    ).sort(by="rok")
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)frit")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)maďars"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)maďars"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)váno[cč]"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)salát")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(
            pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)")
        )
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)mexi")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl):
    df.filter(
        pl.col("100_a").str.contains("Rettigová")
        & pl.col("245_a").str.starts_with("Dom")
    ).select(pl.col(["titul", "rok"]))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("100_a").str.contains("Sandtnerová")).select(
        pl.col(["titul", "rok"])
    )
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("100_a").str.contains("Sandtnerová")).select(
        pl.col(["titul", "rok"])
    ).group_by("titul").len()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Jazyky
    """)
    return


@app.cell
def _(df):
    df.explode("041_h").group_by("041_h").len().sort(by="len", descending=True)
    return


@app.cell
def _(df, pl):
    top_jazyky = (
        df.explode("041_h")
        .group_by("041_h")
        .len()
        .drop_nulls()
        .sort(by="len", descending=True)
        .head(15)
        .select(pl.col("041_h"))
        .to_series()
        .to_list()
    )
    return (top_jazyky,)


@app.cell
def _(alt, df, pl, top_jazyky):
    alt.Chart(
        df.explode("041_h")
        .filter(pl.col("041_h").is_in(top_jazyky))
        .group_by(["rok", "041_h"])
        .len(),
        width=750,
        height=50,
    ).mark_bar().encode(
        alt.X("rok:Q"), alt.Y("len:Q"), alt.Row("041_h:N", sort=top_jazyky)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Trendy
    """)
    return


@app.cell
def _(df, pl):
    top_slova = (
        df.with_columns(pl.col("titul").str.to_lowercase().str.split(" "))
        .explode("titul")
        .group_by("titul")
        .len()
        .filter(pl.col("len") >= 20)
        .sort(by="len", descending=True)
        .select(pl.col("titul"))
        .to_series()
        .to_list()
    )

    print(len(top_slova))

    ", ".join(top_slova)
    return (top_slova,)


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)mikrovln"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)zdrav")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)těstovin"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)postní"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)konzerv")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)zavařov")).select(pl.col(minimum))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)konzerv"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)[^]a]babič")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)prababič")).select(pl.col(minimum))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)babič"))
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)postní")).filter(
        pl.col("rok") > 1990
    )
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)dieta při")).select(
        pl.col(minimum)
    )
    return


@app.cell
def _(df, pl):
    df.with_columns(pl.col("rok").cast(str).str.slice(0, 3)).group_by(
        "rok"
    ).len().sort(by="rok")
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.with_columns(pl.col("rok").cast(str).str.slice(0, 3))
        .filter(pl.col("245_a").str.contains("(?i)postní"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)půst")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)frit")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl, top_slova):
    df.with_columns(pl.col("titul").str.to_lowercase().str.split(" ")).explode(
        "titul"
    ).filter(pl.col("titul").is_in(top_slova)).group_by("titul").agg(
        pl.col("rok").median()
    ).sort(by="rok")
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
def _(df, lematizuj, pl):
    df_lemma = (
        df.with_columns(
            pl.col("titul")
            .str.to_lowercase()
            .map_elements(lematizuj, return_dtype=pl.List(inner=pl.String))
            .alias("titul_lemma")
        )
        .explode("titul_lemma")
        .with_columns(
            pl.col("titul_lemma").str.replace_many(
                [
                    "indická",
                    "čínská",
                    "grilovat",
                    "babiččin",
                    "babičky",
                    "bezlepková",
                    "babiček",
                    "grilujeme",
                    "vegetariánská",
                    "dietní",
                    "péct",
                    "upéct",
                ],
                [
                    "indický",
                    "čínský",
                    "grilování",
                    "babička",
                    "babička",
                    "bezlepkový",
                    "babička",
                    "grilování",
                    "vegetariánský",
                    "dieta",
                    "pečení",
                    "pečení",
                ],
            )
        )
        .with_columns(
            pl.when(pl.col("titul_lemma").str.starts_with("frit"))
            .then(pl.lit("fritování"))
            .when(pl.col("titul_lemma").str.starts_with("diet"))
            .then(pl.lit("dieta"))
            .when(pl.col("titul_lemma").str.starts_with("vegetar"))
            .then(pl.lit("vegetariánský"))
            .when(pl.col("titul_lemma").str.starts_with("babič"))
            .then(pl.lit("babička"))
            .otherwise(pl.col("titul_lemma"))
            .alias("titul_lemma")
        )
    )

    nejcastejsi_lemma = (
        df_lemma.group_by("titul_lemma")
        .len()
        .filter(pl.col("len") >= 30)
        .select(pl.col("titul_lemma"))
        .to_series()
        .to_list()
    )

    median_temat = (
        df_lemma.group_by("titul_lemma").agg(pl.col("rok").median()).sort(by="rok")
    )

    median_temat.filter(pl.col("titul_lemma").is_in(nejcastejsi_lemma))
    return df_lemma, median_temat


@app.cell
def _(median_temat, pl):
    median_temat.filter(pl.col("titul_lemma").str.contains("frit"))
    return


@app.cell
def _():
    hledat_lemma = [
        "postní",
        "zavařování",
        # 'sušení',
        # 'ovoce',
        #   'marmeláda',
        "polotovar",
        "nakládání",
        #   'sójový',
        "mikrovlnné",
        #    'zácpa',
        "dieta",
        "levný",
        "vánoce",
        "vegetariánský",
        "hubnout",
        "grilování",
        "bezlepkový",
        "babička",
        "norma",
        #   "závodní",
        "pečení",
        "fritování",
    ]
    return (hledat_lemma,)


@app.cell
def _(hledat_lemma, median_temat, pl):
    median_temat.filter(pl.col("titul_lemma").str.contains_any(hledat_lemma)).sort(
        by="rok"
    )
    return


@app.cell
def _(hledat_lemma, median_temat, pl):
    razeni = (
        median_temat.filter(pl.col("titul_lemma").str.contains_any(hledat_lemma))
        .sort(by="rok")
        .select(pl.col("titul_lemma"))
        .to_series()
        .to_list()
    )
    return (razeni,)


@app.cell
def _(df_lemma, hledat_lemma, pl):
    do_grafu = pl.DataFrame()
    for h_lemma in hledat_lemma:
        do_grafu = pl.concat(
            [
                do_grafu,
                df_lemma.filter(
                    pl.col("titul_lemma").str.contains(h_lemma)
                ).with_columns(pl.lit(h_lemma).alias("co")),
            ]
        )

    do_grafu = do_grafu.filter(pl.col("rok") >= 1900).group_by(["co", "rok"]).len()
    return (do_grafu,)


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)postní"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)levn")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)levn")).select(
        pl.col(minimum)
    ).filter(pl.col("rok").is_between(1930, 1940))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)zavařování"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)sváteční"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)babič")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)peče")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)gril")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)smoothi"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Z čeho, s čím, pro koho
    """)
    return


@app.cell
def _(df, pl):
    df_zspro = df.with_columns(
        pl.col("titul")
        .str.split(" pro ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("pro"),
        pl.col("titul")
        .str.split(r" z ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("z"),
        pl.col("titul")
        .str.split(r" ze ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("ze"),
        pl.col("titul")
        .str.split(" s ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("s"),
        pl.col("titul")
        .str.split(" bez ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("bez"),
        pl.col("titul")
        .str.split(" podle ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("podle"),
    )
    return (df_zspro,)


@app.cell
def _(df_zspro):
    df_zspro.group_by("s").len().sort(by="len", descending=True)
    return


@app.cell
def _(df_zspro, pl):
    top_s = [
        "láskou",
        "dětmi",
        "vůní",
        "potěšením",
        "chutí",
        "fantazií",
        "bylinkami",
        "rozumem",
        "konopím",
    ]

    df_zspro.filter(pl.col("s").is_in(top_s)).group_by(pl.col("s")).len().sort(
        by="len", descending=True
    )
    return (top_s,)


@app.cell
def _(df_zspro, pl):
    top_pro = [
        "diabetiky",
        "děti",
        "zdraví",
        "každého",
        "labužníky",
        "štíhlou",
        "všední",
        "nemocné",
        "kojence",
        "radost",
    ]

    df_zspro.filter(pl.col("pro").is_in(top_pro)).group_by(
        pl.col("pro")
    ).len().sort(by="len", descending=True).with_columns(
        pl.col("pro")
        .str.replace("štíhlou", "štíhlou (postavu, linii)")
        .str.replace("všední", "všední (příležitosti)")
    ).head(7)
    return (top_pro,)


@app.cell
def _(df_zspro, pl):
    top_z = [
        "masa",
        "polotovarů",
        "brambor",
        "ryb",
        "hub",
        "těstovin",
        "ovoce",
        "drůbeže",
    ]

    df_zspro.filter(pl.col("z").is_in(top_z)).group_by(pl.col("z")).len().sort(
        by="len", descending=True
    ).head(7)
    return (top_z,)


@app.cell
def _(df_zspro, pl):
    top_bez = [
        "lepku",
        "vážení",
        "cukru",
        "cholesterolu",
        "mléka",
        "masa",
        "chemie",
    ]

    df_zspro.filter(pl.col("bez").is_in(top_bez)).group_by(
        pl.col("bez")
    ).len().sort(by="len", descending=True).head(7)
    return (top_bez,)


@app.cell
def _(df_zspro, pl, top_bez, top_pro, top_s, top_z):
    megakombo = pl.concat(
        [
            df_zspro.filter(pl.col("pro").is_in(top_pro))
            .group_by(pl.col("pro"))
            .len()
            .sort(by="len", descending=True)
            .head(7)
            .unpivot(index="len"),
            df_zspro.filter(pl.col("z").is_in(top_z))
            .group_by(pl.col("z"))
            .len()
            .sort(by="len", descending=True)
            .head(7)
            .unpivot(index="len"),
            df_zspro.filter(pl.col("s").is_in(top_s))
            .group_by(pl.col("s"))
            .len()
            .sort(by="len", descending=True)
            .head(7)
            .unpivot(index="len"),
            df_zspro.filter(pl.col("bez").is_in(top_bez))
            .group_by(pl.col("bez"))
            .len()
            .sort(by="len", descending=True)
            .head(7)
            .unpivot(index="len"),
        ]
    ).with_columns(pl.col("value").str.replace("štíhlou", "štíhlou (linii)"))

    megakombo.write_json("data/varime_pro_z_s_bez.json")

    megakombo
    return


@app.cell
def _(df_zspro, pl):
    df_zspro.filter(pl.col("s") == "Měsícem")
    return


@app.cell
def _(df_zspro):
    df_zspro.group_by("pro").len().sort(by="len", descending=True)
    return


@app.cell
def _(df_zspro):
    df_zspro.group_by("z").len().sort(by="len", descending=True)
    return


@app.cell
def _(df_zspro):
    df_zspro.group_by("ze").len().sort(by="len", descending=True)
    return


@app.cell
def _():
    return


@app.cell
def _(df_zspro):
    df_zspro.group_by("bez").len().sort(by="len", descending=True)
    return


@app.cell
def _(df_zspro):
    df_zspro.group_by("podle").len().sort(by="len", descending=True)
    return


@app.cell
def _(df, pl):
    nazvy = df.select(pl.col("245_a")).to_series().to_list()
    nazvy[0:100]
    return (nazvy,)


@app.cell
def _(nazvy):
    [x.split(" pro ")[1] for x in nazvy if " pro " in x]
    return


@app.cell
def _(nazvy):
    [x.split(" s ")[1] for x in nazvy if " s " in x]
    return


@app.cell
def _(nazvy):
    [x.split(" bez ")[1].split(" ")[0] for x in nazvy if " bez " in x]
    return


@app.cell
def _():
    return


@app.cell
def _(df):
    df.explode("490_a").group_by("490_a").len().sort(by="len", descending=True)
    return


@app.cell
def _(df):
    df.explode("041_h").group_by("041_h").len().sort(by="len", descending=True)
    return


@app.cell
def _(df, pl):
    df.explode("041_h").filter(pl.col("041_h") == "pol").sort(by="rok")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Grafy
    """)
    return


@app.cell
def _(alt, do_grafu, pl, razeni):
    hranice = (1900, 2020)

    alt.Chart(
        do_grafu.filter(pl.col("rok").is_between(hranice[0], hranice[1])),
        width=500,
    ).mark_point().encode(
        alt.X("rok:Q", scale=alt.Scale(domain=hranice)),
        alt.Y("co:N", sort=razeni),
        alt.Size("len:Q"),
    )
    return


@app.cell
def _(do_grafu):
    do_grafu
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Devadesátky
    """)
    return


@app.cell
def _(df_lemma, pl):
    devade = list(
        set(
            df_lemma.filter(pl.col("rok").is_between(1990, 1999))
            .select(pl.col("titul_lemma"))
            .to_series()
            .to_list()
        )
    )
    ne_devade = set(
        df_lemma.filter(~pl.col("rok").is_between(1990, 1999))
        .select(pl.col("titul_lemma"))
        .to_series()
        .to_list()
    )
    return devade, ne_devade


@app.cell
def _(devade, ne_devade):
    jen_devade = [x for x in devade if x not in ne_devade]
    return (jen_devade,)


@app.cell
def _(df_lemma, jen_devade, pl):
    df_lemma.filter(pl.col("titul_lemma").is_in(jen_devade)).filter(
        pl.col("titul_lemma").is_in(jen_devade)
    ).group_by("titul_lemma").len().sort(by="len", descending=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bohdalka
    """)
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("Růžičk")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("100_a").str.contains("Růžičková, Hel")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("Bohdal")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("v kuchyni hvězd")).select(pl.col(minimum))
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("Jiřin")).select(pl.col(minimum))
    return


@app.cell
def _(df, pl):
    df.group_by("100_a").agg(pl.col("rok").min().alias("min")).join(
        df.group_by("100_a").agg(pl.col("rok").max().alias("max")),
        on='100_a',
        how="left"
    ).with_columns(
        (pl.col("max") - pl.col("min")).alias("diff")
    ).sort(by="diff",descending=True)
    return


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("100_a").str.contains("Bohdalová, Jiřin")).select(pl.col(minimum))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
