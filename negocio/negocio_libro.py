from config_rutas import ROOT
from sqlalchemy.orm import Session
from modelos.libro import Libro
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable

class NegocioLibro:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def obtener_listado_libros(self):
        # Devuelve solo libros activos en la base de datos
        return self.sesion.query(Libro).filter(Libro.activo == True).all()

    def obtener_libros_inactivos(self):
        """Devuelve todos los libros que están inactivos."""
        return self.sesion.query(Libro).filter(Libro.activo == False).all()

    def buscar_libros_por_nombre(self, buscar_libro: str):
        """
        Devuelve libros cuyo nombre contenga parcial o insensiblemente
        el término de búsqueda, ignorando tildes y mayúsculas.
        Solo libros activos.
        """
        buscar_libro_norm = normalizar_string(buscar_libro)
        libros = self.obtener_listado_libros()
        libros_filtrados = [
            libro for libro in libros
            if buscar_libro_norm in normalizar_string(libro.nombre_libro)
        ]
        return libros_filtrados

    def mostrar_libros_tabla(self, libros):
        tabla = PrettyTable()
        tabla.field_names = ["Índice", "Nombre", "Autor", "Copias disponibles"]
        for i, libro in enumerate(libros, start=1):
            tabla.add_row([
                i,
                libro.nombre_libro,
                libro.autor_libro,
                libro.copias_disponibles
            ])
        print(tabla)

    def agregar_libro(self, nombre, isbn, autor, copias):
        # Agrega un libro nuevo si no existe otro con el mismo nombre exacto
        libros_existentes = self.sesion.query(Libro).filter(Libro.activo == True).all()
        if any(normalizar_string(l.nombre_libro) == normalizar_string(nombre) for l in libros_existentes):
            return None  # Ya existe un libro activo con ese nombre exacto
        nuevo_libro = Libro(
            nombre_libro=nombre.title(),
            isbn_libro=isbn,
            autor_libro=autor.title(),
            copias_disponibles=copias
        )
        self.sesion.add(nuevo_libro)
        self.sesion.commit()
        return nuevo_libro

    def editar_libro(self, libro, nuevo_nombre=None, nuevo_isbn=None, nuevo_autor=None, nuevas_copias=None):
        # Edita los atributos de un libro existente.
        if nuevo_nombre:
            libro.nombre_libro = nuevo_nombre.title()
        if nuevo_isbn:
            libro.isbn_libro = nuevo_isbn
        if nuevo_autor:
            libro.autor_libro = nuevo_autor.title()
        if nuevas_copias is not None:
            libro.copias_disponibles = nuevas_copias
        self.sesion.commit()
        return libro

    def eliminar_libro(self, libro):
        # Borrado lógico en lugar de físico
        libro.activo = False
        self.sesion.commit()
        return libro

    def reactivar_libro(self, libro):
        libro.activo = True
        self.sesion.commit()
        return libro