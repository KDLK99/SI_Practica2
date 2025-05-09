import sqlite3

def get_db_connection():
    conn = sqlite3.connect('../docs/users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    #conn.execute('DROP TABLE IF EXISTS USERS;')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def login(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? and password = ?', (username, password)).fetchone()
    conn.close()
    return user
