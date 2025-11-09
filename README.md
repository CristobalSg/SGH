SGH — Sistema de Gestión de Horario

El proyecto SGH es un Sistema de Gestión de Horarios Académicos, desarrollado como un monorepo que integra todos los componentes del sistema: backend, frontend móvil, documentación técnica y algoritmo generador de horarios.
Su arquitectura está pensada para facilitar la colaboración entre equipos, escalar en entornos distribuidos y mantener una base de código organizada.

📁 Estructura del repositorio
SGH/
├── .github/                  # Workflows y acciones de CI/CD (integración continua)
├── .husky/                   # Hooks de git para validar commits antes de hacer push
├── algorithm/                # Contiene el código fuente del algoritmo FET (generador de horarios)
├── backend/                  # API principal (FastAPI, PostgreSQL, arquitectura hexagonal)
├── deploy/                   # Archivos y scripts de despliegue (Docker, Kubernetes, etc.)
├── docs/                     # Documentación técnica (diagramas UML, arquitectura y roles)
├── mobile/                   # Versión antigua de la app móvil (Ionic / React Native anterior)
├── new-mobile/               # Nueva base del frontend móvil y web (React + Vite + Tailwind)
├── node_modules/             # Dependencias de Node.js (instaladas con pnpm)
├── .env.development          # Variables de entorno para entorno local
├── .gitignore                # Archivos y carpetas ignoradas por Git
├── docker-compose.yml        # Orquestador de servicios principales (backend, DB, frontend)
├── docker-compose.test.yml   # Entorno de testing automatizado
├── commitlint.config.js      # Configuración de estilo de commits (Conventional Commits)
├── LICENSE                   # Licencia del proyecto (MIT / GNU)
├── package.json              # Configuración y scripts globales del monorepo
├── pnpm-lock.yaml            # Bloqueo de dependencias instaladas
└── README.md                 # Este archivo

🧩 Descripción de carpetas principales
🧠 algorithm/

Contiene el algoritmo de generación automática de horarios, basado en la herramienta FET (Free Educational Timetabling).

Escrito en C++ y utiliza Qt 6.9.1 o superior.

Su función es generar horarios válidos según restricciones académicas (disponibilidad de docentes, salas, bloques, etc.).

Se comunica con el backend mediante archivos o endpoints personalizados.

📄 Compilación:

cd algorithm/fet-7.4.4
qmake fet.pro
make -j 16  # compila usando 16 hilos

⚙️ backend/

Implementa la API REST del sistema usando FastAPI bajo una arquitectura hexagonal.
Gestiona:

Usuarios, autenticación JWT y roles (docentes, estudiantes, administradores)

Asignaturas, clases, secciones, salas y restricciones

Conexión con PostgreSQL y migraciones con Alembic

📄 Tecnologías:
FastAPI · SQLAlchemy · PostgreSQL · Docker · pytest · JWT

📄 Ejemplo de estructura interna:

backend/fastapi/
├── api/                 # Endpoints (auth, docentes, asignaturas, etc.)
├── application/         # Casos de uso (lógica del negocio)
├── domain/              # Entidades y puertos
├── infrastructure/      # Controladores, repositorios y DB
├── tests/               # Pruebas automatizadas
└── main.py              # Punto de entrada del backend

📱 new-mobile/

Carpeta que contiene la nueva base frontend del sistema SGH.
Diseñada para reemplazar gradualmente la app anterior, con enfoque en escalabilidad y compatibilidad web/móvil.

📄 Stack principal:

⚡ Vite

⚛️ React 19 + TypeScript

🎨 Tailwind CSS

🧱 Arquitectura limpia (capas de dominio, aplicación y presentación)

📄 Ejemplo de estructura:

src/
 ├─ components/   # Componentes reutilizables (UI)
 ├─ App.tsx
 ├─ main.tsx      # Punto de entrada
 └─ index.css     # Configuración de estilos


📄 Scripts útiles:

pnpm run dev        # Inicia el entorno local
pnpm run build      # Compila para producción
pnpm run lint       # Analiza el código
pnpm run preview    # Visualiza la build

🧾 docs/

Contiene la documentación técnica y visual del proyecto.
Incluye:

Diagramas UML de casos de uso (Administrador, Alumno, Profesor)

Diagramas de arquitectura y componentes (API, BD, frontend, etc.)

Documentación de diseño creada con draw.io / diagrams.net

📂 Ejemplo:

docs/
├── Diagramas de casos de uso/
│   ├── Administrador.png
│   ├── Alumno.png
│   └── Profesor.png
└── Diagramas de arquitectura/
    ├── Diagrama_de_arquitectura_de_software.png
    └── Diagrama_de_componentes.jpeg

🧰 deploy/

Carpeta dedicada al despliegue del sistema.
Puede incluir:

Archivos de configuración para entornos de producción (Kubernetes, Docker Swarm, etc.)

Scripts automatizados de despliegue continuo (CI/CD)

📱 mobile/

Versión anterior de la aplicación móvil, desarrollada inicialmente con Ionic / React Native.
Actualmente reemplazada por new-mobile/, pero se mantiene por compatibilidad y referencia histórica.

🐳 Despliegue con Docker

Para iniciar el sistema completo (backend + frontend + base de datos):

docker-compose --env-file .env.development up -d


Ver estado:

docker-compose ps


Reiniciar un servicio:

docker-compose restart backend


Parar todos los servicios:

docker-compose down

🌍 Acceso al sistema

Aplicación Web: http://localhost:8100

API Backend: http://localhost:8000

Documentación API (Swagger): http://localhost:8000/docs

🧩 Archivos clave
Archivo	Descripción
.env.development	Variables de entorno locales
docker-compose.yml	Define los servicios del proyecto
docker-compose.test.yml	Configuración para testing
package.json	Scripts y dependencias del monorepo
commitlint.config.js	Estilo de commits (Conventional Commits)
pnpm-lock.yaml	Versión bloqueada de dependencias
LICENSE	Licencia del proyecto