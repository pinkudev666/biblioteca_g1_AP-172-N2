import unicodedata

def normalizar_string(cadena):
    s_decomposed = unicodedata.normalize('NFD', cadena)
    s_filtered = ''.join(
        c for c in s_decomposed if unicodedata.category(c) != 'Mn')
    return s_filtered.lower()

def normalizar_rut(rut: str) -> str:
    if not rut:
        return ""
    return rut.replace(".", "").replace("-", "").upper()
