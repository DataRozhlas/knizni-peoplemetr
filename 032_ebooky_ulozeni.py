import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import polars as pl

    return os, pl


@app.cell
def _(os):
    os.listdir("../knizni-peoplemetr/data_raw/ebooky")
    return


@app.cell
def _(os):
    ukazky = []
    for soubor in [x for x in os.listdir("data_raw/ebooky") if '.txt' in x]:
        with open(os.path.join("data_raw/ebooky",soubor), "r", encoding="utf-8") as x:
            try:
                ukazky.append(
                    {
                        'isbn' : soubor.split('.')[0],
                        'text' : x.read()
                    }
                )
            except:
                print(soubor)
    return (ukazky,)


@app.cell
def _(pl, ukazky):
    pl.DataFrame(ukazky)
    return


@app.cell
def _(os, pl, ukazky):
    pl.DataFrame(ukazky).write_parquet(os.path.join("data","ukazky_ebooku.parquet"))
    return


if __name__ == "__main__":
    app.run()
