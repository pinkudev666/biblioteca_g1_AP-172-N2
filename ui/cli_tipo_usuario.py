import sys 
from pathlib import Path 

# agregar raíz del proyecto al sys.path 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from datos.conexion import Session 
from datos.obtener_datos import obtener_listado_objetos
from negocio.negocio_tipo_usuario import (
    obtener_listado_tipos,
    obtener_tipo_por_nombre,
    agregar_tipo_usuario_por_nombre,
    eliminar_tipo_usuario_por_nombre
)
from prettytable import PrettyTable

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
                # Creamos la tabla y le agregamos los datos del tipo encontrado
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Tipo de Usuario"]
                tabla.add_row([tipo.id_tipo_usuario, tipo.tipo_usuario])
                print(tabla)
            else:
                print(f"No se encontró ningún tipo de usuario con nombre '{nombre}'")

        elif opcion == "3":
            nombre = input("Ingrese nombre del tipo de usuario a agregar: ").strip()
            tipo_nuevo = agregar_tipo_usuario_por_nombre(nombre)
            if tipo_nuevo:
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Tipo de Usuario"]
                tabla.add_row([tipo_nuevo["id_tipo_usuario"], tipo_nuevo["tipo_usuario"]])
                print(tabla)
            else:
                print(f"No se pudo agregar el tipo de usuario '{nombre}'")


        elif opcion == "4":
            nombre = input("Nombre del tipo de usuario a eliminar: ").strip()
            eliminado = eliminar_tipo_usuario_por_nombre(nombre)
            if eliminado:
                print(f"Tipo de usuario '{nombre}' eliminado correctamente.")
            else:
                print(f"No se pudo eliminar el tipo de usuario '{nombre}'")

        elif opcion == "0":
            print("Saliendo del menú de tipos de usuario...")
            break

        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()
