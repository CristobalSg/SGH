# 📱 SGH - Aplicación Móvil

Este directorio contiene el código de la **aplicación móvil** del *Sistema de Gestión de Horario* (SGH), desarrollada con **Ionic + React + Capacitor** siguiendo principios de **Clean Architecture**.

---

## 🚀 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- [Node.js](https://nodejs.org/) (versión recomendada: LTS)
- [Ionic CLI](https://ionicframework.com/docs/cli)  
  ```bash
  npm install -g @ionic/cli
  ```
- [Capacitor](https://capacitorjs.com/) (se instala junto con Ionic)
- [Git](https://git-scm.com/)
- [Android Studio](https://developer.android.com/studio) (necesario para compilar y probar en Android)  
  > ⚠️ No olvides instalar el **Android SDK**, **SDK Platform Tools** y configurar las variables de entorno (`ANDROID_HOME`, `PATH`) para que Capacitor pueda usarlos.

---

## ⚙️ Instalación y ejecución

Entra en el directorio de la aplicación móvil y ejecuta:

Instala las dependencias:

```bash
npm install
```

Levanta el proyecto en modo desarrollo:

```bash
ionic serve
```

Compila para producción:

```bash
ionic build
```

Sincroniza con las plataformas nativas:

```bash
npx cap sync
```

Abrir en Android Studio o Xcode:

```bash
npx cap open android
npx cap open ios
```

---
## 🏗️ Estructura de carpetas (Clean Architecture)

La aplicación sigue un formato inspirado en **Clean Architecture** para mantener el código modular y escalable:

```
src/
│── config/         # Configuración general de la aplicación (env, constantes, settings)
│── core/           # Entidades, modelos y lógica central del dominio
│── infrastructure/ # Implementaciones concretas (servicios, repositorios, APIs)
│── presentation/   # Componentes de UI (React + Ionic), vistas y controladores de interfaz
```

### 📂 Descripción breve de cada capa:

- **config/** → Contiene la configuración global de la app (ej: variables de entorno, constantes, providers).  
- **core/** → Define los modelos, entidades y reglas principales del dominio, independiente de frameworks.  
- **infrastructure/** → Se encarga de conectar la app con APIs, base de datos u otros servicios externos.  
- **presentation/** → Maneja la capa visual de la aplicación (páginas, componentes, hooks y lógica de interfaz).  

--

## 📌 Estado actual
🔨 En construcción.  
Se irán añadiendo más dependencias, módulos y guías de uso.

---


