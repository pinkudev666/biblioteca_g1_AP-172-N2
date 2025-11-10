import sys
from pathlib import Path

# agregar raíz del proyecto al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datos.conexion import Session as crear_sesion
from negocio.negocio_prestamo import NegocioPrestamo
from datetime import date, datetime

def menu_prestamos():
    print("\n=== MENÚ PRÉSTAMOS ===")
    print("1. Agregar préstamo")
    print("2. Cambiar estado de préstamo")
    print("3. Listar préstamos pendientes de un usuario")
    print("4. Listar todos los préstamos de un usuario")
    print("5. Reporte préstamos atrasados")
    print("0. Salir")
    return input("Elige una opción: ")

def main():
    sesion = crear_sesion()
    negocio_prestamo = NegocioPrestamo(sesion)

    while True:
        opcion = menu_prestamos()

        try:
            if opcion == "1":
                rut = input("RUT del usuario: ")
                nombre_libro = input("Nombre del libro: ")

                fecha_inicio_str = input("Fecha de inicio (dd-mm-aaaa, Enter = hoy): ")
                fecha_vencimiento_str = input("Fecha de vencimiento (dd-mm-aaaa, Enter = inicio + 5 días): ")

                prestamo, error = negocio_prestamo.agregar_prestamo_por_nombre(
                    rut, nombre_libro, fecha_inicio_str or None, fecha_vencimiento_str or None
                )

                if prestamo:
                    print("Préstamo creado exitosamente:")
                    negocio_prestamo.mostrar_prestamos_tabla([prestamo])
                else:
                    print(f"No se pudo crear el préstamo: {error}")


            elif opcion == "2":
                rut = input("RUT del usuario: ").strip()
                nombre_libro = input("Nombre del libro del préstamo: ").strip()

                # Obtenemos todos los préstamos coincidentes
                prestamos = negocio_prestamo.obtener_prestamos_por_usuario_y_libro(rut, nombre_libro)

                if not prestamos:
                    print("No se encontraron préstamos para ese usuario y libro.")
                    continue

                # Selección si hay varios préstamos coincidentes
                if len(prestamos) > 1:
                    print("Se encontraron varios préstamos que coinciden:")
                    negocio_prestamo.mostrar_prestamos_tabla(prestamos)

                    prestamo = None
                    intentos = 0
                    max_intentos = 3

                    while intentos < max_intentos:
                        entrada = input(
                            f"Elige el ID del préstamo a editar (Tiene 3 intentos en caso de error. Intento {intentos + 1}/{max_intentos}, Enter para cancelar): "
                        ).strip()
                        if not entrada:
                            print("Operación cancelada.")
                            break
                        try:
                            indice = int(entrada)
                            prestamo = next((p for p in prestamos if p.id_prestamo == indice), None)
                            if prestamo:
                                break
                            else:
                                intentos += 1
                                if intentos < max_intentos:
                                    print(f"ID no válido, intenta nuevamente ({max_intentos - intentos} intentos restantes).")
                                else:
                                    print("Has agotado los intentos. Volviendo al menú principal.")
                        except ValueError:
                            intentos += 1
                            if intentos < max_intentos:
                                print(f"Debes ingresar un número válido ({max_intentos - intentos} intentos restantes).")
                            else:
                                print("Has agotado los intentos. Volviendo al menú principal.")

                    if prestamo is None:
                        continue  # vuelve al menú principal si no se seleccionó un préstamo válido
                else:
                    prestamo = prestamos[0]

                print(f"Préstamo actual: {prestamo.estado}")

                # Leer input tal cual; si queda vacío, mandamos None (el negocio mantendrá el valor)
                nuevo_estado_raw = input("Nuevo estado (Pendiente, Devuelto a tiempo, Devuelto atrasado), Enter = mantener estado: ").strip()
                nuevo_estado = None if not nuevo_estado_raw else nuevo_estado_raw.title()

                # Validar que, si el usuario escribió algo, sea uno de los estados permitidos
                estados_permitidos = {"Pendiente", "Devuelto A Tiempo", "Devuelto Atrasado"}
                if nuevo_estado is not None and nuevo_estado not in estados_permitidos:
                    print("Estado no reconocido. Se mantendrá el estado actual.")
                    nuevo_estado = None  # esto hace que el método de negocio conserve el estado

                # Si se detecta que será una devolución (y el usuario escribió algo), pedir fecha
                fecha_dev = None
                if nuevo_estado is not None and nuevo_estado.lower() in ("devuelto a tiempo", "devuelto atrasado"):
                    fecha_dev_str = input("Fecha de devolución (dd-mm-aaaa, Enter = hoy): ").strip()
                    if fecha_dev_str:
                        try:
                            fecha_dev = datetime.strptime(fecha_dev_str, "%d-%m-%Y").date()
                        except ValueError:
                            print("Formato inválido. Se usará la fecha de hoy.")
                            fecha_dev = date.today()
                    else:
                        fecha_dev = date.today()

                # Llamar al negocio siempre: si nuevo_estado es None, la función lo interpretará como 'mantener'
                if fecha_dev:
                    negocio_prestamo.editar_prestamo_estado(prestamo, nuevo_estado, fecha_dev)
                else:
                    negocio_prestamo.editar_prestamo_estado(prestamo, nuevo_estado)

                print("Préstamo actualizado:")
                negocio_prestamo.mostrar_prestamos_tabla([prestamo])

            elif opcion == "3":
                rut = input("RUT del usuario: ")
                negocio_prestamo.listar_prestamos_pendientes_usuario(rut)

            elif opcion == "4":
                rut = input("RUT del usuario: ")
                negocio_prestamo.listar_prestamos_por_usuario(rut)

            elif opcion == "5":
                negocio_prestamo.listar_prestamos_atrasados()

            elif opcion == "0":
                print("Saliendo del programa...")
                break

            else:
                print("Opción no válida, intenta nuevamente.")

        except Exception as e:
            print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
