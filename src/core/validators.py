import pandas as pd
from datetime import datetime

def validate_column_types(df: pd.DataFrame, formatos: dict, tipo_hoja: str):
    errors = []

    for col, tipo in formatos.items():
        if col not in df.columns:
            continue

        values = df[col].dropna().astype(str)

        for i, val in enumerate(values):
            val = val.strip()
            if val == '':
                continue

            if tipo == 'int':
                if not val.isdigit():
                    errors.append(f"{tipo_hoja}: '{col}' tiene valor no entero: {val}")
            elif tipo == 'float' or tipo.startswith('decimal'):
                try:
                    float(val.replace(',', '').replace('%', '').strip())
                except ValueError:
                    errors.append(f"{tipo_hoja}: '{col}' no es decimal válido: {val}")
            elif tipo == 'date':
                try:
                    datetime.strptime(val, '%d/%m/%Y')
                except ValueError:
                    errors.append(f"{tipo_hoja}: '{col}' no es fecha válida (DD/MM/AAAA): {val}")

    if errors:
        raise ValueError("Errores de validación de tipos:\n" + "\n".join(errors))