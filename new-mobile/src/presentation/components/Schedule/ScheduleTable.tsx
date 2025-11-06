import { BellIcon } from "@heroicons/react/24/outline";
import ScheduleListMobile from "./ScheduleListMobile";
import { useScheduleEvents } from "../../hooks/useScheduleEvents";

export default function ScheduleTable() {
  const { events, allEventsCount } = useScheduleEvents();

  return (
    <div className="rounded-3xl border border-[#004F9F1A] bg-white p-5 shadow-lg">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-[#004F9F]">
          <span className="grid place-items-center rounded-full bg-[#004F9F1A] p-2">
            <BellIcon className="h-5 w-5 text-[#004F9F]" />
          </span>
          Horario Semanal
        </h2>
        <span className="text-sm font-medium text-[#FDB813]">{allEventsCount} clases</span>
      </div>

      <ScheduleListMobile events={events} />
    </div>
  );
}
