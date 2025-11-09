# 🧠 Backend API - Sistema de Gestión de Horarios

API REST desarrollada con **FastAPI** bajo una **arquitectura hexagonal (Ports & Adapters)**, diseñada para la gestión de horarios académicos.  
Incluye autenticación JWT, persistencia en PostgreSQL y despliegue mediante Docker y Kubernetes.

---

## 🛠️ Stack Tecnológico

| Componente | Descripción |
|-------------|-------------|
| ⚡ **FastAPI** | Framework web moderno, asíncrono y de alto rendimiento |
| 🗃️ **SQLAlchemy** | ORM para manejo de la base de datos |
| 🐘 **PostgreSQL** | Base de datos relacional |
| 🔄 **Alembic** | Migraciones de esquema |
| 🧩 **Pydantic** | Validación y serialización de datos |
| 🔐 **JWT** | Autenticación basada en tokens |
| 🧪 **pytest** | Framework de testing |
| 🐳 **Docker & Compose** | Contenedorización y orquestación local |
| ☸️ **Kubernetes** | Despliegue en entornos productivos |

---

## 🧱 Arquitectura Hexagonal

backend/
├── api/
│   └── v1/
│       ├── api.py
│       └── endpoints/
│           ├── academic.py
│           ├── auth.py
│           ├── infrastructure.py
│           ├── personnel.py
│           ├── restrictions.py
│           ├── schedule.py
│           └── system.py
│
├── domain/
│   ├── entities.py
│   ├── models.py
│   └── ports.py
│
├── application/
│   └── use_cases/
│       ├── administrador_use_cases.py
│       ├── asignatura_use_cases.py
│       ├── bloque_use_cases.py
│       ├── campus_use_cases.py
│       ├── clase_use_cases.py
│       ├── docente_use_cases.py
│       ├── edificio_use_cases.py
│       ├── estudiante_use_cases.py
│       ├── restriccion_use_cases.py
│       ├── restriccion_horario_use_cases.py
│       ├── sala_use_cases.py
│       ├── seccion_use_cases.py
│       ├── user_auth_use_cases.py
│       └── user_management_use_cases.py
│
├── infrastructure/
│   ├── controllers/
│   ├── database/
│   ├── repositories/
│   ├── auth.py
│   └── dependencies.py
│
├── migrations/
│   └── versions/
│
├── tests/
│   ├── test_auth_api.py
│   ├── test_docentes_api.py
│   ├── test_asignaturas_api.py
│   ├── ...
│
├── main.py
├── config.py
├── requirements.txt
├── Dockerfile
└── Dockerfile.test

---

## 🚀 Inicio Rápido

### 📦 Instalación y Entorno

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

El proyecto utiliza variables definidas en .env.development, ubicado en la raíz del monorepo.
Ejemplo:
DATABASE_URL=postgresql://user:password@localhost:5432/sgh
JWT_SECRET=clave_super_secreta
ENVIRONMENT=development


🐳 Levantar Servicios con Docker Compose
# Iniciar servicios (backend + db)
docker compose --env-file .env.development up -d

# Ver estado de los servicios
docker compose --env-file .env.development ps

# Logs del backend
docker compose --env-file .env.development logs -f backend

# Acceder al contenedor
docker compose --env-file .env.development exec backend bash

# Reconstruir imagen
docker compose --env-file .env.development build backend

# Detener servicios
docker compose --env-file .env.development down


🧪 Testing
Las pruebas están dockerizadas y usan pytest.
# Levantar ambiente de test
docker compose -f docker-compose.test.yml --env-file .env.development up -d

# Ejecutar tests
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest -v

# Con cobertura
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest --cov=. --cov-report=term-missing

# Tests por módulo
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_auth_api.py -v


📖 Documentación API
La documentación interactiva se encuentra disponible en:


🔗 Swagger UI: https://sgh.inf.uct/api/docs


Endpoints principales
CategoríaEndpointsDescripción🔐 Auth & Users/auth, /usersRegistro, login, gestión de usuarios🎓 Académico/docentes, /asignaturas, /seccionesGestión académica🏫 Infraestructura/campus, /edificios, /salasAdministración de espacios físicos⏰ Horarios/bloques, /clases, /restricciones, /restricciones-horarioGestión de disponibilidad y planificación⚙️ Sistema/health, /db/test-dbEstado y verificación de servicios

🔐 Autenticación
La API usa JWT (JSON Web Tokens).
Incluye el token en el header de tus peticiones:
Authorization: Bearer <tu_token>


🧰 Ejemplos de Uso (curl)
Registro de usuario
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "docente@universidad.edu",
    "contrasena": "Docente123!",
    "nombre": "Juan",
    "apellido": "Pérez"
  }'

Login (JSON)
curl -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "docente@universidad.edu",
    "password": "Docente123!"
  }'

Consultar perfil
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"

Verificar conexión DB
curl -X GET "http://localhost:8000/api/db/test-db"


📊 Ejemplo de Flujo Completo
# 1️⃣ Registrar usuario
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@universidad.edu","contrasena":"Admin123!","nombre":"Admin","apellido":"Sistema"}'

# 2️⃣ Hacer login y guardar token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@universidad.edu","password":"Admin123!"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# 3️⃣ Consultar perfil
curl -X GET "http://localhost:8000/api/auth/me" -H "Authorization: Bearer $TOKEN"


🧾 Notas Técnicas


📅 Días de la semana: 1=Lunes … 7=Domingo


⏰ Formato de hora: HH:MM (por ejemplo: "08:00", "14:30")


⚠️ Códigos HTTP:


✅ 200/201/204 — Éxito


❌ 400/401/404/409 — Error del cliente


💥 500 — Error interno del servidor





📄 Licencia
Este proyecto forma parte del monorepo SGH (Sistema de Gestión de Horarios)
Distribuido bajo licencia MIT o la definida en el repositorio raíz.


