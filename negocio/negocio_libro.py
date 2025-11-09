from config_rutas import ROOT
from sqlalchemy.orm import Session
from modelos.libro import Libro
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable
from datos.conexion import Session as crear_sesion

from sqlalchemy.orm import Session
from modelos.libro import Libro
from auxiliares.comparar_strings import normalizar_string

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





