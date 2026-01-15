import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

BASE_PATH = os.getenv("FACTURACION_BASE_PATH", "C:/Facturacion")

def load_config():
    return {
        "BASE_PATH": BASE_PATH,
        "TRANSPORTADORA": os.getenv("TRANSPORTADORA", "TRANSPORT"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO").upper()
    }

def get_transportadora():
    return os.getenv("TRANSPORTADORA", "TRANSPORT")

def get_dynamic_paths():
    """
    Devuelve las rutas de entrada y salida dinámicamente según la fecha actual.
    Crea las carpetas si no existen.

    Returns:
    dict: {'entrada': str, 'salida_proc': str, 'salida_trans': str, 'fecha_str': str}
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month_number = now.month
    date_str = now.strftime("%d%m%Y")
    
    month_names = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    month = month_names[month_number - 1]
    
    entrada = os.path.join(BASE_PATH, year, month, "Entrada")
    salida_proc = os.path.join(BASE_PATH, year, month, "Salida", "Procesamiento")
    salida_trans = os.path.join(BASE_PATH, year, month, "Salida", "Transporte")
    
    for ruta in [entrada, salida_proc, salida_trans]:
        os.makedirs(ruta, exist_ok=True)
        
    return {
        "entrada": entrada,
        "salida_proc": salida_proc,
        "salida_trans": salida_trans,
        "date_str": date_str
    }