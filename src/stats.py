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
    return (abs(diferenciaMantenimiento.dt.days.mean()), abs(diferenciaNoMantenimiento.dt.days.mean()))

def top5Critics():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT nombre, cliente, es_mantenimiento, tipo_incidencia FROM tickets_emitidos JOIN clientes ON cliente = id_cli WHERE es_mantenimiento = 1 AND tipo_incidencia != 1", con)
    return df["nombre"].value_counts().nlargest(5)

def showEmployees():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT nombre FROM empleados e JOIN tickets_empleados t ON e.id_emp = t.id_emp", con)
    return df["nombre"].value_counts()

'''
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
'''

def time_type_incident():
    # Conectar a la base de datos SQLite
    con = sqlite3.connect('../docs/datos.db')

    # Leer los datos de la tabla "tickets_emitidos"
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    con.close()  # Cerrar conexión

    # Asegurar que las fechas sean tipo datetime
    df["fecha_apertura"] = pd.to_datetime(df["fecha_apertura"])
    df["fecha_cierre"] = pd.to_datetime(df["fecha_cierre"])

    # Filtrar filas con valores nulos para evitar errores
    df = df.dropna(subset=["fecha_apertura", "fecha_cierre"])

    # Lista de tipos de incidente únicos
    type_list = df["tipo_incidencia"].unique().tolist()

    # Lista para almacenar los tiempos de resolución
    data = []

    # Calcular la diferencia entre fecha_apertura y fecha_cierre por tipo de incidente
    for tipo in type_list:
        tiempos_resolucion = (df.loc[df["tipo_incidencia"] == tipo, "fecha_cierre"] -
                              df.loc[df["tipo_incidencia"] == tipo, "fecha_apertura"]).dt.days
        for tiempo in tiempos_resolucion:
            data.append({"Tipo de Incidente": tipo, "Tiempo de Resolución (días)": tiempo})

    return pd.DataFrame(data)

def week_day():
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    days = pd.to_datetime(df['fecha_apertura']).dt.day_name()

    final_data = days.value_counts()

    return final_data
