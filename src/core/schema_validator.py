from src.core.expected_columns import EXPECTED_COLUMNS

class SchemaValidationError(Exception):
    def __init__(self, missing_columns):
        self.missing_columns = missing_columns
        message = f"Faltan columnas requeridas: {', '.join(missing_columns)}"
        super().__init__(message)

def validate_schema(df, tipo_hoja):
    tipo_hoja = tipo_hoja.upper()
    required = EXPECTED_COLUMNS.get(tipo_hoja, [])
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise SchemaValidationError(missing)