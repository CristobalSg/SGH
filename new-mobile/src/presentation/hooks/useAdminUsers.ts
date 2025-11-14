import { useCallback, useEffect, useState } from "react";
import {
  UserRepositoryHttp,
  type AdminUserView as RepoAdminUserView,
  type AdminUserUpdateInput,
} from "../../infrastructure/repositories/UserRepositoryHttp";

// Tipo expuesto a la UI
export type AdminUserView = RepoAdminUserView;

export function useAdminUsers() {
  const repo = new UserRepositoryHttp();
  const [users, setUsers] = useState<AdminUserView[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await repo.list();
      setUsers(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || "Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const updateUser = useCallback(async (id: number, data: AdminUserUpdateInput) => {
    try {
      await repo.update(id, data);
    } catch (e: any) {
      throw new Error(e?.response?.data?.detail || e?.message || "No se pudo actualizar el usuario");
    }
  }, []);

  const deleteUser = useCallback(async (id: number) => {
    try {
      await repo.delete(id);
    } catch (e: any) {
      throw new Error(e?.response?.data?.detail || e?.message || "No se pudo eliminar el usuario");
    }
  }, []);

  return { users, loading, error, refresh, updateUser, deleteUser };
}
