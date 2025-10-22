import { useCallback, useEffect, useMemo, useState } from "react";
import { UserRepositoryHttp } from "../../infrastructure/repositories/UserRepositoryHttp";
import type { UserSummary } from "../../domain/users/user";

export interface AdminUserView extends UserSummary {
  docenteId: number | null;
  department?: string | null;
}

const mergeUsersWithDocentes = (users: UserSummary[], docentes: { userId: number; id: number; department?: string | null }[]) => {
  const docenteByUserId = new Map<number, { id: number; department?: string | null }>(
    docentes.map((doc) => [doc.userId, { id: doc.id, department: doc.department ?? null }]),
  );

  return users.map<AdminUserView>((user) => {
    const docente = docenteByUserId.get(user.id);
    return {
      ...user,
      docenteId: docente?.id ?? null,
      department: docente?.department ?? null,
    };
  });
};

export function useAdminUsers() {
  const repo = useMemo(() => new UserRepositoryHttp(), []);
  const [users, setUsers] = useState<AdminUserView[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [userList, docenteList] = await Promise.all([
        repo.listUsers(),
        repo.listDocentes(),
      ]);
      setUsers(mergeUsersWithDocentes(userList, docenteList));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar los usuarios.");
      setUsers([]);
    } finally {
      setLoading(false);
    }
  }, [repo]);

  useEffect(() => {
    load();
  }, [load]);

  return {
    users,
    loading,
    error,
    refresh: load,
  };
}
