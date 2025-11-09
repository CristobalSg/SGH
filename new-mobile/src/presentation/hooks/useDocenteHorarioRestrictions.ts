import { useCallback, useEffect, useMemo, useState } from "react";
import { RestriccionHorarioRepositoryHttp } from "../../infrastructure/repositories/RestriccionHorarioRepositoryHttp";
import type { DayOfWeek, RestriccionHorario } from "../../domain/restricciones/restriccionHorario";

export interface RestriccionHorarioView {
  id: number;
  docenteId: number;
  day: DayOfWeek;
  start: string;
  end: string;
  disponible: boolean;
  descripcion?: string | null;
  activa: boolean;
}

export interface RestriccionHorarioCreateInput {
  dia_semana: DayOfWeek;
  hora_inicio: string;
  hora_fin: string;
  disponible: boolean;
  descripcion?: string | null;
}

const formatTime = (value: string) => {
  if (!value) return value;
  // El backend suele devolver HH:mm:ss; mostramos HH:mm
  return value.slice(0, 5);
};

const normalizeView = (item: RestriccionHorario): RestriccionHorarioView => ({
  id: item.id,
  docenteId: item.docente_id,
  day: item.dia_semana,
  start: formatTime(item.hora_inicio),
  end: formatTime(item.hora_fin),
  disponible: item.disponible,
  descripcion: item.descripcion,
  activa: item.activa,
});

const sortByDayAndTime = (a: RestriccionHorarioView, b: RestriccionHorarioView) => {
  if (a.day !== b.day) return a.day - b.day;
  return a.start.localeCompare(b.start);
};

export function useDocenteHorarioRestrictions() {
  const repo = useMemo(() => new RestriccionHorarioRepositoryHttp(), []);
  const [docenteId, setDocenteId] = useState<number | null>(null);
  const [restricciones, setRestricciones] = useState<RestriccionHorarioView[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [pendingDelete, setPendingDelete] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const docente = await repo.getMyDocenteId();
      setDocenteId(docente);
      const data = await repo.listMine();
      setRestricciones(data.map(normalizeView).sort(sortByDayAndTime));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar las restricciones.");
      setRestricciones([]);
    } finally {
      setLoading(false);
    }
  }, [repo]);

  useEffect(() => {
    load();
  }, [load]);

  const addRestriction = useCallback(async (payload: RestriccionHorarioCreateInput) => {
    if (!docenteId) throw new Error("No se pudo determinar el docente asociado.");
    setSaving(true);
    setError(null);
    try {
      const created = await repo.createMine({
        docente_id: docenteId,
        ...payload,
      });
      setRestricciones((prev) => [...prev, normalizeView(created)].sort(sortByDayAndTime));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar la restricción.");
      throw err;
    } finally {
      setSaving(false);
    }
  }, [docenteId, repo]);

  const updateRestriction = useCallback(async (id: number, payload: RestriccionHorarioCreateInput) => {
    if (!docenteId) throw new Error("No se pudo determinar el docente asociado.");
    setSaving(true);
    setError(null);
    try {
      const updated = await repo.updateMine(id, {
        docente_id: docenteId,
        ...payload,
      });
      setRestricciones((prev) =>
        prev
          .map((item) => (item.id === id ? normalizeView(updated) : item))
          .sort(sortByDayAndTime),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo actualizar la restricción.");
      throw err;
    } finally {
      setSaving(false);
    }
  }, [docenteId, repo]);

  const deleteRestriction = useCallback(async (id: number) => {
    setPendingDelete(id);
    setError(null);
    try {
      await repo.deleteMine(id);
      setRestricciones((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo eliminar la restricción.");
      throw err;
    } finally {
      setPendingDelete(null);
    }
  }, [repo]);

  return {
    restricciones,
    loading,
    saving,
    pendingDelete,
    error,
    refetch: load,
    addRestriction,
    updateRestriction,
    deleteRestriction,
  };
}
