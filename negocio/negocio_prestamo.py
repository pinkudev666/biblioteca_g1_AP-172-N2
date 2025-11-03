from config_rutas import ROOT
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.prestamo import Prestamo
from modelos.libro import Libro
from modelos.usuario import Usuario
from negocio_libro import obtener_libro_por_nombre  # tu función reutilizada
from auxiliares.validaciones import parse_fecha
from prettytable import PrettyTable
from datos.conexion import Session as crear_sesion
from datetime import date

# ---------- Lógica de negocio ----------
def obtener_prestamos(sesion: Session):
    return sesion.query(Prestamo).all()

def obtener_prestamos_pendientes_por_usuario(sesion: Session, rut_usuario: str):
    return sesion.query(Prestamo).filter(
        Prestamo.rut_usuario == rut_usuario,
        Prestamo.estado == 'Pendiente'
    ).all()

def obtener_prestamo_por_usuario_y_libro(sesion: Session, rut_usuario: str, nombre_libro: str):
    prestamos = obtener_prestamos_pendientes_por_usuario(sesion, rut_usuario)
    for p in prestamos:
        if p.libro and p.libro.nombre_libro and p.libro.nombre_libro.strip() != "":
            # comparar usando la misma normalización que usa obtener_libro_por_nombre
            if obtener_libro_por_nombre(sesion, p.libro.nombre_libro) and obtener_libro_por_nombre(sesion, p.libro.nombre_libro).id_libro == obtener_libro_por_nombre(sesion, nombre_libro).id_libro:
                return p
        # fallback más simple (por si la relación no está cargada): comparar lower sin tildes opcional
        # pero tu obtener_libro_por_nombre normaliza, así que la comparativa anterior suele bastar.
    # alternativa más segura: comparar normalizados directo con strings del objeto libro
    for p in prestamos:
        if p.libro and p.libro.nombre_libro:
            if p.libro.nombre_libro.lower().strip() == nombre_libro.lower().strip():
                return p
    return None

def agregar_prestamo_por_nombre(sesion: Session, rut_usuario: str, nombre_libro: str, fecha_inicio: date, fecha_vencimiento: date):
    usuario = sesion.query(Usuario).filter(Usuario.rut_usuario == rut_usuario).first()
    if not usuario:
        return None, "Usuario no existe"

    libro = obtener_libro_por_nombre(sesion, nombre_libro)
    if not libro:
        return None, "Libro no encontrado"

    if libro.copias_disponibles is None or libro.copias_disponibles <= 0:
        return None, "No quedan copias disponibles"

    try:
        nuevo = Prestamo(
            rut_usuario=rut_usuario,
            id_libro=libro.id_libro,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            estado='Pendiente'
        )
        sesion.add(nuevo)
        libro.copias_disponibles = libro.copias_disponibles - 1
        sesion.commit()
        return nuevo, None
    except IntegrityError:
        sesion.rollback()
        return None, "Error al crear préstamo (integrity)"
    except Exception as e:
        sesion.rollback()
        return None, f"Error al crear préstamo: {e}"

def editar_prestamo_estado(sesion: Session, prestamo: Prestamo, nuevo_estado: str):
    """
    Cambia el estado. Si marcamos como devuelto, devuelve la copia al inventario.
    """
    es_devolucion = nuevo_estado in ("Devuelto a tiempo", "Devuelto atrasado")
    try:
        prestamo.estado = nuevo_estado
        if es_devolucion:
            libro = prestamo.libro
            if libro:
                libro.copias_disponibles = (libro.copias_disponibles or 0) + 1
        sesion.commit()  # commit directo, sin with begin
        return prestamo
    except Exception:
        sesion.rollback()
        raise


