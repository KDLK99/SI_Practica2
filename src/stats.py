import sqlite3
import pandas as pd
import plotly

def showMean():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    aperturaMantenimiento = pd.to_datetime(df[df["es_mantenimiento"] == True]["fecha_apertura"]) 
    cierreMantenimiento = pd.to_datetime(df[df["es_mantenimiento"] == True]["fecha_cierre"]) 
    diferenciaMantenimiento = aperturaMantenimiento - cierreMantenimiento

    aperturaNoMantenimiento = pd.to_datetime(df[df["es_mantenimiento"] == False]["fecha_apertura"]) 
    cierreNoMantenimiento = pd.to_datetime(df[df["es_mantenimiento"] == False]["fecha_cierre"]) 
    diferenciaNoMantenimiento = aperturaNoMantenimiento - cierreNoMantenimiento
    con.close()
    return (abs(diferenciaMantenimiento.dt.days.mean()), abs(diferenciaNoMantenimiento.dt.days.mean()))

def top5Critics():
    con = sqlite3.connect('../docs/datos.db')
    
    tickets_emitidos = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    clientes = pd.read_sql_query("SELECT * FROM clientes", con)

    resultado = pd.merge(tickets_emitidos, clientes, left_on='cliente', right_on='id_cli')

    resultado_filtrado = resultado[(resultado['es_mantenimiento'] == 1) & (resultado['tipo_incidencia'] != 1)]

    con.close()
    return resultado_filtrado['nombre'].value_counts().nlargest(5)

def showEmployees():
    con = sqlite3.connect('../docs/datos.db')
    
    empleados = pd.read_sql_query("SELECT * FROM empleados", con)
    tickets_empleados = pd.read_sql_query("SELECT * FROM tickets_empleados", con)

    resultado = pd.merge(empleados, tickets_empleados, left_on='id_emp', right_on='id_emp')

    con.close()

    return resultado['nombre'].value_counts()


def time_type_incident():
    con = sqlite3.connect('../docs/datos.db')

    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    con.close() 

    df["fecha_apertura"] = pd.to_datetime(df["fecha_apertura"])
    df["fecha_cierre"] = pd.to_datetime(df["fecha_cierre"])

    df = df.dropna(subset=["fecha_apertura", "fecha_cierre"])

    type_list = df["tipo_incidencia"].unique().tolist()

    data = []

    for tipo in type_list:
        tiempos_resolucion = (df.loc[df["tipo_incidencia"] == tipo, "fecha_cierre"] -
                              df.loc[df["tipo_incidencia"] == tipo, "fecha_apertura"]).dt.days
        for tiempo in tiempos_resolucion:
            data.append({"Tipo de Incidente": tipo, "Tiempo de Resolución (días)": tiempo})
    con.close()

    return pd.DataFrame(data)

def week_day():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    days = pd.to_datetime(df['fecha_apertura']).dt.day_name()
    
    final_data = days.value_counts()
    order_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    final_data = final_data.reindex(order_of_days)
    con.close()
    print(final_data)

    return final_data