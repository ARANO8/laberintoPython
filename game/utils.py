import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta correcta de los recursos para PyInstaller."""
    if getattr(sys, 'frozen', False):  # Ejecutable
        base_path = sys._MEIPASS
    else:  # Script en ejecución
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
