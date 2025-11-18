import { http } from "../http/httpClient";
import type { UserRepository } from "../../domain/repositories/UserRepository";
import type { DocenteSummary, UserSummary } from "../../domain/users/user";
import { normalizeRole } from "../../domain/auth/roleUtils";

type ApiUser = {
  id: number;
  nombre: string;
  name?: string;
  email: string;
  rol: string;
  activo: boolean;
  created_at?: string;
  updated_at?: string;
};

type ApiDocente = {
  id: number;
  user_id: number;
  departamento?: string | null;
  user?: {
    id: number;
    nombre: string;
    email: string;
    rol: string;
  };
};

const normalizeUser = (item: ApiUser): UserSummary => ({
  id: item.id,
  name: item.nombre ?? item.name ?? "",
  email: item.email,
  role: normalizeRole(item.rol),
  active: item.activo,
  createdAt: item.created_at,
  updatedAt: item.updated_at,
});

const normalizeDocente = (item: ApiDocente): DocenteSummary => ({
  id: item.id,
  userId: item.user_id,
  department: item.departamento ?? null,
});

export class UserRepositoryHttp implements UserRepository {
  // 🔹 Obtener todos los usuarios
  async listUsers(): Promise<UserSummary[]> {
    const { data } = await http.get<ApiUser[]>("/users/", { params: { limit: 500 } });
    return data.map(normalizeUser);
  }

  // 🔹 Obtener todos los docentes
  async listDocentes(): Promise<DocenteSummary[]> {
    const { data } = await http.get<ApiDocente[]>("/docentes/", { params: { limit: 500 } });
    return data.map(normalizeDocente);
  }

  // 🔹 Registrar nuevo usuario (Solo Admin)
  async addUser(userData: {
    nombre: string;
    email: string;
    password: string;
    rol: string;
  }): Promise<UserSummary> {
    const { data } = await http.post<ApiUser>("/auth/register", userData);
    return normalizeUser(data);
  }

  // 🔹 Eliminar usuario por ID
  async deleteUser(userId: number): Promise<void> {
    await http.delete(`/users/${userId}`);
  }

  // 🔹 Obtener información del usuario autenticado (opcional)
  async getMe(): Promise<UserSummary> {
    const { data } = await http.get<ApiUser>("/auth/me");
    return normalizeUser(data);
  }

  // 🔹 Refrescar token (opcional, por si lo usas con JWT)
  async refreshToken(): Promise<{ access_token: string }> {
    const { data } = await http.post<{ access_token: string }>("/auth/refresh");
    return data;
  }
}
