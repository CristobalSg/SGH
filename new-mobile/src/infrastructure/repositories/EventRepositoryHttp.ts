// src/infrastructure/repositories/EventRepositoryHttp.ts
import type { EventRepository } from "../../domain/repositories/EventRepository";
import type { Event, CreateEventDTO, UpdateEventDTO } from "../../domain/events/event";
import http from "../http/httpClient";

export class EventRepositoryHttp implements EventRepository {
  private readonly baseUrl = "/eventos";

  async getAll(): Promise<Event[]> {
    const response = await http.get<Event[]>(`${this.baseUrl}/`);
    return response.data;
  }

  async create(event: CreateEventDTO): Promise<Event> {
    const response = await http.post<Event>(`${this.baseUrl}/`, event);
    return response.data;
  }

  async update(id: number, event: UpdateEventDTO): Promise<Event> {
    const response = await http.put<Event>(`${this.baseUrl}/${id}`, event);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await http.delete(`${this.baseUrl}/${id}`);
  }

  async getById(id: number): Promise<Event> {
    const response = await http.get<Event>(`${this.baseUrl}/${id}`);
    return response.data;
  }
}

// Singleton
export const eventRepository = new EventRepositoryHttp();
