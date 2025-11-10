import sys
from pathlib import Path
from prettytable import PrettyTable

# agregar raíz del proyecto al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from negocio.negocio_usuario import UsuarioNegocio

def menu_usuarios():
    print("\n=== MENÚ USUARIOS ===")
    print("1. Crear usuario")
    print("2. Buscar usuario por RUT")
    print("3. Listar usuarios por tipo de usuario")
    print("4. Actualizar usuario")
    print("5. Eliminar usuario (borrado lógico)")
    print("6. Activar usuario inactivo")
    print("7. Listar usuarios activos")
    print("0. Salir")
    return input("Elige una opción: ").strip()

def mostrar_usuario_tabla(u):
    # Muestra un único usuario en PrettyTable
    tabla = PrettyTable()
    tabla.field_names = ["RUT", "Nombre", "Correo", "ID Tipo", "Activo"]
    tabla.add_row([
        u.rut_usuario,
        u.nombre_usuario,
        u.correo_usuario,
        u.id_tipo_usuario,
        "Sí" if u.usuario_activo else "No"
    ])
    print(tabla)

def mostrar_usuarios_tabla(usuarios):
    # Muestra una lista de usuarios en PrettyTable
    if not usuarios:
        print("No hay usuarios para mostrar.")
        return
    tabla = PrettyTable()
    tabla.field_names = ["RUT", "Nombre", "Correo", "ID Tipo", "Activo"]
    for u in usuarios:
         tabla.add_row([
            u.rut_usuario,
            u.nombre_usuario,
            u.correo_usuario,
            u.id_tipo_usuario,
            "Sí" if u.usuario_activo else "No"
        ])
    print(tabla)

def main():
    negocio = UsuarioNegocio()

    try:
        while True:
            opcion = menu_usuarios()

            if opcion == "1":
                rut = input("RUT: ").strip()
                nombre = input("Nombre: ").strip()
                correo = input("Correo: ").strip()
                id_tipo = input("ID tipo usuario: ").strip()
                try:
                    u = negocio.crear_usuario(rut, nombre, correo, id_tipo)
                    print("Usuario creado:")
                    mostrar_usuario_tabla(u)
                except Exception as e:
                    print(e)

            elif opcion == "2":
                rut = input("Ingrese RUT del usuario: ").strip()
                u = negocio.obtener_usuario(rut)
                if u:
                    print("Usuario encontrado:")
                    mostrar_usuario_tabla(u)
                else:
                    print("Usuario no encontrado.")
            
            elif opcion == "3":
                nombre = input("Nombre del tipo de usuario: ").strip()
                usuarios = negocio.listar_usuarios_por_tipo(nombre)

                if not usuarios:
                    print(f"No existe un tipo de usuario llamado '{nombre}'.")
                else:
                    mostrar_usuarios_tabla(usuarios)


            elif opcion == "4":
                rut = input("Ingrese RUT del usuario a actualizar: ").strip()
                nombre = input("Nuevo nombre (Enter para omitir): ").strip()
                correo = input("Nuevo correo (Enter para omitir): ").strip()
                id_tipo = input("Nuevo ID tipo usuario (Enter para omitir): ").strip()
                cambios = {}
                if nombre: cambios['nombre_usuario'] = nombre
                if correo: cambios['correo_usuario'] = correo
                if id_tipo: cambios['id_tipo_usuario'] = id_tipo
                try:
                    u = negocio.actualizar_usuario(rut, **cambios)
                    if u:
                        print("Usuario actualizado:")
                        mostrar_usuario_tabla(u)
                    else:
                        print("Usuario no encontrado.")
                except Exception as e:
                    print(e)

            elif opcion == "5":
                rut = input("Ingrese RUT del usuario a eliminar: ").strip()
                try:
                    u = negocio.eliminar_usuario(rut)
                    if u:
                        print("Usuario eliminado (inactivo):")
                        mostrar_usuario_tabla(u)
                    else:
                        print("Usuario no encontrado o ya estaba inactivo.")
                except Exception as e:
                    print(e)

            elif opcion == "6":
                rut = input("Ingrese RUT del usuario a activar: ").strip()
                try:
                    u = negocio.activar_usuario(rut)
                    if u:
                        print("Usuario activado:")
                        mostrar_usuario_tabla(u)
                    else:
                        print("Usuario no encontrado o ya activo.")
                except Exception as e:
                    print(e)

            elif opcion == "7":
                usuarios = negocio.obtener_usuarios()
                mostrar_usuarios_tabla(usuarios)

            elif opcion == "0":
                print("Saliendo del menú de usuarios...")
                break

            else:
                print("Opción no válida, intenta nuevamente.")

    finally:
        negocio.cerrar()

if __name__ == "__main__":
    main()
