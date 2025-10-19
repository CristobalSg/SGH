// src/hooks/useAuth.ts
import { useState } from "react";
import { login, setAuthToken } from "../api/authService";

export const useAuth = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await login(email, password);
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
      setAuthToken(data.access_token);
      return true;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al iniciar sesión");
      return false;
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setAuthToken(null);
  };

  return { token, loading, error, handleLogin, handleLogout };
};
