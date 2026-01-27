"""
Configuración global de pytest.
Carga variables de entorno antes de ejecutar cualquier test.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Verificar que las variables críticas existen
assert os.getenv("SUPABASE_DB_URL"), "❌ SUPABASE_DB_URL no encontrada en .env"
assert os.getenv("JWT_SECRET_KEY"), "❌ JWT_SECRET_KEY no encontrada en .env"
assert os.getenv("OPENAI_API_KEY"), "❌ OPENAI_API_KEY no encontrada en .env"

print(f"✅ .env cargado correctamente para tests desde: {env_path}")
