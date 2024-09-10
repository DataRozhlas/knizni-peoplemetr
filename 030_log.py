#!/usr/bin/python3

import os
import datetime
import pandas as pd

current_date = str(datetime.datetime.now())[0:19]

# Create the logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create the log file name with the current date
log_file_name = f'log_knizni_peoplemetr_{current_date.replace(" ", "_").replace(":", "-")}.txt'

# Open the log file in write mode
with open(os.path.join('logs', log_file_name), 'w') as f:
    f.write(f"Log knižního peoplemetru z {current_date}\n==============================================\n")

    df = pd.read_json(os.path.join('data','martinus_vyslo.json'))
    log_string = f"""MARTINUS_VYSLO.JSON:
    - autorstva: {df['M_autorstvo'].nunique()}
    - titulů: {df['M_titul'].nunique()}
    - ISBN: {df['M_isbn'].nunique()}"""
    f.write(log_string)

    df = pd.read_csv(os.path.join("data","goodreads-hodnoceni.csv"))
    df['GR_date'] = pd.to_datetime(df['GR_date'])

    f.write("\nGOODREADS-HODNOCENI.CSV\n")
    f.write(str(df.groupby(pd.Grouper(key='GR_date', freq='W'))['GR_isbn'].nunique().tail(3).iloc[::-1]))

    gr_nejnovejsi = df.groupby(pd.Grouper(key='GR_date', freq='W'))['GR_isbn'].nunique().tail(3).iloc[::-1].index.to_list()[1]
    starsi = df[df['GR_date'] <= str(gr_nejnovejsi)]['GR_title'].to_list()
    novinky = df[~df['GR_title'].isin(starsi)]['GR_title'].to_list()
    f.write(f"\nNovinky {str(gr_nejnovejsi)[0:10]}\n- ")
    f.write('\n- '.join(novinky))

    df = pd.read_csv(os.path.join("data","databazeknih-hodnoceni.csv"))
    df['DK_date'] = pd.to_datetime(df['DK_date'])

    f.write("\nDATABAZEKNIH-HODNOCENI.CSV\n")
    f.write(str(df.groupby(pd.Grouper(key='DK_date', freq='W'))['DK_isbn'].nunique().tail(3).iloc[::-1]))

    dk_nejnovejsi = df.groupby(pd.Grouper(key='DK_date', freq='W'))['DK_isbn'].nunique().tail(3).iloc[::-1].index.to_list()[1]
    starsi = df[df['DK_date'] <= str(dk_nejnovejsi)]['DK_titul'].to_list()
    novinky = df[~df['DK_titul'].isin(starsi)]['DK_titul'].to_list()
    f.write(f"\nNovinky {str(dk_nejnovejsi)[0:10]}\n- ")
    f.write('\n- '.join(novinky))