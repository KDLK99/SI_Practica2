import pandas as pd
from flask import Flask
import plotly.graph_objects as go
from flask import render_template, request, redirect, url_for, session, flash
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

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

if __name__ == '__main__':
    init_db()
    main_program.load_data_from_json()
    app.run(debug = True)
