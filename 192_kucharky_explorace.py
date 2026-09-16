import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import polars as pl

    return alt, mo, pl


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
    df.sample(5)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Produkce podle let
    """)


@app.cell
def _(df):
    len(df.unique(subset=["100_a", "titul"], keep="first"))


@app.cell
def _(alt, df):
    alt.Chart(
        df.unique(subset=["100_a", "titul"], keep="first").group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.unique(subset=["100_a", "titul"], keep="first")
        .group_by("rok")
        .len()
        .filter(pl.col("rok") > 1980),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df):
    alt.Chart(df.group_by("rok").len(), width=800).mark_bar().encode(
        alt.X("rok:Q"), alt.Y("len:Q")
    )


@app.cell
def _(df):
    df.group_by("rok").len().sort(by="len", descending=True)


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.group_by("rok").agg(pl.col("pocet_stran").sum()), width=800
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("pocet_stran:Q"))


@app.cell
def _(df, pl):
    df.group_by("rok").agg(pl.col("pocet_stran").sum()).sort(
        by="pocet_stran", descending=True
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Opakovaná vydání
    """)


@app.cell
def _(df):
    df.group_by(["100_a", "titul"]).len().sort(by="len", descending=True)


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("Hrníčková")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(df):
    df.group_by("100_a").len().sort(by="len", descending=True)


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Vlachová, Libu")
    ).select(pl.col(minimum)).sort(by="rok")


@app.cell
def _(df):
    df.unique(subset=["100_a", "titul"]).group_by("100_a").len().sort(
        by="len", descending=True
    )


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Poláček, Jiř")
    ).select(pl.col(minimum)).sort(by="rok")


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Vašák, Jaro")
    ).select(pl.col(minimum)).sort(by="rok")


@app.cell
def _(df, minimum, pl):
    df.unique(subset=["100_a", "titul"]).filter(
        pl.col("100_a").str.contains("Hejlík, Lu")
    ).select(pl.col(minimum)).sort(by="rok")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Motivy
    """)


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)salát"))


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)kalor"))


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)gril"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)gril")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)diet")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(df, minimum, pl):
    df.filter(pl.col("245_a").str.contains("(?i)diet")).select(pl.col(minimum)).sort(
        by="rok"
    )


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)frit")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)maďars"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)maďars")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)váno[cč]")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)salát")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)"))
        .group_by("rok")
        .len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)mexi")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Jazyky
    """)


@app.cell
def _(df):
    df.explode("041_h").group_by("041_h").len().sort(by="len", descending=True)


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Trendy
    """)


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
        df.filter(pl.col("245_a").str.contains("(?i)mikrovln")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)zdrav")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)těstovin")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)frit")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(df, pl, top_slova):
    df.with_columns(pl.col("titul").str.to_lowercase().str.split(" ")).explode(
        "titul"
    ).filter(pl.col("titul").is_in(top_slova)).group_by("titul").agg(
        pl.col("rok").median()
    ).sort(by="rok")


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)postní")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)zavařování")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)sváteční")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)babič")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)peče")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)gril")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)smoothi")).group_by("rok").len(),
        width=800,
    ).mark_bar().encode(alt.X("rok:Q"), alt.Y("len:Q"))


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Z čeho, s čím, pro koho
    """)


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
        .str.split(" z ")
        .list.slice(1, 1)
        .list.join("")
        .str.split(" ")
        .list.slice(0, 1)
        .list.join("")
        .alias("z"),
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


@app.cell
def _(df_zspro):
    df_zspro.group_by("pro").len().sort(by="len", descending=True)


@app.cell
def _(df_zspro):
    df_zspro.group_by("z").len().sort(by="len", descending=True)


@app.cell
def _(df_zspro):
    df_zspro.group_by("bez").len().sort(by="len", descending=True)


@app.cell
def _(df_zspro):
    df_zspro.group_by("podle").len().sort(by="len", descending=True)


@app.cell
def _(df, pl):
    nazvy = df.select(pl.col("245_a")).to_series().to_list()
    nazvy[0:100]
    return (nazvy,)


@app.cell
def _(nazvy):
    [x.split(" pro ")[1] for x in nazvy if " pro " in x]


@app.cell
def _(nazvy):
    [x.split(" s ")[1] for x in nazvy if " s " in x]


@app.cell
def _(nazvy):
    [x.split(" bez ")[1].split(" ")[0] for x in nazvy if " bez " in x]


@app.cell
def _():
    return


@app.cell
def _(df):
    df.explode("490_a").group_by("490_a").len().sort(by="len", descending=True)


@app.cell
def _(df):
    df.explode("041_h").group_by("041_h").len().sort(by="len", descending=True)


@app.cell
def _(df, pl):
    df.explode("041_h").filter(pl.col("041_h") == "pol").sort(by="rok")


if __name__ == "__main__":
    app.run()
