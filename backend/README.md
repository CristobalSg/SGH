# Backend API - Sistema de Gestión de Horarios

API REST desarrollada con **FastAPI** y **arquitectura hexagonal** para la gestión de horarios académicos.

## 🛠️ Stack Tecnológico

- **FastAPI** - Framework web moderno y de alto rendimiento
- **SQLAlchemy** - ORM para interacción con base de datos
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Gestor de migraciones de base de datos
- **Pydantic** - Validación de datos y configuración
- **JWT** - Autenticación basada en tokens
- **pytest** - Framework de testing
- **Docker & Docker Compose** - Contenedorización y orquestación
- **Kubernetes** - Despliegue en producción

## 📂 Arquitectura Hexagonal

```
backend/fastapi/
├── api/
│   └── v1/
│       ├── api.py                    # Router principal que agrupa todos los endpoints
│       └── endpoints/
│           ├── academic.py           # Asignaturas, secciones, clases
│           ├── auth.py               # Autenticación y usuarios
│           ├── infrastructure.py     # Campus, edificios, salas
│           ├── personnel.py          # Docentes
│           ├── restrictions.py       # Restricciones y restricciones de horario
│           ├── schedule.py           # Bloques horarios
│           └── system.py             # Health checks, database
├── domain/                    # Capa de Dominio
│   ├── entities.py           # Entidades de negocio
│   ├── models.py             # Modelos de datos
│   └── ports.py              # Interfaces (puertos)
│
├── application/               # Capa de Aplicación
│   └── use_cases/            # Casos de uso del negocio
│       ├── administrador_use_cases.py
│       ├── asignatura_use_cases.py
│       ├── bloque_use_cases.py
│       ├── campus_use_cases.py
│       ├── clase_uses_cases.py
│       ├── docente_use_cases.py
│       ├── edificio_use_cases.py
│       ├── estudiante_use_cases.py
│       ├── restriccion_horario_use_cases.py
│       ├── restriccion_use_cases.py
│       ├── sala_use_cases.py
│       ├── seccion_use_cases.py
│       ├── user_auth_use_cases.py
│       └── user_management_use_cases.py
│
├── infrastructure/            # Capa de Infraestructura
│   ├── controllers/          # Controladores HTTP (adaptadores)
│   │   ├── asignatura_controller.py
│   │   ├── auth_controller.py
│   │   ├── bloque_controller.py
│   │   ├── campus_controller.py
│   │   ├── clase_controller.py
│   │   ├── docente_controller.py
│   │   ├── edificio_controller.py
│   │   ├── restriccion_controller.py
│   │   ├── restriccion_horario_controller.py
│   │   ├── sala_controller.py
│   │   ├── seccion_controller.py
│   │   └── user_controller.py
│   │
│   ├── database/             # Configuración de base de datos
│   │   └── config.py
│   │
│   ├── repositories/         # Implementación de repositorios
│   │
│   ├── auth.py               # Utilidades de autenticación
│   └── dependencies.py       # Dependencias de FastAPI
│
├── migrations/                # Migraciones de Alembic
│   └── versions/
│
├── tests/                     # Pruebas automatizadas
│   ├── conftest.py
│   ├── test_asignaturas_api.py
│   ├── test_auth_api.py
│   ├── test_docentes_api.py
│   ├── test_edificios_campus_secciones_bloques_clases_api.py
│   ├── test_restricciones_api.py
│   ├── test_restricciones_horario_api.py
│   ├── test_salas_api.py
│   └── test_users_api.py
│
├── main.py                    # Punto de entrada de la aplicación (simplificado)
├── config.py                  # Configuración de variables de entorno
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Imagen Docker para producción
└── Dockerfile.test            # Imagen Docker para testing
```

## 🚀 Inicio Rápido

### Variables de Entorno

El proyecto utiliza el archivo `.env.development` ubicado en la raíz del proyecto.

### Levantar Servicios con Docker Compose

```bash
# Desde la raíz del proyecto SGH
docker compose --env-file .env.development up -d

# Verificar estado de los servicios
docker compose --env-file .env.development ps

# Ver logs del backend
docker compose --env-file .env.development logs -f backend

# Acceder al contenedor del backend
docker compose --env-file .env.development exec backend bash

# Reconstruir imagen tras cambios
docker compose --env-file .env.development build backend

# Detener servicios
docker compose --env-file .env.development down
```

## 🧪 Testing

El proyecto incluye pruebas automatizadas que se ejecutan en un ambiente dockerizado.

