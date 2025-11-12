import { useEffect, useMemo, useState } from "react";
import { Alert, Spin, message, Input, Select } from "antd";
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

  // Ordenar usuarios alfabéticamente
  const sortedUsers = useMemo(
    () =>
      users
        .slice()
        .sort((a, b) => a.name.localeCompare(b.name, "es", { sensitivity: "base" })),
    [users]
  );

  // Aplicar búsqueda y filtro por tipo
  const filteredUsers = useMemo(() => {
    return sortedUsers.filter((user) => {
      const matchesRole =
        filterRole === "todos" || user.role?.toLowerCase() === filterRole;
      const matchesSearch =
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesRole && matchesSearch;
    });
  }, [sortedUsers, searchTerm, filterRole]);

  const handleSelectUser = (user: AdminUserView) => {
    setSelectedUserId(user.id);
  };

  return (
    <AppLayout title="Usuarios" showBottomNav>
      <div className="space-y-6 pb-6">
        {/* Filtros y búsqueda */}
        <div className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <h2 className="text-base font-semibold text-gray-900 mb-3">
            Filtros de búsqueda
          </h2>
          <div className="flex flex-col sm:flex-row gap-3">
            <Input
              placeholder="Buscar por nombre o correo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              allowClear
              className="sm:w-2/3"
            />
            <Select
              value={filterRole}
              onChange={setFilterRole}
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
            <div className="space-y-2">
              {filteredUsers.map((user) => (
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
