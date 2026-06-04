import pandas as pd
import os
def load_ipc(ruta: str = "ipc.xlsx") -> pd.DataFrame:
    """Carga los datos del Índice de Precios al Consumidor (IPC)."""
    return pd.read_excel(ruta)
def load_poblacion(ruta: str = "poblacion.xlsx") -> pd.DataFrame:
    """Carga los datos de población."""
    return pd.read_excel(ruta)
def load_enaho(ruta: str) -> pd.DataFrame:
    """Lee un archivo .csv de ENAHO."""
    df = pd.read_csv(ruta)
    df.columns = df.columns.str.lower()
    return df
def get_enaho_files(carpeta: str) -> list[str]:
    """Obtiene la lista de archivos .csv en la carpeta especificada."""
    archivos = []
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".csv"):
                archivos.append(archivo)
    return archivos