from config_rutas import ROOT
from modelos.tipo_usuario import Tipo_usuario
from datos.obtener_datos import obtener_listado_objetos
from datos.conexion import Session
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable

class NegocioTipo:
    """Clase de negocio para manejar tipos de usuario."""

    def listar_tipos(self):
        """Lista todos los tipos de usuario en una tabla."""
        listado_tipos = obtener_listado_objetos(Tipo_usuario)
        self.mostrar_tipos_tabla(listado_tipos)

    def agregar_tipo(self, nombre):
        """Agrega un tipo de usuario por nombre."""
        nombre = nombre.strip()
        if not nombre:
            print("No se puede agregar un tipo vacío.")
            return None

        sesion = Session()
        try:
            existente = sesion.query(Tipo_usuario)\
                              .filter(Tipo_usuario.tipo_usuario.ilike(nombre))\
                              .first()
            if existente:
                print(f"El tipo '{nombre}' ya existe.")
                return existente

            nuevo_tipo = Tipo_usuario(tipo_usuario=nombre.title())
            sesion.add(nuevo_tipo)
            sesion.commit()
            print(f"Tipo de usuario '{nombre}' agregado correctamente.")
            return nuevo_tipo

        except Exception as e:
            sesion.rollback()
            print("Error al agregar tipo de usuario:", e)
            return None
        finally:
            sesion.close()

    def eliminar_tipo(self, nombre):
        """Elimina un tipo de usuario por nombre."""
        nombre = nombre.strip()
        if not nombre:
            print("No se puede eliminar un tipo vacío.")
            return False

        sesion = Session()
        try:
            tipo = sesion.query(Tipo_usuario)\
                         .filter(Tipo_usuario.tipo_usuario.ilike(nombre))\
                         .first()
            if tipo:
                sesion.delete(tipo)
                sesion.commit()
                print(f" Tipo de usuario '{tipo.tipo_usuario}' eliminado correctamente.")
                return True
            else:
                print(f" No se encontró el tipo de usuario '{nombre}'.")
                return False
        except Exception as e:
            sesion.rollback()
            print("Error al eliminar:", e)
            return False
        finally:
            sesion.close()

    def buscar_tipos_like(self, buscar_texto):
        """Busca tipos de usuario que contengan el texto dado (like)."""
        listado_tipos = obtener_listado_objetos(Tipo_usuario)
        resultados = []

        if listado_tipos:
            buscar_normalizado = normalizar_string(buscar_texto)
            for tipo in listado_tipos:
                if buscar_normalizado in normalizar_string(tipo.tipo_usuario):
                    resultados.append(tipo)

        if not resultados:
            print(f" No se encontraron tipos de usuario que coincidan con '{buscar_texto}'.")
        return resultados

    def mostrar_tipos_tabla(self, tipos):
        """Muestra una lista de tipos en tabla."""
        tabla = PrettyTable()
        tabla.field_names = ['N°', 'Tipo de Usuario']

        if tipos:
            for tipo in tipos:
                tabla.add_row([tipo.id_tipo_usuario, tipo.tipo_usuario])
            print(tabla)
        else:
            print(" No hay tipos de usuario para mostrar.")
