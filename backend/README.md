
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

## 🚀 Inicio Rápido con Docker

### 1. Levantar los servicios
```bash
# Desde el directorio raíz del proyecto
cd /path/to/SGH
docker compose --env-file .env.development up -d
```

### 2. Verificar que todo funciona
```bash
# Probar la conexión a la base de datos
curl -X GET http://localhost:8000/db/test-db

# Ver los logs del backend
docker compose logs backend
```

### 3. Comandos útiles
```bash
# Reconstruir después de cambios en código
docker compose build backend --no-cache
docker compose up -d

# Entrar al contenedor para debugging
docker compose exec backend bash

# Detener servicios
docker compose down
```

## 🧪 Sistema de Pruebas

### Comandos de Pruebas con Docker
```bash
# Ejecutar todas las pruebas
docker compose exec backend pytest -v

# Solo pruebas unitarias
docker compose exec backend make -f Makefile.tests test-unit

# Solo pruebas de integración  
docker compose exec backend make -f Makefile.tests test-integration

# Pruebas con reporte de cobertura
docker compose exec backend make -f Makefile.tests test-cov
```

## 📖 API Documentation

Una vez que el servidor esté ejecutándose, puedes acceder a la documentación interactiva de la API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Endpoints Principales

### Autenticación

#### POST `/auth/login` - Iniciar sesión
```bash
# Request
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@universidad.edu",
    "password": "admin123"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@universidad.edu",
    "nombre": "Administrador",
    "apellido": "Sistema",
    "role": "admin",
    "is_active": true
  }
}
```

#### POST `/auth/register` - Registrar nuevo usuario
```bash
# Request
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "docente@universidad.edu",
    "password": "docente123",
    "nombre": "Juan Carlos",
    "apellido": "Pérez González",
    "role": "docente"
  }'
```

**Response (201 Created):**
```json
{
  "id": 2,
  "email": "docente@universidad.edu",
  "nombre": "Juan Carlos",
  "apellido": "Pérez González",
  "role": "docente",
  "is_active": true,
  "created_at": "2025-09-14T10:30:00Z"
}
```

### Docentes

#### GET `/docentes` - Listar docentes
```bash
# Request
curl -X GET "http://localhost:8000/docentes?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "nombre": "María Elena",
      "apellido": "García Rodríguez",
      "email": "maria.garcia@universidad.edu",
      "telefono": "+56912345678",
      "departamento": "Ingeniería Informática",
      "especialidad": "Desarrollo de Software",
      "is_active": true,
      "created_at": "2025-09-01T08:00:00Z"
    },
    {
      "id": 2,
      "nombre": "Carlos Alberto",
      "apellido": "Mendoza Silva",
      "email": "carlos.mendoza@universidad.edu",
      "telefono": "+56987654321",
      "departamento": "Matemáticas",
      "especialidad": "Análisis Numérico",
      "is_active": true,
      "created_at": "2025-09-02T09:15:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 10,
  "pages": 3
}
```

#### POST `/docentes` - Crear nuevo docente
```bash
# Request
curl -X POST "http://localhost:8000/docentes" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "nombre": "Ana Patricia",
    "apellido": "López Fernández",
    "email": "ana.lopez@universidad.edu",
    "telefono": "+56998765432",
    "departamento": "Ciencias de la Computación",
    "especialidad": "Inteligencia Artificial"
  }'
```

**Response (201 Created):**
```json
{
  "id": 3,
  "nombre": "Ana Patricia",
  "apellido": "López Fernández",
  "email": "ana.lopez@universidad.edu",
  "telefono": "+56998765432",
  "departamento": "Ciencias de la Computación",
  "especialidad": "Inteligencia Artificial",
  "is_active": true,
  "created_at": "2025-09-14T11:45:00Z"
}
```

### Restricciones de Horario

