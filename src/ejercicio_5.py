# Regresion Lineal
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Cargar los datos
with open('../docs/data_clasified.json', 'r') as f:
    data = json.load(f)['tickets_emitidos']

# Preprocesamiento
def extract_features(ticket):
    tiempo_total = sum([c['tiempo'] for c in ticket['contactos_con_empleados']])
    return {
        'es_mantenimiento': int(ticket['es_mantenimiento']),
        'satisfaccion_cliente': ticket['satisfaccion_cliente'],
        'tipo_incidencia': ticket['tipo_incidencia'],
        'tiempo_total_contacto': tiempo_total,
        'es_critico': int(ticket['es_critico'])
    }

df = pd.DataFrame([extract_features(t) for t in data])

# Separar features y target
X = df.drop('es_critico', axis=1)
y = df['es_critico']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Predicciones
y_pred = model.predict(X_test)

# Evaluación
print("MSE:", mean_squared_error(y_test, y_pred))
print("R^2 Score:", r2_score(y_test, y_pred))

# Mostrar algunas predicciones redondeadas
print("\nPredicciones (redondeadas):")
print(np.round(y_pred[:10]))
print("Reales:")
print(y_test.values[:10])


# Cargar los datos desde el archivo
file_path = "../docs/data_clasified.json"
with open(file_path, 'r') as f:
    data = json.load(f)['tickets_emitidos']

# Extraer características
def extract_features(ticket):
    tiempo_total = sum([c['tiempo'] for c in ticket['contactos_con_empleados']])
    return {
        'es_mantenimiento': int(ticket['es_mantenimiento']),
        'satisfaccion_cliente': ticket['satisfaccion_cliente'],
        'tipo_incidencia': ticket['tipo_incidencia'],
        'tiempo_total_contacto': tiempo_total,
        'es_critico': int(ticket['es_critico'])
    }

# Crear DataFrame
df = pd.DataFrame([extract_features(t) for t in data])

# Separar datos
X = df.drop('es_critico', axis=1)
y = df['es_critico']

# Dividir conjunto de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Predecir
y_pred = model.predict(X_test)

# Visualización: comparación entre predicciones y valores reales
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([0, 1], [0, 1], '--', color='red')  # línea de referencia
plt.xlabel('Valor real (es_critico)')
plt.ylabel('Predicción de regresión lineal')
plt.title('Gráfico de regresión: Valor real vs Predicción')
plt.grid(True)
plt.tight_layout()
plt.show()

# Decision Tree
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Cargar los datos
file_path = "../docs/data_clasified.json"
with open(file_path, 'r') as f:
    data = json.load(f)['tickets_emitidos']

# Extraer características
def extract_features(ticket):
    tiempo_total = sum(c['tiempo'] for c in ticket['contactos_con_empleados'])
    return {
        'es_mantenimiento': int(ticket['es_mantenimiento']),
        'satisfaccion_cliente': ticket['satisfaccion_cliente'],
        'tipo_incidencia': ticket['tipo_incidencia'],
        'tiempo_total_contacto': tiempo_total,
        'es_critico': int(ticket['es_critico'])
    }

df = pd.DataFrame([extract_features(t) for t in data])

# Separar features y target
X = df.drop('es_critico', axis=1)
y = df['es_critico']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar Decision Tree Classifier
tree_model = DecisionTreeClassifier(max_depth=3, random_state=42)
tree_model.fit(X_train, y_train)

# Predicciones y evaluación
y_pred = tree_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=['No crítico', 'Crítico']))

# Visualizar el árbol
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
