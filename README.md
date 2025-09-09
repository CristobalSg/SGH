# SGH - Sistema de Gestión de Horario

Este repositorio corresponde al proyecto **SGH (Sistema de Gestión de Horario)**.  
El proyecto se organiza como un **monorepo**, con dos carpetas principales:

## 📂 Estructura del repositorio

/backend   → Contendrá la lógica del servidor, API y conexión con la base de datos.
/mobile    → Contendrá la aplicación móvil del sistema.
/algorithm → Contendrá el código fuente de la aplicación FET, que se encarga de generar los horarios.


## 🚀 Instrucciones iniciales

1. **Clonar el repositorio:**
Por HTTP:
```bash
git clone https://github.com/CristobalSg/SGH.git
```

Por SSH:
```bash
git clone git@github.com:CristobalSg/SGH.git
```
2. **Navegar a la carpeta deseada:**
```bash
cd backend   # para trabajar en el backend
cd mobile    # para trabajar en la app móvil
cd algorithm # para trabajar en la integración del algoritmo
```
## Compilación del algoritmo de generación de horarios
Para poder compilar el algoritmo es necesario tener instalados Qt 6.9.1 o superior, y compilador C++ compatible con C++17.
```bash
cd algorithm/fet-7.4.4
qmake fet.pro
make -j 16 # suele demorar unos 3 minutos, casi 4
```
