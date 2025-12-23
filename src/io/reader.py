import pandas as pd

def read_excel(file_path):
    """
    Lee un archivo Excel (.xlsx) y extrae dos hojas: 'Procesamiento' y 'Transporte'.

    Args:
        file_path (str): Ruta del archivo Excel.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: DataFrames de las dos hojas esperadas.

    Raises:
        ValueError: Si alguna de las hojas no está presente en el archivo.
    """
    xls = pd.ExcelFile(file_path)
    df_proc = pd.read_excel(xls, 'Procesamiento')
    df_trans = pd.read_excel(xls, 'Transporte')
    return df_proc, df_trans