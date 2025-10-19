import { useCallback, useEffect, useMemo, useState } from "react";
import type { Events, SlotRef } from "../types/schedule";

const STORAGE_KEY = "eventsHorario";

const seed: Events = {
  lunes: { "08:00": ["Matemática"], "10:00": ["Física"] },
  martes: { "09:00": ["Química"], "11:00": ["Lenguaje"] },
};

export function useScheduleEvents() {
  const [events, setEvents] = useState<Events>({});
  const [selected, setSelected] = useState<SlotRef | null>(null);
  const [tipoUsuario] = useState<"profesor" | "alumno">("profesor");

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) setEvents(JSON.parse(stored));
    else {
      setEvents(seed);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
    }
  }, []);

  const persist = useCallback((updated: Events) => {
    setEvents(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }, []);

  const addEvent = useCallback((slot: SlotRef, text: string) => {
    const updated: Events = { ...events };
    if (!updated[slot.day]) updated[slot.day] = {};
    if (!updated[slot.day][slot.hour]) updated[slot.day][slot.hour] = [];
    updated[slot.day][slot.hour] = [...updated[slot.day][slot.hour], text];
    persist(updated);
  }, [events, persist]);

  const editEvent = useCallback((slot: SlotRef, idx: number, text: string) => {
    const updated: Events = { ...events };
    updated[slot.day][slot.hour] = [...(updated[slot.day][slot.hour] || [])];
    updated[slot.day][slot.hour][idx] = text;
    persist(updated);
  }, [events, persist]);

  const deleteEvent = useCallback((slot: SlotRef, idx: number) => {
    const updated: Events = { ...events };
    updated[slot.day][slot.hour] = [...(updated[slot.day][slot.hour] || [])];
    updated[slot.day][slot.hour].splice(idx, 1);
    if (updated[slot.day][slot.hour].length === 0) {
      delete updated[slot.day][slot.hour];
    }
    persist(updated);
  }, [events, persist]);

  const allEventsCount = useMemo(
    () => Object.values(events).flatMap(h => Object.values(h)).flat().length,
    [events]
  );

  return {
    events,
    selected, setSelected,
    tipoUsuario,
    addEvent, editEvent, deleteEvent,
    allEventsCount,
  };
}
