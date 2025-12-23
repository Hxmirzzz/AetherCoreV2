import csv
import os
from datetime import datetime

HISTORY_FILE = os.path.join("logs", "historial_procesamiento.csv")

def log_history(
    nombre_archivo: str,
    acronimo: str,
    tipo_hoja: str,
    filas: int,
    columnas: int,
    archivo_salida: str,
    estado: str,
    error_msg: str = ""
):
    """
    Guarda un registro del procesamiento en un archivo CSV de historial.
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Encabezado solo si es nuevo
        if not file_exists:
            writer.writerow([
                "FECHA_PROCESO", "ARCHIVO_ORIGINAL", "ACRONIMO", "TIPO_HOJA",
                "FILAS", "COLUMNAS", "ARCHIVO_SALIDA", "ESTADO", "MENSAJE_ERROR"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nombre_archivo,
            acronimo,
            tipo_hoja,
            filas,
            columnas,
            archivo_salida,
            estado,
            error_msg
        ])