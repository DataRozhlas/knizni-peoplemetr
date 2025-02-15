# Vytvoření univerzálně využitelné tabulky se základními biografickými údaji.

import os
import polars as pl

aut = pl.read_parquet(os.path.join("data","aut_vyber.parquet"))

wikid = pl.read_parquet(os.path.join("data","wikidata.parquet"))

aut = aut.explode("375_a").with_columns(pl.when(pl.col("375_a") == "muž").then(pl.lit("m")).when(pl.col("375_a") == "žena").then(pl.lit("f")).otherwise(None)
    .alias("gender"))

def rok_z_autorit(retezec):
    try:
        rok = int(re.search(r"\b\d{1,4}(?!\.)\b", retezec).group())
        if "př. Kr." in retezec:
            return -rok
        else:
            return rok
    except:
        return None

def roky_z_autorit(retezec):
    if "činn" in retezec:
        return {"narozeni": None, "umrti": None}
    narozeni = rok_z_autorit(retezec.split('-')[0])
    umrti = rok_z_autorit(retezec.split('-')[1])
    if umrti and narozeni:
        if (umrti < 0) and (narozeni > 0):
            narozeni = -narozeni
    return {"narozeni": narozeni, "umrti": umrti}

aut = aut.explode("100_d").with_columns(pl.col("100_d").map_elements(roky_z_autorit).alias("letopocty")).unnest('letopocty')

aut = aut.explode('678_a').with_columns(pl.col('678_a').map_elements(lambda x: x.split(' ')[0] if x else None).alias('bio1'))

muzska_bio1 = aut.filter(pl.col('gender') == 'm').group_by(['bio1']).len().sort(by='len',descending=True).head(500)
muzska_bio1

muzska_slova = muzska_bio1.select(pl.col('bio1')).to_series().to_list()
muzska_slova = [m for m in muzska_slova if m]
muzska_slova = [m for m in muzska_slova if len(m) > 1]
muzska_slova = [m for m in muzska_slova if m[-1] != 'á']
muzska_slova = [m for m in muzska_slova if m[-1] not in ['.','í'] and m[-2] != '.' and m != 'MD,' and m != 'MB' and m != 'Původem'
               and m != 'Narozena' and m != 'Americká' and m != 'Pseudonym' and m != 'Publikace' and m != 'PhD,' and m != 'DM,']
muzska_slova    

[m for m in muzska_slova if m[-1] == 'a']

zenska_bio1 = aut.filter(pl.col('gender') == 'f').group_by(['bio1']).len().sort(by='len',descending=True).head(500)
zenska_bio1

zenska_slova = zenska_bio1.select(pl.col('bio1')).to_series().to_list()
zenska_slova = [m for m in zenska_slova if m]
zenska_slova = [m for m in zenska_slova if len(m) > 1]
zenska_slova = [m for m in zenska_slova if m[-1] not in ['.','í'] and m[-2] != '.' and m != 'MD,' and m != 'MB' and m != 'Původem' and m != 'Narozen' and m != 'Pseudonym' and m != 'Publikace' and m != 'PhD,' and m != 'Mgr,' and m[-1] != 'y' and m[-1] != 'ý' and m != 'Ing,' and m != 'MA,' and m != 'MUDr,' and m != 'MBA,']
zenska_slova    

aut.filter((pl.col('gender') == 'm') & (pl.col('bio1') == 'Narozena'))

aut = aut.explode('100_7')

skoro_urcite_muzi = aut.filter(pl.col('bio1').is_in(muzska_slova))
predelat_na_muze = skoro_urcite_muzi.select(pl.col('100_7')).to_series().to_list()
skoro_urcite_muzi

skoro_urcite_zeny = aut.filter(pl.col('bio1').is_in(zenska_slova))
predelat_na_zeny = skoro_urcite_zeny.select(pl.col('100_7')).to_series().to_list()
skoro_urcite_zeny

[x for x in zenska_slova if x in muzska_slova]


set(predelat_na_zeny).intersection(set(predelat_na_muze))

predelat = predelat_na_muze + predelat_na_zeny

aut_nebudeme_menit = aut.filter(~pl.col('100_7').is_in(predelat))
aut_budeme_menit = aut.filter(pl.col('100_7').is_in(predelat))

aut_zmeneno = aut_budeme_menit.with_columns(pl.when(
    pl.col('100_7').is_in(predelat_na_muze)
).then(
    pl.lit('m')
).when(
    pl.col('100_7').is_in(predelat_na_zeny)
).then(pl.lit('f')
      ).otherwise(None).alias('gender'))

aut_spojene = pl.concat([aut_nebudeme_menit, aut_zmeneno])

aut_vyplnene = aut_spojene.filter(~pl.col("narozeni").is_null() | ~pl.col("umrti").is_null() | ~pl.col("umrti").is_null()).select(pl.col(['100_7','narozeni','umrti','gender']))


wikid = wikid.with_columns(pl.when(pl.col("w_gender") == "muž").then(pl.lit("m")).when(pl.col("w_gender") == "žena").then(pl.lit("f")).otherwise(None).alias("gender"))

wikid_vyplnene = wikid.with_columns(pl.col("w_narozeni").cast(int).alias("narozeni")).with_columns(pl.col("w_umrti").cast(int).alias("umrti")).rename({'__index_level_0__':'100_7'}).select(pl.col(['100_7','narozeni','umrti','gender'])).filter(~pl.col("narozeni").is_null() | ~pl.col("umrti").is_null()| ~pl.col("gender").is_null())
wikid_vyplnene

def specialized_join(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
    # Perform outer join
    joined = df1.join(
        df2,
        on="100_7",
        how="outer",
        suffix="_df2"
    )
    
    # Coalesce all columns, including the ID column
    result = joined.with_columns([
        pl.coalesce("100_7", "100_7_df2").alias("100_7"),
        pl.coalesce("narozeni", "narozeni_df2").alias("narozeni"),
        pl.coalesce("umrti", "umrti_df2").alias("umrti"),
        pl.coalesce("gender", "gender_df2").alias("gender")
    ])
    
    # Drop the duplicate columns
    result = result.drop(["100_7_df2", "narozeni_df2", "umrti_df2","gender_df2"])
    
    return result


df = specialized_join(aut_vyplnene, wikid_vyplnene)

df = df.unique(subset=['100_7'], keep='first')

df = df.with_columns(
    (pl.col("umrti") - pl.col("narozeni")).alias("doziti")
).with_columns(pl.when(~pl.col('doziti').is_between(15,115)).then(None).otherwise(pl.col('umrti')).alias('umrti'))

print(df.drop('doziti'))

df.drop('doziti').write_parquet(os.path.join('data','narozeni-umrti-gender.parquet'))


