import sys
from pathlib import Path

# agregar raíz del proyecto al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from negocio.negocio_tipo_usuario import NegocioTipo

def menu_tipos_usuarios():
    print("\n=== MENÚ TIPOS DE USUARIO ===")
    print("1. Listar tipos de usuario")
    print("2. Buscar tipo de usuario por nombre")
    print("3. Agregar tipo de usuario")
    print("4. Eliminar tipo de usuario")
    print("0. Salir")
    return input("Elige una opción: ").strip()

def main():
    negocio = NegocioTipo()  # Instancia de la clase de negocio

    while True:
        opcion = menu_tipos_usuarios()

        if opcion == "1":
            negocio.listar_tipos()

        elif opcion == "2":
            buscar = input("Ingrese parte del nombre del tipo de usuario: ").strip()
            if not buscar:
                print("Debe ingresar un texto para buscar.")
                continue
            tipos_encontrados = negocio.buscar_tipos_like(buscar)
            if tipos_encontrados:
                negocio.mostrar_tipos_tabla(tipos_encontrados)

        elif opcion == "3":
            nombre = input("Ingrese nombre del tipo de usuario a agregar: ").strip()
            tipo_nuevo = negocio.agregar_tipo(nombre)
            if tipo_nuevo:
                print("\nLista actualizada de tipos de usuario:")
                negocio.listar_tipos()

        elif opcion == "4":
            nombre = input("Ingrese nombre del tipo de usuario a eliminar: ").strip()
            eliminado = negocio.eliminar_tipo(nombre)
            if eliminado:
                print("\nLista actualizada de tipos de usuario:")
                negocio.listar_tipos()

        elif opcion == "0":
            print("Saliendo del menú de tipos de usuario...")
            break

        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()
