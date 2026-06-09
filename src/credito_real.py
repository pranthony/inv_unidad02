"""
================================================================================
REGRESIÓN MÚLTIPLE POR MCO — DIAGNÓSTICO ECONOMÉTRICO COMPLETO
================================================================================
Modelo:  CR = f(TIR, TM, TD, NO, DM)
Datos:   Serie temporal mensual — Banco de datos BHOTZ SAC
         Fuente: Ultimo_tema.xlsx  |  Período: Ene-2015 → Dic-2025
         132 observaciones mensuales
--------------------------------------------------------------------------------
Autor   : Antony — UNHEVAL, Economía
Curso   : Econometría / Formulación de Proyectos de Inversión
Fecha   : 2026
================================================================================
"""

# ── 0. DEPENDENCIAS ────────────────────────────────────────────────────────────
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.diagnostic import (
    acorr_breusch_godfrey,
    het_breuschpagan,
)

warnings.filterwarnings("ignore")  # suprimir advertencias de convergencia menores


# ══════════════════════════════════════════════════════════════════════════════
# 1. CARGA Y LIMPIEZA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def parse_fecha(valor) -> pd.Timestamp:
    """
    Convierte el campo Tiempo a pd.Timestamp.

    El Excel contiene 11 celdas con formato textual 'SepYY' (p.ej. 'Sep20')
    en lugar del serial numérico de Excel.  Esta función normaliza ambos casos
    para producir un DatetimeIndex mensual limpio.

    Parámetros
    ----------
    valor : any
        Valor crudo leído por pd.read_excel().

    Retorna
    -------
    pd.Timestamp | pd.NaT
    """
    cadena = str(valor).strip()
    if cadena.lower().startswith("sep"):
        anio = "20" + cadena[3:]
        return pd.Timestamp(f"{anio}-09-01")
    try:
        return pd.Timestamp(valor)
    except Exception:
        return pd.NaT


def cargar_datos(ruta: str) -> pd.DataFrame:
    """
    Lee el archivo Excel, repara el índice temporal y devuelve un DataFrame
    indexado por DatetimeIndex con frecuencia mensual (inicio de mes).

    Parámetros
    ----------
    ruta : str
        Ruta al archivo .xlsx.

    Retorna
    -------
    pd.DataFrame  con columnas [CR, TIR, TM, TD, NO, DR]
                  e índice DatetimeIndex mensual.
    """
    df = pd.read_excel(ruta, sheet_name="Hoja1")

    # Sanear columna de tiempo
    df["Tiempo"] = df["Tiempo"].apply(parse_fecha)
    df = df.dropna(subset=["Tiempo"])              # eliminar NaT si los hubiese
    df = df.sort_values("Tiempo").reset_index(drop=True)

    # Establecer índice mensual estándar (primer día de cada mes)
    df = df.set_index("Tiempo")
    df.index = pd.DatetimeIndex(df.index).to_period("M").to_timestamp()
    df.index.name = "Fecha"

    # Renombrar dummy: en el Excel figura como 'DR', en el modelo es 'DM'
    df = df.rename(columns={"DR": "DM"})

    return df


