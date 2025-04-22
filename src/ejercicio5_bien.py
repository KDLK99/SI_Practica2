import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# Cargar los datos desde un archivo JSON
with open("../docs/data_clasified.json", "r") as file:
    data = json.load(file)["tickets_emitidos"]

# Preprocesamiento: transformar los datos a una tabla estructurada
def extract_features(ticket):
    total_tiempo_contacto = sum(c["tiempo"] for c in ticket["contactos_con_empleados"])
    dias_abierto = (pd.to_datetime(ticket["fecha_cierre"]) - pd.to_datetime(ticket["fecha_apertura"])).days
    return {
        "es_mantenimiento": int(ticket["es_mantenimiento"]),
        "satisfaccion_cliente": ticket["satisfaccion_cliente"],
        "tipo_incidencia": ticket["tipo_incidencia"],
        "tiempo_contacto_total": total_tiempo_contacto,
        "dias_abierto": dias_abierto,
        "es_critico": int(ticket["es_critico"])
    }

tickets = [extract_features(t) for t in data]
df = pd.DataFrame(tickets)

# Separar features (X) y etiquetas (y)
X = df.drop("es_critico", axis=1)
y = df["es_critico"]

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Crear el clasificador
clf = LogisticRegression(max_iter=1000)

# Entrenar el modelo
clf.fit(X_train, y_train)

# Predicción
y_pred = clf.predict(X_test)

# Resultados
print("Coeficientes del modelo:", clf.coef_)
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("Reporte de clasificación:")
print(classification_report(y_test, y_pred))

# Visualización (en 2D usando PCA si deseas, pero aquí mostramos simple)
plt.scatter(range(len(y_test)), y_test, color="black", label="Reales")
plt.scatter(range(len(y_pred)), y_pred, color="blue", marker='x', label="Predichos")
plt.title("Clasificación de Tickets Críticos")
plt.xlabel("Índice de muestra")
plt.ylabel("¿Crítico?")
plt.legend()
plt.grid(True)
plt.show()

def creacion_ticket():
    cliente = int(input())
    fecha_apertura = input()
    fecha_cierre = input()
    es_mantenimiento = bool(input())
    satisfaccion = int(input())
    tipo_incidencia = int(input())

    data = {"cliente":cliente, "fecha_apertura":fecha_apertura, "fecha_cierre":fecha_cierre, "es_mantenimiento":es_mantenimiento,
            "satisfaccion_cliente":satisfaccion, "tipo_incidencia":tipo_incidencia}
    return pd.DataFrame(data, index=range(0, 0))

a = creacion_ticket()
y_pred = clf.predict(a)

print(y_pred)

