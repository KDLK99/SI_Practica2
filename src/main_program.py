import sqlite3
import pandas as pd
import json
from pprint import pprint
from datetime import datetime


def load_data():
    with open('../docs/datos.json','r') as f:
        datos=json.load(f)
    return datos

def create_table_clientes(cur:sqlite3.Cursor):
    
    cur.execute("DROP TABLE IF EXISTS clientes;")
    cur.execute("CREATE TABLE IF NOT EXISTS clientes("
        "id_cli INTEGER PRIMARY KEY,"
        "nombre TEXT,"
        "provincia TEXT,"
        "telefono TEXT"
        ");")


def fill_table_clientes(cur:sqlite3.Cursor, data):
    for elem in data:
        cur.execute("INSERT OR IGNORE INTO clientes(id_cli,nombre,provincia,telefono)"\
                    "VALUES ('%d','%s', '%s', '%s')" %
                    (int(elem['id_cli']), elem['nombre'], elem['provincia'],elem['telefono']))

def create_table_empleados(cur:sqlite3.Cursor):
    
    cur.execute("DROP TABLE IF EXISTS empleados;")
    cur.execute("CREATE TABLE IF NOT EXISTS empleados("
        "id_emp INTEGER PRIMARY KEY,"
        "nombre TEXT,"
        "nivel INTEGER,"
        "fecha_contrato TEXT"
        ");")


def fill_table_empleados(cur:sqlite3.Cursor, data):
    for elem in data:
        cur.execute("INSERT OR IGNORE INTO empleados(id_emp,nombre,nivel,fecha_contrato)"\
                    "VALUES ('%d','%s', '%s', '%s')" %
                    (int(elem['id_emp']), elem['nombre'], elem['nivel'],elem['fecha_contrato']))

