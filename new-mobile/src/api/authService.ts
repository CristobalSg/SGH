// src/api/authService.ts
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;
console.log("API_URL =", API_URL);

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (email: string, contrasena: string): Promise<LoginResponse> => {
  const response = await axios.post(`${API_URL}/api/auth/login`, {
    email,
    contrasena,
  });
  console.log("Datos - ", response.data)
  return response.data;
};

// (Opcional) seteo global del header para peticiones autenticadas
export const setAuthToken = (token: string | null) => {
  if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common["Authorization"];
  }
};
