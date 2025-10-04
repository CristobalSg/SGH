// infra/auth/jwtService.ts
import { jwtDecode } from "jwt-decode";

import { TokenPayload } from "../../domain/auth/tokenPayload";

export function decodeToken(token: string): TokenPayload | null {
  try {
    return jwtDecode<TokenPayload>(token);
  } catch (error) {
    console.error("Token inválido", error);
    return null;
  }
}
