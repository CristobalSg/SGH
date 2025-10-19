// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { login as loginService, setAuthToken } from "../api/authService";

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  useEffect(() => {
    setAuthToken(token);
  }, [token]);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const res = await loginService(email, password);
      setToken(res.access_token);
      localStorage.setItem("token", res.access_token);
      setAuthToken(res.access_token);
      return true;
    } catch {
      return false;
    }
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setAuthToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated: !!token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }
  return context;
};
