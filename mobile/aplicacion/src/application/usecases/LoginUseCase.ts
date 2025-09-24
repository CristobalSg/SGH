import { AuthRepository } from "../../domain/repositories/AuthRepository";
import { User } from "../../domain/models/User";

export class LoginUseCase {
  constructor(private authRepository: AuthRepository) {}

  async execute(email: string, contrasena: string): Promise<User> {
    return await this.authRepository.login(email, contrasena);
  }
}