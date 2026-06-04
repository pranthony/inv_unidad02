import os
import pandas as pd
from config import CARPETA_ENAHO, IPC
from data_loader import load_ipc, load_poblacion, load_enaho, get_enaho_files
from data_processing import procesar_encuesta, unir_datos

def main():
    print("Iniciando procesamiento...")
    
    try:
        ipc = load_ipc(IPC)
        poblacion = load_poblacion("poblacion.xlsx")
    except FileNotFoundError as e:
        print(f"Error al cargar archivos externos: {e}")
        return

    archivos_enaho = get_enaho_files(CARPETA_ENAHO)
    
    if not archivos_enaho:
        print(f"No se encontraron archivos .csv en el directorio: {CARPETA_ENAHO}")
        return

    resultados = []

    for archivo in archivos_enaho:
        try:
            anio = int(archivo[:4])
        except ValueError:
            print(f"No se pudo determinar el año del archivo {archivo}. Saltando...")
            continue
            
        ruta = os.path.join(CARPETA_ENAHO, archivo)
        print(f"Procesando archivo: {archivo} (Año {anio})...")
        
        try:
            df = load_enaho(ruta)
            resumen = procesar_encuesta(df, anio)
            if not resumen.empty:
                resultados.append(resumen)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    if not resultados:
        print("No se generaron resultados para procesar.")
        return

    print("Uniendo resultados...")
    panel_base = pd.concat(resultados, ignore_index=True)
    panel_final = unir_datos(panel_base, ipc, poblacion)

    ruta_salida = "panel_ingreso_real_huanuco.xlsx"
    panel_final.to_excel(ruta_salida, index=False)

    print(f"Proceso terminado. Archivo guardado en: {ruta_salida}")
    print(panel_final.head())

if __name__ == "__main__":
    main()
