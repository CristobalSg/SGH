import { RestriccionesRepository } from "../../domain/repositories/RestriccionesRepository";
import { Restriccion } from "../../domain/entities/Restriccion";

export class RestriccionesUseCase {
  constructor(private restriccionesRepo: RestriccionesRepository) {}

  async listar() {
    return await this.restriccionesRepo.getAll();
  }

  async agregar(restriccion: Restriccion) {
    return await this.restriccionesRepo.create(restriccion);
  }

  async editar(id: string, restriccion: Restriccion) {
    return await this.restriccionesRepo.update(id, restriccion);
  }

  async eliminar(id: string) {
    return await this.restriccionesRepo.delete(id);
  }
}
