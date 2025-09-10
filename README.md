# SGH - Sistema de Gestión de Horario

Este repositorio corresponde al proyecto **SGH (Sistema de Gestión de Horario)**.  
El proyecto se organiza como un **monorepo**, con dos carpetas principales:

## 📂 Estructura del repositorio

/backend → Contendrá la lógica del servidor, API y conexión con la base de datos.
/mobile → Contendrá la aplicación móvil del sistema.


## 🚀 Instrucciones iniciales

1. **Clonar el repositorio:**
   ```bash
   git clone <URL-del-repo>
   cd SGH
2. **Navegar a la carpeta deseada:**
cd backend   # para trabajar en el backend
cd mobile    # para trabajar en la app móvil
<<<<<<< Updated upstream
=======
cd algorithm # para trabajar en la integración del algoritmo
```
## Compilación del algoritmo de generación de horarios
Para poder compilar el algoritmo es necesario tener instalados Qt 6.9.1 o superior, y compilador C++ compatible con C++17.
```bash
cd algorithm/fet-7.4.4
qmake fet.pro
make -j 16 # suele demorar unos 3 minutos, casi 4
```
### Configurar permisos para inicialización con Docker
```bash
# Dar permisos al script de inicio
chmod +x backend/fastapi/start.sh
```

### Levantar con Docker
```bash
# Iniciar todos los servicios (backend + frontend + base de datos)
docker-compose --env-file .env.development up -d

# Ver que todo esté funcionando
docker-compose --env-file .env.development ps
```

### Acceder al sistema
- **🌐 Aplicación web**: http://localhost:8100
- **🔧 API del backend**: http://localhost:8000  
- **📚 Documentación API**: http://localhost:8000/docs

## 🔄 Actualizar después de cambios en el código

### Si alguien del equipo hizo cambios:

1. **Obtener cambios:**
   ```bash
   git pull origin main
   ```

2. **Si solo cambió código** (archivos .py, .tsx, .css):
   ```bash
   # ✅ NO hacer nada - Los cambios se ven automáticamente
   ```

3. **Si cambió dependencias** (package.json, requirements.txt):
   ```bash
   # Reconstruir el servicio que cambió
   docker-compose --env-file .env.development build --no-cache mobile    # si cambió frontend
   docker-compose --env-file .env.development build --no-cache backend   # si cambió backend
   
   # Reiniciar servicios
   docker-compose --env-file .env.development up -d
   ```

## 📋 Comandos útiles

```bash
# Ver logs de todos los servicios
docker-compose --env-file .env.development logs -f

# Ver logs de un servicio específico
docker-compose --env-file .env.development logs backend
docker-compose --env-file .env.development logs mobile

# Parar todos los servicios
docker-compose --env-file .env.development down

# Reiniciar un servicio específico
docker-compose --env-file .env.development restart backend
```

## ⚙️ Archivo de configuración (.env.development)

El archivo `.env.development` debe contener todas las configuraciones necesarias en la carpeta raiz del proyecto.
>>>>>>> Stashed changes
