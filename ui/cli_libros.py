import sys  
from pathlib import Path
from prettytable import PrettyTable

# agregar raíz del proyecto al sys.path 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from negocio.negocio_libro import NegocioLibro
from datos.conexion import Session as crear_sesion
from auxiliares.comparar_strings import normalizar_string

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

def seleccionar_libro(lista_libros):
    """Permite al usuario elegir un libro de una lista si hay varios."""
    if len(lista_libros) == 1:
        return lista_libros[0]

    print("Se encontraron varios libros que coinciden:")
    print(tabla_desde_libros(lista_libros))
    
    intentos = 0
    max_intentos = 3
    while intentos < max_intentos:
        entrada = input(f"Elige el ID del libro (Intento {intentos + 1}/{max_intentos}, Enter para cancelar): ").strip()
        if not entrada:
            return None
        try:
            indice = int(entrada)
            libro = next((l for l in lista_libros if l.id_libro == indice), None)
            if libro:
                return libro
            else:
                intentos += 1
                print(f"ID no válido ({max_intentos - intentos} intentos restantes).")
        except ValueError:
            intentos += 1
            print(f"Debes ingresar un número válido ({max_intentos - intentos} intentos restantes).")
    print("Has agotado los intentos. Volviendo al menú.")
    return None

# ---------- CLI ----------
def menu_libros():
    print("\n=== MENÚ LIBROS ===")
    print("1. Agregar libro")
    print("2. Buscar libro por nombre (activos)")
    print("3. Editar libro (activos)")
    print("4. Eliminar libro (borrado lógico)")
    print("5. Mostrar todos los libros (activos)")
    print("6. Reactivar libro")
    print("0. Salir")
    return input("Elige una opción: ")

def main():
    sesion = crear_sesion()
    negocio = NegocioLibro(sesion)
    
    # Método extra para reactivar libros
    def activar_libro(libro):
        libro.activo = True
        sesion.commit()
        return libro

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

                libro = negocio.agregar_libro(nombre, isbn, autor, copias)
                if libro:
                    print(tabla_libro_unico(libro))
                else:
                    print("El libro ya existe.")

            elif opcion == "2":
                nombre = input("Nombre del libro a buscar: ")
                libros = negocio.buscar_libros_por_nombre(nombre)
                if libros:
                    print(tabla_desde_libros(libros))
                else:
                    print("Libro NO encontrado.")

            elif opcion == "3":
                nombre = input("Nombre del libro a editar: ")
                libros = negocio.buscar_libros_por_nombre(nombre)
                libro = seleccionar_libro(libros)
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

                    libro_editado = negocio.editar_libro(
                        libro, nuevo_nombre, nuevo_isbn, nuevo_autor, nuevas_copias
                    )
                    print(tabla_libro_unico(libro_editado))
                else:
                    print("Libro NO seleccionado o cancelado.")

            elif opcion == "4":
                nombre = input("Nombre del libro a eliminar: ")
                libros = negocio.buscar_libros_por_nombre(nombre)
                libro = seleccionar_libro(libros)
                if libro:
                    confirm = input(f"¿Seguro que quieres eliminar '{libro.nombre_libro}'? (s/n): ")
                    if confirm.lower() == 's':
                        libro.activo = False
                        sesion.commit()
                        print(f'Libro "{libro.nombre_libro}" eliminado (borrado lógico).')
                    else:
                        print("Operación cancelada.")
                else:
                    print("Libro NO seleccionado o cancelado.")

            elif opcion == "5":
                libros = negocio.obtener_listado_libros()
                print(tabla_desde_libros(libros))

            elif opcion == "6":
                nombre = input("Nombre del libro a reactivar: ")
                libros_inactivos = negocio.obtener_libros_inactivos()
                libros_filtrados = [l for l in libros_inactivos if normalizar_string(nombre) in normalizar_string(l.nombre_libro)]
                libro = seleccionar_libro(libros_filtrados)
                if libro:
                    negocio.reactivar_libro(libro)
                    print(f'Libro "{libro.nombre_libro}" reactivado.')
                else:
                    print("No se seleccionó ningún libro para reactivar.")

            elif opcion == "0":
                print("Saliendo del programa...")
                break

            else:
                print("Opción no válida, intenta nuevamente.")

        except Exception as e:
            print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
