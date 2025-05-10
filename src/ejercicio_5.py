import json
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

reg = 0
tree_model = 0
random_forest = 0


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

def linear_regression(X_train, y_train, X_test, y_test):
    
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    
    y_pred_continuo = reg.predict(X_test)
    y_pred = (y_pred_continuo > 0.5).astype(int)  

    plt.scatter(range(len(y_test)), y_test, color="black", label="Reales")
    plt.scatter(range(len(y_pred)), y_pred, color="blue", marker='x', label="Predichos (umbralizado)")
    plt.title("Regresión Lineal sobre Tickets Críticos")
    plt.xlabel("Índice de muestra")
    plt.ylabel("¿Crítico?")
    plt.legend()
    plt.grid(True)
    
    plt.savefig("static/plot1.png")
    plt.close()


    return reg

def decision_tree(X_train, y_train, X):
    
    tree_model = DecisionTreeClassifier()
    tree_model.fit(X_train, y_train)

    
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
    
    plt.savefig("static/plot2.png")
    plt.close()

    return tree_model

def randomForest(X_train, y_train, X):
    
    random_forest = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
    random_forest.fit(X_train, y_train)


    
    n_estimators = len(random_forest.estimators_)
    cols = 5  
    rows = (n_estimators + cols - 1) // cols  

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    axes = axes.flatten()

    for i, tree in enumerate(random_forest.estimators_):
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

    
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    
    plt.savefig("static/plot3.png")
    plt.close()

    return random_forest


def creacion_ticket(cliente, fecha_apertura, fecha_cierre, es_mantenimiento, satisfaccion, tipo_incidencia):
    data = {"cliente": cliente, "fecha_apertura": fecha_apertura, "fecha_cierre": fecha_cierre,
            "es_mantenimiento": es_mantenimiento,
            "satisfaccion_cliente": satisfaccion, "tipo_incidencia": tipo_incidencia}
    a = extract_features(data)
    return pd.DataFrame(a, index=range(0, 1))


def prediccion(decision, ticket, reg, tree_model, random_forest):
    result = None
    
    if decision == '0':
        result = reg.predict(ticket)

        if result[0] >= 0.5:
            result[0] = 1
        else:
            result[0] = 0

    
    elif decision == '1':
        result = tree_model.predict(ticket)
    
    elif decision == '2':
        result = random_forest.predict(ticket)

    return result


def ejercicio5(decision, ticket):
    return prediccion(decision, ticket, reg, tree_model, random_forest)

def prepare_ejercicio5():
    with open("../docs/data_clasified.json", "r") as file:
            data = json.load(file)["tickets_emitidos"]

    
    tickets = [extract_features(t) for t in data]
    df = pd.DataFrame(tickets)

    
    X = df.drop("es_critico", axis=1)
    y = df["es_critico"]

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    global reg 
    reg = linear_regression(X_train, y_train, X_test, y_test)
    global tree_model
    tree_model = decision_tree(X_train, y_train, X)
    global random_forest
    random_forest = randomForest(X_train, y_train, X)