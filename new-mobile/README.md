# 🌐 SGH — Frontend Base (Next Gen)

Este proyecto constituye la **nueva base frontend del Sistema de Gestión de Horarios (SGH)**, desarrollada con un stack moderno y una **arquitectura limpia**, enfocada en rendimiento, mantenibilidad y compatibilidad con entornos web y móviles.  
Su meta es reemplazar gradualmente la versión anterior del frontend, unificando la experiencia de usuario y sentando las bases para su futura integración con **Capacitor** como aplicación móvil.

---

## ⚙️ Stack Tecnológico

| Componente | Descripción |
|-------------|-------------|
| ⚡ **Vite** | Bundler ultrarrápido con soporte nativo para HMR |
| ⚛️ **React 19 + TypeScript** | Interfaz declarativa, segura y escalable |
| 🎨 **Tailwind CSS** | Sistema de estilos utilitarios con diseño responsivo |
| 🔤 **Heroicons** | Iconos SVG optimizados y personalizables para React |
| 🧱 **Arquitectura Limpia** | Separación clara entre capas de dominio, aplicación y presentación |
| 🧩 **pnpm** | Gestor de dependencias rápido y eficiente |
| ☁️ **Vercel** | Plataforma de despliegue automática para proyectos frontend modernos |

> 🧩 *Ionic ha sido descartado temporalmente debido a conflictos con TailwindCSS.*

---

## 🧠 Estructura General

new-mobile/
├── src/
│ ├── components/ # Componentes reutilizables (UI / layout)
│ ├── pages/ # Páginas principales
│ ├── hooks/ # Lógica reutilizable
│ ├── services/ # Integraciones API / capa de datos
│ ├── types/ # Tipos globales de TypeScript
│ ├── App.tsx
│ ├── index.css # Configuración base de Tailwind
│ └── main.tsx # Punto de entrada de la app
│
├── public/ # Recursos estáticos
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts

yaml


---

## 🚀 Instalación y Ejecución

El proyecto forma parte del **monorepo de SGH**, por lo tanto puedes instalar dependencias desde la raíz o directamente dentro del directorio `new-mobile`.

# Instalar todas las dependencias del monorepo
pnpm install

# O solo las del frontend
cd new-mobile
pnpm install
🔧 Scripts disponibles

pnpm run dev        # Inicia el entorno de desarrollo local
pnpm run build      # Compila la aplicación para producción
pnpm run lint       # Analiza el código y verifica estándares
pnpm run preview    # Ejecuta una vista previa del build


# 📘 Inventario de Endpoints — Backend FastAPI

Este documento lista los endpoints definidos en `backend/fastapi/api/v1/endpoints/`, indicando su propósito y los controladores asociados.  
El backend se organiza en módulos que agrupan la lógica por dominio funcional.

---

## 🔐 auth.py

