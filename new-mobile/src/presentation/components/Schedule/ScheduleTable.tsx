import { BellIcon } from "@heroicons/react/24/outline";
import EventModal from "./EventModal";
import ScheduleGridDesktop from "./ScheduleGridDesktop";
import ScheduleListMobile from "./ScheduleListMobile";
import { useScheduleEvents } from "../../hooks/useScheduleEvents";
import type { SlotRef } from "../../types/schedule";

export default function ScheduleTable() {
  const {
    events,
    selected, setSelected,
    tipoUsuario,
    addEvent, editEvent, deleteEvent,
    allEventsCount,
  } = useScheduleEvents();

  const openSlot = (day: string, hour: string) => setSelected({ day, hour } as SlotRef);

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <BellIcon className="h-5 w-5 text-blue-500" />
          Horario Semanal
        </h2>
        <span className="text-sm text-gray-500">{allEventsCount} eventos</span>
      </div>

      {/* Mobile (cards) */}
      <ScheduleListMobile events={events} onSlotTap={openSlot} />

      {/* Desktop (table) */}
      <ScheduleGridDesktop events={events} onCellClick={openSlot} />

      <EventModal
        open={!!selected}
        onClose={() => setSelected(null)}
        events={events}
        slot={selected}
        canEdit={tipoUsuario === "profesor"}
        onAdd={addEvent}
        onEdit={editEvent}
        onDelete={deleteEvent}
      />
    </div>
  );
}
