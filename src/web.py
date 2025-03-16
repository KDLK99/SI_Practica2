import pandas as pd
from flask import Flask
import plotly.graph_objects as go
import plotly
from flask import render_template
import json
import main_program
import stats
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h2>Inicio</h2>' \
           '<a href=/ejercicio_2>Ejercicio 2</a>' \
            '<br>' \
           '<a href=/ejercicio_3>Ejercicio 3</a>' \
           '<br>' \
           '<a href=/ejercicio_4>Ejercicio 4</a>'

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
                f'<p><b>Empleado con menos tickets:</b> {results[12][0]} ({results[12][1]} veces)</p>' \
                f'<br>' \
                f'<br>' \
                f'<a href=/>Volver</a>'
    return html_code

@app.route('/ejercicio_3')
def ejercicio3():
    results = main_program.calc_values2()
    return render_template('ex3.html', empleado_1=results[0].to_html(classes='data', header="true", index=False),
                        empleado_2=results[1].to_html(classes='data', header="true", index=False),
                        empleado_3=results[2],
                        empleado_4=results[3],
                        empleado_5=results[4],
                        empleado_6=results[5],
                        empleado_7=results[6],
                        nivel_1=results[7].to_html(classes='data', header="true", index=False),
                        nivel_2=results[8].to_html(classes='data', header="true", index=False),
                        nivel_3=results[9],
                        nivel_4=results[10],
                        nivel_5=results[11],
                        nivel_6=results[12],
                        nivel_7=results[13],
                        cliente_1=results[14].to_html(classes='data', header="true", index=False),
                        cliente_2=results[15].to_html(classes='data', header="true", index=False),
                        cliente_3=results[16],
                        cliente_4=results[17],
                        cliente_5=results[18],
                        cliente_6=results[19],
                        cliente_7=results[20],
                        tipo_de_incidente_1=results[21].to_html(classes='data', header="true", index=False),
                        tipo_de_incidente_2=results[22].to_html(classes='data', header="true", index=False),
                        tipo_de_incidente_3=results[23],
                        tipo_de_incidente_4=results[24],
                        tipo_de_incidente_5=results[25],
                        tipo_de_incidente_6=results[26],
                        tipo_de_incidente_7=results[27],
                        dia_de_la_semana_1=results[28].to_html(classes='data', header="true", index=False),
                        dia_de_la_semana_2=results[29].to_html(classes='data', header="true", index=False),
                        dia_de_la_semana_3=results[30],
                        dia_de_la_semana_4=results[31],
                        dia_de_la_semana_5=results[32],
                        dia_de_la_semana_6=results[33],
                        dia_de_la_semana_7=results[34])


@app.route('/ejercicio_4')
def graficas():
    a = plotly.utils.PlotlyJSONEncoder
    # Primer apartado
    values_1 = stats.showMean()
    fig1 = go.Figure(
      data=[go.Bar(y=[values_1[0], values_1[1]],x=["Mantenimiento", "No Mantenimiento"])],
      layout_title_text="Número de incidentes agrupados por mantenimiento o no",
    )
    fig1.update_layout(
        xaxis_title="Tipo",
        yaxis_title="Número de incidentes"
    )
    graph1 = json.dumps(fig1, cls=a)

    # Segundo apartado
    df_plot = stats.time_type_incident()

    fig2 = px.box(df_plot, x=df_plot.iloc[:, 0], y=df_plot.iloc[:, 1])

    fig2.update_layout(
        title=dict(
            text="Número de actuaciones por día de la semana"
        ),
        xaxis_title="Tipo incidencia",
        yaxis_title="Tiempos de resolución",

    )
    percentiles = df_plot.groupby("Tipo de Incidente")["Tiempo de Resolución (días)"].quantile([0.05, 0.90]).unstack()

    # Agregar líneas para los percentiles 5% y 90%
    for tipo in df_plot["Tipo de Incidente"].unique():
        fig2.add_hline(y=percentiles.loc[tipo, 0.05], line_dash="dot", line_color="red",
                       annotation_text=f"5% - Tipo {tipo}")
        fig2.add_hline(y=percentiles.loc[tipo, 0.90], line_dash="dot", line_color="blue",
                       annotation_text=f"90% - Tipo {tipo}")
    graph2 = json.dumps(fig2, cls=a)

    # Tercer apartado
    values_3 = stats.top5Critics()
    fig3 = go.Figure(
        data=[go.Bar(y=list(values_3.values), x=list(values_3.keys().values))],
        layout_title_text="5 clientes más críticos",
    )
    fig3.update_layout(
        xaxis_title="Nombre",
        yaxis_title="Número de incidentes"
    )
    graph3 = json.dumps(fig3, cls=a)

    # Cuarto apartado
    values_4 = stats.showEmployees()
    fig4 = go.Figure(
        data=[go.Bar(y=list(values_4.values), x=list(values_4.keys().values))],
        layout_title_text="Usuarios con las acciones realizadas por los empleados",
    )
    fig4.update_layout(
        xaxis_title="Nombre de los usuarios",
        yaxis_title="Número de acciones realizadas por los empleados"
    )
    graph4 = json.dumps(fig4, cls=a)


    # Quinto apartado
    results_week_day = stats.week_day()
    fig5 = go.Figure(
        data=[go.Bar(y=[results_week_day[2], results_week_day[4], results_week_day[5], results_week_day[6], results_week_day[0],
                        results_week_day[1], results_week_day[3]],
        x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])],

    )

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
    return render_template('hello.html', graph1=graph1,graph2=graph2, graph3=graph3, graph4=graph4,graph5=graph5)
if __name__ == '__main__':
    app.run(debug = True)
