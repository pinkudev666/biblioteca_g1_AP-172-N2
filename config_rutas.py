from pathlib import Path
import sys

# --- ROOT del proyecto dinámico ---
# ROOT apunta a la carpeta donde está config_rutas.py (la raíz del proyecto)
ROOT = Path(__file__).resolve().parent  # si config_rutas.py está en la raíz, esto ya es suficiente

# agregar ROOT a sys.path para que Python encuentre módulos en la raíz
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
