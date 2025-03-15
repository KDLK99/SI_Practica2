import pandas as pd
from flask import Flask
import plotly.graph_objects as go
import plotly
from flask import render_template
from flask import request
import json
import main_program
import stats
import plotly.express as px
import sqlite3
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


@app.route('/ejercicio_4')
def graficas():
    a = plotly.utils.PlotlyJSONEncoder
    # Primer apartado
    values_1 = stats.showMean()

    values1_dict = pd.DataFrame({
        "Tipo": ["Mantenimiento", "No Mantenimiento"],
        "Número de incidentes": values_1
    })


    fig1 = px.bar(values1_dict, x="Tipo", y="Número de incidentes", title="Número de incidentes agrupados por mantenimiento o no")

    graph1 = json.dumps(fig1, cls=a)

    # Segundo apartado

    def time_type_incident():
        # Conectar a la base de datos SQLite
        con = sqlite3.connect('../docs/datos.db')

        # Leer los datos de la tabla "tickets_emitidos"
        df = pd.read_sql_query("SELECT * FROM tickets_emitidos", con)
        con.close()  # Cerrar conexión

        # Asegurar que las fechas sean tipo datetime
        df["fecha_apertura"] = pd.to_datetime(df["fecha_apertura"])
        df["fecha_cierre"] = pd.to_datetime(df["fecha_cierre"])

        # Filtrar filas con valores nulos para evitar errores
        df = df.dropna(subset=["fecha_apertura", "fecha_cierre"])

        # Lista de tipos de incidente únicos
        type_list = df["tipo_incidencia"].unique().tolist()

        # Lista para almacenar los tiempos de resolución
        data = []

        # Calcular la diferencia entre fecha_apertura y fecha_cierre por tipo de incidente
        for tipo in type_list:
            tiempos_resolucion = (df.loc[df["tipo_incidencia"] == tipo, "fecha_cierre"] -
                                  df.loc[df["tipo_incidencia"] == tipo, "fecha_apertura"]).dt.days
            for tiempo in tiempos_resolucion:
                data.append({"Tipo de Incidente": tipo, "Tiempo de Resolución (días)": tiempo})

        return pd.DataFrame(data)

    # Obtener los datos en formato DataFrame
    df_plot = time_type_incident()

    # Crear gráfico de boxplot con Plotly
    fig = px.box(
        df_plot,
        x="Tipo de Incidente",
        y="Tiempo de Resolución (días)",
        points="outliers",  # Mostrar valores atípicos
        title="Distribución de tiempos de resolución por tipo de incidente"
    )

    # Calcular percentiles 5% y 90%
    percentiles = df_plot.groupby("Tipo de Incidente")["Tiempo de Resolución (días)"].quantile([0.05, 0.90]).unstack()

    # Agregar líneas para los percentiles 5% y 90%
    for tipo in df_plot["Tipo de Incidente"].unique():
        fig.add_hline(y=percentiles.loc[tipo, 0.05], line_dash="dot", line_color="red",
                      annotation_text=f"5% - Tipo {tipo}")
        fig.add_hline(y=percentiles.loc[tipo, 0.90], line_dash="dot", line_color="blue",
                      annotation_text=f"90% - Tipo {tipo}")

    # Mostrar gráfico
    fig.show()

    # Tercer apartado
    values_3 = stats.top5Critics()
    fig3 = px.bar(values_3, title="5 clientes más críticos")
    fig3.update_layout(
        xaxis_title="Nombre",
        yaxis_title="Número de incidentes"
    )
    graph3 = json.dumps(fig3, cls=a)

    # Cuarto apartado
    values_4 = stats.showEmployees()
    fig4 = px.bar(values_4, title="Usuarios con las acciones realizadas por los empleados")
    fig4.update_layout(
        xaxis_title="Nombre de los usuarios",
        yaxis_title="Número de acciones realizadas por los empleados"
    )
    graph4 = json.dumps(fig4, cls=a)


    # Quinto apartado
    results_week_day = stats.week_day()
    fig5 = plotly.plot(results_week_day, "bar")

    fig5.update_layout(title=dict(
        text="Número de actuaciones por día de la semana"
    ),
        xaxis=dict(
            title=dict(
                text="Día de la semana"
            )
        ),
        yaxis=dict(
            title=dict(
                text="Número de actuaciones"
            )
        )
    )

    graph5 = json.dumps(fig5, cls=a)
    return render_template('hello.html', graph1=graph1, graph3=graph3, graph4=graph4,graph5=graph5)
if __name__ == '__main__':
    app.run(debug = True)
