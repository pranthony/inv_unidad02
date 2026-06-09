import pandas as pd

# Cargar tus datos
df = pd.read_csv('data/processed/Ultimo_tema.csv', sep=';')
print(df)

# Aplicar interpolación lineal a la columna NO
df['NO_Completada'] = df['NO'].interpolate(method='linear')

# Guardar el nuevo archivo listo
df.to_csv('Datos_Completados.csv', index=False)