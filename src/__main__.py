import sqlite3
import pandas as pd
import json
from pprint import pprint


def load_data():
    with open('docs/datos.json','r') as f:
        datos=json.load(f)
    print(datos.keys())
    # pprint(datos['empleados'])
    # exit()
    # pprint(datos['clientes'])
    # pprint(datos['tickets_emitidos'])
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
    
    cur.execute("DROP TABLE IF EXISTS empelados;")
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

def main():
    datos = load_data()
    con = sqlite3.connect('docs/datos.db')
    cur = con.cursor()
    create_table_clientes(cur)
    con.commit()
    fill_table_clientes(cur, datos['clientes'])
    con.commit()
    cur.execute("Select * from clientes;")
    pprint(cur.fetchall())
    create_table_empleados(cur)
    con.commit()
    fill_table_empleados(cur, datos['empleados'])
    con.commit()
    cur.execute("Select * from empleados;")
    pprint(cur.fetchall())

    


if __name__ == '__main__':
    main()








# con = sqlite3.connect('docs/datos.db')

# cur.execute("DROP TABLE IF EXISTS tickets_emitidos;")
# cur.execute("CREATE TABLE IF NOT EXISTS tickets_emitidos("
#     "id INTEGER PRIMARY KEY,"
#     "cliente INTEGER,"
#     "es_mantenimiento INTEGER NOT NULL CHECK (es_mantenimiento IN (0, 1)),"
#     "fecha_apertura TEXT,"
#     "fecha_cierre TEXT,"
#     "satisfaccion_cliente INTEGER,"
#     "tipo_incidencia INTEGER"
#     ");")
# con.commit()
# cur.execute("PRAGMA table_info(tickets_emitidos);")
# print(cur.fetchall())
# exit()
# for elem in datos["tickets_emitidos"]:
#     #print (elem)
#     clave= list(elem.keys())[0]
#     print(clave)
#     print (elem[clave]["nombre"])

#     cur.execute("INSERT OR IGNORE INTO fichajes(id,nombre,sucursal,departamento)"\
#                 "VALUES ('%d','%s', '%s', '%s')" %
#                 (int(clave), elem[clave]['nombre'], elem[clave]['sucursal'],elem[clave]['departamento']))
#     con.commit()

