from config_rutas import ROOT
from datos.conexion import Session
from modelos.tipo_usuario import Tipo_usuario
from modelos.usuario import Usuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo
from auxiliares.validaciones import *

# -------------------------------------------------------
# Funciones CRUD básicas usando contexto de sesión
# -------------------------------------------------------
def agregar_tipo_usuario(tipo_nombre):
    session = Session()
    try:
        nuevo_tipo = Tipo_usuario(tipo_usuario=tipo_nombre.title())
        session.add(nuevo_tipo)
        session.commit()
        session.refresh(nuevo_tipo)
        print('Tipo de usuario agregado correctamente.')
    except Exception as e:
        session.rollback()
        print("Error al agregar tipo de usuario:", e)
    finally:
        session.close()
        
def listar_tipos():
    """Retorna lista de objetos Tipo_usuario (vacío si no hay)."""
    return obtener_listado_objetos(Tipo_usuario) or []

def obtener_tipo_por_nombre(buscar_tipo):
    """Retorna Tipo_usuario o None."""
    if not buscar_tipo:
        return None
    buscar_norm = normalizar_string(buscar_tipo)
    for tipo in listar_tipos():
        if normalizar_string(tipo.tipo_usuario) == buscar_norm:
            return tipo
    return None

def obtener_tipo_por_id(id_tipo):
    """Retorna Tipo_usuario por id o None."""
    try:
        id_int = int(id_tipo)
    except Exception:
        return None
    for tipo in listar_tipos():
        if getattr(tipo, 'id_tipo_usuario', None) == id_int:
            return tipo
    return None

def tipo_existe(id_tipo=None, nombre=None):
    """Devuelve (True, tipo_obj) si existe por id o nombre, else (False, None)."""
    if id_tipo is not None:
        t = obtener_tipo_por_id(id_tipo)
        if t:
            return True, t
    if nombre is not None:
        t = obtener_tipo_por_nombre(nombre)
        if t:
            return True, t
    return False, None

def agregar_tipo_usuario(tipo_nombre):
    """
    Intenta crear un tipo. Retorna (True, tipo_obj) si se creó,
    o (False, 'mensaje de error') si no.
    """
    tipo_nombre = (tipo_nombre or "").strip()
    if not tipo_nombre:
        return False, "Nombre vacío."

    existe, _ = tipo_existe(nombre=tipo_nombre)
    if existe:
        return False, f'El tipo "{tipo_nombre}" ya existe.'

    nuevo_tipo = Tipo_usuario(tipo_usuario=tipo_nombre.title())
    try:
        insertar_objeto(nuevo_tipo)
        return True, nuevo_tipo
    except Exception as e:
        return False, f"Error al insertar: {e}"

