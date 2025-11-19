# 📘 Documentación del Proyecto SGH

Este directorio contiene la **documentación técnica completa** del proyecto **SGH (Sistema de Gestión de Horarios)**, incluyendo diagramas UML, arquitectura del sistema y documentación de seguridad.

---

## 📂 Estructura de la carpeta

### 🔒 Documentación de Seguridad

La carpeta **`security/`** contiene documentación exhaustiva sobre seguridad del sistema, alineada con **OWASP A04:2021 - Insecure Design**.

| Archivo | Descripción |
|---------|-------------|
| **[README.md](./security/README.md)** | Índice general y guía de uso de la documentación de seguridad |
| **[security-checklist.md](./security/security-checklist.md)** | Checklist completa de controles de seguridad (177 controles, 67% implementados) |
| **[threat-analysis.md](./security/threat-analysis.md)** | Análisis detallado de amenazas usando metodología STRIDE (20 amenazas identificadas) |
| **[threat-diagrams.md](./security/threat-diagrams.md)** | Diagramas visuales de arquitectura de seguridad, flujos de datos y superficie de ataque |
| **[mitigation-controls.md](./security/mitigation-controls.md)** | Controles de mitigación implementados y planificados (105 controles totales) |
| **[incident-response.md](./security/incident-response.md)** | Plan completo de respuesta a incidentes de seguridad con playbooks |

#### 🎯 Highlights de Seguridad

- ✅ **RBAC Granular**: Sistema de roles y permisos bien implementado
- ✅ **Autenticación JWT**: Tokens seguros con RS256
- ✅ **Validación Robusta**: Pydantic + Middlewares de sanitización
- ✅ **Protección contra Inyección**: ORM SQLAlchemy con prepared statements
- ✅ **Rate Limiting**: Protección contra ataques de fuerza bruta y DoS
- 🔄 **En desarrollo**: Token blacklist, auditoría completa, MFA
- ⏳ **Planificado**: WAF, DDoS protection, monitoring avanzado

---

## 📂 Diagramas y Arquitectura

### 🧩 Diagramas de casos de uso

Ubicados en la carpeta `Diagrama de casos de usos/`.
Representan las acciones principales que cada tipo de usuario puede realizar dentro del sistema.

| Archivo               | Descripción                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Administrador.png** | Muestra las funciones del administrador, como gestionar usuarios, aprobar restricciones y revisar horarios. |
| **Alumno.png**        | Representa las acciones disponibles para los alumnos, como consultar horarios o eventos.                    |
| **Profesor.png**      | Describe las operaciones del profesor, como agregar o modificar restricciones y visualizar sus horarios.    |

---

### 🧱 Diagramas de arquitectura y componentes

| Archivo                                      | Descripción                                                                                            |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Diagrama_de_arquitectura_de_software.png** | Presenta la estructura general del sistema, incluyendo las capas de backend, frontend y base de datos. |
| **Diagrama_de_componentes.jpeg**             | Ilustra los principales módulos del sistema (API, base de datos, interfaz móvil) y sus relaciones.     |

---

## 🛠️ Herramientas utilizadas

* **draw.io / diagrams.net** → Para crear los diagramas visuales.
* **UML 2.0** → Lenguaje estándar utilizado para la representación de los diagramas.

---

## 📎 Nota

Estos diagramas son parte de la documentación técnica del proyecto y deben mantenerse actualizados conforme evolucione la arquitectura o se agreguen nuevas funcionalidades.
