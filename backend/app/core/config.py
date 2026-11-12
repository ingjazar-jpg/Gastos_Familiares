
from pathlib import Path


# Raíz del proyecto: sistema_gastos_familiar/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Directorio y archivo de persistencia
DATA_DIR = PROJECT_ROOT / "datos"
DATA_FILE = DATA_DIR / "datos_gastos.json"

# Nombre de la aplicación
APP_NAME = "Sistema de Control de Gastos Familiares"
APP_VERSION = "0.1.0"
