// src/presentation/viewmodels/useEventsVM.ts
import { useMemo, useState } from "react";
import dayjs, { Dayjs } from "dayjs";
import { useEvents } from "../hooks/useEvents";

export type EventItem = {
  id: string;
  title: string;
  description?: string;
  time?: string; // 'HH:mm'
  startTime?: string; // 'HH:mm:ss'
  endTime?: string; // 'HH:mm:ss'
  apiId?: number; // ID del backend
  active?: boolean;
};
export type EventsMap = Record<string, EventItem[]>;

export function useEventsVM() {
  const [selectedDate, setSelectedDate] = useState<Dayjs | null>(dayjs());
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const { events: apiEvents, loading, createEvent, updateEvent, deleteEvent } = useEvents();

  const dateKey = useMemo(
    () => (selectedDate ? selectedDate.format("YYYY-MM-DD") : ""),
    [selectedDate]
  );

  // Convertir eventos de la API al formato del UI
  const eventsMap: EventsMap = useMemo(() => {
    const map: EventsMap = {};
    apiEvents.forEach((event) => {
      // Si hora_inicio es solo tiempo (HH:mm:ss), usar la fecha de hoy o created_at
      let eventDate: string;
      let eventTime: string;
      
      // Intentar parsear como datetime completo primero
      if (event.hora_inicio.includes('T') || event.hora_inicio.includes(' ')) {
        const parsedDate = dayjs(event.hora_inicio);
        eventDate = parsedDate.format("YYYY-MM-DD");
        eventTime = parsedDate.format("HH:mm");
      } else {
        // Es solo tiempo (HH:mm:ss)
        // Usar created_at si está disponible, sino usar fecha de hoy
        eventDate = event.created_at 
          ? dayjs(event.created_at).format("YYYY-MM-DD")
          : dayjs().format("YYYY-MM-DD");
        eventTime = event.hora_inicio.substring(0, 5); // "09:00:00" -> "09:00"
      }
      
      const item: EventItem = {
        id: `api-${event.id}`,
        apiId: event.id,
        title: event.nombre,
        description: event.descripcion,
        time: eventTime,
        startTime: event.hora_inicio,
        endTime: event.hora_cierre,
        active: event.active,
      };
      if (!map[eventDate]) map[eventDate] = [];
      map[eventDate].push(item);
    });
    
    // Ordenar eventos por hora
    Object.keys(map).forEach((date) => {
      map[date].sort((a, b) => (a.time ?? "99:99").localeCompare(b.time ?? "99:99"));
    });
    
    return map;
  }, [apiEvents]);

  const eventsForSelected: EventItem[] = useMemo(
    () => (dateKey && eventsMap[dateKey] ? eventsMap[dateKey] : []),
    [dateKey, eventsMap]
  );

  // Navegación/selección
  const openForDate = (value: Dayjs) => {
    setSelectedDate(value);
    setIsModalOpen(true);
    setEditingId(null);
  };

  // Crear/Actualizar
  const upsertEvent = async (payload: Omit<EventItem, "id"> & { 
    id?: string;
    startTime?: string;
    endTime?: string;
  }) => {
    const title = payload.title.trim();
    if (!title) return;

    // Obtener la fecha seleccionada para el campo fecha (si el backend lo soporta)
    const selectedDateStr = selectedDate ? selectedDate.format("YYYY-MM-DD") : dayjs().format("YYYY-MM-DD");
    
    // El backend solo acepta tiempo en formato HH:mm:ss
    const startTimeStr = payload.startTime || "09:00";
    const endTimeStr = payload.endTime || "10:00";
    
    const startTime = startTimeStr + ":00"; // "09:00" -> "09:00:00"
    const endTime = endTimeStr + ":00"; // "10:00" -> "10:00:00"

    // Si es edición
    if (payload.id) {
      const existing = eventsForSelected.find((e) => e.id === payload.id);
      if (existing?.apiId) {
        await updateEvent(existing.apiId, {
          nombre: title,
          descripcion: payload.description?.trim(),
          hora_inicio: startTime,
          hora_cierre: endTime,
          fecha: selectedDateStr, // Intentar enviar fecha separada
        });
      }
    } else {
      // Crear nuevo
      await createEvent({
        nombre: title,
        descripcion: payload.description?.trim(),
        hora_inicio: startTime,
        hora_cierre: endTime,
        fecha: selectedDateStr, // Intentar enviar fecha separada
      });
    }
    
    setEditingId(null);
  };

  const beginEdit = (item: EventItem) => setEditingId(item.id);

  const removeEvent = async (id: string) => {
    const item = eventsForSelected.find((e) => e.id === id);
    if (item?.apiId) {
      await deleteEvent(item.apiId);
    }
    if (editingId === id) setEditingId(null);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingId(null);
  };

  return {
    // estado
    selectedDate,
    isModalOpen,
    eventsForSelected,
    eventsMap,
    editingId,
    dateKey,
    loading,
    // acciones
    openForDate,
    upsertEvent,
    beginEdit,
    removeEvent,
    closeModal,
    setSelectedDate,
  };
}
