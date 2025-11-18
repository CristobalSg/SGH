import { useEffect, useMemo, useState } from "react";
import { Alert, Spin, Input, Select } from "antd";
import AppLayout from "../components/layout/AppLayout";
import { useAdminUsers, type AdminUserView } from "../hooks/useAdminUsers";
import AddUserModal from "../components/admin/AddUserModal";

const { Option } = Select;

const roleLabels: Record<string, string> = {
  docente: "Docente",
  estudiante: "Estudiante",
  admin: "Administrador",
};

// 🟢 Tarjeta de usuario
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

// 🟣 Página principal de administración de usuarios (solo usuarios)
export default function AdminUsersPage() {
  const { users, loading, error, refresh } = useAdminUsers();

  const [searchTerm, setSearchTerm] = useState("");
  const [filterRole, setFilterRole] = useState<string>("todos");
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [page, setPage] = useState(1);

  const PAGE_SIZE = 20;

  // Reset página cuando cambian filtros/búsqueda
  useEffect(() => {
    setPage(1);
  }, [searchTerm, filterRole]);

  // Ordenar usuarios alfabéticamente
  const sortedUsers = useMemo(
    () =>
      users
        .slice()
        .sort((a, b) => a.name.localeCompare(b.name, "es", { sensitivity: "base" })),
    [users]
  );

  // Aplicar búsqueda y filtro por rol
  const filteredUsers = useMemo(() => {
    return sortedUsers.filter((user) => {
      const matchesRole =
        filterRole === "todos" || user.role?.toLowerCase() === filterRole;
      const term = searchTerm.toLowerCase();
      const matchesSearch =
        user.name.toLowerCase().includes(term) ||
        user.email.toLowerCase().includes(term);
      return matchesRole && matchesSearch;
    });
  }, [sortedUsers, searchTerm, filterRole]);

  const totalPages = Math.max(1, Math.ceil(filteredUsers.length / PAGE_SIZE));

  // Datos paginados
  const paginatedUsers = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return filteredUsers.slice(start, start + PAGE_SIZE);
  }, [filteredUsers, page]);

  const handleSelectUser = (user: AdminUserView) => {
    setSelectedUserId(user.id);
  };

  const goToPage = (p: number) => {
    if (p < 1 || p > totalPages) return;
    setPage(p);
  };

  return (
    <AppLayout title="Usuarios" showBottomNav>
      <div className="space-y-6 pb-6">
        {/* Filtros y búsqueda */}
        <div className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <h2 className="mb-3 text-base font-semibold text-gray-900">Filtros de búsqueda</h2>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Input
              placeholder="Buscar por nombre o correo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              allowClear
              className="sm:w-2/3"
            />
            <Select
              value={filterRole}
              onChange={(v) => setFilterRole(v)}
              className="sm:w-1/3"
            >
              <Option value="todos">Todos</Option>
              <Option value="admin">Administrador</Option>
              <Option value="docente">Docente</Option>
              <Option value="estudiante">Estudiante</Option>
            </Select>
          </div>
        </div>

        {/* Listado de usuarios */}
        <div className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-base font-semibold text-gray-900">Listado</h2>
            <div className="flex gap-2">
              <button
                onClick={refresh}
                className="text-xs font-medium text-indigo-600 hover:text-indigo-700"
                type="button"
              >
                Actualizar
              </button>
              <button
                onClick={() => setShowAddModal(true)}
                className="text-xs font-medium text-green-600 hover:text-green-700"
                type="button"
              >
                Agregar usuario
              </button>
            </div>
          </div>

          <div className="mb-2 text-xs text-gray-500">
            {filteredUsers.length} usuario(s) · Página {page} de {totalPages}
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
          ) : filteredUsers.length === 0 ? (
            <div className="py-6 text-center text-sm text-gray-500">
              No se encontraron usuarios.
            </div>
          ) : (
            <>
              <div className="space-y-2">
                {paginatedUsers.map((user) => (
                  <UserRow
                    key={user.id}
                    user={user}
                    selected={selectedUserId === user.id}
                    onSelect={handleSelectUser}
                  />
                ))}
              </div>

              {/* Paginación */}
              <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
                <button
                  type="button"
                  onClick={() => goToPage(page - 1)}
                  disabled={page === 1}
                  className="rounded-md border border-gray-300 bg-white px-3 py-1 text-xs font-medium text-gray-700 disabled:cursor-not-allowed disabled:opacity-40 hover:bg-gray-50"
                >
                  ← Anterior
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter((p) => {
                    // Mostrar primeras, últimas y ventana alrededor de la actual
                    const window = 2;
                    if (p === 1 || p === totalPages) return true;
                    if (Math.abs(p - page) <= window) return true;
                    return false;
                  })
                  .map((p, idx, arr) => {
                    // Insertar puntos suspensivos donde se salta rango
                    const prev = arr[idx - 1];
                    if (prev && p - prev > 1) {
                      return (
                        <span
                          key={`gap-${prev}-${p}`}
                          className="px-2 text-xs text-gray-400 select-none"
                        >
                          …
                        </span>
                      );
                    }
                    return (
                      <button
                        key={p}
                        type="button"
                        onClick={() => goToPage(p)}
                        className={[
                          "rounded-md px-3 py-1 text-xs font-medium transition",
                          p === page
                            ? "bg-indigo-600 text-white shadow-sm"
                            : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50",
                        ].join(" ")}
                      >
                        {p}
                      </button>
                    );
                  })}
                <button
                  type="button"
                  onClick={() => goToPage(page + 1)}
                  disabled={page === totalPages}
                  className="rounded-md border border-gray-300 bg-white px-3 py-1 text-xs font-medium text-gray-700 disabled:cursor-not-allowed disabled:opacity-40 hover:bg-gray-50"
                >
                  Siguiente →
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Modal para agregar usuario */}
      <AddUserModal
        visible={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSuccess={refresh}
      />
    </AppLayout>
  );
}
