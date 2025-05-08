import sqlite3
import pandas as pd
from flask import Flask, json
import plotly
import plotly.graph_objects as go
from flask import render_template, request, redirect, url_for, session, flash
import ejercicio_1
import main_program
import plotly.express as px
from database import init_db, add_user, login as user_login
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def home():
    return render_template('home.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user_login(username, password)
        if user:
            session['username'] = username
            flash('Inicio de sesión exitoso', 'success')
            redirect(url_for('login'))
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            add_user(username, password)
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error al registrar el usuario: ' + str(e), 'danger')
    
    return render_template('register.html')

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    con = sqlite3.connect('../docs/datos.db')
    clientes = pd.read_sql_query("SELECT * FROM clientes", con)
    maxClientes = len(clientes)

    incidentes = pd.read_sql_query("SELECT * FROM tipos_incidentes", con)
    maxIncidentes = len(incidentes)

    nClientes = request.args.get('nClientes')
    if nClientes is None:
        nClientes = -1
    nClientes = int(nClientes)

    nIncidentes = request.args.get('nIncidentes')
    if nIncidentes is None:
        nIncidentes = -1
    nIncidentes = int(nIncidentes)

    if nClientes <= 0 or nClientes > maxClientes:
        nClientes = 5
    if nIncidentes <= 0 or nIncidentes > maxIncidentes:
        nIncidentes = 5

    a = plotly.utils.PlotlyJSONEncoder
    values_1 = ejercicio_1.topClients(nClientes)
    fig1 = go.Figure(
        data=[go.Bar(y=list(values_1.values), x=list(values_1.keys().values))],
    )
    fig1.update_layout(
        xaxis_title="Nombre",
        yaxis_title="Número de incidentes"
    )
    graph1 = fig1.to_json()

    values_2 = ejercicio_1.topIncidents(nIncidentes)
    fig2 = go.Figure(
        data=[go.Bar(y=list(values_2["result"]), x=list(values_2["nombre"]))],
    )
    fig2.update_layout(
        xaxis_title="Nombre",
        yaxis_title="Tiempo de resolución"
    )
    graph2 = fig2.to_json()
    
    return render_template('estadisticas.html', graph1=graph1, graph2=graph2, x=nClientes, y=nIncidentes)

if __name__ == '__main__':
    init_db()
    main_program.load_data_from_json()
    app.run(debug = True)
