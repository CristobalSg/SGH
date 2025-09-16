# Contribuyendo al Proyecto

Gracias por colaborar 🙌. Para mantener un flujo de trabajo ordenado, seguimos las siguientes convenciones de **commits** y **ramas**.

---

## 🚀 Flujo de trabajo
1. Crear una rama a partir de `main` o `develop` con el formato:
   ```
   feat/nombre-tarea
   fix/nombre-tarea
   chore/nombre-tarea
   docs/nombre-tarea
   ```
   Ejemplos:
   - feat/consulta-clientes
   - fix/error-login
   - chore/update-dependencies

2. Realizar tus cambios en la rama correspondiente.

3. Hacer commits siguiendo la convención **Conventional Commits**.

4. Subir la rama y abrir un **Pull Request** hacia `develop` o `main`.

---

## 📝 Convención de Commits
Este repositorio usa [Conventional Commits](https://www.conventionalcommits.org/).  
El formato es:

```
<tipo>(opcional-alcance): descripción breve
```

### Tipos permitidos
- **feat:** Nueva funcionalidad.
- **fix:** Corrección de un error.
- **docs:** Cambios en documentación.
- **style:** Cambios de estilo (formato, punto y coma, espacios, etc).
- **refactor:** Refactorización de código sin cambiar funcionalidad.
- **test:** Agregar o modificar tests.
- **chore:** Tareas de mantenimiento, configuración, dependencias, etc.

### Ejemplos de commits válidos:
```
feat: agregar validación en login
fix(auth): corregir error de token expirado
docs: actualizar guía de instalación
chore: actualizar dependencias de seguridad
```

---

## ✅ Recomendaciones
- Usa **commits pequeños y descriptivos**.  
- Una rama debe resolver **una sola tarea o feature**.  
- Antes de subir tu PR, asegúrate que el proyecto **compila** y pasa los tests.

---

💡 **Nota**: Este repositorio usa **Husky + Commitlint**, por lo que los commits que no respeten el formato serán rechazados automáticamente.