#### GET `/restricciones-horario` - Listar restricciones de horario
```bash
# Request
curl -X GET "http://localhost:8000/restricciones-horario?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "docente_id": 1,
      "dia_semana": 1,
      "hora_inicio": "08:00:00",
      "hora_fin": "12:00:00",
      "disponible": true,
      "descripcion": "Disponible para clases matutinas - Lunes",
      "docente": {
        "id": 1,
        "nombre": "María Elena",
        "apellido": "García Rodríguez",
        "email": "maria.garcia@universidad.edu"
      }
    },
    {
      "id": 2,
      "docente_id": 1,
      "dia_semana": 2,
      "hora_inicio": "14:00:00",
      "hora_fin": "18:00:00",
      "disponible": false,
      "descripcion": "No disponible - Reunión departamental",
      "docente": {
        "id": 1,
        "nombre": "María Elena",
        "apellido": "García Rodríguez",
        "email": "maria.garcia@universidad.edu"
      }
    },
    {
      "id": 3,
      "docente_id": 2,
      "dia_semana": 3,
      "hora_inicio": "09:00:00",
      "hora_fin": "13:00:00",
      "disponible": true,
      "descripcion": "Disponible para laboratorios - Miércoles",
      "docente": {
        "id": 2,
        "nombre": "Carlos Alberto",
        "apellido": "Mendoza Silva",
        "email": "carlos.mendoza@universidad.edu"
      }
    }
  ],
  "total": 45,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

#### GET `/restricciones-horario/{id}` - Obtener restricción por ID
```bash
# Request
curl -X GET "http://localhost:8000/restricciones-horario/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "docente_id": 1,
  "dia_semana": 1,
  "hora_inicio": "08:00:00",
  "hora_fin": "12:00:00",
  "disponible": true,
  "descripcion": "Disponible para clases matutinas - Lunes",
  "created_at": "2025-09-10T08:00:00Z",
  "updated_at": "2025-09-12T10:30:00Z",
  "docente": {
    "id": 1,
    "nombre": "María Elena",
    "apellido": "García Rodríguez",
    "email": "maria.garcia@universidad.edu",
    "departamento": "Ingeniería Informática"
  }
}
```

#### POST `/restricciones-horario` - Crear nueva restricción
```bash
# Request
curl -X POST "http://localhost:8000/restricciones-horario" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "docente_id": 2,
    "dia_semana": 4,
    "hora_inicio": "10:00",
    "hora_fin": "14:00",
    "disponible": true,
    "descripcion": "Disponible para clases teóricas - Jueves"
  }'
```

**Response (201 Created):**
```json
{
  "id": 4,
  "docente_id": 2,
  "dia_semana": 4,
  "hora_inicio": "10:00:00",
  "hora_fin": "14:00:00",
  "disponible": true,
  "descripcion": "Disponible para clases teóricas - Jueves",
  "created_at": "2025-09-14T12:00:00Z",
  "updated_at": "2025-09-14T12:00:00Z"
}
```

#### PUT `/restricciones-horario/{id}` - Actualizar restricción completa
```bash
# Request
curl -X PUT "http://localhost:8000/restricciones-horario/4" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "docente_id": 2,
    "dia_semana": 4,
    "hora_inicio": "09:00",
    "hora_fin": "13:00",
    "disponible": true,
    "descripcion": "Horario actualizado - Disponible jueves mañana"
  }'
```

**Response (200 OK):**
```json
{
  "id": 4,
  "docente_id": 2,
  "dia_semana": 4,
  "hora_inicio": "09:00:00",
  "hora_fin": "13:00:00",
  "disponible": true,
  "descripcion": "Horario actualizado - Disponible jueves mañana",
  "created_at": "2025-09-14T12:00:00Z",
  "updated_at": "2025-09-14T12:15:00Z"
}
```

#### PATCH `/restricciones-horario/{id}` - Actualizar restricción parcial
```bash
# Request
curl -X PATCH "http://localhost:8000/restricciones-horario/4" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "disponible": false,
    "descripcion": "No disponible - Actividad especial"
  }'
