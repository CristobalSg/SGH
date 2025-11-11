# Scripts de Bootstrap de Usuarios

Este directorio contiene scripts para inicializar usuarios en el sistema SGH.

## 📋 Scripts Disponibles

### 1. `bootstrap_admin.py` ⚙️

**Propósito:** Crea o actualiza el usuario administrador principal del sistema.

**Ejecución:** 
- Se ejecuta **automáticamente** al iniciar el backend en `start.sh`
- También puede ejecutarse manualmente

**Variables de entorno requeridas:**
```bash
INITIAL_ADMIN_USERNAME=admin
INITIAL_ADMIN_EMAIL=admin@inf.uct.cl
INITIAL_ADMIN_PASSWORD=TuPasswordSeguro123!
```

**Características:**
- ✅ **Idempotente**: Si el usuario ya existe, lo actualiza
- ✅ **Automático**: Se ejecuta en cada inicio del backend
- ✅ **Seguro**: Usa variables de entorno (no hardcoded)

---

### 2. `bootstrap_dev_users.py` 🎓

**Propósito:** Crea usuarios de desarrollo para roles de docente y estudiante.

**Ejecución:**
- Se ejecuta **automáticamente** en modo desarrollo (`BACK_ENV=development`)
- También puede ejecutarse manualmente

**Variables de entorno opcionales:**
```bash
# Docente de desarrollo
DEV_DOCENTE_NAME="Juan Carlos Pérez"
DEV_DOCENTE_EMAIL=juan.perez@inf.uct.cl
DEV_DOCENTE_PASSWORD=DocenteDev123!
DEV_DOCENTE_DEPARTAMENTO=INFORMATICA

# Estudiante de desarrollo
DEV_ESTUDIANTE_NAME="María González Rodríguez"
DEV_ESTUDIANTE_EMAIL=maria.gonzalez@alu.uct.cl
DEV_ESTUDIANTE_PASSWORD=EstudianteDev123!
DEV_ESTUDIANTE_MATRICULA=2024001
```

**Características:**
- ✅ **Opcional**: Solo se crea si las variables están definidas
- ✅ **Idempotente**: Si el usuario ya existe, lo actualiza
- ✅ **Compartido**: Estos usuarios son visibles por todo el equipo
- ⚠️ **Solo desarrollo**: No se ejecuta en producción

---

### 3. ~~`user_create.py`~~ ❌ (OBSOLETO)

**Estado:** Este script está obsoleto y debe ser eliminado o refactorizado.

**Problemas:**
- ❌ Crea admin (duplica `bootstrap_admin.py`)
- ❌ Contraseñas hardcodeadas
- ❌ No es idempotente
- ❌ Expone credenciales en el código

**Recomendación:** Eliminar o usar los nuevos scripts bootstrap.

---

## 🚀 Cómo Usar

### Inicio Automático (Recomendado)

Los scripts se ejecutan automáticamente al iniciar el backend:

```bash
# Desde la raíz del proyecto
docker compose --env-file .env.development up backend
```

**Qué sucede:**
1. ✅ Se ejecutan las migraciones de Alembic
2. ✅ Se crea/actualiza el usuario administrador
3. ✅ Se crean/actualizan usuarios de desarrollo (si `BACK_ENV=development`)
4. ✅ Se inicia el servidor FastAPI

---

### Ejecución Manual

#### Dentro del contenedor Docker:

```bash
# Crear admin
docker compose --env-file .env.development exec backend python scripts/bootstrap_admin.py

# Crear usuarios de desarrollo
docker compose --env-file .env.development exec backend python scripts/bootstrap_dev_users.py
```

#### Localmente (sin Docker):

```bash
# Asegúrate de estar en backend/fastapi
cd backend/fastapi

# Cargar variables de entorno
export $(cat ../../.env.development | xargs)

# Ejecutar scripts
python scripts/bootstrap_admin.py
python scripts/bootstrap_dev_users.py
```

