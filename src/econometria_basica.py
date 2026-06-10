# importar librerias
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# cargar datos

# datos desde google drive 
url = "https://docs.google.com/spreadsheets/d/16Tp3jetE_DNAN-yDG0XHxljK3uYY9xpjbb6zPEtQ4d8/export?format=csv"
data = pd.read_csv(url)

# mostrar los primeros registros
#print(data.head())

# mostrar información general del dataframe
# print(data.describe())

# inicializar datos
y = data['Crecimiento_Y']

# que todas las variables independientes esten en un mismo dataframe
x = data[['Regulacion_X1', 'Bolsa_Sost_X2', 'Token_Burn_X3', 'Sentimiento_X4']]

# agregar una constante a las variables independientes
x = sm.add_constant(x)

# ajustar el modelo de regresión lineal multiple
model = sm.OLS(y, x).fit()

# mostrar el resumen del modelo
print(model.summary())