```

**Response (200 OK):**
```json
{
  "id": 4,
  "docente_id": 2,
  "dia_semana": 4,
  "hora_inicio": "09:00:00",
  "hora_fin": "13:00:00",
  "disponible": false,
  "descripcion": "No disponible - Actividad especial",
  "created_at": "2025-09-14T12:00:00Z",
  "updated_at": "2025-09-14T12:30:00Z"
}
```

#### DELETE `/restricciones-horario/{id}` - Eliminar restricción
```bash
# Request
curl -X DELETE "http://localhost:8000/restricciones-horario/4" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (204 No Content):**
```
(Sin contenido - eliminación exitosa)
```

#### GET `/restricciones-horario/docente/{docente_id}` - Restricciones por docente
```bash
# Request
curl -X GET "http://localhost:8000/restricciones-horario/docente/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "docente_id": 1,
    "dia_semana": 1,
    "hora_inicio": "08:00:00",
    "hora_fin": "12:00:00",
    "disponible": true,
    "descripcion": "Disponible para clases matutinas - Lunes"
  },
  {
    "id": 2,
    "docente_id": 1,
    "dia_semana": 2,
    "hora_inicio": "14:00:00",
    "hora_fin": "18:00:00",
    "disponible": false,
    "descripcion": "No disponible - Reunión departamental"
  }
]
```

#### GET `/restricciones-horario/dia/{dia_semana}` - Restricciones por día
```bash
# Request
curl -X GET "http://localhost:8000/restricciones-horario/dia/1?disponible=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "docente_id": 1,
    "dia_semana": 1,
    "hora_inicio": "08:00:00",
    "hora_fin": "12:00:00",
    "disponible": true,
    "descripcion": "Disponible para clases matutinas - Lunes",
    "docente": {
      "nombre": "María Elena",
      "apellido": "García Rodríguez",
      "email": "maria.garcia@universidad.edu"
    }
  },
  {
    "id": 5,
    "docente_id": 3,
    "dia_semana": 1,
    "hora_inicio": "14:00:00",
    "hora_fin": "17:00:00",
    "disponible": true,
    "descripcion": "Disponible para tutorías - Lunes tarde",
    "docente": {
      "nombre": "Ana Patricia",
      "apellido": "López Fernández",
      "email": "ana.lopez@universidad.edu"
    }
  }
]
```

### Testing Database
- `GET /db/test-db` - Verificar conexión a la base de datos

```bash
# Request
curl -X GET "http://localhost:8000/db/test-db"
```

**Response (200 OK):**
```json
{
  "message": "Conexión exitosa a la base de datos",
  "database": "sgh_db",
  "timestamp": "2025-09-14T12:45:00Z"
}
```

## 📝 Códigos de Estado HTTP

### Respuestas Exitosas
- `200 OK` - Solicitud procesada exitosamente
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa

### Errores del Cliente
- `400 Bad Request` - Datos de entrada inválidos
- `401 Unauthorized` - Token de autenticación requerido o inválido
- `403 Forbidden` - Permisos insuficientes
- `404 Not Found` - Recurso no encontrado
- `409 Conflict` - Conflicto con el estado actual del recurso

### Errores del Servidor
- `500 Internal Server Error` - Error interno del servidor

## 🔐 Autenticación

Todos los endpoints (excepto `/auth/login` y `/auth/register`) requieren autenticación mediante Bearer Token:

```bash
# Incluir en todas las peticiones autenticadas
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📅 Referencia de Días de la Semana

Para el campo `dia_semana` en restricciones de horario:
- `1` = Lunes
- `2` = Martes  
- `3` = Miércoles
- `4` = Jueves
- `5` = Viernes
- `6` = Sábado
- `7` = Domingo

## ⏰ Formato de Horas

Las horas deben enviarse en formato `HH:MM` (24 horas):
- Ejemplo: `"08:00"`, `"14:30"`, `"23:59"`
- La API responde con formato completo: `"08:00:00"`
