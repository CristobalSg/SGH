// core/domain/auth/tokenPayload.ts
export interface TokenPayload {
  sub: string;       // email o identificador
  user_id: number;
  rol: string;
  exp: number;       // timestamp de expiración
  type: string;      // access | refresh
}
