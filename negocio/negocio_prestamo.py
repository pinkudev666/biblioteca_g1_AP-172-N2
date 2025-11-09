from modelos.prestamo import Prestamo
from modelos.usuario import Usuario
from modelos.libro import Libro
from datetime import date, timedelta, datetime
from sqlalchemy.exc import IntegrityError
from negocio.negocio_libro import NegocioLibro
from prettytable import PrettyTable

class NegocioPrestamo:
    def __init__(self, sesion):
        self.sesion = sesion
        self.negocio_libro = NegocioLibro(sesion)

    # ---------- Préstamos ----------

    def obtener_prestamos_pendientes_por_usuario(self, rut_usuario: str):
        """Retorna todos los préstamos pendientes de un usuario."""
        return self.sesion.query(Prestamo).filter(
            Prestamo.rut_usuario == rut_usuario,
            Prestamo.estado == 'Pendiente'
        ).all()

    def obtener_prestamos_por_usuario_y_libro(self, rut_usuario: str, nombre_libro: str):
        """
        Retorna todos los préstamos de un usuario para libros que coincidan
        parcial o totalmente con el nombre indicado.
        """
        libros = self.negocio_libro.buscar_libros_por_nombre(nombre_libro)
        if not libros:
            return []

        prestamos = self.sesion.query(Prestamo).filter(
            Prestamo.rut_usuario == rut_usuario,
            Prestamo.id_libro.in_([l.id_libro for l in libros])
        ).all()

        return prestamos

    def agregar_prestamo_por_nombre(
        self, rut_usuario: str, nombre_libro: str,
        fecha_inicio: str | date = None, fecha_vencimiento: str | date = None
    ):
        """Crea un préstamo para el usuario y libro indicado. Las fechas pueden ser string o date."""

        # Parsear fechas si vienen como string
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
            except ValueError:
                fecha_inicio = date.today()
        if isinstance(fecha_vencimiento, str):
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%d-%m-%Y").date()
            except ValueError:
                fecha_vencimiento = (fecha_inicio or date.today()) + timedelta(days=5)

        fecha_inicio = fecha_inicio or date.today()
        fecha_vencimiento = fecha_vencimiento or (fecha_inicio + timedelta(days=5))

        # Validaciones de usuario
        usuario = self.sesion.query(Usuario).filter(Usuario.rut_usuario == rut_usuario).first()
        if not usuario:
            return None, "Usuario no existe"
        if not usuario.usuario_activo:
            return None, "Usuario inactivo. No puede solicitar préstamos"

        # Buscar libros
        libros = self.negocio_libro.buscar_libros_por_nombre(nombre_libro)
        if not libros:
            return None, "Libro no encontrado"

        # Selección si hay varios
        if len(libros) > 1:
            print("Se encontraron varios libros que coinciden:")
            self.negocio_libro.mostrar_libros_tabla(libros)
            while True:
                try:
                    opcion = int(input("Elige el índice del libro a prestar: "))
                    if 1 <= opcion <= len(libros):
                        libro = libros[opcion - 1]
                        break
                    else:
                        print("Índice fuera de rango, intenta nuevamente.")
                except ValueError:
                    print("Debes ingresar un número válido.")
        else:
            libro = libros[0]

        try:
            libro = self.sesion.query(Libro).filter(Libro.id_libro == libro.id_libro).with_for_update().first()
            if libro.copias_disponibles is None or libro.copias_disponibles <= 0:
                return None, f"No quedan copias disponibles de '{libro.nombre_libro}'"

            nuevo = Prestamo(
                rut_usuario=rut_usuario,
                id_libro=libro.id_libro,
                fecha_inicio=fecha_inicio,
                fecha_vencimiento=fecha_vencimiento,
                estado='Pendiente'
            )
            self.sesion.add(nuevo)
            libro.copias_disponibles -= 1
            self.sesion.commit()
            return nuevo, None

        except IntegrityError:
            self.sesion.rollback()
            return None, "Error al crear préstamo (integrity)"
        except Exception as e:
            self.sesion.rollback()
            return None, f"Error al crear préstamo: {e}"

    def editar_prestamo_estado(self, prestamo, nuevo_estado: str, fecha_devolucion: date = None):
        """
        Cambia el estado de un préstamo y registra fecha de devolución si corresponde.
        """
        es_devolucion = nuevo_estado.lower() in ("devuelto a tiempo", "devuelto atrasado")
        try:
            prestamo.estado = nuevo_estado
            if es_devolucion:
                prestamo.fecha_devolucion = fecha_devolucion or date.today()
                if prestamo.libro:
                    prestamo.libro.copias_disponibles = (prestamo.libro.copias_disponibles or 0) + 1
            self.sesion.commit()
            return prestamo
        except Exception:
            self.sesion.rollback()
            raise

    def obtener_prestamos_atrasados(self):
        """Retorna todos los préstamos pendientes que ya están vencidos."""
        hoy = date.today()
        return self.sesion.query(Prestamo).filter(
            Prestamo.estado == 'Pendiente',
            Prestamo.fecha_vencimiento < hoy
        ).all()

    def obtener_prestamos_por_usuario(self, rut_usuario: str):
        """Retorna todos los préstamos de un usuario, independientemente del estado."""
        return self.sesion.query(Prestamo).filter(Prestamo.rut_usuario == rut_usuario).all()

    # ---------- Helpers / tablas ----------

    def mostrar_prestamos_tabla(self, prestamos):
        if not prestamos:
            print("No hay préstamos para mostrar.")
            return

        tabla = PrettyTable()
        tabla.field_names = ['ID', 'RUT Usuario', 'Libro', 'Fecha Inicio', 'Fecha Vencimiento', 'Fecha Devolución', 'Estado']

        for p in prestamos:
            nombre_libro = p.libro.nombre_libro if p.libro else f"(libro id {p.id_libro})"
            tabla.add_row([
                p.id_prestamo,
                p.rut_usuario,
                nombre_libro,
                p.fecha_inicio.strftime("%d-%m-%Y") if p.fecha_inicio else "",
                p.fecha_vencimiento.strftime("%d-%m-%Y") if p.fecha_vencimiento else "",
                p.fecha_devolucion.strftime("%d-%m-%Y") if p.fecha_devolucion else "",
                p.estado
            ])
        print(tabla)

    def listar_prestamos_pendientes_usuario(self, rut: str):
        pendientes = self.obtener_prestamos_pendientes_por_usuario(rut)
        if not pendientes:
            print(f"El usuario {rut} no tiene préstamos pendientes.")
            return
        self.mostrar_prestamos_tabla(pendientes)

    def listar_prestamos_por_usuario(self, rut: str):
        prestamos = self.obtener_prestamos_por_usuario(rut)
        if not prestamos:
            print(f"El usuario {rut} no tiene préstamos registrados.")
            return
        self.mostrar_prestamos_tabla(prestamos)

    def listar_prestamos_atrasados(self):
        atrasados = self.obtener_prestamos_atrasados()
        if not atrasados:
            print("No hay préstamos atrasados.")
            return
        self.mostrar_prestamos_tabla(atrasados)
