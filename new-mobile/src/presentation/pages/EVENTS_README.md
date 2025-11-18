# Eventos - Documentación de Integración

## Estructura de Archivos

### Domain Layer
- `domain/events/event.ts` - Entidades y DTOs de eventos
- `domain/repositories/EventRepository.ts` - Interfaz del repositorio

### Infrastructure Layer
- `infrastructure/repositories/EventRepositoryHttp.ts` - Implementación HTTP del repositorio

### Presentation Layer
- `presentation/hooks/useEvents.ts` - Hook personalizado para gestión de eventos
- `presentation/viewmodels/useEventsVM.ts` - ViewModel con lógica de UI
- `presentation/pages/EventsPage.tsx` - Página principal
- `presentation/components/Events/` - Componentes relacionados

## API Endpoint

### POST `/api/eventos/`
Crear un nuevo evento

**Request Body:**
```json
{
  "nombre": "Reunión de Profesores",
  "descripcion": "string (opcional)",
  "hora_inicio": "09:00:00",
  "hora_cierre": "11:00:00",
  "active": true,
  "user_id": 1
}
```

**Nota importante:** El backend espera formato de **tiempo solamente** (`HH:mm:ss`), **NO** datetime completo.

**Response:**
```json
{
  "id": 1,
  "nombre": "Reunión de Profesores",
  "descripcion": "string",
  "hora_inicio": "09:00:00",
  "hora_cierre": "11:00:00",
  "active": true,
  "user_id": 1,
  "created_at": "2025-11-18T10:00:00",
  "updated_at": "2025-11-18T10:00:00"
}
```

**Nota:** Los campos `hora_inicio` y `hora_cierre` son de tipo **time** (HH:mm:ss), no datetime.

### GET `/api/eventos/`
Obtener todos los eventos del usuario autenticado

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Reunión de Profesores",
    "descripcion": "string",
    "hora_inicio": "09:00:00",
    "hora_cierre": "11:00:00",
    "active": true,
    "user_id": 1,
    "created_at": "2025-11-18T10:00:00",
    "updated_at": "2025-11-18T10:00:00"
  }
]
```

**Nota:** Los eventos se agrupan por fecha usando el campo `created_at` ya que `hora_inicio` solo contiene la hora.

### PUT `/api/eventos/{id}`
Actualizar un evento

**Request Body:**
```json
{
  "nombre": "Reunión Actualizada",
  "descripcion": "Nueva descripción",
  "hora_inicio": "10:00:00",
  "hora_cierre": "12:00:00",
  "active": true
}
```

### DELETE `/api/eventos/{id}`
Eliminar un evento

**Response:** 204 No Content

## Flujo de Datos

1. **Carga inicial**: 
   - `useEvents()` se ejecuta al montar el componente
   - Llama a `eventRepository.getAll()`
   - Los eventos se guardan en el estado

2. **Visualización**:
   - `useEventsVM()` transforma los eventos de la API al formato de UI
   - Agrupa eventos por fecha en `eventsMap`
   - El calendario muestra badges con el número de eventos

3. **Crear evento**:
   - Usuario selecciona fecha en el calendario
   - Completa el formulario en el modal
   - `upsertEvent()` llama a `createEvent()`
   - La lista se actualiza automáticamente

4. **Editar evento**:
   - Click en botón editar de un evento
   - Se carga en el formulario
   - `upsertEvent()` llama a `updateEvent()`

5. **Eliminar evento**:
   - Click en botón eliminar
   - `removeEvent()` llama a `deleteEvent()`
   - Se elimina de la lista

## Permisos

- **Administradores**: Pueden crear eventos para cualquier docente
- **Docentes**: Solo pueden crear eventos para sí mismos
- Verificar la autenticación con el token Bearer

## Formato de Horas

- **Frontend**: Usa formato "HH:mm" para mostrar (ej: "09:00")
- **Backend**: Espera formato de **tiempo solamente** "HH:mm:ss" (ej: "09:00:00")
  - ❌ NO enviar: "2025-11-18T09:00:00" (datetime completo)
  - ✅ SÍ enviar: "09:00:00" (solo tiempo)
- La conversión se realiza automáticamente en `useEventsVM.upsertEvent()`
- Los eventos se asocian a fechas usando el campo `created_at` del backend

## Estado de Carga

El hook `useEvents` proporciona:
- `loading`: Boolean que indica si hay una operación en curso
- `error`: String con el mensaje de error (o null)
- Se muestran mensajes de éxito/error con Ant Design message

## Próximos Pasos

- [ ] Agregar filtros por rango de fechas
- [ ] Implementar vista de lista vs calendario
- [ ] Agregar notificaciones para eventos próximos
- [ ] Permitir eventos recurrentes
- [ ] Exportar eventos a calendario
