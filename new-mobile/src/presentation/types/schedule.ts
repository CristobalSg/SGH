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
  "08:00","09:00","10:00","11:00","12:00",
  "13:00","14:00","15:00","16:00","17:00",
];
