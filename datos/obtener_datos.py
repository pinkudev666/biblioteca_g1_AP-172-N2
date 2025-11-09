from config_rutas import ROOT
from datos.conexion import Session 


def obtener_listado_objetos(obj_class):
    # Devuelve todos los objetos de una clase de SQLAlchemy.
    sesion = Session()  # Crear sesión concreta
    try:
        return sesion.query(obj_class).all()
    except Exception as e:
        print(f"Error al obtener objetos de {obj_class.__name__}: {e}")
        return []
    finally:
        sesion.close()  # Cerrar siempre la sesión

def obtener_objeto_por_id(obj_class, id_obj):
    # Devuelve un objeto por su ID.
    sesion = Session()
    try:
        return sesion.query(obj_class).get(id_obj)
    except Exception as e:
        print(f"Error al obtener {obj_class.__name__} con ID {id_obj}: {e}")
        return None
    finally:
        sesion.close()