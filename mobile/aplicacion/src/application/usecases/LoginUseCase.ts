// application/usecases/LoginUseCase.ts
import { AuthApiRepository } from "../../infrastructure/repositories/AuthApiRepository";
import { AuthResponse } from "../../domain/models/AuthResponse";

export class LoginUseCase {
  constructor(private authRepo: AuthApiRepository) {}

  async execute(email: string, password: string): Promise<AuthResponse> {
    return await this.authRepo.login(email, password);
  }
}
