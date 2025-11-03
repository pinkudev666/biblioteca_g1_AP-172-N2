from config_rutas import ROOT
from datos.conexion import Session as crear_sesion
from modelos.tipo_usuario import Tipo_usuario
from datos.obtener_datos import obtener_listado_objetos
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable


def obtener_listado_tipos():
    tabla_tipos = PrettyTable()
    tabla_tipos.field_names = ['N°', 'Tipo de Usuario']
    listado_tipos = obtener_listado_objetos(Tipo_usuario)
    if listado_tipos:
        for tipo in listado_tipos:
            tabla_tipos.add_row([tipo.id_tipo_usuario, tipo.tipo_usuario])
        print(tabla_tipos)


def obtener_tipo_por_nombre(buscar_tipo):
    tipo_encontrado = None
    listado_tipos = obtener_listado_objetos(Tipo_usuario)
    if listado_tipos:
        for tipo in listado_tipos:
            if normalizar_string(tipo.tipo_usuario) == normalizar_string(buscar_tipo):
                tipo_encontrado = tipo
        if tipo_encontrado == None:
            print('Tipo de usuario NO encontrado.')
    return tipo_encontrado

def agregar_tipo_usuario():
    tipo = input('Ingrese nombre del tipo de usuario: ').strip()
    if not tipo:
        print("No se puede agregar un tipo vacío.")
        return

    sesion = crear_sesion()
    try:
        # Verificar si ya existe
        existente = sesion.query(Tipo_usuario).filter(Tipo_usuario.tipo_usuario.ilike(tipo)).first()
        if existente:
            print(f'El tipo "{tipo}" ya existe.')
            return

        nuevo_tipo = Tipo_usuario(tipo_usuario=tipo.title())
        sesion.add(nuevo_tipo)
        sesion.commit()
        print(f'Tipo de usuario "{tipo}" agregado correctamente.')
    except Exception as e:
        sesion.rollback()
        print("Error al agregar tipo de usuario:", e)
    finally:
        sesion.close()


def agregar_tipo_usuario_por_nombre(nombre):
    sesion = crear_sesion()
    try:
        # Verificar si ya existe
        existente = sesion.query(Tipo_usuario).filter(Tipo_usuario.tipo_usuario.ilike(nombre)).first()
        if existente:
            print(f'El tipo "{nombre}" ya existe.')
            return existente

        nuevo_tipo = Tipo_usuario(tipo_usuario=nombre.title())
        sesion.add(nuevo_tipo)
        sesion.commit()
        print(f'Tipo de usuario "{nombre}" agregado correctamente.')
        return nuevo_tipo
    except Exception as e:
        sesion.rollback()
        print("Error al agregar tipo de usuario:", e)
    finally:
        sesion.close()

def eliminar_tipo_usuario_por_nombre(nombre):
    sesion = crear_sesion()  # una única sesión
    try:
        tipo = sesion.query(Tipo_usuario).filter(Tipo_usuario.tipo_usuario.ilike(nombre)).first()
        if tipo:
            sesion.delete(tipo)
            sesion.commit()
            print(f'Tipo de usuario "{tipo.tipo_usuario}" eliminado (solo prueba).')
        else:
            print("No se encontró el tipo de usuario.")
    except Exception as e:
        sesion.rollback()
        print("Error al eliminar:", e)
    finally:
        sesion.close()



def menu_tipos_usuarios():
    print("\n=== MENÚ TIPOS DE USUARIO ===")
    print("1. Listar tipos de usuario")
    print("2. Buscar tipo de usuario por nombre")
    print("3. Agregar tipo de usuario")
    print("4. Eliminar tipo de usuario")
    print("0. Salir")
    return input("Elige una opción: ").strip()

def main():
    while True:
        opcion = menu_tipos_usuarios()

        if opcion == "1":
            obtener_listado_tipos()

        elif opcion == "2":
            nombre = input("Nombre del tipo de usuario a buscar: ").strip()
            tipo = obtener_tipo_por_nombre(nombre)
            if tipo:
                print(f'Tipo encontrado: ID {tipo.id_tipo_usuario} - {tipo.tipo_usuario}')

        elif opcion == "3":
            agregar_tipo_usuario()

        elif opcion == "4":
            nombre = input("Nombre del tipo de usuario a eliminar: ").strip()
            eliminar_tipo_usuario_por_nombre(nombre)

        elif opcion == "0":
            print("Saliendo del menú de tipos de usuario...")
            break

        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()