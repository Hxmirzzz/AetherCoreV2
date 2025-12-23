from src.io.writer import export_to_txt
from src.io.formatter import transform_dataframe
from src.io.pathing import get_output_path
from src.core.tipos_columnas import TIPOS_COLUMNAS
from src.core.cleaning import cleaning_dataframe
from src.core.schema_validator import validate_schema
from src.core.validators import validate_column_types

def save(df, tipo_hoja, file_name):
    """
    Guarda el DataFrame como archivo .txt en la ruta correspondiente, basada en el tipo.
    Aplica formatos de fecha, numéricos y decimales según especificación.
    """
    tipo_hoja = tipo_hoja.upper()
    validate_schema(df, tipo_hoja)
    df = cleaning_dataframe(df)

    if 'ENTIDAD' in df.columns:
        df = df[df['ENTIDAD'].notna() & df['ENTIDAD'].astype(str).str.strip().ne('')].copy()
    else:
        last_row = df.tail(1)
        empty_ratio = ((last_row.isna()) | (last_row == 0)).sum(axis=1) / df.shape[1]
        if empty_ratio.iloc[0] > 0.8:
            df = df.iloc[:-1].copy()
    
    formatos = TIPOS_COLUMNAS.get(tipo_hoja, {})
    df = transform_dataframe(df, tipo_hoja, formatos)
    validate_column_types(df, formatos, tipo_hoja)
    output_path = get_output_path(tipo_hoja, file_name)
    export_to_txt(df, output_path, formatos)
    return output_path