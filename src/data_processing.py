import pandas as pd
import numpy as np
from config import VAR_UBIGEO, VAR_INGRESO, VAR_FACTOR, PROVINCIAS_HUANUCO

def procesar_encuesta(df: pd.DataFrame, anio: int) -> pd.DataFrame:
    """Filtra y procesa la encuesta para calcular el ingreso corriente por provincia."""
    columnas = [VAR_UBIGEO, VAR_INGRESO, VAR_FACTOR]
    
    # Validar que existan las columnas
    columnas_presentes = [c for c in columnas if c in df.columns]
    df = df[columnas_presentes].copy()
    df = df.dropna()
    
    if len(df) == 0:
        return pd.DataFrame()

    df[VAR_UBIGEO] = df[VAR_UBIGEO].astype(str)
    df["provincia"] = df[VAR_UBIGEO].str[:4]
    
    df = df[df["provincia"].isin(PROVINCIAS_HUANUCO.keys())]
    
    if len(df) == 0:
        return pd.DataFrame()

    resumen = (
        df.groupby("provincia")
        .apply(
            lambda x: pd.Series({
                "ingreso_corriente":
                    np.sum(x[VAR_INGRESO] * x[VAR_FACTOR]) /
                    np.sum(x[VAR_FACTOR])
            })
        )
        .reset_index()
    )
    resumen["anio"] = anio
    return resumen

def unir_datos(panel: pd.DataFrame, ipc: pd.DataFrame, poblacion: pd.DataFrame) -> pd.DataFrame:
    """Une el panel base con datos de IPC y Población y calcula valores reales."""
    
    # Agregar IPC
    panel = panel.merge(ipc, on="anio", how="left")
    panel["ingreso_real"] = (panel["ingreso_corriente"] / panel["ipc"] * 100)
    
    # Agregar Población
    panel = panel.merge(poblacion, on=["anio", "provincia"], how="left")
    panel["ingreso_percapita_real"] = (panel["ingreso_real"] / panel["poblacion"])
    
    # Agregar nombre de provincia
    panel["nombre_provincia"] = panel["provincia"].map(PROVINCIAS_HUANUCO)
    
    # Seleccionar orden final de columnas
    columnas_finales = [
        "anio",
        "provincia",
        "nombre_provincia",
        "ingreso_corriente",
        "ipc",
        "ingreso_real",
        "poblacion",
        "ingreso_percapita_real"
    ]
    
    # Filtrar solo columnas presentes por seguridad
    columnas_finales = [c for c in columnas_finales if c in panel.columns]
    panel = panel[columnas_finales]
    
    return panel
