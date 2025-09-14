import os
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar variables de entorno para testing antes de importar cualquier módulo del proyecto
os.environ.setdefault("DB_URL", "sqlite:///:memory:")
os.environ.setdefault("POSTGRES_DB", "test_sgh")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("NODE_ENV", "testing")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000,http://localhost:8100")
os.environ.setdefault("JWT_SECRET_KEY", "test_secret_key_for_testing")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRE_MINUTES", "30")

# Configurar pytest-asyncio
import pytest

pytest_plugins = ["pytest_asyncio"]