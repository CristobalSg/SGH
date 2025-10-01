# Backend API - Sistema de Gestión de Horarios

API REST desarrollada con **FastAPI** y **arquitectura hexagonal** para la gestión de horarios académicos.

## 🛠️ Stack Tecnológico
- **FastAPI** + *## 📝 Notas

**Días de la semana**: 1=Lunes, 2=Martes, ..., 7=Domingo  
**Formato hora**: `HH:MM` (ej: `"08:00"`, `"14:30"`)  
**Códigos HTTP**: 200/201/204 (éxito), 400/401/404/409 (error cliente), 500 (error servidor)

### Endpoints Disponibles
- ✅ **Autenticación** (`/auth`) - Registro, login, información de usuario
- ✅ **Restricciones** (`/restricciones`) - CRUD completo de restricciones generales
- ✅ **Restricciones de Horario** (`/restricciones-horario`) - CRUD + consultas específicas
- ✅ **Base de Datos** (`/db`) - Testing de conexión
- ✅ **Sistema** (`/`, `/health`) - Información y estado

### Próximos Endpoints
- 🔄 **Docentes** (`/docentes`) - Gestión de docentes
- 🔄 **Asignaturas** (`/asignaturas`) - Gestión de asignaturas  
- 🔄 **Bloques** (`/bloques`) - Gestión de bloques horarios
- 🔄 **Secciones** (`/secciones`) - Gestión de secciones
- 🔄 **Clases** (`/clases`) - Gestión de clases programadaslchemy** + **PostgreSQL**
- **Alembic** (migraciones) + **pytest** (testing)
- **Docker** + **Docker Compose**

## 📂 Estructura (Arquitectura Hexagonal)
```
fastapi/
├── domain/              # Entidades y reglas de negocio
├── application/         # Casos de uso
├── infrastructure/      # Adaptadores (DB, HTTP, Auth)
├── tests/              # Pruebas unitarias e integración  
├── migrations/         # Migraciones de DB
└── main.py            # Configuración de la aplicación
```

## 🚀 Inicio Rápido

### Levantar servicios
```bash
# Desde la raíz del proyecto SGH
docker compose --env-file .env.development up -d

# Verificar estado
curl http://localhost:8000/db/test-db
```

### Comandos útiles
```bash
# Rebuild tras cambios
docker compose --env-file .env.development build backend 

# Levantar contenedores
docker compose --env-file .env.development up -d

# Logs y debug
docker compose --env-file .env.development logs backend
docker compose --env-file .env.development exec backend bash

# Estado de los contenedores
docker compose --env-file .env.development ps 

# Detener
docker compose --env-file .env.development down
```

## 🧪 Testing

```bash
# Todas las pruebas
docker compose --env-file .env.development exec backend pytest -v

# Comandos específicos con make (ahora completamente actualizados)
docker compose --env-file .env.development exec backend make -f Makefile.tests test-unit
docker compose --env-file .env.development exec backend make -f Makefile.tests test-integration

# Pruebas específicas por módulo
docker compose --env-file .env.development exec backend make -f Makefile.tests test-docente
docker compose --env-file .env.development exec backend make -f Makefile.tests test-asignatura
docker compose --env-file .env.development exec backend make -f Makefile.tests test-clase
docker compose --env-file .env.development exec backend make -f Makefile.tests test-seccion
docker compose --env-file .env.development exec backend make -f Makefile.tests test-bloque
docker compose --env-file .env.development exec backend make -f Makefile.tests test-restriccion
docker compose --env-file .env.development exec backend make -f Makefile.tests test-restriccion-horario
docker compose --env-file .env.development exec backend make -f Makefile.tests test-auth

# Pruebas de API específicas
docker compose --env-file .env.development exec backend make -f Makefile.tests test-auth-api
docker compose --env-file .env.development exec backend make -f Makefile.tests test-db-api
docker compose --env-file .env.development exec backend make -f Makefile.tests test-restricciones-api
docker compose --env-file .env.development exec backend make -f Makefile.tests test-restriccion-horario-api

# Con cobertura específica
docker compose --env-file .env.development exec backend make -f Makefile.tests test-cov
docker compose --env-file .env.development exec backend make -f Makefile.tests test-docente-cov
docker compose --env-file .env.development exec backend make -f Makefile.tests test-auth-cov

# Ver ayuda completa con todos los comandos disponibles
docker compose --env-file .env.development exec backend make -f Makefile.tests help
```

