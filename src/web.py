import sqlite3
import pandas as pd
from flask import Flask, json
import plotly
import plotly.graph_objects as go
from flask import render_template, request, redirect, url_for, session, flash
import ejercicio_1
import ejercicio_3
import ejercicio_5
import main_program
import plotly.express as px
from database import init_db, add_user, login as user_login
from functools import wraps
import hashlib
import os
from newsapi import NewsApiClient


app = Flask(__name__, template_folder="static/templates")
app.secret_key = os.urandom(30)

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

@app.route('/news')
@login_required
def galey():
    newsapi = NewsApiClient(api_key='f7c4ca0f65974295b4064ecb7504ef41')
    news = newsapi.get_everything(qintitle='ciberataque',
                                    language='es')
    i = 0
    images = [] 
    for n in news['articles']:
         img = {}
         img['src'] = n['urlToImage']
         img['text'] = n['title']
         img['link'] = n['url']
         img['subtext'] = n['source']['name']
         images.append(img)
         i+=1
         if i == 9:
             break
    return render_template('news.html', images = images)


@app.route('/cves')
@login_required
def cves():
    values = ejercicio_3.access_cve_api()
    return render_template('cves.html', datos = values)


@app.route('/ia')
@login_required
def ia():
    all_params = 1
    cliente = request.args.get('cliente')
    if cliente is None:
        all_params = 0
    else:
        cliente = int(cliente)
    fecha_apertura = request.args.get('fecha_apertura')
    if fecha_apertura is None:
        all_params = 0
    fecha_cierre = request.args.get('fecha_cierre')
    if fecha_cierre is None:
        all_params = 0
    es_mantenimiento = request.args.get('es_mantenimiento')
    if es_mantenimiento is None:
        es_mantenimiento = False
    else:
        es_mantenimiento = False
    satisfacion = request.args.get('satisfacion')
    if satisfacion is None:
        all_params = 0
    else:
        satisfacion = int(satisfacion)
    tipo_incidente = request.args.get('tipo_incidente')
    if tipo_incidente is None:
        all_params = 0
    else:
        tipo_incidente = int(tipo_incidente)
    modelo = request.args.get('modelo')
    if modelo is None:
        all_params = 0
    
    if all_params == 0:
        return render_template('ia.html')
    else:
        ticket = ejercicio_5.creacion_ticket(cliente, fecha_apertura, fecha_cierre, es_mantenimiento, satisfacion, tipo_incidente)
        value = ejercicio_5.ejercicio5(modelo, ticket)
        if value[0] == 1:
            value = "El nuevo cliente será crítico"
        else:
            value = "El nuevo cliente NO será crítico"
        return render_template('ia.html', value = value)

@app.route('/ia_images')
@login_required
def ia_images():
    return render_template('ia_images.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        user = user_login(username, hashed_pass)
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
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        try:
            add_user(username, hashed_pass)
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error al registrar el usuario: ' + str(e), 'danger')
    
    return render_template('register.html')

@app.route('/estadisticas')
@login_required
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

    values_3 = ejercicio_1.topEmpleados()
    fig3 = go.Figure(
        data=[go.Bar(y=list(values_3["tiempo"]), x=list(values_3["nombre"]))],
    )
    fig3.update_layout(
        xaxis_title="Nombre",
        yaxis_title="Tiempo de resolución"
    )
    graph3 = fig3.to_json()
    
    return render_template('estadisticas.html', graph1=graph1, graph2=graph2, graph3=graph3 , x=nClientes, y=nIncidentes)

def main():
    init_db()
    main_program.load_data_from_json()
    ejercicio_5.prepare_ejercicio5()
    app.run(debug = True)

if __name__ == '__main__':
    main()
