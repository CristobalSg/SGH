# ⚠️ LIMITACIÓN IMPORTANTE DEL BACKEND

## Problema Identificado

El backend de eventos **NO soporta un campo de fecha separado**. Solo acepta:
- `hora_inicio`: formato `HH:mm:ss`
- `hora_cierre`: formato `HH:mm:ss`

**NO acepta:**
- ❌ Datetime completo: `2025-11-21T10:00:00`
- ❌ Campo fecha separado: `fecha: "2025-11-21"`

## Impacto

Todos los eventos se crean con:
- **Fecha**: La fecha actual del servidor (cuando se crea)
- **Hora**: La hora especificada por el usuario

Esto significa que **NO ES POSIBLE** crear eventos para fechas futuras con esta versión del endpoint.

## Comportamiento Actual

### Lo que el usuario hace:
1. Selecciona en el calendario: **25 de noviembre 2025**
2. Crea evento para las 10:00 - 11:00
3. ✅ Envía al backend:
   ```json
   {
     "hora_inicio": "10:00:00",
     "hora_cierre": "11:00:00",
     "fecha": "2025-11-25"  ← El backend IGNORA este campo
   }
   ```

### Lo que realmente sucede:
- El evento se crea con `created_at` = **HOY** (18 de noviembre)
- El evento aparece en el calendario el día de **hoy**, no el día seleccionado
- El campo `fecha` es ignorado o causa un error

## Soluciones Posibles

### Opción 1: Actualizar el Backend (RECOMENDADO)

Modificar el modelo del backend para agregar un campo `fecha`:

```python
# Backend - Modelo Event
class Event(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    fecha = Column(Date)  # ← AGREGAR ESTE CAMPO
    hora_inicio = Column(Time)
    hora_cierre = Column(Time)
    active = Column(Boolean)
    user_id = Column(Integer)
```

**Ventajas:**
- ✅ Permite eventos en cualquier fecha
- ✅ Separación clara entre fecha y hora
- ✅ Facilita consultas por rango de fechas

### Opción 2: Usar created_at para filtrar (TEMPORAL)

Mantener el código actual y **filtrar localmente** los eventos:

```typescript
// Solo mostrar eventos creados hoy
const todayEvents = apiEvents.filter(event => 
  dayjs(event.created_at).isSame(dayjs(), 'day')
);
```

**Desventajas:**
- ❌ Solo sirve para eventos del día actual
- ❌ No permite planificación futura
- ❌ Experiencia de usuario confusa

### Opción 3: Cambiar hora_inicio a DateTime (ALTERNATIVA)

Modificar el backend para que `hora_inicio` y `hora_cierre` sean DateTime en lugar de Time:

```python
# Backend - Modelo Event
class Event(Base):
    hora_inicio = Column(DateTime)  # En lugar de Time
    hora_cierre = Column(DateTime)  # En lugar de Time
```

**Ventajas:**
- ✅ Incluye fecha y hora en un solo campo
- ✅ No requiere campo adicional

**Desventajas:**
- ⚠️ Requiere migración de base de datos
- ⚠️ Cambio más invasivo

## Recomendación

**Opción 1** es la mejor solución a largo plazo:

1. Agregar campo `fecha` al modelo del backend
2. Hacer migration de base de datos
3. Actualizar endpoint para aceptar:
   ```json
   {
     "nombre": "Reunión",
     "fecha": "2025-11-25",
     "hora_inicio": "10:00:00",
     "hora_cierre": "11:00:00"
   }
   ```

## Código del Backend Sugerido

```python
# models/event.py
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from datetime import date, time

class Event(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500), nullable=True)
    fecha = Column(Date, nullable=False)  # ← NUEVO CAMPO
    hora_inicio = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# schemas/event.py
from pydantic import BaseModel, Field, validator
from datetime import date, time

class EventCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    fecha: date  # ← NUEVO CAMPO
    hora_inicio: time
    hora_cierre: time
    active: bool = True
    user_id: int
    
    @validator('hora_inicio', 'hora_cierre')
    def validate_time_range(cls, v):
        if v.hour < 8 or v.hour >= 21:
            raise ValueError('Las horas deben estar entre 08:00 y 21:00')
        return v
    
    @validator('hora_cierre')
    def validate_end_after_start(cls, v, values):
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('La hora de cierre debe ser posterior a la hora de inicio')
        return v
```

## Estado Actual del Frontend

El frontend **YA ESTÁ PREPARADO** para enviar el campo `fecha`. Solo falta que el backend lo acepte.

### Payload actual del frontend:
```json
{
  "nombre": "Reunión",
  "descripcion": "Planificación",
  "hora_inicio": "10:00:00",
  "hora_cierre": "11:00:00",
  "fecha": "2025-11-25",  ← El frontend ya lo envía
  "active": true,
  "user_id": 1
}
```

## Próximos Pasos

1. ⚠️ **BACKEND**: Agregar campo `fecha` al modelo Event
2. ⚠️ **BACKEND**: Crear migration de base de datos
3. ⚠️ **BACKEND**: Actualizar validaciones para aceptar `fecha`
4. ✅ **FRONTEND**: Ya está listo, solo espera que el backend acepte `fecha`

## Workaround Temporal

Mientras se actualiza el backend, el frontend puede:

1. **Solo permitir eventos para HOY**:
   ```typescript
   // Bloquear selección de fechas futuras
   const disabledDate = (current: Dayjs) => {
     return current && !current.isSame(dayjs(), 'day');
   };
   ```

2. **Mostrar advertencia** al usuario:
   ```
   ⚠️ Nota: Los eventos solo se pueden crear para el día actual
       debido a limitaciones del servidor.
   ```

## Archivos Afectados

- ✅ Frontend listo: `presentation/viewmodels/useEventsVM.ts`
- ⚠️ Backend requiere actualización
