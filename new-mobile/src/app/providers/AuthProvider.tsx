import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { AuthRepositoryHttp } from "../../infrastructure/repositories/AuthRepositoryHttp";
import { makeLoginUseCase } from "../../application/usecases/auth/login";
import { makeGetCurrentUserUseCase } from "../../application/usecases/auth/getCurrentUser";
import { setAuthToken } from "../../infrastructure/http/httpClient";
import type { User, Role } from "../../domain/auth/user";

type AuthContextType = {
  token: string | null;
  user: User | null;
  role: Role | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const repo = useMemo(() => new AuthRepositoryHttp(), []);
  const loginUC = useMemo(() => makeLoginUseCase(repo), [repo]);
  const getMeUC = useMemo(() => makeGetCurrentUserUseCase(repo), [repo]);

  // Propaga token al http client
  useEffect(() => { setAuthToken(token); }, [token]);

  // Hidratación: si hay token, valida /me; si falla, limpia
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        if (token) {
          const me = await getMeUC();
          if (mounted) setUser(me);
        } else {
          if (mounted) setUser(null);
        }
      } catch {
        // Token inválido/expirado: limpia estado
        localStorage.removeItem("token");
        setAuthToken(null);
        if (mounted) {
          setToken(null);
          setUser(null);
        }
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, [token, getMeUC]);

  const login = async (email: string, password: string) => {
    try {
      const res = await loginUC(email, password);
      localStorage.setItem("token", res.access_token);
      setToken(res.access_token); // el efecto de arriba hará /me
      return true;
    } catch {
      return false;
    }
  };

  const logout = async () => {
    try { await repo.logout(); } finally {
      localStorage.removeItem("token");
      setAuthToken(null);
      setToken(null);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        role: user?.role ?? null,
        isAuthenticated: !!token,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