---

## 🔐 Seguridad y Buenas Prácticas

### ✅ **Usar Variables de Entorno**

```bash
# ✅ CORRECTO
INITIAL_ADMIN_PASSWORD=AdminPass123

# ❌ INCORRECTO (hardcoded en código)
admin_password = "AdminPass123"
```

### ✅ **Separar Entornos**

- **Desarrollo**: `.env.development` con usuarios de prueba compartidos
- **Producción**: `.env.production` con credenciales reales y seguras

### ⚠️ **Usuarios Compartidos en Desarrollo**

Los usuarios creados por `bootstrap_dev_users.py` están en la **base de datos compartida**.

**Esto significa:**
- 👥 Todo el equipo puede ver estos usuarios
- 🔑 Las contraseñas están en `.env.development` (versionado)
- ⚠️ **NO cambies las contraseñas** sin coordinarlo con el equipo
- 📝 Si necesitas usuarios personales, créalos con el endpoint `/api/auth/register`

### ✅ **Git y Variables de Entorno**

```bash
# ✅ Versionar (desarrollo)
.env.development  # Usuarios compartidos, contraseñas conocidas

# ❌ NO versionar (producción)
.env.production   # Agregar a .gitignore
.env.local        # Credenciales personales
```

---

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────┐
│         Inicio del Backend (start.sh)          │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Migraciones Alembic   │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  bootstrap_admin.py   │
          │  ✓ Crea/actualiza     │
          │    administrador      │
          └───────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ ¿BACK_ENV=development? │
         └────────┬───────┬────────┘
                  │ Sí    │ No
                  ▼       └────────┐
      ┌────────────────────┐       │
      │bootstrap_dev_users │       │
      │  ✓ Crea docente    │       │
      │  ✓ Crea estudiante │       │
      └────────┬───────────┘       │
               │                   │
               ▼                   ▼
          ┌─────────────────────────┐
          │   Inicia FastAPI        │
          └─────────────────────────┘
```

---

## 🎯 Resumen de Credenciales

### Usuarios Creados Automáticamente

| Rol | Email | Password (dev) | Creado por |
|-----|-------|----------------|------------|
| **Administrador** | `admin@inf.uct.cl` | `AdminPass123` | `bootstrap_admin.py` |
| **Docente** | `juan.perez@inf.uct.cl` | `DocenteDev123!` | `bootstrap_dev_users.py` |
| **Estudiante** | `maria.gonzalez@alu.uct.cl` | `EstudianteDev123!` | `bootstrap_dev_users.py` |

⚠️ **IMPORTANTE:** Estas credenciales son para **desarrollo solamente**.

---

## 🐛 Troubleshooting

### Error: "Configuración requerida para bootstrap del admin"

**Causa:** Faltan variables de entorno obligatorias.

**Solución:**
```bash
# Verifica que estén definidas:
echo $INITIAL_ADMIN_USERNAME
echo $INITIAL_ADMIN_EMAIL
echo $INITIAL_ADMIN_PASSWORD

# Si faltan, cárgalas:
export $(cat .env.development | xargs)
```

### Error: "No se configuró docente/estudiante de desarrollo"

**Causa:** Variables opcionales no definidas (es normal).

**Solución:** Si quieres crear estos usuarios, define las variables en `.env.development`.

### Los usuarios no se crean

**Causa:** El script no se ejecuta o falla silenciosamente.

**Solución:**
```bash
# Ejecuta manualmente con logs:
docker compose --env-file .env.development exec backend python scripts/bootstrap_admin.py
docker compose --env-file .env.development exec backend python scripts/bootstrap_dev_users.py

# Revisa los logs del contenedor:
docker compose --env-file .env.development logs backend
```

---

## 📚 Referencias

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [12 Factor App - Config](https://12factor.net/config)
- [OWASP - Secure Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
