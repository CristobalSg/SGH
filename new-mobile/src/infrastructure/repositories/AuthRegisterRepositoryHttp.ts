import { http } from "../http/httpClient";

export type RegisterUserDto = {
  name: string;
  email: string;
  password: string;
  role: string;
  active?: boolean;
};

export class AuthRegisterRepositoryHttp {
  async registerUser(user: RegisterUserDto): Promise<any> {
    const payload = {
      nombre: user.name,
      email: user.email,
      rol: user.role,
      activo: user.active ?? true,
      contrasena: user.password,
    };

    try {
      const { data } = await http.post("/auth/register", payload, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      });

      console.log("✅ Respuesta del servidor:", data);
      return data;

    } catch (error: any) {
      // Si el servidor responde con error (por ejemplo 400 o 500)
      if (error.response) {
        console.error("❌ Error del servidor:", error.response.data);
      } else if (error.request) {
        // Si no hubo respuesta (problema de conexión, timeout, etc.)
        console.error("⚠️ No hubo respuesta del servidor:", error.request);
      } else {
        // Error al preparar la solicitud
        console.error("⚙️ Error en la configuración de la solicitud:", error.message);
      }

      throw error; // se relanza para manejarlo arriba si es necesario
    }
  }
}
