import pandas as pd
import numpy as np
import yfinance as yf

# 1. Definimos un diccionario con el nombre que queremos y su Ticker de Yahoo
tickers = {
    'Credicorp': 'BAP',
    'Peru_Mercado': 'EPU',
    'Precio_cobre': 'HG=F',
    'ETF_XLF': 'XLF'
}

# 2. Creamos un DataFrame vacío para ir guardando los precios
df_precios = pd.DataFrame()

print("Descargando datos...")
for nombre_columna, ticker in tickers.items():
    # Descargamos cada activo por separado
    data = yf.download(ticker, start="2020-12-01", end="2026-07-01", interval="1mo")
    
    # Si tiene 'Adj Close' lo usamos, si no (como el tipo de cambio), usamos 'Close'
    if 'Adj Close' in data.columns:
        df_precios[nombre_columna] = data['Adj Close']
    else:
        df_precios[nombre_columna] = data['Close']

# Limpiar filas donde se crucen días feriados o sin datos
df_precios = df_precios.dropna()

# 3. Transformar los precios a rendimientos logarítmicos
df_rendimientos = np.log(df_precios / df_precios.shift(1)).dropna()

# 4. Renombrar las columnas con el prefijo 'R_' para saber que son rendimientos
df_rendimientos.columns = ['R_Credicorp', 'R_Peru_Mercado', 'Precio_cobre', 'ETF_XLF']

# 5. Guardar el resultado en un CSV
df_rendimientos.to_csv("data/processed/base_datos_econometria.csv")

print("\n¡Todo listo! Base de datos guardada como 'base_datos_econometria.csv'")
print(f"Total de registros listos para la regresión: {len(df_rendimientos)}")
print(df_rendimientos.head())