# ---------- Interfaz / Helpers ----------
def mostrar_prestamos_tabla(sesion: Session, prestamos=None):
    if prestamos is None:
        prestamos = obtener_prestamos(sesion)

    if not prestamos:  #Si no hubieran préstamos
        print("No hay préstamos registrados.")
        return

    tabla = PrettyTable()
    tabla.field_names = ['ID', 'RUT Usuario', 'Libro', 'Fecha Inicio', 'Fecha Vencimiento', 'Estado']
    for p in prestamos:
        nombre_libro = p.libro.nombre_libro if p.libro else f"(libro id {p.id_libro})"
        tabla.add_row([
            p.id_prestamo,
            p.rut_usuario,
            nombre_libro,
            p.fecha_inicio.strftime("%d-%m-%Y") if p.fecha_inicio else "",
            p.fecha_vencimiento.strftime("%d-%m-%Y") if p.fecha_vencimiento else "",
            p.estado
        ])
    print(tabla)

def listar_prestamos_pendientes_usuario(sesion: Session, rut: str):
    pendientes = obtener_prestamos_pendientes_por_usuario(sesion, rut)
    if not pendientes:
        print("No se encontraron préstamos pendientes para ese usuario.")
        return
    mostrar_prestamos_tabla(sesion, pendientes)

# ---------- CLI ----------
def menu_prestamos():
    print("\n=== MENÚ PRÉSTAMOS ===")
    print("1. Agregar préstamo (por nombre de libro)")
    print("2. Listar préstamos pendientes por RUT")
    print("3. Devolver libro (editar estado)")
    print("4. Eliminar préstamo")
    print("5. Mostrar todos los préstamos")
    print("0. Salir")
    return input("Elige una opción: ").strip()

def main():
    sesion = crear_sesion()
    while True:
        opcion = menu_prestamos()

        if opcion == "1":
            rut = input("RUT del usuario: ").strip()
            nombre_libro = input("Nombre del libro (sin tildes es ok): ").strip()
            fecha_inicio_str = input("Fecha inicio (DD-MM-YYYY): ").strip()
            fecha_vencimiento_str = input("Fecha vencimiento (DD-MM-YYYY): ").strip()
            try:
                fecha_inicio = parse_fecha(fecha_inicio_str)
                fecha_vencimiento = parse_fecha(fecha_vencimiento_str)
            except ValueError as e:
                print(e)
                continue

            prestamo, err = agregar_prestamo_por_nombre(sesion, rut, nombre_libro, fecha_inicio, fecha_vencimiento)
            if err:
                print("No se pudo agregar el préstamo:", err)
            else:
                print(f"Préstamo creado: ID {prestamo.id_prestamo} - Libro: {prestamo.libro.nombre_libro}")

        elif opcion == "2":
            rut = input("RUT del usuario: ").strip()
            listar_prestamos_pendientes_usuario(sesion, rut)

        elif opcion == "3":
            rut = input("RUT del usuario: ").strip()
            nombre_libro = input("Nombre del libro a devolver: ").strip()
            prestamo = obtener_prestamo_por_usuario_y_libro(sesion, rut, nombre_libro)
            if prestamo:
                print(f"Préstamo encontrado: ID {prestamo.id_prestamo} - Libro: {prestamo.libro.nombre_libro}")
                print("1. Devuelto a tiempo\n2. Devuelto atrasado")
                opcion_estado = input("Elige el estado: ").strip()
                if opcion_estado == "1":
                    nuevo_estado = "Devuelto a tiempo"
                elif opcion_estado == "2":
                    nuevo_estado = "Devuelto atrasado"
                else:
                    print("Opción inválida.")
                    continue
                editar_prestamo_estado(sesion, prestamo, nuevo_estado)
                print("Préstamo actualizado.")
            else:
                print("No se encontró préstamo pendiente para ese libro y usuario.")

        elif opcion == "4":
            rut = input("RUT del usuario: ").strip()
            nombre_libro = input("Nombre del libro: ").strip()
            prestamo = obtener_prestamo_por_usuario_y_libro(sesion, rut, nombre_libro)
            if prestamo:
                eliminar_prestamo(sesion, prestamo)
                print("Préstamo eliminado.")
            else:
                print("No se encontró préstamo pendiente para ese libro y usuario.")

        elif opcion == "5":
            mostrar_prestamos_tabla(sesion)

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()
