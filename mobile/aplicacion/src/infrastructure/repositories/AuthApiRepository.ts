import { AuthRepository } from "../../domain/repositories/AuthRepository";
import { User } from "../../domain/models/User";
import { AuthResponse } from "../../domain/models/AuthResponse";


import axios from "axios";

export const API_URL = "https://sgh.inf.uct.cl/api";

export class AuthApiRepository implements AuthRepository {
  async login(email: string, contrasena: string): Promise<AuthResponse> {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, contrasena })
    });

    if (!res.ok) throw new Error("Credenciales inválidas");

    return res.json() as Promise<AuthResponse>;
  }

  async logout(): Promise<void> {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  async register(user: Omit<User, "id" | "token"> & { contrasena: string }): Promise<User> {
    const response = await axios.post(`${API_URL}/auth/register`, user);
    return response.data;
  }

  async getProfile(token: string): Promise<User> {
    const response = await axios.get(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  }
}
