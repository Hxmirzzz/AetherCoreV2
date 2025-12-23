def generate_filename(tipo: str, transportadora: str, banco: str, fecha) -> str:
    """
    Genera el nombre del archivo .txt final según la convención:
    LIQ_{tipo}{transportadora}{banco}{fecha_ddmmaaaa}.txt

    Args:
        tipo (str): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE').
        transportadora (str): Nombre de la transportadora.
        banco (str): Acrónimo del banco (columna ENTIDAD).
        fecha (datetime): Fecha para incrustar en el nombre.

    Returns:
        str: Nombre del archivo generado.
    """
    fecha_str = fecha.strftime('%d%m%Y')  # DDMMAAAA
    return f"LIQ_{tipo}{transportadora}{banco}{fecha_str}.txt"