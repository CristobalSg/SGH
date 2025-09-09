
---

### **/backend/README.md**

# Gestión de horarios API (Hexagonal + FastAPI)

## 🛠️ Tecnologías Utilizadas
- **FastAPI**: Framework web para APIs REST
- **SQLAlchemy**: ORM para manejo de base de datos
- **Alembic**: Migraciones de base de datos
- **Pydantic**: Validación y serialización de datos
- **PostgreSQL**: Base de datos relacional
- **pytest**: Framework de pruebas unitarias
- **pytest-cov**: Análisis de cobertura de código


## 📂 Estructura del Proyecto
```
fastapi/
├── domain/              # Entidades y puertos (reglas del negocio)
├── application/         # Casos de uso (orquestación del dominio)
├── infrastructure/      # Adaptadores (repositorios, controladores HTTP, DB)
├── tests/              # Pruebas unitarias e integración
│   └── application/
│       └── use_cases/
├── migrations/         # Migraciones de base de datos (Alembic)
├── main.py            # Composición de la app (inyección de dependencias)
├── requirements.txt   # Dependencias del proyecto
├── pytest.ini       # Configuración de pruebas
└── Makefile.tests   # Comandos para ejecutar pruebas
```

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

## 🧪 Sistema de Pruebas

El proyecto cuenta con un sistema completo de pruebas automatizadas que incluye:

### Tipos de Pruebas Implementadas
- **Pruebas Unitarias**: Testing de casos de uso y lógica de negocio
- **Pruebas de Integración**: Testing de endpoints API y flujos completos
- **Análisis de Cobertura**: Reportes detallados de cobertura de código

### Estructura de Pruebas
```
tests/
├── application/
│   └── use_cases/
│       └── test_restriccion_horario_use_cases.py    # Pruebas unitarias
└── integration/
    ├── conftest.py                                  # Configuración y fixtures
    └── test_restricciones_api.py                   # Pruebas de integración API
```

### Comandos de Pruebas
```bash
# Ejecutar todas las pruebas (unitarias + integración)
make -f Makefile.tests test

# Solo pruebas unitarias
make -f Makefile.tests test-unit

# Solo pruebas de integración
make -f Makefile.tests test-integration

# Pruebas con reporte de cobertura
make -f Makefile.tests test-cov

# Pruebas de API específicas
make -f Makefile.tests test-api
```

### Configuración de Testing
- **SQLite in-memory**: Base de datos temporal para pruebas aisladas
- **Fixtures**: Datos de prueba reutilizables
- **pytest**: Framework principal con configuración en `pytest.ini`
- **Makefile.tests**: Automatización de comandos de pruebas

## 📖 API Documentation

Una vez que el servidor esté ejecutándose, puedes acceder a la documentación interactiva de la API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Endpoints Principales

### Restricciones
- `GET /restricciones` - Listar restricciones (con paginación)
- `POST /restricciones` - Crear nueva restricción
- `GET /restricciones/{id}` - Obtener restricción por ID
- `PUT /restricciones/{id}` - Actualizar restricción completa
- `PATCH /restricciones/{id}` - Actualizar restricción parcial
- `DELETE /restricciones/{id}` - Eliminar restricción

### Testing Database
- `GET /db/test-db` - Verificar conexión a la base de datos
