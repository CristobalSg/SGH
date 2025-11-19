import { RestriccionesRepository } from "../../domain/repositories/RestriccionesRepository";
import { Restriccion } from "../../domain/entities/Restriccion";
import { getToken } from "../auth/jwtService";

const API_URL = "https://sgh.inf.uct.cl/api";

export class RestriccionesApiRepository implements RestriccionesRepository {
  async getAll(): Promise<Restriccion[]> {
    const token = getToken();
    const res = await fetch(`${API_URL}/restricciones`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Error al obtener restricciones");
    return await res.json();
  }

  async create(data: Restriccion): Promise<Restriccion> {
    const token = getToken();
    const res = await fetch(`${API_URL}/restricciones`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error al crear restricción");
    return await res.json();
  }

  async update(id: string, data: Restriccion): Promise<Restriccion> {
    const token = getToken();
    const res = await fetch(`${API_URL}/restricciones/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error al actualizar restricción");
    return await res.json();
  }

  async delete(id: string): Promise<void> {
    const token = getToken();
    const res = await fetch(`${API_URL}/restricciones/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Error al eliminar restricción");
  }
}
