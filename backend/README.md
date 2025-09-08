
---

### **/backend/README.md**

# Gestión de horarios API (Hexagonal + FastAPI)

## 📂 Capas de la arquitectura
- **domain**: entidades y puertos (reglas del negocio, sin dependencias externas)
- **application**: casos de uso; orquestan el dominio mediante puertos
- **infrastructure**: adaptadores (repositorios, controladores HTTP, DB, etc.)
- **main.py**: composición de la app (inyección de dependencias)

## 🚀 Requisitos
- Python 3.12+
- PostgreSQL 16+
- Entorno virtual (`venv`)

## ⚙️ Instalación y Configuración

### 1. Configuración del Entorno
```bash
# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

### 2. Configuración de la Base de Datos

1. Crear el usuario y la base de datos en PostgreSQL:
```bash
# Crear la base de datos (como usuario postgres)
sudo -u postgres createdb db

# Crear el usuario y asignar permisos (Cambiar variables como user, db, '' por credenciales que correspondan)
sudo -u postgres psql -c "CREATE USER user WITH PASSWORD '';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE db TO user;"
sudo -u postgres psql -d SGH -c "GRANT ALL ON SCHEMA public TO user;"
```

2. Configurar las variables de entorno:
```bash
# Crear archivo .env en /backend/fastapi
echo "DB_URL=postgresql://user:password@localhost:port/db" > .env
```

3. Ejecutar las migraciones de la base de datos:
```bash
# Desde el directorio /backend/fastapi
alembic upgrade head
```

### 3. Iniciar el Servidor
```bash
# Desde el directorio /backend/fastapi
uvicorn main:app --reload --port 8000
```

### 4. Verificar la Instalación
Para verificar que todo está funcionando correctamente:
```bash
# Probar la conexión a la base de datos
curl -X GET http://localhost:8000/db/test-db
```

Deberías recibir una respuesta confirmando que la conexión a la base de datos es exitosa.
