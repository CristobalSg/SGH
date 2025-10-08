import { jwtDecode } from "jwt-decode";
import { TokenPayload } from "../../domain/auth/tokenPayload";

/**
 * Decodifica el token y devuelve su payload.
 */
export function decodeToken(token: string): TokenPayload | null {
  try {
    return jwtDecode<TokenPayload>(token);
  } catch (error) {
    console.error("Token inválido", error);
    return null;
  }
}

/**
 * Guarda el token JWT en memoria local.
 */
export function saveToken(token: string): void {
  localStorage.setItem("auth_token", token);
}

/**
 * Obtiene el token JWT desde memoria local.
 */
export function getToken(): string | null {
  return localStorage.getItem("auth_token");
}

/**
 * Elimina el token (logout).
 */
export function clearToken(): void {
  localStorage.removeItem("auth_token");
}
