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
    cliente = 2
    fecha_apertura = "2025-01-10"
    fecha_cierre = "2025-01-12"
    es_mantenimiento = True
    satisfaccion = 1
    tipo_incidencia = 1

    data = {"cliente": cliente, "fecha_apertura": fecha_apertura, "fecha_cierre": fecha_cierre,
            "es_mantenimiento": es_mantenimiento,
            "satisfaccion_cliente": satisfaccion, "tipo_incidencia": tipo_incidencia}
    a = extract_features(data)
    return pd.DataFrame(a, index=range(0, 1))

a = creacion_ticket()
y_pred = clf.predict(a)

print(y_pred)

# Decision Tree
# Entrenar Decision Tree Classifier
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)

# Predicciones y evaluación
b = creacion_ticket()
y_pred = tree_model.predict(b)

print(y_pred)

clf = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
clf.fit(X_train, y_train)

c = creacion_ticket()
y_pred = clf.predict(c)

print(y_pred)

