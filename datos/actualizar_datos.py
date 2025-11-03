from config_rutas import ROOT
from datos.conexion import Session
from modelos.tipo_usuario import Tipo_usuario
from modelos.usuario import Usuario
from modelos.libro import Libro
from modelos.prestamo import Prestamo
from auxiliares.validaciones import *


def actualizar_tipo_usuario():
    try:
        id_tipo = int(input("Ingrese ID del tipo de usuario a actualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    tipo = sesion.get(Tipo_usuario, id_tipo)
    if not tipo:
        print("Tipo de usuario no encontrado.")
        return

    nuevo_nombre = input(f"Ingrese nuevo nombre (actual: {tipo.tipo_usuario}): ").strip()
    if nuevo_nombre:
        tipo.tipo_usuario = nuevo_nombre

    try:
        sesion.commit()
        print("Tipo de usuario actualizado con éxito.")
    except Exception as e:
        sesion.rollback()
        print(f"Error al actualizar TipoUsuario: {e}")

def actualizar_usuario():
    rut = input("Ingrese RUT del usuario a actualizar: ").strip()
    usuario = sesion.get(Usuario, rut)
    if not usuario:
        print("Usuario no encontrado.")
        return

    # nombre (opcional)
    nombre = input(f"Ingrese nuevo nombre (actual: {usuario.nombre_usuario}): ").strip()
    if nombre:
        usuario.nombre_usuario = nombre

    # correo (opcional y validado)
    while True:
        correo = input(f"Ingrese nuevo correo (actual: {usuario.correo_usuario}): ").strip()
        if not correo:
            break  # deja el actual
        if validar_email(correo):
            usuario.correo_usuario = correo
            break
        print("Correo inválido. Intente nuevamente.")

    # id_tipo (opcional)
    id_tipo_input = input(f"Ingrese nuevo ID tipo (actual: {usuario.id_tipo_usuario}): ").strip()
    if id_tipo_input:
        try:
            usuario.id_tipo_usuario = int(id_tipo_input)
        except ValueError:
            print("ID tipo inválido. No se cambió.")

    # commit final
    try:
        sesion.commit()
        print("Usuario actualizado con éxito.")
    except Exception as e:
        sesion.rollback()
        print(f"Error al actualizar Usuario: {e}")


def actualizar_libro():
    try:
        id_libro = int(input("Ingrese ID del libro a actualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    libro = sesion.get(Libro, id_libro)
    if not libro:
        print("Libro no encontrado.")
        return

    isbn = input(f"Ingrese nuevo ISBN (actual: {libro.isbn_libro}): ").strip()
    if isbn:
        libro.isbn_libro = isbn

    nombre = input(f"Ingrese nuevo nombre (actual: {libro.nombre_libro}): ").strip()
    if nombre:
        libro.nombre_libro = nombre

    autor = input(f"Ingrese nuevo autor (actual: {libro.autor_libro}): ").strip()
    if autor:
        libro.autor_libro = autor

    # copias (opcional y validado)
    while True:
        copias_input = input(f"Ingrese nueva cantidad de copias (actual: {libro.copias_disponibles}): ").strip()
        if copias_input == "":
            break
        try:
            copias = int(copias_input)
            if copias < 0:
                print("Cantidad no puede ser negativa.")
            else:
                libro.copias_disponibles = copias
                break
        except ValueError:
            print("Ingrese un número válido.")

    try:
        sesion.commit()
        print("Libro actualizado con éxito.")
    except Exception as e:
        sesion.rollback()
        print(f"Error al actualizar Libro: {e}")

VALORES_ESTADO = ['Pendiente', 'Devuelto a tiempo', 'Devuelto atrasado']

def actualizar_prestamo():
    try:
        id_prestamo = int(input("Ingrese ID del préstamo a actualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    prestamo = sesion.get(Prestamo, id_prestamo)
    if not prestamo:
        print("Préstamo no encontrado.")
        return

    # fechas (opcional)
    fecha_inicio = input(f"Ingrese nueva fecha inicio (actual: {prestamo.fecha_inicio}) DD-MM-YYYY: ").strip()
    if fecha_inicio:
        try:
            prestamo.fecha_inicio = parse_fecha(fecha_inicio)
        except ValueError as e:
            print(e)
            return

    fecha_vencimiento = input(f"Ingrese nueva fecha vencimiento (actual: {prestamo.fecha_vencimiento}) DD-MM-YYYY: ").strip()
    if fecha_vencimiento:
        try:
            prestamo.fecha_vencimiento = parse_fecha(fecha_vencimiento)
        except ValueError as e:
            print(e)
            return

    # cambiar usuario (opcional)
    rut_usuario = input(f"Ingrese nuevo RUT usuario (actual: {prestamo.rut_usuario}): ").strip()
    if rut_usuario:
        usuario = sesion.get(Usuario, rut_usuario)
        if not usuario:
            print("El RUT ingresado no corresponde a un usuario existente. Abortando.")
            return
        prestamo.rut_usuario = rut_usuario

    # cambiar libro (opcional)
    id_libro_input = input(f"Ingrese nuevo ID libro (actual: {prestamo.id_libro}): ").strip()
    if id_libro_input:
        try:
            id_libro = int(id_libro_input)
            libro = sesion.get(Libro, id_libro)
            if not libro:
                print("Libro no existe. Abortando.")
                return
            prestamo.id_libro = id_libro
        except ValueError:
            print("ID libro inválido. Abortando.")
            return

    # estado (opcional)
    estado = input(f"Ingrese nuevo estado {VALORES_ESTADO} (actual: {prestamo.estado}): ").strip()
    if estado and estado in VALORES_ESTADO:
        prestamo.estado = estado
    elif estado:
        print("Estado inválido. No se cambió.")

    try:
        sesion.commit()
        print("Préstamo actualizado con éxito.")
    except Exception as e:
        sesion.rollback()
        print(f"Error al actualizar Prestamo: {e}")

if __name__ == "__main__":
    sesion = Session()  # aseguramos la sesión al inicio
    try:
        while True:
            print("\n=== Actualizar Datos ===")
            print("1) TipoUsuario")
            print("2) Usuario")
            print("3) Libro")
            print("4) Préstamo")
            print("q) Salir")

            opcion = input("Seleccione una opción: ").strip().lower()

            if opcion == "1":
                actualizar_tipo_usuario()
            elif opcion == "2":
                actualizar_usuario()
            elif opcion == "3":
                actualizar_libro()
            elif opcion == "4":
                actualizar_prestamo()
            elif opcion in ("q", "salir", "exit"):
                print("Saliendo...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    finally:
        sesion.close()
