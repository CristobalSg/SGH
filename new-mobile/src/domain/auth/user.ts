export type Role = "docente" | "estudiante" | "admin";

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role; // Asegúrate que tu backend devuelva "role" o mapea en el repo
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type?: string;
}
