import sys
from pathlib import Path


# agregar raíz del proyecto al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, date
from negocio.negocio_prestamo import (
    agregar_prestamo_por_nombre,
    editar_prestamo_estado,
    listar_prestamos_pendientes_usuario,
    listar_prestamos_por_usuario,
    listar_prestamos_atrasados,
    obtener_prestamo_por_usuario_y_libro
)
from datos.conexion import Session as crear_sesion

# ---------- CLI ----------
def menu_prestamos():
    print("\n=== MENÚ PRÉSTAMOS ===")
    print("1. Agregar préstamo")
    print("2. Cambiar estado de préstamo")
    print("3. Listar préstamos pendientes de un usuario")
    print("4. Listar todos los préstamos de un usuario")
    print("5. Reporte de préstamos atrasados")
    print("0. Salir")
    return input("Elige una opción: ")

def main():
    sesion = crear_sesion()
    while True:
        opcion = menu_prestamos()

        try:
            if opcion == "1":
                rut = input("RUT del usuario: ")
                nombre_libro = input("Nombre del libro: ")

                # Opcional: ingresar fechas
                fecha_inicio_input = input("Fecha de inicio (dd-mm-aaaa) o Enter para hoy: ")
                fecha_vencimiento_input = input("Fecha de vencimiento (dd-mm-aaaa) o Enter para 5 días después: ")

                fecha_inicio = datetime.strptime(fecha_inicio_input, "%d-%m-%Y").date() if fecha_inicio_input else None
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_input, "%d-%m-%Y").date() if fecha_vencimiento_input else None

                prestamo, error = agregar_prestamo_por_nombre(sesion, rut, nombre_libro, fecha_inicio, fecha_vencimiento)
                if prestamo:
                    print(f"Préstamo creado correctamente: {prestamo.id_prestamo}")
                else:
                    print(f"No se pudo crear el préstamo: {error}")

            elif opcion == "2":
                rut = input("RUT del usuario: ")
                nombre_libro = input("Nombre del libro: ")
                prestamo = obtener_prestamo_por_usuario_y_libro(sesion, rut, nombre_libro)
                if prestamo:
                    print(f"Préstamo encontrado: ID {prestamo.id_prestamo}, Estado: {prestamo.estado}")
                    nuevo_estado = input("Nuevo estado (Pendiente / Devuelto a tiempo / Devuelto atrasado): ")
                    editar_prestamo_estado(sesion, prestamo, nuevo_estado)
                    print("Estado actualizado correctamente.")
                else:
                    print("No se encontró un préstamo pendiente para ese libro y usuario.")

            elif opcion == "3":
                rut = input("RUT del usuario: ")
                listar_prestamos_pendientes_usuario(sesion, rut)

            elif opcion == "4":
                rut = input("RUT del usuario: ")
                listar_prestamos_por_usuario(sesion, rut)

            elif opcion == "5":
                listar_prestamos_atrasados(sesion)

            elif opcion == "0":
                print("Saliendo del programa...")
                break

            else:
                print("Opción no válida, intenta nuevamente.")

        except Exception as e:
            print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
