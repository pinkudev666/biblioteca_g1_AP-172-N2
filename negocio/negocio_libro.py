from config_rutas import ROOT
from sqlalchemy.orm import Session
from modelos.libro import Libro
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable
from datos.conexion import Session as crear_sesion

# ---------- Lógica de negocio ----------
def obtener_listado_libros(sesion: Session):
    return sesion.query(Libro).all()

def obtener_libro_por_nombre(sesion: Session, buscar_libro: str):
    listado_libros = obtener_listado_libros(sesion)
    for libro in listado_libros:
        if normalizar_string(libro.nombre_libro) == normalizar_string(buscar_libro):
            return libro
    return None

def agregar_libro(sesion: Session, nombre, isbn, autor, copias):
    if obtener_libro_por_nombre(sesion, nombre):
        return None  # ya existe
    nuevo_libro = Libro(
        nombre_libro=nombre.title(),
        isbn_libro=isbn,
        autor_libro=autor.title(),
        copias_disponibles=copias
    )
    sesion.add(nuevo_libro)
    sesion.commit()
    return nuevo_libro

def editar_libro(sesion: Session, libro, nuevo_nombre=None, nuevo_isbn=None, nuevo_autor=None, nuevas_copias=None):
    if nuevo_nombre:
        libro.nombre_libro = nuevo_nombre.title()
    if nuevo_isbn:
        libro.isbn_libro = nuevo_isbn
    if nuevo_autor:
        libro.autor_libro = nuevo_autor.title()
    if nuevas_copias is not None:
        libro.copias_disponibles = nuevas_copias
    sesion.commit()
    return libro

def eliminar_libro(sesion: Session, libro):
    sesion.delete(libro)
    sesion.commit()

# ---------- Función de interfaz ----------
def mostrar_libros_tabla(sesion: Session):
    listado_libros = obtener_listado_libros(sesion)
    tabla = PrettyTable()
    tabla.field_names = ['N°', 'ISBN', 'Nombre', 'Autor', 'Copias disponibles']
    for libro in listado_libros:
        tabla.add_row([
            libro.id_libro,
            libro.isbn_libro,
            libro.nombre_libro,
            libro.autor_libro,
            libro.copias_disponibles
        ])
    print(tabla)

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

        if opcion == "1":
            nombre = input("Nombre del libro: ")
            isbn = input("ISBN: ")
            autor = input("Autor: ")
            copias = input("Número de copias: ")
            try:
                copias = int(copias)
            except ValueError:
                copias = 0
            libro = agregar_libro(sesion, nombre, isbn, autor, copias)
            if libro:
                print(f'Libro "{libro.nombre_libro}" agregado correctamente.')
            else:
                print("El libro ya existe.")

        elif opcion == "2":
            nombre = input("Nombre del libro a buscar: ")
            libro = obtener_libro_por_nombre(sesion, nombre)
            if libro:
                print(f'Libro encontrado: {libro.nombre_libro} - {libro.autor_libro} - Copias: {libro.copias_disponibles}')
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
                if nuevas_copias:
                    try:
                        nuevas_copias = int(nuevas_copias)
                    except ValueError:
                        nuevas_copias = None
                else:
                    nuevas_copias = None

                editar_libro(sesion, libro, nuevo_nombre, nuevo_isbn, nuevo_autor, nuevas_copias)
                print("Libro actualizado correctamente.")
            else:
                print("Libro NO encontrado.")

        elif opcion == "4":
            nombre = input("Nombre del libro a eliminar: ")
            libro = obtener_libro_por_nombre(sesion, nombre)
            if libro:
                eliminar_libro(sesion, libro)
                print(f'Libro "{libro.nombre_libro}" eliminado.')
            else:
                print("Libro NO encontrado.")

        elif opcion == "5":
            mostrar_libros_tabla(sesion)

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()
