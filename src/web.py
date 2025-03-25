import pandas as pd
from flask import Flask
import plotly.graph_objects as go
from flask import render_template
import main_program
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h2>Inicio</h2>' \
           '<a href=/>Ejercicio 2</a>' \
            '<br>' \
           '<a href=/>Ejercicio 3</a>' \
           '<br>' \
           '<a href=/>Ejercicio 4</a>'

if __name__ == '__main__':
    main_program.load_data_from_json()
    app.run(debug = True)
