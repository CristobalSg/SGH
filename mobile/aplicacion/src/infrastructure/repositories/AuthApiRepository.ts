import { AuthRepository } from "../../domain/repositories/AuthRepository";
import { User } from "../../domain/models/User";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class AuthApiRepository implements AuthRepository {
  async login(email: string, contrasena: string): Promise<User> {
    const response = await axios.post(`${API_URL}/auth/login-json`, {
      email,
      contrasena,
    });
    return {
      email,
      nombre: response.data.nombre,
      apellido: response.data.apellido,
      token: response.data.access_token,
    };
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
