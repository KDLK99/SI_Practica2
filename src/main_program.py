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
                    (int(elem['cliente']), elem['fecha_apertura'], elem['contactos_con_empleados'][-1]['fecha'], elem['es_mantenimiento'], elem['satisfaccion_cliente'], elem['tipo_incidencia']))

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


def main():
    load_data_from_json()



    


if __name__ == '__main__':
    main()

