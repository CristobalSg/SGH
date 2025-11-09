// src/presentation/components/EventsCalendar.tsx
import React from "react";
import { Calendar } from "antd";
import type { Dayjs } from "dayjs";

type Props = {
  value?: Dayjs | null;
  onSelect: (d: Dayjs) => void;
};

const EventsCalendar: React.FC<Props> = ({ value, onSelect }) => {
  return (
    <div className="bg-white shadow-sm p-3 w-full rounded-xl border border-gray-200">
      <Calendar fullscreen={false} value={value ?? undefined} onSelect={onSelect} />
    </div>
  );
};

export default EventsCalendar;
