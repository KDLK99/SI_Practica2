import sqlite3
import pandas as pd


def topClients(n):
    con = sqlite3.connect('../docs/datos.db')
    
    tickets_emitidos = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    clientes = pd.read_sql_query("SELECT * FROM clientes", con)

    resultado = pd.merge(clientes, tickets_emitidos, left_on='id_cli', right_on='cliente')

    con.close()
    return resultado['nombre'].value_counts().nlargest(n)

def topIncidents(n):
    con = sqlite3.connect('../docs/datos.db')

    tickets_emitidos = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
    tipos_incidentes = pd.read_sql_query("SELECT * FROM tipos_incidentes", con)

    df = pd.merge(tickets_emitidos, tipos_incidentes, left_on='tipo_incidencia', right_on='id_inci')
    df["result"] = pd.to_datetime(df["fecha_apertura"]) - pd.to_datetime(df["fecha_cierre"])
    df["result"] = abs(df["result"].dt.days)

    result = df.groupby("nombre")["result"].mean().reset_index()

    con.close()
    return result.nlargest(n, "result")

def topEmpleados():
    con = sqlite3.connect('../docs/datos.db')
    
    tickets_empleados = pd.read_sql_query("SELECT * FROM tickets_empleados", con)
    empleados = pd.read_sql_query("SELECT * FROM empleados", con)

    tiempo_empleados = tickets_empleados.groupby("id_emp")["tiempo"].sum().reset_index()
    resultado = pd.merge(tiempo_empleados, empleados, on='id_emp', how='left')

    con.close()
    return resultado[["nombre", "tiempo"]].nlargest(5, "tiempo")
