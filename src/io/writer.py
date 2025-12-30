import pandas as pd
from src.core.expected_columns import EXCLUDED_FROM_EXPORT
from src.core.logger_config import setup_logger

logger = setup_logger()

def export_to_txt(df, output_path, formatos=None, tipo_hoja=None):
    """
    Exporta un DataFrame a un archivo .txt separado por comas, codificado en UTF-8.

    Aplica formato específico a las columnas si se proporciona `formatos`:
    - decimal2: 2 decimales fijos
    - decimal4: 4 decimales fijos
    - otros tipos → convertidos a str sin encabezado

    Args:
        df (pd.DataFrame): DataFrame a exportar.
        output_path (str): Ruta del archivo .txt destino.
        formatos (dict, optional): Diccionario de tipos de formato por columna.
        tipo_hoja (str, optional): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE') para aplicar exclusiones.

    Returns:
        None
    """
    # Crear una copia para no modificar el DataFrame original
    df_export = df.copy()
    
    # Excluir columnas según configuración
    if tipo_hoja:
        tipo_hoja_upper = tipo_hoja.upper()
        columnas_excluidas = EXCLUDED_FROM_EXPORT.get(tipo_hoja_upper, [])
        
        if columnas_excluidas:
            # Filtrar columnas que existen en el DataFrame
            columnas_a_eliminar = [col for col in columnas_excluidas if col in df_export.columns]
            
            if columnas_a_eliminar:
                logger.info(f"Excluyendo columnas de exportación en {tipo_hoja}: {', '.join(columnas_a_eliminar)}")
                df_export = df_export.drop(columns=columnas_a_eliminar)
    
    # Aplicar formatos
    for col in df_export.columns:
        tipo = formatos.get(col, None) if formatos else None
        
        if tipo == "decimal4":
            df_export[col] = df_export[col].map(lambda x: f"{float(x):.4f}")
        elif tipo == "decimal2":
            df_export[col] = df_export[col].map(lambda x: f"{float(x):.2f}")
        else:
            df_export[col] = df_export[col].astype(str)
    
    # Exportar
    df_export.to_csv(output_path, sep=',', encoding='utf-8', index=False, header=True)