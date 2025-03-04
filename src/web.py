from flask import Flask
import plotly.graph_objects as go
from flask import render_template
from flask import request
import json
import main_program
import stats
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/ejercicio_2')
def ejercicio2():
    results = main_program.calc_values()
    html_code = f'<p><b>Número de tickets emitidos (muestras):</b> {results[0]}</p>' \
                f'<p><b>Media de los incidentes con valoración mayor de 5:</b> {results[1]:.2f}</p>' \
                f'<p><b>Desviación típica de los incidentes con valoración mayor de 5:</b> {results[2]:.2f}</p>' \
                f'<p><b>Media del número de incidentes por cliente:</b> {results[3]}</p>' \
                f'<p><b>Desviación típica del número de incidentes por cliente:</b> {results[4]:.2f}</p>' \
                f'<p><b>Media del número de horas por incidente:</b> {results[5]}</p>' \
                f'<p><b>Desviación típica de las horas por incidente:</b> {results[6]:.2f}</p>' \
                f'<p><b>Empleado con más horas trabajadas:</b> {results[7][0]} ({results[7][1]} horas)</p>' \
                f'<p><b>Empleado con menos horas trabajadas:</b> {results[8][0]} ({results[8][1]} horas)</p>' \
                f'<p><b>Diferencia mínima:</b> {results[9]} días</p>' \
                f'<p><b>Diferencia máxima:</b> {results[10]} días</p>' \
                f'<p><b>Empleado con más tickets:</b> {results[11][0]} ({results[11][1]} veces)</p>' \
                f'<p><b>Empleado con menos tickets:</b> {results[12][0]} ({results[12][1]} veces)</p>'
    return html_code


@app.route('/foto_pies')
def graficas():
    fig = go.Figure(
        data=[go.Bar(y=[2, 1, 3])],
        layout_title_text="Figura"
    )
    # fig.show()
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('hello.html', graphJSON=graphJSON)
if __name__ == '__main__':
    app.run(debug = True)
