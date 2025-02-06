def alt_friendly(frejm):

    import polars as pl
    import datetime

    # Vrátí dataframe upravený tak, aby uměl zvizualizovat Altair.
    # 1/ Převede sloupec "rok" na datum, 2/ zkonvertuje Polars df na pandas df.

    return frejm.with_columns(
        pl.col("rok")
        .map_elements(
            lambda x: datetime.date(year=int(x), month=1, day=1), return_dtype=pl.Date
        )
        .cast(pl.Datetime)
    ).to_pandas()