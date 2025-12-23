"""
Diccionario de mapeos de datos para transformar valores de origen (XLSX) a destino (TXT).
Cada clave representa una columna, y su valor es un diccionario con los mapeos específicos.

IMPORTANTE: Los mapeos se aplican ANTES de la limpieza de texto (clean_text),
por lo que los valores de origen deben incluir tildes y caracteres especiales si existen en el Excel.
"""

MAPEOS_DATOS = {
    "PROCESAMIENTO": {
        "TIPO_SERVICIO": {
            # ALMACENAMIENTO
            "ALMACENAMIENTO BILLETE": "ALMACENAMIENTO",
            "ALMACENAMIENTO MONEDA": "ALMACENAMIENTO",
            
            # CLASIFICACION
            "CLASIFICACION EFECTIVO FAJADO (ALTA)": "CLASIFICACION",
            "CLASIFICACION EFECTIVO FAJADO (BAJA)": "CLASIFICACION",
            
            # VERIFICACION
            "VERIFICACION DE MONEDAS": "VERIFICACION",
            
            # PAQUETEO
            "PAQUETEO BANCO REPUBLICA": "PAQUETEO",
        }
    },
    "TRANSPORTE": {
        # Aquí se pueden agregar mapeos para TRANSPORTE en el futuro
        # Ejemplo:
        # "TIPO_SERVICIO": {
        #     "VALOR_ORIGEN": "VALOR_DESTINO",
        # },
    }
}


def aplicar_mapeo(valor: str, columna: str, tipo_hoja: str) -> str:
    """
    Aplica el mapeo de datos definido para transformar un valor de origen a destino.
    
    Args:
        valor (str): Valor original del Excel.
        columna (str): Nombre de la columna a mapear.
        tipo_hoja (str): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE').
    
    Returns:
        str: Valor transformado según el diccionario de mapeos, o el valor original si no hay mapeo.
    """
    tipo_hoja = tipo_hoja.upper()
    
    # Si no hay configuración de mapeo para esta hoja, retornar el valor original
    if tipo_hoja not in MAPEOS_DATOS:
        return valor
    
    mapeos_hoja = MAPEOS_DATOS[tipo_hoja]
    
    # Si la columna no tiene mapeos definidos, retornar el valor original
    if columna not in mapeos_hoja:
        return valor
    
    diccionario_mapeo = mapeos_hoja[columna]
    
    # Convertir a string y limpiar espacios
    valor_limpio = str(valor).strip()
    
    # Buscar el mapeo (case-insensitive para mayor robustez)
    for origen, destino in diccionario_mapeo.items():
        if valor_limpio.upper() == origen.upper():
            return destino
    
    # Si no se encuentra mapeo, retornar el valor original
    return valor


def obtener_mapeos_columna(columna: str, tipo_hoja: str) -> dict:
    """
    Obtiene todos los mapeos definidos para una columna específica.
    
    Args:
        columna (str): Nombre de la columna.
        tipo_hoja (str): Tipo de hoja ('PROCESAMIENTO' o 'TRANSPORTE').
    
    Returns:
        dict: Diccionario con los mapeos de la columna, o diccionario vacío si no hay mapeos.
    """
    tipo_hoja = tipo_hoja.upper()
    
    if tipo_hoja not in MAPEOS_DATOS:
        return {}
    
    return MAPEOS_DATOS[tipo_hoja].get(columna, {})