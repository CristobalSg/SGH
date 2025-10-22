import { Fragment } from "react";
import { DIAS, HORAS } from "../../types/schedule";
import type { Events } from "../../types/schedule";

const capitalize = (value: string) => value.charAt(0).toUpperCase() + value.slice(1);

export default function ScheduleListMobile({ events }: { events: Events }) {
  return (
    <div className="overflow-x-auto">
      <div
        className="grid min-w-[560px] gap-px rounded-3xl bg-[#004F9F]"
        style={{ gridTemplateColumns: `80px repeat(${DIAS.length}, minmax(110px, 1fr))` }}
      >
        <div className="bg-[#004F9F] p-3 text-sm font-semibold uppercase tracking-wide text-white">
          Hora
        </div>
        {DIAS.map((day) => (
          <div
            key={`head-${day}`}
            className="bg-[#004F9F] p-3 text-center text-sm font-semibold uppercase tracking-wide text-white"
          >
            {capitalize(day)}
          </div>
        ))}

        {HORAS.map((hora) => (
          <Fragment key={`row-${hora}`}>
            <div
              className="bg-white p-3 text-sm font-semibold text-[#004F9F]"
            >
              {hora}
            </div>
            {DIAS.map((day) => {
              const key = `${day}-${hora}`;
              const evts = events[day]?.[hora] ?? [];
              const has = evts.length > 0;
              return (
                <div
                  key={key}
                  className={`min-h-[80px] w-full bg-white p-3 text-left ${
                    has ? "shadow-[0_0_0_1px_#FDB81366] bg-[#FDB8131A]" : ""
                  }`}
                >
                  {has ? (
                    <div className="space-y-2">
                      {evts.slice(0, 2).map((evt, idx) => (
                        <span
                          key={`${key}-${idx}`}
                          className="inline-flex w-full flex-col rounded-xl bg-[#FDB813] px-3 py-2 text-xs font-semibold text-[#004F9F] shadow-sm"
                        >
                          {evt.split("\n").map((line, index) => (
                            <span key={`${key}-${idx}-line-${index}`} className={index === 0 ? "text-[13px]" : "text-[11px] font-medium text-[#004F9FCC]"}>
                              {line}
                            </span>
                          ))}
                        </span>
                      ))}
                      {evts.length > 2 && (
                        <span className="text-xs font-semibold text-[#004F9F]">
                          +{evts.length - 2} más
                        </span>
                      )}
                    </div>
                  ) : (
                    <span className="text-xs font-medium uppercase tracking-wide text-[#004F9F66]">
                      Disponible
                    </span>
                  )}
                </div>
              );
            })}
          </Fragment>
        ))}
      </div>
    </div>
  );
}
