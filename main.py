from pathlib import Path
import sys
import importlib

# Asegúrate de ejecutar este archivo desde la raíz del proyecto o que la raíz esté en PYTHONPATH.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Configura aquí tus entradas: key -> (Etiqueta, módulo, función_a_llamar)
MENU_ENTRIES = {
    "1": ("Menú Usuarios", "ui.cli_usuario", "main"),
    "2": ("Menú Tipos de Usuarios", "ui.cli_tipo_usuario", "main"),
    "3": ("Menú Libros", "ui.cli_libros", "main"),
    "4": ("Menú Préstamo", "ui.cli_prestamo", "main"),
    "0": ("Salir", None, None),
}

def build_menu_text():
    lines = ["\n=== MENÚ PRINCIPAL ==="]
    for key, (label, *_ ) in MENU_ENTRIES.items():
        lines.append(f"[{key}] {label}")
    return "\n".join(lines)

def load_and_call(module_path: str, func_name: str):
    if not module_path or not func_name:
        # No hay módulo/función definidos: no hacemos nada (seguro)
        return

    try:
        module = importlib.import_module(module_path)
    except Exception as e:
        print(f"[ERROR] No se pudo importar '{module_path}': {e}")
        return

    func = getattr(module, func_name, None)
    if func is None or not callable(func):
        print(f"[ERROR] El módulo '{module_path}' no tiene una función ejecutable '{func_name}'.")
        return

    try:
        func()
    except SystemExit:
        print("(La IU terminó con exit; volviendo al menú.)")
    except Exception as e:
        print(f"[ERROR] Al ejecutar {module_path}.{func_name}: {e}")

def main():
    while True:
        print(build_menu_text())
        choice = input("Selecciona una opción: ").strip()
        if choice not in MENU_ENTRIES:
            print("Opción inválida. Intenta de nuevo.")
            continue

        label, module_path, func_name = MENU_ENTRIES[choice]

        # Si la opción es "0" (Salir) salimos del bucle
        if choice == "0":
            print("Saliendo. ¡Hasta luego!")
            break

        print(f"\n-- Abrir: {label} --\n")
        load_and_call(module_path, func_name)
        input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    main()
