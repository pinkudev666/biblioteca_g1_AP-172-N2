# ui/cli_tipo_usuario.py
import sys
from pathlib import Path

# permitir ejecutar desde subcarpetas sin romper imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datos.conexion import Session  
from negocio.negocio_tipo_usuario import NegocioTipo
from modelos.tipo_usuario import Tipo_usuario

def pedir_int(prompt: str) -> int | None:
    v = input(prompt).strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        print("ID inválido (debe ser número).")
        return None

def mostrar_menu():
    print("\n--- GESTIÓN: TIPOS DE USUARIO ---")
    print("1) Listar tipos activos")
    print("2) Listar todos (activos e inactivos)")
    print("3) Buscar por texto")
    print("4) Crear tipo")
    print("5) Editar nombre (por ID)")
    print("6) Editar nombre por texto")
    print("7) Borrar lógicamente (por ID o nombre)")
    print("8) Restaurar tipo (por ID o nombre)")
    print("0) Salir")

def cli_loop(negocio: NegocioTipo):
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            tipos = negocio.obtener_listado_tipos()
            negocio.mostrar_tipos_tabla(tipos)

        elif opcion == "2":
            activos = negocio.obtener_listado_tipos()
            inactivos = negocio.obtener_tipos_inactivos()
            print("\n--- Activos ---")
            negocio.mostrar_tipos_tabla(activos)
            print("\n--- Inactivos ---")
            negocio.mostrar_tipos_tabla(inactivos)

        elif opcion == "3":
            texto = input("Texto a buscar (parcial): ").strip()
            if not texto:
                print("Texto vacío.")
                continue
            resultados = negocio.buscar_tipos_por_nombre(texto)
            negocio.mostrar_tipos_tabla(resultados)

        elif opcion == "4":
            nombre = input("Nombre del nuevo tipo: ").strip()
            if not nombre:
                print("Nombre vacío.")
                continue
            creado = negocio.agregar_tipo(nombre)
            if creado:
                # mostrar el nuevo tipo en tabla (reutilizando la función del negocio)
                negocio.mostrar_tipos_tabla([creado])
            else:
                print("No se pudo crear el tipo. Puede que ya exista un tipo activo con ese nombre o hubo un error.")

        elif opcion == "5":
            # editar pasando objeto -> usa editar_tipo(tipo_obj, nuevo_nombre)
            tipo_id = pedir_int("ID del tipo a editar: ")
            if tipo_id is None:
                continue
            tipo_obj = negocio.sesion.query(Tipo_usuario).get(tipo_id)
            if not tipo_obj:
                print("Tipo no encontrado.")
                continue
            nuevo_nombre = input(f"Nuevo nombre para '{tipo_obj.tipo_usuario}': ").strip()
            if not nuevo_nombre:
                print("Nombre vacío.")
                continue
            actualizado = negocio.editar_tipo(tipo_obj, nuevo_nombre)
            if actualizado:
                negocio.mostrar_tipos_tabla([actualizado])
            else:
                print("No se pudo actualizar. Puede haber conflicto o error de BD.")

        elif opcion == "6":
            # editar por coincidencia parcial (usa editar_nombre_por_like si existe)
            texto = input("Texto para buscar coincidencia (parcial): ").strip()
            if not texto:
                print("Texto vacío.")
                continue
            candidatos = negocio.buscar_tipos_por_nombre(texto)
            if len(candidatos) == 0:
                print("No se encontró ninguna coincidencia.")
                continue
            if len(candidatos) > 1:
                print("Hay más de una coincidencia. Especifica mejor o usa editar por ID.")
                negocio.mostrar_tipos_tabla(candidatos)
                continue
            tipo_obj = candidatos[0]
            nuevo_nombre = input(f"Nuevo nombre para '{tipo_obj.tipo_usuario}': ").strip()
            if not nuevo_nombre:
                print("Nombre vacío.")
                continue
            # si tu negocio implementó editar_nombre_por_like, úsalo; si no, pasamos por editar_tipo
            if hasattr(negocio, "editar_nombre_por_like"):
                actualizado = negocio.editar_nombre_por_like(tipo_obj.tipo_usuario, nuevo_nombre)
            else:
                actualizado = negocio.editar_tipo(tipo_obj, nuevo_nombre)
            if actualizado:
                negocio.mostrar_tipos_tabla([actualizado])
            else:
                print("No se pudo actualizar (coincidencia ambigua, duplicado o error).")


        elif opcion == "7":
            entrada = input("ID o nombre del tipo a borrar lógicamente: ").strip()
            if not entrada:
                print("Entrada vacía.")
                continue
            try:
                val = int(entrada)
                tipo_obj = negocio.sesion.query(Tipo_usuario).get(val)
                if not tipo_obj:
                    print("Tipo no encontrado por ID.")
                    continue
                resultado = negocio.eliminar_tipo(tipo_obj)
            except ValueError:
                resultado = negocio.eliminar_tipo(entrada)
            if resultado:
                print(f"Tipo marcado como inactivo: ID {getattr(resultado, 'id_tipo_usuario', '?')} — {getattr(resultado, 'tipo_usuario', '')}")
            else:
                print("No se pudo borrar el tipo. Puede que existan usuarios activos asociados o hubo un error.")

        elif opcion == "8":
            entrada = input("ID o nombre del tipo a restaurar: ").strip()
            if not entrada:
                print("Entrada vacía.")
                continue
            try:
                val = int(entrada)
                tipo_obj = negocio.sesion.query(Tipo_usuario).get(val)
                if not tipo_obj:
                    print("Tipo no encontrado por ID.")
                    continue
                resultado = negocio.reactivar_tipo(tipo_obj)
            except ValueError:
                resultado = negocio.reactivar_tipo(entrada)
            if resultado:
                negocio.mostrar_tipos_tabla([resultado])
            else:
                print("No se pudo reactivar el tipo. Puede que ya exista un tipo activo con ese nombre o hubo un error.")

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


def main():
    # crear sesión y pasarla al negocio; cerrar al final
    session = Session()
    negocio = NegocioTipo(session)
    try:
        cli_loop(negocio)
    finally:
        try:
            session.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
