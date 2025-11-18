// src/domain/events/event.ts
export interface Event {
  id?: number;
  nombre: string;
  descripcion?: string;
  hora_inicio: string; // Puede ser "HH:mm:ss" o datetime "YYYY-MM-DDTHH:mm:ss"
  hora_cierre: string; // Puede ser "HH:mm:ss" o datetime "YYYY-MM-DDTHH:mm:ss"
  active: boolean;
  user_id: number;
  fecha?: string; // Campo opcional de fecha si existe en el backend
  created_at?: string;
  updated_at?: string;
}

export interface CreateEventDTO {
  nombre: string;
  descripcion?: string;
  hora_inicio: string;
  hora_cierre: string;
  active?: boolean;
  user_id: number;
  fecha?: string; // Campo opcional de fecha
}

export interface UpdateEventDTO {
  nombre?: string;
  descripcion?: string;
  hora_inicio?: string;
  hora_cierre?: string;
  active?: boolean;
  fecha?: string; // Campo opcional de fecha
}