def create_table_tipos_incidentes(cur:sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS tipos_incidentes;")
    cur.execute("CREATE TABLE IF NOT EXISTS tipos_incidentes("
        "id_inci INTEGER PRIMARY KEY,"
        "nombre TEXT"
        ");")

def fill_table_tipos_incidentes(cur:sqlite3.Cursor, data):
    for elem in data:
        cur.execute("INSERT OR IGNORE INTO tipos_incidentes(id_inci,nombre)"\
                    "VALUES ('%d','%s')" %
                    (int(elem['id_inci']), elem['nombre']))

def create_table_tickets_emitidos(cur:sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS tickets_emitidos;")
    cur.execute("CREATE TABLE IF NOT EXISTS tickets_emitidos("
        "id_tick INTEGER PRIMARY KEY AUTOINCREMENT,"
        "cliente INTEGER,"
        "fecha_apertura TEXT,"
        "fecha_cierre TEXT,"
        "es_mantenimiento INTEGER NOT NULL CHECK (es_mantenimiento IN (0, 1)),"
        "satisfaccion_cliente INTEGER,"
        "tipo_incidencia INTEGER,"
        "FOREIGN KEY (cliente) REFERENCES clientes(cliente),"
        "FOREIGN KEY (tipo_incidencia) REFERENCES tipos_incidentes(id)"
        ");")

def fill_table_tickets_emitidos(cur:sqlite3.Cursor, data):
    for elem in data:
        cur.execute("INSERT OR IGNORE INTO tickets_emitidos(cliente,fecha_apertura,fecha_cierre,es_mantenimiento,satisfaccion_cliente,tipo_incidencia)"\
                    "VALUES ('%d','%s','%s','%d','%d','%d')" %
                    (int(elem['cliente']), elem['fecha_apertura'], elem['fecha_cierre'], elem['es_mantenimiento'], elem['satisfaccion_cliente'], elem['tipo_incidencia']))

def create_table_tickets_empleados(cur:sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS tickets_empleados;")
    cur.execute("CREATE TABLE IF NOT EXISTS tickets_empleados("
        "id_emp INTEGER,"
        "id_ticket INTEGER,"
        "fecha TEXT,"
        "tiempo REAL,"
        "PRIMARY KEY (id_emp,id_ticket),"
        "FOREIGN KEY (id_emp) REFERENCES empleados(id_emp),"
        "FOREIGN KEY (id_ticket) REFERENCES tickets_emitidos(id_tick)"
        ");")

def fill_table_tickets_empleados(cur:sqlite3.Cursor, data):
    id_ticket = 1
    for elem in data:
        for e in elem["contactos_con_empleados"]:
            cur.execute("INSERT OR IGNORE INTO tickets_empleados(id_emp,id_ticket,fecha,tiempo)"\
                        "VALUES ('%d','%d','%s','%f')" %
                        (int(e['id_emp']), id_ticket, e['fecha'], e['tiempo']))
        id_ticket += 1

def load_data_from_json():
    datos = load_data()
    con = sqlite3.connect('../docs/datos.db')
    cur = con.cursor()
    create_table_clientes(cur)
    con.commit()
    fill_table_clientes(cur, datos['clientes'])
    con.commit()
    create_table_empleados(cur)
    con.commit()
    fill_table_empleados(cur, datos['empleados'])
    con.commit()
    create_table_tipos_incidentes(cur)
    con.commit()
    fill_table_tipos_incidentes(cur, datos['tipos_incidentes'])
    con.commit()
    create_table_tickets_emitidos(cur)
    con.commit()
    fill_table_tickets_emitidos(cur, datos['tickets_emitidos'])
    con.commit()
    create_table_tickets_empleados(cur)
    con.commit()
    fill_table_tickets_empleados(cur, datos['tickets_emitidos'])
    con.commit()

def calc_values():
    results = []
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)

    print(f"Número de tickets emitidos (muestras): {len(df)}")
    results.append(len(df))

    print()

    mean_incident = df[df.satisfaccion_cliente > 5]["satisfaccion_cliente"].mean()
    std_incident = df[df.satisfaccion_cliente > 5]["satisfaccion_cliente"].std()
    print(f"Media de valoración en los incidentes con valoración mayor de 5: {mean_incident:.2f}")
    print(f"Desviación típica de valoración en los incidentes con valoración mayor de 5: {std_incident:.2f}")
    results.append(mean_incident)
    results.append(std_incident)

    print()

    tickets_emitidos = pd.read_sql('SELECT * FROM tickets_emitidos', con)
    incidentes_por_cliente = tickets_emitidos['cliente'].value_counts()
    desviacion_tipica = incidentes_por_cliente.std()
    media = incidentes_por_cliente.mean()
    print(f"Media del número de incidentes por cliente: {media:.2f}")
    print(f'Desviación típica del número de incidentes por cliente: {desviacion_tipica:.2f}')
    results.append(media)    
    results.append(desviacion_tipica)

    print()

    df = pd.read_sql_query(f"SELECT * FROM tickets_empleados", con)
    add_time = df['tiempo'].sum()
    df1 = pd.read_sql_query(f"SELECT * FROM tickets_emitidos", con)
    num_incidentes = len(df1)
    print(f"Media del número de horas por incidente: {add_time/num_incidentes}")
    results.append(add_time/num_incidentes)

    # Unir las tablas en base al ID del ticket
    tickets_df = df.merge(df1, left_on='id_ticket', right_on='id_tick')

    # Calcular la desviación típica de las horas por incidente
    desviacion_tipica = tickets_df['tiempo'].std()

    print(f'Desviación típica de las horas por incidente: {desviacion_tipica:.2f}')
    results.append(desviacion_tipica)

    print()
    df = pd.read_sql_query("SELECT id_emp, tiempo FROM tickets_empleados", con)


    # Sumar las horas trabajadas por empleado
    empleados_horas = df.groupby("id_emp")["tiempo"].sum()

    # Obtener el empleado con más horas trabajadas
    empleado_max = empleados_horas.idxmax()
    max_horas = empleados_horas.max()

    # Obtener el empleado con menos horas trabajadas
    empleado_min = empleados_horas.idxmin()
    min_horas = empleados_horas.min()

    print(f"Empleado con más horas trabajadas: {empleado_max} ({max_horas} horas)")
    print(f"Empleado con menos horas trabajadas: {empleado_min} ({min_horas} horas)")
    results.append((empleado_max, max_horas))
    results.append((empleado_min, min_horas))

    print()

    df = pd.read_sql_query("SELECT fecha_apertura, fecha_cierre FROM tickets_emitidos", con)

    df['fecha_apertura'] = pd.to_datetime(df['fecha_apertura'])
    df['fecha_cierre'] = pd.to_datetime(df['fecha_cierre'])

    # Calcular la diferencia en días
    df['diferencia_dias'] = (df['fecha_cierre'] - df['fecha_apertura']).dt.days

    # Obtener los valores mínimo y máximo de la diferencia
    min_diferencia = df['diferencia_dias'].min()
    max_diferencia = df['diferencia_dias'].max()

    print(f"Diferencia mínima: {min_diferencia} días")
    print(f"Diferencia máxima: {max_diferencia} días")
    results.append(min_diferencia)
    results.append(max_diferencia)

    print()

    df = pd.read_sql_query("SELECT id_emp FROM tickets_empleados", con)

    # Contar la cantidad de veces que aparece cada empleado
    empleados_count = df["id_emp"].value_counts()

    # Obtener el empleado con más tickets
    empleado_max = empleados_count.idxmax()
    max_tickets = empleados_count.max()

    # Obtener el empleado con menos tickets
    empleado_min = empleados_count.idxmin()
    min_tickets = empleados_count.min()

    print(f"Empleado con más tickets: {empleado_max} ({max_tickets} veces)")
    print(f"Empleado con menos tickets: {empleado_min} ({min_tickets} veces)")
    print()
    results.append((empleado_max, max_tickets))
    results.append((empleado_min, min_tickets))

    con.close()
    return results


def calc_values2():
    print("\n----- EJERCICIO 3 -----\n")
    con = sqlite3.connect('../docs/datos.db')
    df = pd.read_sql_query("SELECT e.id_emp, e.nombre, e.nivel, t.cliente, te.fecha, te.tiempo, t.id_tick, t.fecha_apertura, t.fecha_cierre, t.es_mantenimiento, t.satisfaccion_cliente, t.tipo_incidencia FROM empleados e JOIN tickets_empleados te ON e.id_emp = te.id_emp JOIN tickets_emitidos t ON te.id_ticket = t.id_tick;", con)
    df = df[df.tipo_incidencia == 5]
    
    ## Empleado ##
    print("\n-- Empleados --\n")
    df_empleados = df.groupby("id_emp")

    df_empleados2 = df_empleados['id_tick'].count().reset_index()
    df_empleados2.rename(columns={'id_tick': 'n_tickets'}, inplace=True)
    print("Número de incidentes por empleado:")
    print(df_empleados2)

    
    print("Mediana de número de incidentes por empleado: ", end="")
    df_empleados3 = df_empleados2['n_tickets'].median()
    print(df_empleados3)
    print("Media de número de incidentes por empleado: ", end="")
    df_empleados3 = df_empleados2['n_tickets'].mean()
    print(df_empleados3)
    print("Varianza de número de incidentes por empleado: ", end="")
    df_empleados3 = df_empleados2['n_tickets'].var()
    print(df_empleados3)
    print("Mayor valor de número de incidentes por empleado: ", end="")
    df_empleados3 = df_empleados2['n_tickets'].max()
    print(df_empleados3)
    print("Menor valor de número de incidentes por empleado: ", end="")
    df_empleados3 = df_empleados2['n_tickets'].min()
    print(df_empleados3)





    ## Nivel de empleado ##
    print("\n-- Nivel --\n")
    df_nivel = df.groupby("nivel")

    df_nivel2 = df_nivel['id_tick'].count().reset_index()
    df_nivel2.rename(columns={'id_tick': 'n_tickets'}, inplace=True)
    print("Número de incidentes por nivel:")
    print(df_nivel2)

    print("Mediana de número de incidentes por nivel: ", end="")
    df_nivel3 = df_nivel2['n_tickets'].median()
    print(df_nivel3)
    print("Media de número de incidentes por nivel: ", end="")
    df_nivel3 = df_nivel2['n_tickets'].mean()
    print(df_nivel3)
    print("Varianza de número de incidentes por nivel: ", end="")
    df_nivel3 = df_nivel2['n_tickets'].var()
    print(df_nivel3)
    print("Mayor valor de número de incidentes por nivel: ", end="")
    df_nivel3 = df_nivel2['n_tickets'].max()
    print(df_nivel3)
    print("Menor valor de número de incidentes por nivel: ", end="")
    df_nivel3 = df_nivel2['n_tickets'].min()
    print(df_nivel3)


    ## Cliente ##
    print("\n-- Cliente --\n")
    df_cliente = df.groupby("cliente")

    df_cliente2 = df_cliente['id_tick'].count().reset_index()
    df_cliente2.rename(columns={'id_tick': 'n_tickets'}, inplace=True)
    print("Número de incidentes por cliente:")
    print(df_cliente2)

    print("Mediana de número de incidentes por cliente: ", end="")
    df_cliente3 = df_cliente2['n_tickets'].median()
    print(df_cliente3)
    print("Media de número de incidentes por cliente: ", end="")
    df_cliente3 = df_cliente2['n_tickets'].mean()
    print(df_cliente3)
    print("Varianza de número de incidentes por cliente: ", end="")
    df_cliente3 = df_cliente2['n_tickets'].var()
    print(df_cliente3)
    print("Mayor valor de número de incidentes por cliente: ", end="")
    df_cliente3 = df_cliente2['n_tickets'].max()
    print(df_cliente3)
    print("Menor valor de número de incidentes por cliente: ", end="")
    df_cliente3 = df_cliente2['n_tickets'].min()
    print(df_cliente3)

    ## Tipo de incidente ##

    print("\n-- Tipo de incidente --\n")
    df_tincidente = df.groupby("tipo_incidencia")

    df_tincidente2 = df_tincidente['id_tick'].count().reset_index()
    df_tincidente2.rename(columns={'id_tick': 'n_tickets'}, inplace=True)
    print("Número de incidentes por cliente:")
    print(df_tincidente2)

    print("Mediana de número de incidentes por tipo de incidente: ", end="")
    df_tincidente3 = df_tincidente2['n_tickets'].median()
    print(df_tincidente3)
    print("Media de número de incidentes por tipo de incidente: ", end="")
    df_tincidente3 = df_tincidente2['n_tickets'].mean()
    print(df_tincidente3)
    print("Varianza de número de incidentes por tipo de incidente: ", end="")
    df_tincidente3 = df_tincidente2['n_tickets'].var()
    print(df_tincidente3)
    print("Mayor valor de número de incidentes por tipo de incidente: ", end="")
    df_tincidente3 = df_tincidente2['n_tickets'].max()
    print(df_tincidente3)
    print("Menor valor de número de incidentes por tipo de incidente: ", end="")
    df_tincidente3 = df_tincidente2['n_tickets'].min()
    print(df_tincidente3)


    ## Dia de la semana ##

    print("\n-- Día de la semana --\n")

    df['fecha'] = pd.to_datetime(df['fecha'])
    df['dia_semana'] = df['fecha'].dt.day_name()
    df_diasemana = df.groupby("dia_semana")

    df_diasemana2 = df_diasemana['id_tick'].count().reset_index()
    df_diasemana2.rename(columns={'id_tick': 'n_tickets'}, inplace=True)
    print("Número de incidentes por cliente:")
    print(df_diasemana2)

    print("Mediana de número de incidentes por tipo de incidente: ", end="")
    df_diasemana3 = df_diasemana2['n_tickets'].median()
    print(df_diasemana3)
    print("Media de número de incidentes por tipo de incidente: ", end="")
    df_diasemana3 = df_diasemana2['n_tickets'].mean()
    print(df_diasemana3)
    print("Varianza de número de incidentes por tipo de incidente: ", end="")
    df_diasemana3 = df_diasemana2['n_tickets'].var()
    print(df_diasemana3)
    print("Mayor valor de número de incidentes por tipo de incidente: ", end="")
    df_diasemana3 = df_diasemana2['n_tickets'].max()
    print(df_diasemana3)
    print("Menor valor de número de incidentes por tipo de incidente: ", end="")
    df_diasemana3 = df_diasemana2['n_tickets'].min()
    print(df_diasemana3)



def main():
    load_data_from_json()
    calc_values()
    calc_values2()



    


if __name__ == '__main__':
    main()

