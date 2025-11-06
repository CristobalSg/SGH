import { useEffect, useMemo, useState } from "react";
import { Alert, Empty, Spin, Tag } from "antd";
import AppLayout from "../components/layout/AppLayout";
import { useAdminUsers, type AdminUserView } from "../hooks/useAdminUsers";
import {
  useAdminDocenteRestrictions,
  type AdminRestrictionView,
} from "../hooks/useAdminDocenteRestrictions";

const dayLabels = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

const roleLabels: Record<string, string> = {
  docente: "Docente",
  estudiante: "Estudiante",
  admin: "Administrador",
};

const RestrictionCard = ({ restriction }: { restriction: AdminRestrictionView }) => (
  <div className="rounded-2xl border border-gray-100 bg-white px-4 py-3 shadow-sm">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p className="text-sm font-semibold text-gray-900">
          {dayLabels[restriction.day]} · {restriction.start} - {restriction.end}
        </p>
        {restriction.descripcion && (
          <p className="text-xs text-gray-500">{restriction.descripcion}</p>
        )}
      </div>
      <div className="flex items-center gap-2">
        <Tag color={restriction.disponible ? "green" : "red"} className="text-xs">
          {restriction.disponible ? "Disponible" : "No disponible"}
        </Tag>
        {!restriction.activa && <Tag color="orange" className="text-xs">Inactiva</Tag>}
      </div>
    </div>
  </div>
);

const UserRow = ({
  user,
  selected,
  onSelect,
}: {
  user: AdminUserView;
  selected: boolean;
  onSelect: (user: AdminUserView) => void;
}) => {
  const roleLabel = roleLabels[user.role] ?? user.role;

  return (
    <button
      type="button"
      onClick={() => onSelect(user)}
      className={[
        "w-full rounded-2xl border px-4 py-3 text-left transition",
        selected
          ? "border-indigo-500 bg-indigo-50 shadow-sm"
          : "border-gray-100 bg-white hover:border-indigo-200 hover:bg-indigo-50/60",
      ].join(" ")}
    >
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="text-sm font-semibold text-gray-900">{user.name}</p>
          <p className="text-xs text-gray-500">{user.email}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className="text-xs font-medium text-indigo-600">{roleLabel}</span>
          {user.docenteId && (
            <span className="text-[11px] text-gray-500">
              ID Docente: {user.docenteId}
              {user.department ? ` · ${user.department}` : ""}
            </span>
          )}
        </div>
      </div>
    </button>
  );
};

const RestrictionPanel = ({
  selectedUser,
  restrictions,
  loading,
  error,
  onRetry,
}: {
  selectedUser: AdminUserView | null;
  restrictions: AdminRestrictionView[];
  loading: boolean;
  error: string | null;
  onRetry: () => void | Promise<void>;
}) => {
  if (!selectedUser) {
    return (
      <div className="rounded-3xl border border-dashed border-gray-200 bg-white p-6 text-center text-sm text-gray-500">
        Selecciona un usuario para revisar sus restricciones.
      </div>
    );
  }

  if (selectedUser.role !== "docente" || !selectedUser.docenteId) {
    return (
      <div className="rounded-3xl border border-dashed border-gray-200 bg-white p-6 text-center text-sm text-gray-500">
        Este usuario no está asociado a un docente, por lo que no tiene restricciones horarias.
      </div>
    );
  }

  if (loading) {
    return (
      <div className="py-10 text-center">
        <Spin />
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        type="error"
        message="No se pudieron cargar las restricciones"
        description={error}
        showIcon
        action={
          <button
            onClick={onRetry}
            className="text-sm font-medium text-indigo-600 hover:text-indigo-700"
          >
            Reintentar
          </button>
        }
      />
    );
  }

  if (restrictions.length === 0) {
    return (
      <div className="rounded-3xl border border-gray-100 bg-white py-10 text-center">
        <Empty description="Sin restricciones registradas" />
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {restrictions.map((item) => (
        <RestrictionCard key={item.id} restriction={item} />
      ))}
    </div>
  );
};

export default function AdminUsersPage() {
  const { users, loading, error, refresh } = useAdminUsers();
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const {
    restrictions,
    loading: restrictionsLoading,
    error: restrictionsError,
    fetchForDocente,
    refetch: refetchRestrictions,
    clear,
  } = useAdminDocenteRestrictions();

  const sortedUsers = useMemo(
    () =>
      users
        .slice()
        .sort((a, b) => a.name.localeCompare(b.name, "es", { sensitivity: "base" })),
    [users],
  );

  const selectedUser = useMemo(
    () => (selectedUserId ? sortedUsers.find((u) => u.id === selectedUserId) ?? null : null),
    [sortedUsers, selectedUserId],
  );

  useEffect(() => {
    if (sortedUsers.length === 0) {
      setSelectedUserId(null);
      return;
    }

    if (!selectedUserId) {
      setSelectedUserId(sortedUsers[0].id);
    } else {
      const stillExists = sortedUsers.some((user) => user.id === selectedUserId);
      if (!stillExists) {
        setSelectedUserId(sortedUsers[0].id);
      }
    }
  }, [sortedUsers, selectedUserId]);

  useEffect(() => {
    if (!selectedUser) {
      clear();
      return;
    }

    if (selectedUser.docenteId) {
      fetchForDocente(selectedUser.docenteId);
    } else {
      clear();
    }
  }, [selectedUser, fetchForDocente, clear]);

  const handleSelectUser = (user: AdminUserView) => {
    setSelectedUserId(user.id);
  };

  return (
    <AppLayout title="Usuarios" showBottomNav>
      <div className="space-y-6 pb-6">
        <div className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-base font-semibold text-gray-900">Listado</h2>
            <button
              onClick={refresh}
              className="text-xs font-medium text-indigo-600 hover:text-indigo-700"
              type="button"
            >
              Actualizar
            </button>
          </div>

          {error && (
            <Alert
              type="error"
              message="No se pudieron cargar los usuarios"
              description={error}
              showIcon
              className="mb-3"
              action={
                <button
                  onClick={refresh}
                  className="text-sm font-medium text-indigo-600 hover:text-indigo-700"
                >
                  Reintentar
                </button>
              }
            />
          )}

          {loading ? (
            <div className="py-10 text-center">
              <Spin />
            </div>
          ) : sortedUsers.length === 0 ? (
            <div className="py-6 text-center text-sm text-gray-500">
              No hay usuarios registrados.
            </div>
          ) : (
            <div className="space-y-2">
              {sortedUsers.map((user) => (
                <UserRow
                  key={user.id}
                  user={user}
                  selected={selectedUserId === user.id}
                  onSelect={handleSelectUser}
                />
              ))}
            </div>
          )}
        </div>

        <div className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <div>
              <h2 className="text-base font-semibold text-gray-900">Restricciones</h2>
              {selectedUser && (
                <p className="text-xs text-gray-500">
                  {selectedUser.name} · {selectedUser.email}
                </p>
              )}
            </div>
            {selectedUser?.docenteId && (
              <button
                onClick={refetchRestrictions}
                className="text-xs font-medium text-indigo-600 hover:text-indigo-700"
                type="button"
              >
                Recargar
              </button>
            )}
          </div>

          <RestrictionPanel
            selectedUser={selectedUser}
            restrictions={restrictions}
            loading={restrictionsLoading}
            error={restrictionsError}
            onRetry={refetchRestrictions}
          />
        </div>
      </div>
    </AppLayout>
  );
}
