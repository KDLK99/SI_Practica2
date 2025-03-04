import main_program
import sqlite3
import pandas as pd
def time_type_incident():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    type_list = list(range(1,max(df["tipo_incidencia"]+1)))
    print(type_list)

    datos = []
    for i in range(1, max(df["tipo_incidencia"]+1)):
        apertura_tipo_incidente = pd.to_datetime(df[df.tipo_incidencia == i]['fecha_apertura'])
        cierre_tipo_incidente= pd.to_datetime(df[df.tipo_incidencia == i]['fecha_cierre'])
        datos.append((abs(apertura_tipo_incidente-cierre_tipo_incidente)))

    return (datos, type_list)

def week_day():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    days = pd.to_datetime(df['fecha_apertura']).dt.day_name()

    final_data = days.value_counts()

    return final_data