### Ejecutar Tests con Docker Compose

```bash
# Desde la raíz del proyecto SGH

# Levantar ambiente de testing
docker compose -f docker-compose.test.yml --env-file .env.development up -d

# Ejecutar todas las pruebas
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest -v

# Ejecutar pruebas con cobertura
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest --cov=. --cov-report=term-missing

# Ejecutar pruebas específicas por módulo
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_auth_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_users_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_docentes_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_asignaturas_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_salas_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_edificios_campus_secciones_bloques_clases_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_restricciones_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_restricciones_horario_api.py -v
docker compose -f docker-compose.test.yml --env-file .env.development exec backend pytest tests/test_system_api.py -v

# Ver logs de las pruebas
docker compose -f docker-compose.test.yml --env-file .env.development logs backend

# Detener ambiente de testing
docker compose -f docker-compose.test.yml --env-file .env.development down
```

## 📖 Documentación API

La API está desplegada en producción con Kubernetes y cuenta con documentación interactiva:

- **Swagger UI (Documentación Interactiva)**: https://sgh.inf.uct/api/docs

### Endpoints Disponibles

#### Autenticación y Usuarios
- ✅ **`/auth`** - Registro, login, información de usuario autenticado
- ✅ **`/users`** - Gestión de usuarios

#### Gestión Académica
- ✅ **`/docentes`** - CRUD de docentes
- ✅ **`/asignaturas`** - CRUD de asignaturas
- ✅ **`/secciones`** - CRUD de secciones

#### Infraestructura
- ✅ **`/campus`** - CRUD de campus
- ✅ **`/edificios`** - CRUD de edificios
- ✅ **`/salas`** - CRUD de salas

#### Planificación Horaria
- ✅ **`/bloques`** - CRUD de bloques horarios
- ✅ **`/clases`** - CRUD de clases programadas
- ✅ **`/restricciones`** - CRUD de restricciones generales
- ✅ **`/restricciones-horario`** - CRUD de restricciones de horario por docente

#### Sistema
- ✅ **`/`** - Información de la API
- ✅ **`/health`** - Estado de salud del sistema
- ✅ **`/db/test-db`** - Verificación de conexión a base de datos

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación. Para acceder a endpoints protegidos, incluir el token en los headers:

```bash
Authorization: Bearer YOUR_TOKEN
```

## � Ejemplos de Uso

A continuación se muestran ejemplos de cómo interactuar con la API usando `curl`. Asegúrate de tener los servicios levantados con Docker Compose.

### Autenticación

#### 1. Registrar un nuevo usuario

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "docente@universidad.edu",
    "contrasena": "Docente123!",
    "nombre": "Juan Carlos",
    "apellido": "Pérez"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 1,
  "email": "docente@universidad.edu",
  "nombre": "Juan Carlos",
  "apellido": "Pérez",
  "rol": "docente",
  "activo": true
}
```

#### 2. Iniciar sesión (Login con JSON)

```bash
curl -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "docente@universidad.edu",
    "password": "Docente123!"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Iniciar sesión (Login con Form Data)

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=docente@universidad.edu&password=Docente123!"
```

**Respuesta exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 4. Obtener información del usuario autenticado

```bash
# Primero obtén el token del login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "email": "docente@universidad.edu",
  "nombre": "Juan Carlos",
  "apellido": "Pérez",
  "rol": "docente",
  "activo": true
}
```

#### 5. Verificar conexión a la base de datos

```bash
curl -X GET "http://localhost:8000/api/db/test-db"
```

**Respuesta exitosa (200):**
```json
{
  "status": "success",
  "message": "Database connection successful"
}
```

#### 6. Verificar estado de salud del sistema

```bash
curl -X GET "http://localhost:8000/api/health"
```

**Respuesta exitosa (200):**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-14T12:00:00"
}
```

### Flujo completo de autenticación

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@universidad.edu",
    "contrasena": "Admin123!",
    "nombre": "Administrador",
    "apellido": "Sistema"
  }'

# 2. Hacer login y guardar el token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@universidad.edu",
    "password": "Admin123!"
  }' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# 3. Usar el token para acceder a endpoints protegidos
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## �📝 Notas Técnicas

- **Días de la semana**: 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado, 7=Domingo
- **Formato de hora**: `HH:MM` (ejemplo: `"08:00"`, `"14:30"`)
- **Códigos HTTP**:
  - `200/201/204` - Operación exitosa
  - `400/401/404/409` - Error del cliente
  - `500` - Error del servidor
