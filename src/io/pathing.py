import os
from src.core.config import get_dynamic_paths

def get_output_path(tipo_hoja: str, file_name: str) -> str:
    """
    Retorna la ruta de salida del archivo .txt a generar según el tipo de hoja.

    Lee la configuración dinámica (config.yaml o similar) para obtener la ruta adecuada:
    - PROCESAMIENTO → salida_proc
    - TRANSPORTE → salida_trans

    Si la carpeta no existe, la crea.

    Args:
        tipo_hoja (str): 'PROCESAMIENTO' o 'TRANSPORTE'.
        file_name (str): Nombre del archivo .txt generado.

    Returns:
        str: Ruta completa al archivo .txt donde se guardará.
    """
    rutas = get_dynamic_paths()
    output_dir = rutas['salida_proc'] if tipo_hoja == 'PROCESAMIENTO' else rutas['salida_trans']
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, file_name)