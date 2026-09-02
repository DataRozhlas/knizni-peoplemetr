import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import altair as alt

    return alt, pl


@app.cell
def _(pl):
    interpunkce = [",","?",":","/",".",";","!","\""]

    df = pl.read_parquet("data/cnb_kucharky.parquet").with_columns(
        pl.col('245_a').str.replace_many(interpunkce, ["" for x in interpunkce]).str.strip_chars()
    ).sort(by="rok")
    return (df,)


@app.cell
def _():
    return


@app.cell
def _(alt, df):
    alt.Chart(
        df.group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
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
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)diet")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)frit")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)maďars"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)maďars")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)váno[cč]")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)salát")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)"))
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)(bezmas|bez mas|vegetar|vegan)")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("245_a").str.contains("(?i)mexi")).group_by("rok").len(),
        width = 800
    ).mark_bar().encode(
        alt.X("rok:Q"),
        alt.Y("len:Q")
    )
    return


@app.cell
def _(df, pl):
    nazvy = df.select(pl.col("245_a")).to_series().to_list()
    nazvy[0:100]
    return (nazvy,)


@app.cell
def _(nazvy):
    [x.split(' pro ')[1] for x in nazvy if ' pro ' in x]
    return


@app.cell
def _(nazvy):
    [x.split(' s ')[1] for x in nazvy if ' s ' in x]
    return


@app.cell
def _(nazvy):
    [x.split(' bez ')[1].split(' ')[0] for x in nazvy if ' bez ' in x]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
