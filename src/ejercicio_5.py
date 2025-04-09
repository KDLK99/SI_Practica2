import pandas
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn import metrics
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_json("../docs/data_clasified.json")

data_list = data["tickets_emitidos"]

good_data = []

for i in range(len(data_list)):
    good_data.append(data_list[i])

good_dataframe = pd.DataFrame(good_data)

data_regresion = good_dataframe[["es_critico", "tipo_incidencia"]]

Y = data_regresion["tipo_incidencia"]
X = data_regresion[["es_critico"]]

x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.8)
model_lr = LinearRegression()
model_lr.fit(x_train, y_train)

y_pred_1 = model_lr.predict(x_train)
plt.scatter(x_train, y_train)
plt.scatter(x_train, y_pred_1, color="red")
plt.show()
print("a")