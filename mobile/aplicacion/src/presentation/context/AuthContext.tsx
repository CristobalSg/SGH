import { createContext, useContext, useState } from "react";
import { User } from "../../domain/models/User";
import { AuthApiRepository } from "../../infrastructure/repositories/AuthApiRepository";
import { LoginUseCase } from "../../application/usecases/LoginUseCase";

const authRepository = new AuthApiRepository();
const loginUseCase = new LoginUseCase(authRepository);

interface AuthContextProps {
  user?: User;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | undefined>(undefined);

  const login = async (email: string, password: string) => {
    const loggedUser = await loginUseCase.execute(email, password);
    setUser(loggedUser);
    localStorage.setItem("token", loggedUser.token || "");
  };

  const logout = () => {
    setUser(undefined);
    localStorage.removeItem("token");
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
