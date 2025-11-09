import { Dropdown } from "antd";
import type { MenuProps } from "antd";
import { ClockIcon, EllipsisVerticalIcon } from "@heroicons/react/24/solid";
import dayjs from "dayjs";
import type { RestriccionHorarioView } from "../../hooks/useDocenteHorarioRestrictions";

interface RestrictionListProps {
  restricciones: RestriccionHorarioView[];
  onDelete?: (id: number) => void;
  deletingId?: number | null;
  onEdit?: (item: RestriccionHorarioView) => void;
}

const DAY_NAMES = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
const STATUS_STYLES = {
  disponible: "bg-[#FDB813] text-[#004F9F]",
  noDisponible: "bg-white/80 text-[#004F9F]",
};

const formatDuration = (start: string, end: string) => {
  const startTime = dayjs(start, "HH:mm");
  const endTime = dayjs(end, "HH:mm");
  if (!startTime.isValid() || !endTime.isValid()) return "";

  let minutes = endTime.diff(startTime, "minute");
  if (minutes <= 0) return "";

  const hours = Math.floor(minutes / 60);
  minutes -= hours * 60;

  const parts = [];
  if (hours > 0) parts.push(`${hours} h`);
  if (minutes > 0) parts.push(`${minutes} min`);

  return parts.join(" ") || "";
};

export default function RestrictionList({
  restricciones,
  onDelete,
  deletingId,
  onEdit,
}: RestrictionListProps) {
  if (restricciones.length === 0) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-300 bg-slate-50 px-6 py-10 text-center text-sm text-slate-500">
        No hay restricciones registradas
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {restricciones.map((item) => {
        const isDeleting = deletingId === item.id;
        const dayLabel = DAY_NAMES[item.day] ?? `Día ${item.day}`;
        const duration = formatDuration(item.start, item.end);
        const statusKey = item.disponible ? "disponible" : "noDisponible";
        const menuItems: MenuProps["items"] = [
          ...(onEdit ? [{ key: "edit", label: "Editar" }] : []),
          ...(onDelete ? [{ key: "delete", label: <span className="text-red-500">Eliminar</span>, disabled: isDeleting }] : []),
        ];

        return (
          <div
            key={item.id}
            className="relative overflow-hidden rounded-3xl bg-[#004F9F] p-5 shadow-lg transition-transform hover:-translate-y-0.5"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="text-xs font-medium uppercase tracking-wide text-[#FDB813]">
                  {dayLabel}
                </div>
                <div className="mt-1 flex items-center gap-2 text-base font-semibold text-white">
                  <ClockIcon className="h-5 w-5 text-[#FDB813]" />
                  <span>
                    {item.start} – {item.end}
                  </span>
                </div>
                {duration && (
                  <div className="mt-1 text-xs font-medium text-white/80">
                    {duration}
                  </div>
                )}
                <div className="mt-3 text-sm font-semibold text-white">
                  {item.descripcion?.trim() || (item.disponible ? "Disponible para asignar" : "Bloqueado")}
                </div>
                {!item.disponible && (
                  <div className="mt-1 text-xs text-white/70">
                    Tiempo marcado como no disponible.
                  </div>
                )}
              </div>

              {(onDelete || onEdit) && menuItems.length > 0 && (
                <Dropdown
                  menu={{
                    items: menuItems,
                    onClick: ({ key }) => {
                      if (key === "edit") onEdit?.(item);
                      if (key === "delete") onDelete?.(item.id);
                    },
                  }}
                  trigger={["click"]}
                >
                  <button
                    type="button"
                    className="rounded-full bg-white/80 p-2 text-[#004F9F] shadow-sm transition hover:bg-white"
                  >
                    <EllipsisVerticalIcon className="h-5 w-5" />
                  </button>
                </Dropdown>
              )}
            </div>

            <div className="mt-4 flex justify-end">
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${STATUS_STYLES[statusKey]}`}
              >
                {item.disponible ? "Disponible" : "No disponible"}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
