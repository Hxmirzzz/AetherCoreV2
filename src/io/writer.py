def export_to_txt(df, output_path, formatos=None):
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

    Returns:
        None
    """
    for col in df.columns:
        tipo = formatos.get(col, None) if formatos else None
        
        if tipo == "decimal4":
            df[col] = df[col].map(lambda x: f"{float(x):.4f}")
        elif tipo == "decimal2":
            df[col] = df[col].map(lambda x: f"{float(x):.2f}")
        else:
            df[col] = df[col].astype(str)
    
    df.to_csv(output_path, sep=',', encoding='utf-8', index=False, header=True)