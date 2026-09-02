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
    df_pre = pl.read_parquet("data/cnb_kucharky.parquet")

    stats = []
    for c in df_pre.columns:
        stats.append( { 'sloupec':c, 'vyplnenych':len(df_pre.filter(pl.col(c).is_not_null()))})

    vyhodit = pl.DataFrame(stats).filter(pl.col("vyplnenych") < (len(df_pre) / 10)).select(pl.col('sloupec')).to_series().to_list()

    def najdi_rok(nulaosm):
        try:
            return int(nulaosm[7:11])
        except:
            return None

    najdi_rok("000706s1926")

    df = df_pre.drop(vyhodit).with_columns(
        pl.col("008").map_elements(najdi_rok, return_dtype=int).alias("rok")
    ).sort(by="rok")
    return (df,)


@app.cell
def _():
    return


@app.cell
def _(df):
    df
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


if __name__ == "__main__":
    app.run()
