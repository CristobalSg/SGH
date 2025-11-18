import { http } from "../http/httpClient";
import { normalizeRole } from "../../domain/auth/roleUtils";

type ApiUser = {
  id: number;
  nombre?: string;
  name?: string;
  email: string;
  rol?: string;
  role?: string;
  activo?: boolean;
  active?: boolean;
  created_at?: string;
  updated_at?: string;
  // A veces vienen campos de docente embebidos
  docente_id?: number | null;
  departamento?: string | null;
  docente?: { id: number; departamento?: string | null } | null;
};

export type AdminUserView = {
  id: number;
  name: string;
  email: string;
  role: "admin" | "docente" | "estudiante";
  active?: boolean;
  docenteId?: number | null;
  department?: string | null;
  createdAt?: string;
  updatedAt?: string;
};

export type AdminUserUpdateInput = {
  name: string;
  email: string;
  role: string;
  password?: string;
};

function extractArray<T = any>(payload: any): T[] {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.results)) return payload.results;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.data)) return payload.data;
  return [];
}

function normalizeUser(u: ApiUser): AdminUserView {
  // Role puede venir como rol o role
  const rawRole = (u.rol ?? u.role ?? "").toString();
  const role = normalizeRole(rawRole) as AdminUserView["role"];
  // Docente embebido si existe
  const docenteId =
    u.docente_id ?? u.docente?.id ?? null;
  const department =
    u.departamento ?? u.docente?.departamento ?? null;

  return {
    id: u.id,
    name: u.nombre ?? u.name ?? "",
    email: u.email,
    role,
    active: u.activo ?? u.active,
    docenteId,
    department,
    createdAt: u.created_at,
    updatedAt: u.updated_at,
  };
}

async function tryPutThenPatch<T>(url: string, payload: any): Promise<T> {
  try {
    const res = await http.put<T>(url, payload);
    return res as any as T;
  } catch (e: any) {
    // Fallback: PATCH
    const res = await http.patch<T>(url, payload);
    return res as any as T;
  }
}

export class UserRepositoryHttp {
  private base = "/users/";

  async list(): Promise<AdminUserView[]> {
    const res = await http.get(this.base, { params: { limit: 500 } });
    const arr = extractArray<ApiUser>(res.data);
    return arr.map(normalizeUser);
  }

  async update(id: number, data: AdminUserUpdateInput): Promise<AdminUserView> {
    const payload: any = {
      nombre: data.name,
      email: data.email,
      rol: data.role,
    };
    if (data.password) payload.password = data.password;

    // Intentar con trailing slash y sin slash
    const urlSlash = `${this.base}${id}/`;
    const urlNoSlash = `${this.base}${id}`;
    try {
      const res = await tryPutThenPatch<ApiUser>(urlSlash, payload);
      return normalizeUser((res as any).data ?? (res as any));
    } catch {
      const res = await tryPutThenPatch<ApiUser>(urlNoSlash, payload);
      return normalizeUser((res as any).data ?? (res as any));
    }
  }

  async delete(id: number): Promise<void> {
    const urlSlash = `${this.base}${id}/`;
    const urlNoSlash = `${this.base}${id}`;
    try {
      await http.delete(urlSlash);
    } catch {
      await http.delete(urlNoSlash);
    }
  }

  async add(userData: { name: string; email: string; password: string; role: string }): Promise<AdminUserView> {
    const res = await http.post<ApiUser>("/auth/register", {
      nombre: userData.name,
      email: userData.email,
      password: userData.password,
      rol: userData.role,
    });
    return normalizeUser(res.data);
  }
}
