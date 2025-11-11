import { useState, useEffect, useCallback } from "react";
import { restrictionService } from "../../infrastructure/services/restrictionService";

export const useAllRestrictions = () => {
  const [restricciones, setRestricciones] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (opts: { limit?: number } = {}) => {
    setLoading(true);
    setError(null);
    try {
      const data = await restrictionService.listAll({ limit: opts.limit ?? 500 });
      setRestricciones(data);
    } catch (e: any) {
      setError(e?.message ?? "Error al cargar restricciones");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { restricciones, loading, error, refetch: load };
};