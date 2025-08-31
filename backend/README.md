
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
- PostgreSQL (cuando esté lista la base de datos)
- Entorno virtual (`venv`)

## ⚙️ Instalación
Clonar el repo y levantar entorno:

```bash
# Crear entorno virtual
python3 -m venv env
source env/bin/activate

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

#runnear la API
uvicorn main:app --reload --port 8000
