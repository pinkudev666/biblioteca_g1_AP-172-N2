import sys  
from pathlib import Path 
from prettytable import PrettyTable

# agregar raíz del proyecto al sys.path 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from negocio.negocio_libro import (
    agregar_libro,
    obtener_libro_por_nombre,
    obtener_listado_libros,
    editar_libro,
    eliminar_libro
)
from datos.conexion import Session as crear_sesion

# ---------- Funciones de interfaz ----------
def tabla_desde_libros(libros):
    tabla = PrettyTable()
    tabla.field_names = ['N°', 'ISBN', 'Nombre', 'Autor', 'Copias disponibles']
    for libro in libros:
        tabla.add_row([
            libro.id_libro,
            libro.isbn_libro,
            libro.nombre_libro,
            libro.autor_libro,
            libro.copias_disponibles
        ])
    return tabla

def tabla_libro_unico(libro):
    return tabla_desde_libros([libro] if libro else [])

# ---------- CLI ----------
def menu_libros():
    print("\n=== MENÚ LIBROS ===")
    print("1. Agregar libro")
    print("2. Buscar libro por nombre")
    print("3. Editar libro")
    print("4. Eliminar libro")
    print("5. Mostrar todos los libros")
    print("0. Salir")
    return input("Elige una opción: ")

def main():
    sesion = crear_sesion()
    while True:
        opcion = menu_libros()

        try:
            if opcion == "1":
                nombre = input("Nombre del libro: ")
                isbn = input("ISBN: ")
                autor = input("Autor: ")
                copias = input("Número de copias: ")
                try:
                    copias = int(copias)
                except ValueError:
                    print("Número de copias inválido, se asigna 0 por defecto.")
                    copias = 0

                libro = agregar_libro(sesion, nombre, isbn, autor, copias)
                if libro:
                    print(tabla_libro_unico(libro))
                else:
                    print("El libro ya existe.")

            elif opcion == "2":
                nombre = input("Nombre del libro a buscar: ")
                libro = obtener_libro_por_nombre(sesion, nombre)
                if libro:
                    print(tabla_libro_unico(libro))
                else:
                    print("Libro NO encontrado.")

            elif opcion == "3":
                nombre = input("Nombre del libro a editar: ")
                libro = obtener_libro_por_nombre(sesion, nombre)
                if libro:
                    nuevo_nombre = input("Nuevo nombre (Enter para mantener): ")
                    nuevo_isbn = input("Nuevo ISBN (Enter para mantener): ")
                    nuevo_autor = input("Nuevo autor (Enter para mantener): ")
                    nuevas_copias = input("Nuevas copias (Enter para mantener): ")

                    if nuevas_copias != "":
                        try:
                            nuevas_copias = int(nuevas_copias)
                        except ValueError:
                            print("Valor de copias inválido, no se actualizará.")
                            nuevas_copias = None
                    else:
                        nuevas_copias = None

                    libro_editado = editar_libro(sesion, libro, nuevo_nombre, nuevo_isbn, nuevo_autor, nuevas_copias)
                    print(tabla_libro_unico(libro_editado))
                else:
                    print("Libro NO encontrado.")

            elif opcion == "4":
                nombre = input("Nombre del libro a eliminar: ")
                libro = obtener_libro_por_nombre(sesion, nombre)
                if libro:
                    confirm = input(f"¿Seguro que quieres eliminar '{libro.nombre_libro}'? (s/n): ")
                    if confirm.lower() == 's':
                        eliminar_libro(sesion, libro)
                        print(f'Libro "{libro.nombre_libro}" eliminado.')
                    else:
                        print("Operación cancelada.")
                else:
                    print("Libro NO encontrado.")

            elif opcion == "5":
                libros = obtener_listado_libros(sesion)
                print(tabla_desde_libros(libros))

            elif opcion == "0":
                print("Saliendo del programa...")
                break

            else:
                print("Opción no válida, intenta nuevamente.")

        except Exception as e:
            print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
