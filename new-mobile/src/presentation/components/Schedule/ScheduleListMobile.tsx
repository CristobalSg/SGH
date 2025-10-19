import { Card } from "antd";
import { DIAS, HORAS } from "../../types/schedule";
import type { Events } from "../../types/schedule";

interface Props {
  events: Events;
  onSlotTap: (day: string, hour: string) => void;
}

export default function ScheduleListMobile({ events, onSlotTap }: Props) {
  return (
    <div className="md:hidden space-y-3">
      {HORAS.map((hora) => (
        <Card key={hora} size="small" className="rounded-xl shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold">{hora}</h3>
          </div>
          <div className="grid grid-cols-2 gap-2">
            {DIAS.map((day) => {
              const evts = events[day]?.[hora] ?? [];
              const has = evts.length > 0;
              return (
                <button
                  key={`${day}-${hora}`}
                  className={`text-left p-3 rounded-lg border transition
                    ${has ? "bg-pink-50 border-pink-200" : "bg-white hover:bg-gray-50 border-gray-200"}`}
                  onClick={() => onSlotTap(day, hora)}
                >
                  <div className="text-xs text-gray-500 mb-1">
                    {day.charAt(0).toUpperCase() + day.slice(1)}
                  </div>
                  <div className="text-sm">
                    {has ? evts.join(", ") : <span className="text-gray-400">—</span>}
                  </div>
                </button>
              );
            })}
          </div>
        </Card>
      ))}
    </div>
  );
}
