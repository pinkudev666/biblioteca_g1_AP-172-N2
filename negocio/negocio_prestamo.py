from config_rutas import ROOT
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.prestamo import Prestamo
from modelos.libro import Libro
from modelos.usuario import Usuario
from negocio.negocio_libro import obtener_libro_por_nombre  
from auxiliares.validaciones import parse_fecha
from prettytable import PrettyTable
from datos.conexion import Session as crear_sesion
from datetime import date, timedelta

# ---------- Lógica de negocio ----------
def obtener_prestamos_pendientes_por_usuario(sesion: Session, rut_usuario: str):
    #Retorna todos los préstamos pendientes de un usuario específico (lista vacía si no hay)
    return sesion.query(Prestamo).filter(
        Prestamo.rut_usuario == rut_usuario,
        Prestamo.estado == 'Pendiente'
    ).all()

def obtener_prestamo_por_usuario_y_libro(sesion: Session, rut_usuario: str, nombre_libro: str):
    # Retorna un préstamo pendiente de un usuario para un libro específico, si existe.
    libro = obtener_libro_por_nombre(sesion, nombre_libro)
    if not libro:
        return None
    prestamos = obtener_prestamos_pendientes_por_usuario(sesion, rut_usuario)
    for p in prestamos:
        if p.id_libro == libro.id_libro:
            return p
    return None


def agregar_prestamo_por_nombre(
    sesion: Session,
    rut_usuario: str,
    nombre_libro: str,
    fecha_inicio: date = None,
    fecha_vencimiento: date = None
):
    # Agrega un préstamo de un libro para un usuario activo, con fechas flexibles.
    
    # Obtener usuario
    usuario = sesion.query(Usuario).filter(Usuario.rut_usuario == rut_usuario).first()
    if not usuario:
        return None, "Usuario no existe"
    if not usuario.usuario_activo:
        return None, "Usuario inactivo. No puede solicitar préstamos"

    # Obtener libro
    libro = obtener_libro_por_nombre(sesion, nombre_libro)
    if not libro:
        return None, "Libro no encontrado"
    if libro.copias_disponibles is None or libro.copias_disponibles <= 0:
        return None, "No quedan copias disponibles"

     # Fechas flexibles: puedes pasar fecha_inicio y fecha_vencimiento, o dejar que se calculen automáticamente
    fecha_inicio = fecha_inicio or date.today()  # Si no se pasó, hoy
    fecha_vencimiento = fecha_vencimiento or (fecha_inicio + timedelta(days=5))  # Si no se pasó, 5 días después

    # Crear préstamo
    try:
        nuevo = Prestamo(
            rut_usuario=rut_usuario,
            id_libro=libro.id_libro,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            estado='Pendiente'
        )
        sesion.add(nuevo)
        libro.copias_disponibles -= 1
        sesion.commit()
        return nuevo, None
    except IntegrityError:
        sesion.rollback()
        return None, "Error al crear préstamo (integrity)"
    except Exception as e:
        sesion.rollback()
        return None, f"Error al crear préstamo: {e}"


def editar_prestamo_estado(sesion: Session, prestamo: Prestamo, nuevo_estado: str):
    # Cambia el estado de un préstamo y devuelve la copia al inventario si corresponde.
    es_devolucion = nuevo_estado in ("Devuelto a tiempo", "Devuelto atrasado")
    try:
        prestamo.estado = nuevo_estado
        if es_devolucion and prestamo.libro:
            prestamo.libro.copias_disponibles = (prestamo.libro.copias_disponibles or 0) + 1
        sesion.commit()
        return prestamo
    except Exception:
        sesion.rollback()
        raise


def obtener_prestamos_atrasados(sesion: Session):
    # Realiza un REPORTE de todos los préstamos pendientes que ya están vencidos. 
    hoy = date.today()
    return sesion.query(Prestamo).filter(
        Prestamo.estado == 'Pendiente',
        Prestamo.fecha_vencimiento < hoy
    ).all()


def obtener_prestamos_por_usuario(sesion: Session, rut_usuario: str):
    # Retorna todos los préstamos de un usuario, independientemente de su estado.
    return sesion.query(Prestamo).filter(Prestamo.rut_usuario == rut_usuario).all()


# ---------- Interfaz / Helpers ----------

def mostrar_prestamos_tabla(prestamos):
    # Recibe una lista de préstamos y muestra en formato PrettyTable o mensaje si está vacía.
    if not prestamos:
        print("No hay préstamos para mostrar.")
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
    # Muestra préstamos pendientes de un usuario específico.
    pendientes = obtener_prestamos_pendientes_por_usuario(sesion, rut)
    if not pendientes:
        print(f"El usuario {rut} no tiene préstamos pendientes.")
        return
    mostrar_prestamos_tabla(pendientes)


def listar_prestamos_por_usuario(sesion: Session, rut: str):
    # Muestra todos los préstamos de un usuario, sin importar el estado.
    prestamos = obtener_prestamos_por_usuario(sesion, rut)
    if not prestamos:
        print(f"El usuario {rut} no tiene préstamos registrados.")
        return
    mostrar_prestamos_tabla(prestamos)


def listar_prestamos_atrasados(sesion: Session):
    # Muestra todos los préstamos pendientes que están vencidos.
    atrasados = obtener_prestamos_atrasados(sesion)
    if not atrasados:
        print("No hay préstamos atrasados.")
        return
    mostrar_prestamos_tabla(atrasados)
