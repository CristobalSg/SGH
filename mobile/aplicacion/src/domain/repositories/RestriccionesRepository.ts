import { Restriccion } from "../entities/Restriccion";

export interface RestriccionesRepository {
  getAll(): Promise<Restriccion[]>;
  create(data: Restriccion): Promise<Restriccion>;
  update(id: string, data: Restriccion): Promise<Restriccion>;
  delete(id: string): Promise<void>;
}
