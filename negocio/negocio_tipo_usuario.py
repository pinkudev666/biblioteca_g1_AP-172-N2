from config_rutas import ROOT
from modelos.tipo_usuario import Tipo_usuario
from datos.obtener_datos import obtener_listado_objetos
from datos.conexion import Session
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable

def obtener_listado_tipos():
    #Lista todos los tipos de usuario en una tabla.
    tabla_tipos = PrettyTable()
    tabla_tipos.field_names = ['N°', 'Tipo de Usuario']
    listado_tipos = obtener_listado_objetos(Tipo_usuario)
    if listado_tipos:
        for tipo in listado_tipos:
            tabla_tipos.add_row([tipo.id_tipo_usuario, tipo.tipo_usuario])
        print(tabla_tipos)

def obtener_tipo_por_nombre(buscar_tipo):
    #Busca un tipo de usuario por nombre.
    tipo_encontrado = None
    listado_tipos = obtener_listado_objetos(Tipo_usuario)
    if listado_tipos:
        for tipo in listado_tipos:
            if normalizar_string(tipo.tipo_usuario) == normalizar_string(buscar_tipo):
                tipo_encontrado = tipo
        if tipo_encontrado is None:
            print('Tipo de usuario NO encontrado.')
    return tipo_encontrado

def agregar_tipo_usuario_por_nombre(nombre):
    # Agrega un tipo de usuario por nombre.
    if not nombre.strip():
        print("No se puede agregar un tipo vacío.")
        return None

    sesion = Session()  # crear sesión concreta
    try:
        existente = sesion.query(Tipo_usuario).filter(Tipo_usuario.tipo_usuario.ilike(nombre)).first()
        if existente:
            print(f'El tipo "{nombre}" ya existe.')
            return {"id_tipo_usuario": existente.id_tipo_usuario,
                    "tipo_usuario": existente.tipo_usuario}

        nuevo_tipo = Tipo_usuario(tipo_usuario=nombre.title())
        sesion.add(nuevo_tipo)
        sesion.commit()
        print(f'Tipo de usuario "{nombre}" agregado correctamente.')
        # Retornamos solo los datos necesarios, no el objeto completo
        return {"id_tipo_usuario": nuevo_tipo.id_tipo_usuario,
                "tipo_usuario": nuevo_tipo.tipo_usuario}
    except Exception as e:
        sesion.rollback()
        print("Error al agregar tipo de usuario:", e)
        return None
    finally:
        sesion.close()  # cerrar sesión siempre

def eliminar_tipo_usuario_por_nombre(nombre):
    # Elimina un tipo de usuario por nombre.
    sesion = Session()
    try:
        tipo = sesion.query(Tipo_usuario).filter(Tipo_usuario.tipo_usuario.ilike(nombre)).first()
        if tipo:
            nombre_tipo = tipo.tipo_usuario  # Guardamos el nombre antes de borrar
            sesion.delete(tipo)
            sesion.commit()
            return True
        else:
            print("No se encontró el tipo de usuario.")
            return False
    except Exception as e:
        sesion.rollback()
        print("Error al eliminar:", e)
        return False
    finally:
        sesion.close()

