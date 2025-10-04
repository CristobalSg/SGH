import { createContext, useContext, useState } from "react";
import { User } from "../../domain/models/User";
import { AuthApiRepository } from "../../infrastructure/repositories/AuthApiRepository";
import { LoginUseCase } from "../../application/usecases/LoginUseCase";
import { jwtDecode } from "jwt-decode";

const authRepository = new AuthApiRepository();
const loginUseCase = new LoginUseCase(authRepository);

interface AuthContextProps {
  user?: User;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | undefined>(undefined);

  const login = async (email: string, password: string) => {
    // Llama al caso de uso → este debería devolver AuthResponse (tokens)
    const authResponse = await loginUseCase.execute(email, password);

    // Guarda tokens
    localStorage.setItem("access_token", authResponse.access_token);
    localStorage.setItem("refresh_token", authResponse.refresh_token);

    // Decodifica el access_token
    const decoded: any = jwtDecode(authResponse.access_token);

    const loggedUser: User = {
      id: decoded.user_id,
      email: decoded.sub,
      rol: decoded.rol,
    };

    setUser(loggedUser);
    return loggedUser;
  };

  const logout = () => {
    setUser(undefined);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
