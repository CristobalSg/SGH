// src/presentation/viewmodels/useEventsVM.ts
import { useMemo, useState } from "react";
import dayjs, { Dayjs } from "dayjs";

export type EventItem = {
  id: string;
  title: string;
  description?: string;
  time?: string; // 'HH:mm'
};
export type EventsMap = Record<string, EventItem[]>;

export function useEventsVM() {
  const [selectedDate, setSelectedDate] = useState<Dayjs | null>(dayjs());
  const [eventsMap, setEventsMap] = useState<EventsMap>({});
  const [editingId, setEditingId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const dateKey = useMemo(
    () => (selectedDate ? selectedDate.format("YYYY-MM-DD") : ""),
    [selectedDate]
  );

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
  const upsertEvent = (payload: Omit<EventItem, "id"> & { id?: string }) => {
    const id = payload.id ?? `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const newItem: EventItem = { id, title: payload.title.trim(), description: payload.description?.trim(), time: payload.time };
    setEventsMap((prev) => {
      const current = prev[dateKey] ?? [];
      const exists = current.some((e) => e.id === id);
      const next = exists ? current.map((e) => (e.id === id ? newItem : e)) : [...current, newItem];
      next.sort((a, b) => (a.time ?? "99:99").localeCompare(b.time ?? "99:99"));
      return { ...prev, [dateKey]: next };
    });
    setEditingId(null);
  };

  const beginEdit = (item: EventItem) => setEditingId(item.id);

  const removeEvent = (id: string) => {
    setEventsMap((prev) => {
      const list = prev[dateKey] ?? [];
      const next = list.filter((e) => e.id !== id);
      const copy = { ...prev };
      if (next.length === 0) delete copy[dateKey];
      else copy[dateKey] = next;
      return copy;
    });
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
    editingId,
    dateKey,
    // acciones
    openForDate,
    upsertEvent,
    beginEdit,
    removeEvent,
    closeModal,
    setSelectedDate,
  };
}
