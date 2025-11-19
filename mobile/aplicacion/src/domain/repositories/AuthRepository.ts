// domain/repositories/AuthRepository.ts
import { AuthResponse } from "../models/AuthResponse";

export interface AuthRepository {
  login(email: string, contrasena: string): Promise<AuthResponse>;
  logout(): Promise<void>;
}
