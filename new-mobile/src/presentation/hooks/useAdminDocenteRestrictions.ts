import { useCallback, useMemo, useState } from "react";
import { RestriccionHorarioRepositoryHttp } from "../../infrastructure/repositories/RestriccionHorarioRepositoryHttp";
import type { DayOfWeek } from "../../domain/restricciones/restriccionHorario";

export interface AdminRestrictionView {
  id: number;
  docenteId: number;
  day: DayOfWeek;
  start: string;
  end: string;
  disponible: boolean;
  descripcion?: string | null;
  activa: boolean;
}

const formatTime = (value: string) => (value ? value.slice(0, 5) : value);

const normalize = (item: AdminRestrictionView): AdminRestrictionView => ({
  ...item,
  start: formatTime(item.start),
  end: formatTime(item.end),
});

const sortByDayAndTime = (a: AdminRestrictionView, b: AdminRestrictionView) => {
  if (a.day !== b.day) return a.day - b.day;
  return a.start.localeCompare(b.start);
};

export function useAdminDocenteRestrictions() {
  const repo = useMemo(() => new RestriccionHorarioRepositoryHttp(), []);
  const [docenteId, setDocenteId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [restrictions, setRestrictions] = useState<AdminRestrictionView[]>([]);

  const clear = useCallback(() => {
    setDocenteId(null);
    setRestrictions([]);
    setError(null);
    setLoading(false);
  }, []);

  const fetchForDocente = useCallback(
    async (targetDocenteId: number | null) => {
      if (!targetDocenteId) {
        clear();
        return;
      }

      setLoading(true);
      setError(null);
      setDocenteId(targetDocenteId);

      try {
        const data = await repo.listByDocente(targetDocenteId);
        const normalized = data.map((item) =>
          normalize({
            id: item.id,
            docenteId: item.docente_id,
            day: item.dia_semana,
            start: item.hora_inicio,
            end: item.hora_fin,
            disponible: item.disponible,
            descripcion: item.descripcion,
            activa: item.activa,
          }),
        );
        setRestrictions(normalized.sort(sortByDayAndTime));
      } catch (err) {
        setError(err instanceof Error ? err.message : "No se pudieron cargar las restricciones.");
        setRestrictions([]);
      } finally {
        setLoading(false);
      }
    },
    [clear, repo],
  );

  const refetch = useCallback(() => {
    if (docenteId) {
      return fetchForDocente(docenteId);
    }
    return Promise.resolve();
  }, [docenteId, fetchForDocente]);

  return {
    docenteId,
    loading,
    error,
    restrictions,
    fetchForDocente,
    refetch,
    clear,
  };
}
