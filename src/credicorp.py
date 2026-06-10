import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.diagnostic as sms
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 1. Cargar la base de datos (generada en el paso anterior)
df = pd.read_csv("data/processed/base_datos_econometria.csv", index_col=0)

# Definir Variable Dependiente (Y) e Independientes (X)
y = df['R_Credicorp']
X = df[['R_Peru_Mercado', 'Precio_cobre', 'ETF_XLF']]

# ESENCIAL EN ECONOMETRÍA: Añadir la constante (Beta_0 o Intercepto)
X = sm.add_constant(X)

# 2. Ajustar el modelo de Regresión Múltiple (MCO / OLS)
modelo = sm.OLS(y, X).fit()

# Guardar los residuos (los necesitaremos para las pruebas de diagnóstico)
residuos = modelo.resid


# ==============================================================================
# IMPRESIÓN DE RESULTADOS
# ==============================================================================

print("======= 1. COEFICIENTES Y 2. NIVEL DE SIGNIFICANCIA =======")
print(modelo.summary())
print("\n" + "="*60 + "\n")

print("======= 3. PRUEBA DE NORMALIDAD (Jarque-Bera) =======")
jb_estadistico, p_valor = stats.jarque_bera(residuos)
print(f"Estadístico Jarque-Bera: {jb_estadistico:.4f}")
print(f"p-valor: {p_valor:.4f}")
if p_valor > 0.05:
    print("Resultado: No se rechaza H0. Los residuos se distribuyen NORMALMENTE.")
else:
    print("Resultado: Se rechaza H0. Los residuos NO se distribuyen normalmente.")
print("\n" + "="*60 + "\n")

print("======= 4. AUTOCORRELACIÓN =======")
# Durbin-Watson (ya viene en el summary, pero lo analizamos aquí)
dw = sm.stats.stattools.durbin_watson(residuos)
print(f"Estadístico Durbin-Watson: {dw:.4f}")
if 1.5 <= dw <= 2.5:
    print("Resultado (DW): No hay indicios graves de autocorrelación de primer orden.")
else:
    print("Resultado (DW): Alerta. Posible presencia de autocorrelación.")

# Prueba más robusta: Breusch-Godfrey (para autocorrelación de orden superior, ej. 2 rezagos)
bg_test = sms.acorr_breusch_godfrey(modelo, nlags=2)
bg_pvalue = bg_test[1]
print(f"p-valor (Breusch-Godfrey): {bg_pvalue:.4f}")
if bg_pvalue > 0.05:
    print("Resultado (BG): No hay autocorrelación en los residuos.")
else:
    print("Resultado (BG): Se rechaza H0. Existe AUTOCORRELACIÓN.")
print("\n" + "="*60 + "\n")

print("======= 5. HETEROCEDASTICIDAD (Breusch-Pagan) =======")
bp_test = sms.het_breuschpagan(residuos, X)
bp_pvalue = bp_test[1]
print(f"p-valor (Breusch-Pagan): {bp_pvalue:.4f}")
if bp_pvalue > 0.05:
    print("Resultado: No se rechaza H0. Los residuos son HOMOCEDÁSTICOS (Varianza constante).")
else:
    print("Resultado: Se rechaza H0. Los residuos sufren de HETEROCEDASTICIDAD.")