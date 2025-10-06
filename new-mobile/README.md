# SGH — Frontend Base

Este proyecto corresponde a la **nueva base frontend de SGH**, desarrollada con una arquitectura limpia, moderna y optimizada para escalar en entornos web y móviles.  
Su objetivo es reemplazar gradualmente la versión anterior del front, unificando la experiencia y preparando el sistema para su futura integración con **Capacitor** como aplicación móvil.

---

## 🚀 Tecnologías principales

- ⚡ **Vite** — Herramienta de desarrollo rápida y modular.  
- ⚛️ **React 19 + TypeScript** — Interfaz declarativa y tipada.  
- 🎨 **Tailwind CSS** — Estilos utilitarios para un diseño limpio y mantenible.  
- 🔤 **Heroicons** — Iconos optimizados y personalizables para React.  
- 🧱 **Arquitectura limpia** — Separación de capas de dominio, aplicación y presentación.  

> 🧩 *Ionic ha sido descartado temporalmente debido a conflictos con TailwindCSS.*

---

## 🧠 Estructura general (propuesta)

```
src/
 ├─ components/      # Componentes reutilizables (UI)
 ├─ App.tsx
 ├─ Index.css        # All configuración de tailwind (temas)
 └─ main.tsx         # Punto de entrada de la aplicación
```

---

## 🧩 Scripts disponibles

```bash
pnpm run dev        # Inicia el entorno de desarrollo
pnpm run build      # Genera la build optimizada para producción
pnpm run lint       # Ejecuta el análisis estático de código
pnpm run preview    # Visualiza la build localmente
```

---

## 🌐 Despliegue

El proyecto está preparado para ser desplegado en **Vercel**, aprovechando la compatibilidad nativa con aplicaciones basadas en Vite.

---

## 📱 Futuro del proyecto

- Integración con **Capacitor** para la creación de la versión móvil.  
- Inclusión progresiva de módulos desde el frontend anterior.  
- Mejora continua bajo principios de **arquitectura limpia** y **responsividad total**.  

---

## 🧭 Convenciones

- Uso de `pnpm` como gestor de paquetes.  
- Nombres de ramas siguiendo el formato:
  ```
  feature/<nombre>
  fix/<nombre>
  refactor/<nombre>
  ```
- Estilo de commits tipo *Conventional Commits*, por ejemplo:
  ```
  feat: add new login layout
  fix: resolve Tailwind class conflict
  ```

---

## 📄 Licencia

Este proyecto forma parte del sistema **SGH**.  
Todos los derechos reservados © 2025.
