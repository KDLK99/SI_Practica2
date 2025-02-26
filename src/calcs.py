import sqlite3
import pandas as pd

def mean_time():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    print(df[df['es_mantenimiento' == 1]])

    #openDate_true = pd.to_datetime(df[df['es_mantenimiento' == 1]]['fecha_apertura'])
    #closeDate_true = pd.to_datetime(df[df['es_mantenimiento' == 1]]['fecha_apertura'])
    #duration = (closeDate - openDate).dt.days
    #mean = duration.mean()
    #print(f'Media: {mean}')

mean_time()