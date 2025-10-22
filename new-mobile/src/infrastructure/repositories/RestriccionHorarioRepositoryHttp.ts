import { http } from "../http/httpClient";
import type {
  RestriccionHorario,
  RestriccionHorarioCreate,
  RestriccionHorarioUpdate,
} from "../../domain/restricciones/restriccionHorario";

type ApiRestriction = {
  id: number;
  docente_id: number;
  dia_semana: number;
  hora_inicio: string;
  hora_fin: string;
  disponible: boolean;
  descripcion?: string | null;
  activa: boolean;
};

type MeDetailedResponse = {
  docente_info?: { id: number };
};

const normalize = (item: ApiRestriction): RestriccionHorario => ({
  id: item.id,
  docente_id: item.docente_id,
  dia_semana: item.dia_semana as RestriccionHorario["dia_semana"],
  hora_inicio: item.hora_inicio,
  hora_fin: item.hora_fin,
  disponible: item.disponible,
  descripcion: item.descripcion,
  activa: item.activa,
});

export class RestriccionHorarioRepositoryHttp {
  async getMyDocenteId(): Promise<number> {
    const { data } = await http.get<MeDetailedResponse>("/auth/me/detailed");
    const docenteId = data?.docente_info?.id;
    if (!docenteId) {
      throw new Error("No se encontró un perfil de docente para el usuario autenticado.");
    }
    return docenteId;
  }

  async listMine(): Promise<RestriccionHorario[]> {
    const { data } = await http.get<ApiRestriction[]>("/restricciones-horario/docente/mis-restricciones");
    return data.map(normalize);
  }

  async listByDocente(docenteId: number): Promise<RestriccionHorario[]> {
    const { data } = await http.get<ApiRestriction[]>(`/restricciones-horario/docente/${docenteId}`);
    return data.map(normalize);
  }

  async createMine(payload: RestriccionHorarioCreate): Promise<RestriccionHorario> {
    const { data } = await http.post<ApiRestriction>("/restricciones-horario/docente/mis-restricciones", payload);
    return normalize(data);
  }

  async updateMine(id: number, payload: RestriccionHorarioUpdate): Promise<RestriccionHorario> {
    const { data } = await http.patch<ApiRestriction>(`/restricciones-horario/docente/mis-restricciones/${id}`, payload);
    return normalize(data);
  }

  async deleteMine(id: number): Promise<void> {
    await http.delete(`/restricciones-horario/docente/mis-restricciones/${id}`);
  }
}