## 📖 Documentación API

**Documentación interactiva**: http://localhost:8000/docs  
**ReDoc**: http://localhost:8000/redoc

## 🎯 Endpoints Principales

### Autenticación (`/auth`)
```bash
# Registro de usuario
POST /auth/register
{
  "email": "docente@universidad.edu",
  "contrasena": "Docente123",
  "nombre": "Juan Carlos",
  "apellido": "Pérez"
}

# Login con formulario
POST /auth/login
Content-Type: application/x-www-form-urlencoded
username=admin@universidad.edu&password=admin123

# Login con JSON
POST /auth/login-json
{
  "email": "admin@universidad.edu",
  "password": "admin123"
}

# Obtener información del usuario actual
GET /auth/me
Authorization: Bearer YOUR_TOKEN
```

### Restricciones (`/restricciones`)
```bash
GET    /restricciones                    # Listar todas las restricciones
GET    /restricciones/{id}               # Obtener restricción por ID
POST   /restricciones                    # Crear nueva restricción
PUT    /restricciones/{id}               # Actualizar restricción completa
PATCH  /restricciones/{id}               # Actualizar restricción parcial
DELETE /restricciones/{id}               # Eliminar restricción
```

### Restricciones de Horario (`/restricciones-horario`)
```bash
# Operaciones CRUD básicas
GET    /restricciones-horario            # Listar todas
GET    /restricciones-horario/{id}       # Obtener por ID
POST   /restricciones-horario            # Crear nueva
PATCH  /restricciones-horario/{id}       # Actualizar parcial
DELETE /restricciones-horario/{id}       # Eliminar

# Consultas específicas
GET    /restricciones-horario/docente/{docente_id}     # Por docente
GET    /restricciones-horario/dia/{dia_semana}         # Por día (1-7)
GET    /restricciones-horario/disponibilidad/{docente_id}  # Disponibilidad de docente
DELETE /restricciones-horario/docente/{docente_id}     # Eliminar todas las restricciones de un docente
```

### Base de Datos (`/db`)
```bash
GET /db/test-db                          # Verificar conexión a la base de datos
```

### Sistema
```bash
GET /                                    # Información de la API
GET /health                              # Estado de salud del sistema
```

## 📋 Ejemplos de Uso

### Crear Restricción de Horario
```bash
curl -X POST "http://localhost:8000/restricciones-horario" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "docente_id": 1,
    "dia_semana": 1,
    "hora_inicio": "08:00",
    "hora_fin": "12:00",
    "disponible": true,
    "descripcion": "Disponible para clases matutinas - Lunes"
  }'
```

### Obtener Disponibilidad de Docente
```bash
curl -X GET "http://localhost:8000/restricciones-horario/disponibilidad/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Crear Restricción General
```bash
curl -X POST "http://localhost:8000/restricciones" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "titulo": "No disponible en feriados",
    "descripcion": "Restricción para días feriados",
    "tipo": "FERIADO",
    "activa": true
  }'
```

## 🔐 Autenticación

Incluir en headers (excepto login/register):
```bash
Authorization: Bearer YOUR_TOKEN
```

## � Notas

**Días de la semana**: 1=Lunes, 2=Martes, ..., 7=Domingo  
**Formato hora**: `HH:MM` (ej: `"08:00"`, `"14:30"`)  
**Códigos HTTP**: 200/201/204 (éxito), 400/401/404/409 (error cliente), 500 (error servidor)
