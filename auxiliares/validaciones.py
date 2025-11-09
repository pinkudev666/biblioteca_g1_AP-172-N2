import re
from datetime import datetime, date


# Validaciones de correo electrónico
def validar_email(email: str) -> bool:
    """ Valida si el correo tiene formato correcto.
    Retorna True si es válido, False si no.  """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Validaciones de fecha
def parse_fecha(fecha_str: str) -> datetime.date:
    """ Valida formato DD-MM-YYYY. Retorna objeto datetime.date si es válido.
    Lanza ValueError si el formato es incorrecto. """
    try:
        fecha_obj = datetime.strptime(fecha_str, "%d-%m-%Y").date()
        return fecha_obj
    except ValueError:
        raise ValueError("Fecha inválida, debe ser en formato DD-MM-YYYY")


# Validaciones de enteros positivos
def validar_entero_positivo(valor: str) -> int:
    """ Convierte string a entero positivo.
    Lanza ValueError si es inválido.  """
    entero = int(valor)
    if entero < 0:
        raise ValueError("El número debe ser positivo")
    return entero

# Validación de préstamo atrasado
def es_devolucion_atrasada(fecha_vencimiento: date, fecha_devolucion: date) -> bool:
    """
    Retorna True si fecha_devolucion > fecha_vencimiento (estricto).
    Si fecha_devolucion es None -> False (no devuelto).
    """
    if fecha_devolucion is None:
        return False
    return fecha_devolucion > fecha_vencimiento
