# 🔧 Corrección: Fecha del Evento

## Problema Identificado

Los eventos se estaban creando con la **fecha de hoy** en lugar de la **fecha seleccionada** en el calendario.

### Comportamiento Anterior (Incorrecto)

```
Usuario selecciona: 25 de noviembre 2025
Sistema crea evento: 18 de noviembre 2025 (hoy) ❌
```

## Solución Implementada

### Cambio en `useEventsVM.ts`

**Antes:**
```typescript
// Solo enviaba la hora
const startTime = startTimeStr + ":00";  // "09:00:00"
const endTime = endTimeStr + ":00";      // "10:00:00"

await createEvent({
  hora_inicio: startTime,  // Solo hora
  hora_cierre: endTime,    // Solo hora
});
```

**Ahora:**
```typescript
// Combina la fecha seleccionada con la hora
const selectedDateStr = selectedDate 
  ? selectedDate.format("YYYY-MM-DD") 
  : dayjs().format("YYYY-MM-DD");

const startDateTime = `${selectedDateStr}T${startTimeStr}:00`;
const endDateTime = `${selectedDateStr}T${endTimeStr}:00`;

await createEvent({
  hora_inicio: startDateTime,  // "2025-11-25T09:00:00"
  hora_cierre: endDateTime,    // "2025-11-25T10:00:00"
});
```

## Flujo Completo

### 1. Usuario Selecciona Fecha en Calendario
```
📅 Click en: 25 de noviembre 2025
```

### 2. Se Abre el Modal
```
Título: [          ]
Hora Inicio: [09:00]
Hora Fin: [10:00]
```

### 3. Sistema Combina Fecha + Hora
```typescript
selectedDate = "2025-11-25"
startTime = "09:00"
endTime = "10:00"

// Construcción del datetime
startDateTime = "2025-11-25" + "T" + "09:00" + ":00"
              = "2025-11-25T09:00:00"

endDateTime = "2025-11-25" + "T" + "10:00" + ":00"
            = "2025-11-25T10:00:00"
```

### 4. Petición al Backend
```json
POST /api/eventos/

{
  "nombre": "Reunión de Equipo",
  "descripcion": "Planificación semanal",
  "hora_inicio": "2025-11-25T09:00:00",  ← Fecha correcta
  "hora_cierre": "2025-11-25T10:00:00",  ← Fecha correcta
  "active": true,
  "user_id": 1
}
```

### 5. Evento Creado
```
✅ Evento guardado para: 25 de noviembre 2025
✅ Hora: 09:00 - 10:00
```

## Casos de Uso

### Caso 1: Evento para Hoy
```
Usuario selecciona: 18 de noviembre (hoy)
Hora: 14:00 - 15:00
Resultado: "2025-11-18T14:00:00" ✅
```

### Caso 2: Evento para el Futuro
```
Usuario selecciona: 30 de noviembre
Hora: 10:00 - 11:30
Resultado: "2025-11-30T10:00:00" ✅
```

### Caso 3: Evento para Mañana
```
Usuario selecciona: 19 de noviembre
Hora: 08:00 - 09:00
Resultado: "2025-11-19T08:00:00" ✅
```

## Visualización en el Calendario

Ahora los eventos aparecen en el **día correcto**:

```
Noviembre 2025

Lun  Mar  Mié  Jue  Vie  Sáb  Dom
                    18   19   20
                    (1)       (2)  ← Badge muestra cantidad
21   22   23   24   25   26   27
               (3)  (1)
```

- **18**: Evento de hoy
- **20**: 2 eventos programados
- **24**: 3 eventos programados
- **25**: 1 evento programado

## Formato de Datetime

El sistema ahora usa el estándar **ISO 8601**:

```
YYYY-MM-DDTHH:mm:ss
│    │  │ │  │  │
│    │  │ │  │  └─ Segundos (siempre :00)
│    │  │ │  └──── Minutos
│    │  │ └─────── Horas (08-21)
│    │  └──────── Separador de fecha/hora
│    └─────────── Día del mes
└──────────────── Año-Mes

Ejemplo: 2025-11-25T09:00:00
```

## Validación

El sistema valida que:
- ✅ La fecha seleccionada se usa correctamente
- ✅ La hora está en rango (08:00-21:00)
- ✅ La hora de fin > hora de inicio
- ✅ El formato datetime es correcto

## Archivos Modificados

- ✅ `presentation/viewmodels/useEventsVM.ts`
- ✅ `domain/events/event.ts`
- ✅ Documentación actualizada

## Prueba

1. Abre el calendario
2. Selecciona el **25 de noviembre**
3. Crea evento con hora 09:00 - 10:00
4. Verifica en la consola del navegador:
   ```json
   {
     "hora_inicio": "2025-11-25T09:00:00",
     "hora_cierre": "2025-11-25T10:00:00"
   }
   ```
5. ✅ El evento debe aparecer el día 25, no hoy

## Estado

🟢 **RESUELTO** - Los eventos ahora se crean en la fecha seleccionada por el usuario.
