import json
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Leer el archivo de datos ya clasificados
with open("../docs/data_clasified.json", "r") as file:
    data = json.load(file)["tickets_emitidos"]


# Preprocesamiento: transformar los datos a una tabla estructurada
def extract_features(ticket):
    dias_abierto = (pd.to_datetime(ticket["fecha_cierre"]) - pd.to_datetime(ticket["fecha_apertura"])).days
    try:
        return {
            "es_mantenimiento": int(ticket["es_mantenimiento"]),
            "satisfaccion_cliente": ticket["satisfaccion_cliente"],
            "tipo_incidencia": ticket["tipo_incidencia"],
            "dias_abierto": dias_abierto,
            "es_critico": int(ticket["es_critico"])
        }
    except:
        return {
            "es_mantenimiento": int(ticket["es_mantenimiento"]),
            "satisfaccion_cliente": ticket["satisfaccion_cliente"],
            "tipo_incidencia": ticket["tipo_incidencia"],
            "dias_abierto": dias_abierto,
        }

# Sacar las caracterísiticas y crear un DataFrame con ello
tickets = [extract_features(t) for t in data]
df = pd.DataFrame(tickets)

# Separar X e y
X = df.drop("es_critico", axis=1)
y = df["es_critico"]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Regresión lineal
reg = LinearRegression()
reg.fit(X_train, y_train)

# Predicción
y_pred_continuo = reg.predict(X_test)
y_pred = (y_pred_continuo > 0.5).astype(int)  # Umbral para convertir a clasificación

# Resultados
print("Coeficientes del modelo:", reg.coef_)
print("Intercepto:", reg.intercept_)
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("Reporte de clasificación:")
print(classification_report(y_test, y_pred))

# Visualización
plt.scatter(range(len(y_test)), y_test, color="black", label="Reales")
plt.scatter(range(len(y_pred)), y_pred, color="blue", marker='x', label="Predichos (umbralizado)")
plt.title("Regresión Lineal sobre Tickets Críticos")
plt.xlabel("Índice de muestra")
plt.ylabel("¿Crítico?")
plt.legend()
plt.grid(True)
plt.show()

# Función para crear tickets
def creacion_ticket():
    cliente = 5
    fecha_apertura = "2025-05-07"
    fecha_cierre = "2025-05-14"
    es_mantenimiento = False
    satisfaccion = 3
    tipo_incidencia = 4

    data = {"cliente": cliente, "fecha_apertura": fecha_apertura, "fecha_cierre": fecha_cierre,
            "es_mantenimiento": es_mantenimiento,
            "satisfaccion_cliente": satisfaccion, "tipo_incidencia": tipo_incidencia}
    a = extract_features(data)
    return pd.DataFrame(a, index=range(0, 1))
# Predicción con Regresión Lineal
a = creacion_ticket()
y_pred = reg.predict(a)

if y_pred[0] >= 0.5:
    y_pred[0] = 1
else:
    y_pred[0] = 0
print(y_pred)

# Decision Tree
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)

# Predicciones y evaluación
b = creacion_ticket()
y_pred = tree_model.predict(b)

print(y_pred)
# Mostrar el modelo
plt.figure(figsize=(12, 8))
plot_tree(
    tree_model,
    feature_names=X.columns,
    class_names=['No crítico', 'Crítico'],
    filled=False,
    rounded=True,
    proportion=True
)
plt.title('Árbol de Decisión (profundidad máxima = 3)')
plt.tight_layout()
plt.show()

# Random Forest
clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf.fit(X_train, y_train)

c = creacion_ticket()
y_pred = clf.predict(c)

print(y_pred)

# Mostrar modelo
n_estimators = len(clf.estimators_)
cols = 5  # Número de columnas por fila
rows = (n_estimators + cols - 1) // cols  # Número de filas necesarias

fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
axes = axes.flatten()

for i, tree in enumerate(clf.estimators_):
    plot_tree(
        tree,
        feature_names=X.columns,
        class_names=['No crítico', 'Crítico'],
        filled=True,
        rounded=True,
        proportion=True,
        ax=axes[i]
    )
    axes[i].set_title(f'Árbol {i}')

# Eliminar subplots no usados si clf.n_estimators no es múltiplo de cols
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
