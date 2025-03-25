import pandas as pd
from flask import Flask
import plotly.graph_objects as go
import plotly
from flask import render_template
import json
import main_program
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h2>Inicio</h2>' \
           '<a href=/ejercicio_1>Ejercicio 2</a>' \
            '<br>' \
           '<a href=/ejercicio_2>Ejercicio 3</a>' \
           '<br>' \
           '<a href=/ejercicio_3>Ejercicio 4</a>'

@app.route('/ejercicio_1')
def ejercicio2():
    pass

@app.route('/ejercicio_2')
def ejercicio2():
    pass

@app.route('/ejercicio_3')
def ejercicio3():
    pass


if __name__ == '__main__':
    main_program.load_data_from_json()
    app.run(debug = True)
