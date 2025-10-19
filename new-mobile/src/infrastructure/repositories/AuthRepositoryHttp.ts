// src/infrastructure/repositories/AuthRepositoryHttp.ts
import type { AuthRepository, LoginResponse } from "../../domain/repositories/AuthRepository";
import { http } from "../http/httpClient";
import type { User} from "../../domain/auth/user";

export class AuthRepositoryHttp implements AuthRepository {
  async login(email: string, contrasena: string): Promise<LoginResponse> {
    const { data } = await http.post<LoginResponse>("/auth/login", { email, contrasena });
    return data;
  }

  async logout(): Promise<void> {
    // si tu API expone logout:
    try { await http.post("/auth/logout"); } catch { /* noop */ }
  }

  async me(): Promise<User> {
    const { data } = await http.get("/auth/me");
    // Normaliza el payload al shape User
    return {
      id: String(data.id),
      name: data.name ?? data.fullName ?? data.username ?? "",
      email: data.email,
      role: (data.role ?? data.rol) as User["role"], // mapea "rol" -> "role" si tu API usa "rol"
    };
  }
}
