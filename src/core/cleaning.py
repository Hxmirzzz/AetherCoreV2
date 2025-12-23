import pandas as pd
import numpy as np

def cleaning_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia los datos eliminando espacios, normalizando valores y reemplazando nulos.
    """
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(r'[\n\r\t]', ' ', regex=True)
        df[col] = df[col].str.strip().str.replace(r'\s{2,}', ' ', regex=True)
        df[col] = df[col].replace({'nan': '', 'NaN': '', 'None': '', 'NULL': '', 'null': ''})
        
    return df