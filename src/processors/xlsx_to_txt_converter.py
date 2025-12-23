import time
import pandas as pd
from datetime import datetime
from src.io.reader import read_excel
from src.io.naming import generate_filename
from src.core.file_operations import save
from src.core.logger_config import setup_logger
from src.core.history_log import log_history
from src.core.expected_columns import EXPECTED_COLUMNS, OPTIONAL_COLUMNS, REQUIRED_COLUMNS
from src.core.config import get_transportadora

logger = setup_logger()

TRANSPORTADORA = get_transportadora()

def validate_columns(df, tipo_hoja):
    """
    Valida que las columnas requeridas estén presentes en el DataFrame
    y que no existan columnas no reconocidas según la configuración para el tipo de hoja.

    Args:
        df (pd.DataFrame): DataFrame a validar.
        tipo_hoja (str): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE').

    Raises:
        ValueError: Si faltan columnas requeridas.
        logger.warning: Si existen columnas adicionales no reconocidas.
    """
    tipo_hoja = tipo_hoja.upper()

    required = set(EXPECTED_COLUMNS[tipo_hoja])
    optional = set(OPTIONAL_COLUMNS.get(tipo_hoja, []))
    allowed = required.union(optional)

    actual = set(df.columns)

    missing = required - actual
    extra = actual - allowed

    if missing:
        raise ValueError(f"Faltan columnas en {tipo_hoja}: {', '.join(missing)}")
    if extra:
        logger.warning(f"Columnas no reconocidas detectadas en {tipo_hoja}: {', '.join(extra)}")
        
def validate_critical_columns(df, tipo_hoja):
    """
    Valida que las columnas críticas (requeridas) no estén completamente vacías.
    Las columnas opcionales no se revisan aquí.
    """
    tipo_hoja = tipo_hoja.upper()
    critical_columns = REQUIRED_COLUMNS.get(tipo_hoja, [])
    empty_cols = []

    for col in critical_columns:
        if col in df.columns:
            if df[col].replace('', pd.NA).dropna().empty:
                empty_cols.append(col)

    if empty_cols:
        raise ValueError(f"Columnas vacías críticas en {tipo_hoja}: {', '.join(empty_cols)}")

def process_xlsx_file(file_path):
    """
    Procesa un archivo .xlsx que contiene dos hojas: 'Procesamiento' y 'Transporte'.
    Genera archivos .txt para cada hoja si el esquema es válido.

    Args:
        file_path (str): Ruta del archivo Excel (.xlsx) a procesar.

    Side Effects:
        - Guarda dos archivos .txt formateados en la carpeta correspondiente.
        - Escribe información en el logger durante todo el proceso.

    Raises:
        Exception: Si ocurre un error inesperado durante el procesamiento.
    """
    try:
        logger.info(f"Procesando archivo: {file_path}")
        start_time = time.time()
        
        df_proc, df_trans = read_excel(file_path)
        acronimo = str(df_proc['ENTIDAD'].iloc[0]).strip()
        fecha_actual = datetime.now()
        
        validate_columns(df_proc, "PROCESAMIENTO")
        validate_columns(df_trans, "TRANSPORTE")
        validate_critical_columns(df_proc, "PROCESAMIENTO")
        validate_critical_columns(df_trans, "TRANSPORTE")
        
        # HOJA PROCESAMIENTO
        nombre_proc = generate_filename("PROCESAMIENTO", TRANSPORTADORA, acronimo, fecha_actual)
        output_proc = save(df_proc, "PROCESAMIENTO", nombre_proc)
        logger.info(f"Procesamiento completado: {output_proc}")
        logger.info(f"Filas: {len(df_proc)}, Columnas: {df_proc.shape[1]}")
        log_history(file_path, acronimo, "PROCESAMIENTO", len(df_proc), df_proc.shape[1], output_proc, "EXITO")

        #HOJA TRANSPORTE
        nombre_trans = generate_filename("TRANSPORTE", TRANSPORTADORA, acronimo, fecha_actual)
        output_trans = save(df_trans, "TRANSPORTE", nombre_trans)
        logger.info(f"Transporte completado: {output_trans}")
        logger.info(f"Filas: {len(df_trans)}, Columnas: {df_trans.shape[1]}")
        log_history(file_path, acronimo, "TRANSPORTE", len(df_trans), df_trans.shape[1], output_trans, "EXITO")
        
        total_time = round(time.time() - start_time, 2)
        logger.info(f"Tiempo total: {total_time} segundos")
        
    except Exception as e:
        logger.error(f"Error al procesar {file_path}: {e}")
        log_history(file_path, "N/A", "GENERAL", 0, 0, "", "ERROR", str(e))