**Descripción:** Endpoints de autenticación y gestión de usuarios.  
**Controladores asociados:**
- `auth_controller.py`
- `user_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| POST | `/auth/login` | Inicia sesión de usuario | ✅ Implementado |
| POST | `/auth/register` | Crea un nuevo usuario | 🕓 Pendiente |
| GET | `/auth/me` | Devuelve información del usuario actual | ✅ Implementado |
| PUT | `/users/{id}` | Actualiza información de usuario | 🕓 Pendiente |

---

## 🏫 academic.py

**Descripción:** Endpoints de gestión académica (asignaturas, secciones, clases).  
**Controladores asociados:**
- `asignatura_controller.py`
- `seccion_controller.py`
- `clase_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/academic/asignaturas` | Lista todas las asignaturas | ✅ Implementado |
| POST | `/academic/asignatura` | Crea una nueva asignatura | 🕓 Pendiente |
| GET | `/academic/secciones` | Lista secciones activas | ✅ Implementado |
| GET | `/academic/clases` | Lista clases disponibles | ✅ Implementado |

---

## 🏗️ infrastructure.py

**Descripción:** Endpoints de infraestructura física (campus, edificios, salas).  
**Controladores asociados:**
- `campus_controller.py`
- `edificio_controller.py`
- `sala_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/infrastructure/campus` | Lista campus disponibles | ✅ Implementado |
| GET | `/infrastructure/edificios` | Lista edificios por campus | ✅ Implementado |
| GET | `/infrastructure/salas` | Lista salas disponibles | ✅ Implementado |
| POST | `/infrastructure/sala` | Crea una nueva sala | 🕓 Pendiente |

---

## 👥 personnel.py

**Descripción:** Endpoints de personal académico (docentes).  
**Controladores asociados:**
- `docente_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/personnel/docentes` | Lista docentes registrados | ✅ Implementado |
| POST | `/personnel/docente` | Crea un nuevo docente | 🕓 Pendiente |

---

## ⛔ restrictions.py

**Descripción:** Endpoints de restricciones (generales y de horario).  
**Controladores asociados:**
- `restriccion_controller.py`
- `restriccion_horario_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/restrictions` | Lista restricciones generales | ✅ Implementado |
| GET | `/restrictions/horarios` | Lista restricciones de horario | ✅ Implementado |
| POST | `/restrictions/add` | Crea una nueva restricción | ✅ Implementado |
| DELETE | `/restrictions/{id}` | Elimina restricción existente | 🕓 Pendiente |

---

## ⏰ schedule.py

**Descripción:** Endpoints de horarios y bloques.  
**Controladores asociados:**
- `bloque_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/schedule/bloques` | Lista bloques de horario disponibles | ✅ Implementado |
| POST | `/schedule/bloque` | Crea un nuevo bloque | 🕓 Pendiente |

---

## ⚙️ system.py

**Descripción:** Endpoints del sistema (verificación y conexión con base de datos).  
**Controladores asociados:**
- `test_db_controller.py`

| Método | Endpoint | Descripción | Estado Frontend |
|---------|-----------|-------------|-----------------|
| GET | `/system/health` | Verifica estado general del backend | ✅ Implementado |
| GET | `/system/db-test` | Comprueba conexión con la base de datos | ✅ Implementado |

---

## 🧩 Notas

- Los controladores se ubican en `backend/fastapi/infrastructure/controllers/`.
- Cada controlador implementa los routers expuestos por los módulos en `api/v1/endpoints/`.
- El estado del frontend se refiere a la integración actual con **New Mobile**.

---


http://localhost:8100
⚙️ Si el puerto está ocupado, Vite asignará automáticamente uno disponible.

🌐 Despliegue en Vercel
La aplicación está optimizada para Vercel, con integración directa desde GitHub.
Cada push a la rama main o production genera un despliegue automático.

🚢 Pasos para desplegar
Crea un nuevo proyecto en Vercel.

Conecta el repositorio del monorepo SGH.

En Root Directory, selecciona new-mobile/.

Configura el comando de build:
bash

pnpm run build
Define el directorio de salida:

nginx

dist
Guarda y despliega 🚀

🌍 Variables de Entorno
Si la aplicación se conecta al backend (FastAPI), define las siguientes variables en
Vercel → Settings → Environment Variables:

ini

VITE_API_URL=https://sgh.inf.uct/api
VITE_APP_ENV=production
🧩 Flujo de Trabajo Recomendado
📂 Ramas
Usa la siguiente convención de nombres:

php-template

feature/<nombre>     → nuevas funcionalidades
fix/<nombre>         → correcciones de bugs
refactor/<nombre>    → mejoras internas o reestructuración
💬 Commits
Sigue el estándar Conventional Commits:


feat: add responsive login layout
fix: resolve Tailwind CSS conflict in navbar
refactor: optimize state management with custom hook
🧭 Convenciones Generales
Gestor de paquetes: pnpm

Formateo: Prettier + ESLint

Componentes: Reutilizables y desacoplados

Estilos: Basados en clases Tailwind y diseño consistente

Commits: Estilo Conventional Commits

Ramas: Según propósito (feature, fix, refactor, etc.)

📱 Futuro del Proyecto
🤝 Integración con Capacitor para versión móvil híbrida.

📦 Inclusión progresiva de módulos desde el frontend anterior.

🧩 Implementación de autenticación y comunicación con el backend SGH.

⚡ Optimización de rendimiento y soporte para SSR (Server Side Rendering) futuro.

📄 Licencia
Este proyecto forma parte del sistema SGH (Sistema de Gestión de Horarios).
Todos los derechos reservados © 2025 — Equipo SGH.