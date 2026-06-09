# importar librerias
import pandas as pd
import matplotlib.pyplot as plt

# cargar datos
data = pd.read_csv('data/processed/bonos_verdes.csv')

# mostrar los primeros registros
print(data.head())

# mostrar información general del dataframe
print(data.describe())

plt.scatter( data['Sorpresa_Inflacion_X1'], data['Retorno_BonoVerde_Y'])
plt.xlabel('Sorpresa Inflacion')
plt.ylabel('Retorno Bono Verde')
plt.title('Relación entre Sorpresa Inflacion y Retorno Bono Verde')
plt.show()

# prepar datos
X = data['Sorpresa_Inflacion_X1']
y = data['Retorno_BonoVerde_Y']

# agregar constante para el modelo de regresión
import statsmodels.api as sm
X = sm.add_constant(X)

# ajustar modelo de regresión lineal
model = sm.OLS(y, X).fit()

# mostrar resumen del modelo
print(model.summary())

