import unicodedata
import re

def clean_text(value: str) -> str:
    """
    Limpia un texto eliminando:
    - tildes
    - caracteres especiales no permitidos
    - múltiples espacios
    - caracteres invisibles como saltos de línea y tabs
    """    
    if not isinstance(value, str):
        value = str(value)

    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[\r\n\t]", " ", value)
    value = re.sub(r"[^A-Za-z0-9\s\-.,#()/]", "", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value