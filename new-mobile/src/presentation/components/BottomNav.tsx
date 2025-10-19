import {
  HomeIcon,
  ChartBarIcon,
  UserIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/outline";
import {
  HomeIcon as HomeSolid,
  ChartBarIcon as ChartBarSolid,
  UserIcon as UserSolid,
  Cog6ToothIcon as CogSolid,
} from "@heroicons/react/24/solid";
import { useNavigate, useLocation } from "react-router-dom";
import type { ComponentType, SVGProps } from "react";

type Item = {
  id: "home" | "stats" | "profile" | "settings";
  label: string;
  path: string;
  outline: ComponentType<SVGProps<SVGSVGElement>>;
  solid: ComponentType<SVGProps<SVGSVGElement>>;
};

const items: Item[] = [
  { id: "home", label: "Home",   outline: HomeIcon,      solid: HomeSolid,      path: "/home" },
  { id: "stats", label: "Likes", outline: ChartBarIcon,  solid: ChartBarSolid,  path: "/stats" },
  { id: "profile", label: "Profile", outline: UserIcon,  solid: UserSolid,      path: "/profile" },
  { id: "settings", label: "Search", outline: Cog6ToothIcon, solid: CogSolid,    path: "/settings" },
];

// Colores del chip activo por pestaña (ajústalos a tu paleta)
const activeClasses: Record<Item["id"], string> = {
  home: "bg-violet-500 text-white",
  stats: "bg-pink-500 text-white",
  profile: "bg-sky-500 text-white",
  settings: "bg-amber-500 text-white",
};

export default function BottomNav() {
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const activeId: Item["id"] | undefined =
    items.find((i) => pathname.startsWith(i.path))?.id ?? "home";

  const handleClick = (it: Item) => {
    if (!pathname.startsWith(it.path)) navigate(it.path);
  };

  return (
    <nav
      className="fixed bottom-3 left-1/2 -translate-x-1/2 z-20 w-full"
      style={{ paddingBottom: "env(safe-area-inset-bottom, 0px)" }}
      aria-label="Barra de navegación"
    >
      <div className="mx-auto max-w-md px-4">
        {/* Contenedor flotante estilo “pill” */}
        <div className="w-full rounded-3xl border border-black/5 bg-white/90 dark:bg-neutral-900/90 backdrop-blur-xl shadow-lg">
          <div className="flex items-center justify-between gap-1 px-2 py-2">
            {items.map((it) => {
              const isActive = activeId === it.id;
              const Icon = isActive ? it.solid : it.outline;
              return (
                <button
                  key={it.id}
                  onClick={() => handleClick(it)}
                  aria-current={isActive ? "page" : undefined}
                  aria-label={it.label}
                  className={[
                    "group relative flex items-center justify-center transition-all duration-200",
                    "rounded-2xl px-2 py-2",
                    isActive
                      ? `shadow-sm ${activeClasses[it.id]}`
                      : "text-gray-600 dark:text-gray-300 hover:bg-gray-100/70 dark:hover:bg-white/5",
                  ].join(" ")}
                  style={{
                    // Chip más ancho cuando está activo (para mostrar texto)
                    minWidth: isActive ? 92 : 48,
                  }}
                >
                  <Icon
                    className={`h-5 w-5 transition-transform duration-200 ${
                      isActive ? "scale-100" : "scale-95"
                    }`}
                  />
                  {/* Etiqueta: visible solo en el activo */}
                  <span
                    className={[
                      "ml-2 text-xs font-medium transition-opacity duration-200",
                      isActive ? "opacity-100" : "opacity-0 w-0 overflow-hidden",
                    ].join(" ")}
                  >
                    {it.label}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Línea “home indicator” opcional (solo visual) */}
        <div className="mx-auto mt-2 h-1 w-24 rounded-full bg-gray-300/70 dark:bg-gray-600/70" />
      </div>
    </nav>
  );
}