# ══════════════════════════════════════════════════════════════════════════════
# 2. ESTADÍSTICAS DESCRIPTIVAS
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_descriptivos(df: pd.DataFrame) -> None:
    """Imprime estadísticos descriptivos básicos del panel de datos."""
    separador = "─" * 70
    print(separador)
    print("  ESTADÍSTICAS DESCRIPTIVAS")
    print(separador)
    print(f"  Período     : {df.index.min().strftime('%b-%Y')} → {df.index.max().strftime('%b-%Y')}")
    print(f"  Obs. totales: {len(df)}")
    print()
    print(df.describe().round(4).to_string())
    print(separador + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# 3. ESTIMACIÓN MCO
# ══════════════════════════════════════════════════════════════════════════════

VARIABLE_ENDOGENA   = "CR"
VARIABLES_EXOGENAS  = ["TIR", "TM", "TD", "NO", "DM"]


def estimar_mco(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    Estima el modelo de regresión múltiple por MCO.

        CR_t = β₀ + β₁·TIR_t + β₂·TM_t + β₃·TD_t + β₄·NO_t + β₅·DM_t + ε_t

    Parámetros
    ----------
    df : pd.DataFrame

    Retorna
    -------
    resultado : RegressionResultsWrapper (statsmodels OLS)
    """
    Y = df[VARIABLE_ENDOGENA]
    X = sm.add_constant(df[VARIABLES_EXOGENAS], has_constant="add")

    modelo = sm.OLS(endog=Y, exog=X)
    resultado = modelo.fit()
    return resultado


# ══════════════════════════════════════════════════════════════════════════════
# 4. DIAGNÓSTICO ECONOMÉTRICO
# ══════════════════════════════════════════════════════════════════════════════

ALPHA = 0.05   # nivel de significancia para todas las pruebas


def _veredicto(p_valor: float, alpha: float = ALPHA) -> str:
    """Retorna 'RECHAZA H₀' o 'NO rechaza H₀' según el p-valor."""
    return "✗  RECHAZA H₀" if p_valor < alpha else "✓  NO rechaza H₀"


def prueba_normalidad_jb(residuos: pd.Series) -> dict:
    """
    Prueba de Jarque-Bera para normalidad de los residuos.

    H₀ : Los residuos siguen una distribución Normal (sesgo=0, curtosis=3).
    H₁ : Los residuos NO son normales.

    Parámetros
    ----------
    residuos : pd.Series — residuos del modelo MCO.

    Retorna
    -------
    dict con estadístico, p-valor, sesgo y curtosis.
    """
    jb_stat, jb_p, sesgo, curtosis = jarque_bera(residuos)
    return {
        "prueba"     : "Jarque-Bera (Normalidad)",
        "estadistico": round(jb_stat, 4),
        "p_valor"    : round(jb_p, 4),
        "sesgo"      : round(float(sesgo), 4),
        "curtosis"   : round(float(curtosis), 4),
        "decision"   : _veredicto(jb_p),
    }


def prueba_autocorrelacion_bg(resultado, n_rezagos: int = 2) -> dict:
    """
    Prueba de Breusch-Godfrey para autocorrelación serial (LM test).

    Preferida sobre Durbin-Watson en series de tiempo porque:
      (a) aplica a modelos con variables dependientes rezagadas, y
      (b) contrasta autocorrelación de orden superior (AR(p), p > 1).

    H₀ : No existe autocorrelación serial hasta el rezago p.
    H₁ : Existe autocorrelación serial de algún orden ≤ p.

    Parámetros
    ----------
    resultado   : RegressionResultsWrapper
    n_rezagos   : int — número de rezagos a contrastar (default = 2).

    Retorna
    -------
    dict con estadístico LM, p-valor y estadístico F auxiliar.
    """
    lm_stat, lm_p, f_stat, f_p = acorr_breusch_godfrey(resultado, nlags=n_rezagos)
    return {
        "prueba"      : f"Breusch-Godfrey (Autocorrelación, {n_rezagos} rezagos)",
        "estadistico" : round(lm_stat, 4),
        "p_valor"     : round(lm_p, 4),
        "f_estadistico": round(f_stat, 4),
        "f_p_valor"   : round(f_p, 4),
        "decision"    : _veredicto(lm_p),
    }


def prueba_heterocedasticidad_bp(resultado) -> dict:
    """
    Prueba de Breusch-Pagan para heterocedasticidad.

    Regresa el cuadrado de los residuos sobre los regresores originales
    (forma paramétrica más parsimoniosa que la prueba de White).

    H₀ : Homocedasticidad — Var(ε_t | X) = σ² constante.
    H₁ : Heterocedasticidad — la varianza depende de algún regresor.

    Parámetros
    ----------
    resultado : RegressionResultsWrapper

    Retorna
    -------
    dict con estadístico LM, p-valor y estadístico F auxiliar.
    """
    lm_stat, lm_p, f_stat, f_p = het_breuschpagan(
        resultado.resid,
        resultado.model.exog,
    )
    return {
        "prueba"       : "Breusch-Pagan (Heterocedasticidad)",
        "estadistico"  : round(lm_stat, 4),
        "p_valor"      : round(lm_p, 4),
        "f_estadistico": round(f_stat, 4),
        "f_p_valor"    : round(f_p, 4),
        "decision"     : _veredicto(lm_p),
    }


def imprimir_diagnostico(resultados_pruebas: list[dict]) -> None:
    """Imprime el panel de diagnóstico econométrico formateado."""
    separador = "─" * 70
    print(separador)
    print("  DIAGNÓSTICO ECONOMÉTRICO  (α = {:.0%})".format(ALPHA))
    print(separador)

    for r in resultados_pruebas:
        print(f"\n  [{r['prueba']}]")
        print(f"    Estadístico LM : {r['estadistico']}")
        print(f"    P-valor        : {r['p_valor']}")

        # Mostrar campos extra si existen (F-stat, sesgo, curtosis)
        if "f_estadistico" in r:
            print(f"    F-estadístico  : {r['f_estadistico']}")
            print(f"    F p-valor      : {r['f_p_valor']}")
        if "sesgo" in r:
            print(f"    Sesgo          : {r['sesgo']}")
            print(f"    Curtosis       : {r['curtosis']}")

        print(f"    Decisión       : {r['decision']}")

    print("\n" + separador)
    print("  NOTAS DE INTERPRETACIÓN")
    print(separador)
    print("  • Jarque-Bera : si NO se rechaza H₀ → residuos normales (MCO válido).")
    print("  • Breusch-Godfrey: si se RECHAZA H₀ → autocorrelación detectada")
    print("    → considerar HAC (Newey-West) o modelo ARIMA en los errores.")
    print("  • Breusch-Pagan : si se RECHAZA H₀ → heterocedasticidad detectada")
    print("    → considerar errores robustos (HC3) o WLS.")
    print(separador + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# 5. PIPELINE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    RUTA_DATOS = "data/processed/Base_datos.xlsx"   # ajustar si el archivo está en otra ruta

    # ── 5.1 Carga de datos ────────────────────────────────────────────────────
    df = cargar_datos(RUTA_DATOS)

    separador_mayor = "═" * 70
    print(separador_mayor)
    print("  MODELO MCO — CRÉDITO REAL (CR)")
    print("  Variable endógena : CR  (Crédito Real, millones de S/)")
    print("  Regresores        : TIR · TM · TD · NO · DM")
    print(separador_mayor + "\n")

    mostrar_descriptivos(df)

    # ── 5.2 Estimación MCO ────────────────────────────────────────────────────
    resultado = estimar_mco(df)
    print("─" * 70)
    print("  RESUMEN DE REGRESIÓN (OLS)")
    print("─" * 70)
    print(resultado.summary())
    print()

    # ── 5.3 Pruebas de diagnóstico ────────────────────────────────────────────
    pruebas = [
        prueba_normalidad_jb(resultado.resid),
        prueba_autocorrelacion_bg(resultado, n_rezagos=2),
        prueba_heterocedasticidad_bp(resultado),
    ]
    imprimir_diagnostico(pruebas)

    # ── 5.4 Métricas de bondad de ajuste complementarias ─────────────────────
    separador = "─" * 70
    print(separador)
    print("  BONDAD DE AJUSTE COMPLEMENTARIA")
    print(separador)
    print(f"  R²            : {resultado.rsquared:.4f}")
    print(f"  R² ajustado   : {resultado.rsquared_adj:.4f}")
    print(f"  AIC           : {resultado.aic:.2f}")
    print(f"  BIC           : {resultado.bic:.2f}")
    print(f"  Durbin-Watson : {sm.stats.durbin_watson(resultado.resid):.4f}")
    print(f"  Log-Likelihood: {resultado.llf:.4f}")
    print(separador + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()