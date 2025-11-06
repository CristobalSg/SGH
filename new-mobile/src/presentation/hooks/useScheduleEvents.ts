import { useMemo } from "react";
import type { Events } from "../types/schedule";

const previewEvents: Events = {
  lunes: {
    "08:15 - 09:45": [
      "Cálculo Vectorial\nSala B104 • Prof. López",
    ],
    "10:00 - 11:30": [
      "Estructuras de Datos\nSala C203 • Prof. Rojas",
    ],
    "11:45 - 13:15": [
      "Laboratorio de Programación\nLab Redes • Ing. Vergara",
    ],
    "14:30 - 16:00": [
      "Arquitectura de Computadores\nSala A210 • Dra. Núñez",
    ],
    "16:15 - 17:45": [
      "Gestión de Servicios TI\nSala E101 • Prof. Fuentes",
    ],
  },
  martes: {
    "08:15 - 09:45": [
      "Probabilidades y Estadística\nSala C105 • Prof. Gutiérrez",
    ],
    "10:00 - 11:30": [
      "Sistemas Distribuidos\nSala B206 • Dra. Pinto",
    ],
    "11:45 - 13:15": [
      "Proyecto Integrador I\nSala Innovation • Mg. Saavedra",
    ],
    "14:30 - 16:00": [
      "Metodologías Ágiles\nSala Scrum • Coach Díaz",
    ],
    "16:15 - 17:45": [
      "Gestión de Proyectos TI\nSala D101 • Prof. Ortiz",
    ],
  },
  miércoles: {
    "08:15 - 09:45": [
      "Ingeniería de Software\nSala B302 • Prof. Carrasco",
    ],
    "10:00 - 11:30": [
      "Bases de Datos Avanzadas\nSala DataLab • Dra. Morales",
    ],
    "11:45 - 13:15": [
      "Laboratorio de Datos\nSala DataLab • Equipo Ayudantes",
    ],
    "14:30 - 16:00": [
      "Redes y Comunicaciones\nSala Telecom • Ing. Salinas",
    ],
    "16:15 - 17:45": [
      "Seminario de Investigación\nSala I+D • Dr. Valdés",
    ],
  },
  jueves: {
    "08:15 - 09:45": [
      "Inteligencia Artificial\nSala AI Lab • Dr. Blanco",
    ],
    "10:00 - 11:30": [
      "Electivo: Computación Gráfica\nSala Visual • Prof. Muñoz",
    ],
    "11:45 - 13:15": [
      "Formulación y Evaluación de Proyectos\nSala C201 • Prof. Vera",
    ],
    "14:30 - 16:00": [
      "Electivo: Ciberseguridad\nSala SecOps • Ing. Molina",
    ],
    "16:15 - 17:45": [
      "Seminario de Título\nSala Consejo • Comisión Carrera",
    ],
  },
  viernes: {
    "08:15 - 09:45": [
      "Sistemas Operativos\nSala C108 • Prof. Herrera",
    ],
    "10:00 - 11:30": [
      "Ética Profesional\nSala Magna • Dra. Silva",
    ],
    "11:45 - 13:15": [
      "Taller de Innovación Tecnológica\nHub UCI • Equipo Mentores",
    ],
    "14:30 - 16:00": [
      "Práctica Profesional\nSala Vinculación • Coordinación UCI",
    ],
    "16:15 - 17:45": [
      "Actividad de Extensión\nAuditorio Central • Invitados",
    ],
  },
};

export function useScheduleEvents() {
  const events = useMemo(() => previewEvents, []);
  const allEventsCount = useMemo(
    () => Object.values(events).flatMap((h) => Object.values(h)).flat().length,
    [events],
  );

  return { events, allEventsCount };
}
