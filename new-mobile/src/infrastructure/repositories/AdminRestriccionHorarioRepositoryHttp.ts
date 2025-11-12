import { http } from "../http/httpClient"; // ajusta si tu cliente HTTP está en otro lugar
import type { DayOfWeek } from "../../domain/restricciones/restriccionHorario";

export interface AdminRestriccionHorarioDTO {
  id: number;
  docente_id: number;
  dia_semana: DayOfWeek;
  hora_inicio: string;
  hora_fin: string;
  disponible: boolean;
  descripcion?: string | null;
  activa: boolean;
}

export class AdminRestriccionHorarioRepositoryHttp {
  private baseUrl = "/restricciones-horario";

  async list(): Promise<AdminRestriccionHorarioDTO[]> {
    const response = await http.get(this.baseUrl);
    return response.data;
  }

  async getById(id: number): Promise<AdminRestriccionHorarioDTO> {
    const response = await http.get(`${this.baseUrl}/${id}`);
    return response.data;
  }

  async create(
    payload: Partial<AdminRestriccionHorarioDTO>
  ): Promise<AdminRestriccionHorarioDTO> {
    const response = await http.post(this.baseUrl, payload);
    return response.data;
  }

  async update(
    id: number,
    payload: Partial<AdminRestriccionHorarioDTO>
  ): Promise<AdminRestriccionHorarioDTO> {
    const response = await http.put(`${this.baseUrl}/${id}`, payload);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await http.delete(`${this.baseUrl}/${id}`);
  }

  /**
   * ✅ Aceptar o rechazar una restricción (actualiza el campo "activa")
   * @param id ID de la restricción
   * @param activa true = aceptar, false = rechazar
   */
  async toggleActiva(
    id: number,
    activa: boolean
  ): Promise<AdminRestriccionHorarioDTO> {
    const response = await http.put(`${this.baseUrl}/${id}`, { activa });
    return response.data;
  }
}
