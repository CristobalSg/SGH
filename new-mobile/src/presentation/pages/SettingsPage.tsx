import { BellIcon, ChevronLeftIcon } from "@heroicons/react/24/outline";
import AppLayout from "../components/layout/AppLayout";

const SettingsPage = () => {
  return (
    <AppLayout
      title="Configuración"
      leftAction={
        <button
          aria-label="Volver"
          onClick={() => window.history.back()}
          className="p-1 rounded-md hover:bg-gray-100 active:bg-gray-200"
        >
          <ChevronLeftIcon className="h-6 w-6 text-gray-700" />
        </button>
      }
      rightAction={
        <button
          aria-label="Notificaciones"
          className="p-1 rounded-md hover:bg-gray-100 active:bg-gray-200"
        >
          <BellIcon className="h-6 w-6 text-gray-700" />
        </button>
      }
    >
      <p className="text-gray-700 text-sm mt-4">
        Preferencias, ajustes de notificaciones y otros parámetros del sistema.
      </p>

      <section className="mt-4 space-y-3">
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h2 className="text-sm font-semibold text-gray-800">Cuenta</h2>
          <p className="text-xs text-gray-500 mt-1">
            Correo, contraseña y seguridad.
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h2 className="text-sm font-semibold text-gray-800">Notificaciones</h2>
          <p className="text-xs text-gray-500 mt-1">
            Push, correo y recordatorios.
          </p>
        </div>
      </section>
    </AppLayout>
  );
};

export default SettingsPage;
