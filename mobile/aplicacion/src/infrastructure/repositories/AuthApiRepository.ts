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

    const data = response.data
    //console.log("Data User", email, data.user.first_name, data.user.last_name)
    //console.log("token", data.access_token)

    return {
      email,
      nombre: data.user.first_name,
      apellido: data.user.last_name,
      token: data.access_token,
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
