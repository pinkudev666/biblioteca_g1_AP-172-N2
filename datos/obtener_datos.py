from config_rutas import ROOT
from datos.conexion import sesion
from modelos.tipo_usuario import Tipo_usuario
from modelos.usuario import Usuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo
from auxiliares.validaciones import *
from modelos.usuario import Usuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo


def obtener_listado_objetos(obj_class):
    """Devuelve todos los objetos de una clase de SQLAlchemy."""
    return sesion.query(obj_class).all()

def mostrar_listado(objetos):
    if objetos:
        for obj in objetos:
            print(obj)
    else:
        print("No se encontraron registros.")

def main():
    while True:
        print("\n=== Menú Obtener Datos ===")
        print("1) Listar todos los usuarios")
        print("2) Listar todos los libros")
        print("3) Listar todos los préstamos")
        print("q) Salir")
        opcion = input("Seleccione una opción: ").strip().lower()

        if opcion == "1":
            listado = obtener_listado_objetos(Usuario)
            mostrar_listado(listado)
        elif opcion == "2":
            listado = obtener_listado_objetos(Libro)
            mostrar_listado(listado)
        elif opcion == "3":
            listado = obtener_listado_objetos(Prestamo)
            mostrar_listado(listado)
        elif opcion in ("q", "salir", "exit"):
            print("Saliendo del CLI...")
            break
        else:
            print("Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    main()