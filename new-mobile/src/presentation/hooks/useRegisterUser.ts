import { useState } from "react";
import { AuthRegisterRepositoryHttp, type RegisterUserDto } from "../../infrastructure/repositories/AuthRegisterRepositoryHttp";

const repository = new AuthRegisterRepositoryHttp();

export function useRegisterUser() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createUser = async (data: RegisterUserDto) => {
    setLoading(true);
    setError(null);
    try {
      const result = await repository.registerUser(data);
      return result;
    } catch (err: any) {
      setError(err.response?.data?.message || "Error al registrar usuario");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { createUser, loading, error };
}
