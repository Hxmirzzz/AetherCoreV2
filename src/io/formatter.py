import pandas as pd
from src.core.text_cleaner import clean_text
from src.core.data_mappings import aplicar_mapeo, obtener_mapeos_columna
from src.core.logger_config import setup_logger

logger = setup_logger()

def transform_dataframe(df: pd.DataFrame, tipo_hoja: str, formatos: dict) -> pd.DataFrame:
    """
    Transforma columnas de un DataFrame según tipos definidos en `formatos`.

    Aplica limpieza y formateo específico para:
    - Mapeos de datos (usando `data_mappings.py`)
    - Fechas (al formato DD/MM/YYYY)
    - Números enteros
    - Decimales (con precisión 2 o 4)
    - Porcentajes (convierte valores como 0.1 -> 10%)
    - Texto: limpia tildes y caracteres especiales

    Args:
        df (pd.DataFrame): DataFrame de entrada a transformar.
        tipo_hoja (str): Tipo de hoja ("PROCESAMIENTO" o "TRANSPORTE").
        formatos (dict): Diccionario con nombre de columna y tipo: 'fecha', 'numerico', 'decimal2', etc.

    Returns:
        pd.DataFrame: DataFrame transformado y limpio.
    """
    df = aplicar_mapeos(df, tipo_hoja)

    columnas_sin_formato = [col for col in df.columns if col not in formatos]
    for col in columnas_sin_formato:
        df[col] = df[col].astype(str).fillna("").apply(clean_text)
    
    for col, tipo in formatos.items():
        if col in df.columns:
            if tipo == "fecha":
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime("%d/%m/%Y")
            elif tipo == "numerico":
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            elif tipo == "decimal2":
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).round(2)
            elif tipo == "decimal4":
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).round(4)
            elif tipo == "porcentaje":
                df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                df[col] = df[col].apply(lambda x: x * 100 if 0 < x < 1 else x)
                df[col] = df[col].round(0).astype(int)
            
    return df

def aplicar_mapeos(df: pd.DataFrame, tipo_hoja: str) -> pd.DataFrame:
    """
    Aplica los mapeos de datos definidos en data_mappings.py al DataFrame.
    Registra en el logger las transformaciones realizadas.
    
    Args:
        df (pd.DataFrame): DataFrame original.
        tipo_hoja (str): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE').
    
    Returns:
        pd.DataFrame: DataFrame con los valores mapeados.
    """
    df_copy = df.copy()
    
    from src.core.data_mappings import MAPEOS_DATOS

    tipo_hoja_upper = tipo_hoja.upper()
    if tipo_hoja_upper not in MAPEOS_DATOS:
        return df_copy

    mapeos_hoja = MAPEOS_DATOS[tipo_hoja_upper]
    
    for columna in mapeos_hoja.keys():
        if columna not in df_copy.columns:
            logger.warning(f"Columna {columna} no encontrada en el DataFrame.")
            continue
        
        mapeos_col = obtener_mapeos_columna(columna, tipo_hoja)

        if not mapeos_col:
            continue

        transformaciones = 0
        valores_unicos_origen = set()

        for idx in df_copy.index:
            valor_original = df_copy.at[idx, columna]
            valor_mapeado = aplicar_mapeo(valor_original, columna, tipo_hoja)

            if str(valor_original).strip() != str(valor_mapeado).strip():
                df_copy.at[idx, columna] = valor_mapeado
                transformaciones += 1
                valores_unicos_origen.add(str(valor_original).strip())

        if transformaciones > 0:
            logger.info(
                f"Mapeo en {tipo_hoja}.{columna}: {transformaciones} valores transformados"
                f"({len(valores_unicos_origen)} valores únicos de origen)"
            )
            logger.debug(f"Valores origen mapeados: {', '.join(sorted(valores_unicos_origen))}")
    
    return df_copy