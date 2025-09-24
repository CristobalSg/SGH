import { User } from "../models/User";

export interface AuthRepository {
  login(email: string, contrasena: string): Promise<User>;
  register(user: Omit<User, "id" | "token"> & { contrasena: string }): Promise<User>;
  getProfile(token: string): Promise<User>;
}
