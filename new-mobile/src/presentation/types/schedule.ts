export type DayKey = "lunes" | "martes" | "miércoles" | "jueves" | "viernes";

export interface Events {
  [day: string]: { [hour: string]: string[] };
}

export interface SlotRef {
  day: DayKey;
  hour: string;
}

export const DIAS: DayKey[] = ["lunes", "martes", "miércoles", "jueves", "viernes"];

export const HORAS: string[] = [
  "08:15 - 09:45",
  "10:00 - 11:30",
  "11:45 - 13:15",
  "14:30 - 16:00",
  "16:15 - 17:45",
];
