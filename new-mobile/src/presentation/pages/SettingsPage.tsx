// src/presentation/pages/SettingsPage.tsx
import { BellIcon, ChevronLeftIcon, ArrowRightOnRectangleIcon } from "@heroicons/react/24/outline";
import AppLayout from "../components/layout/AppLayout";
import { useAuth } from "../../app/providers/AuthProvider";
import { useNavigate } from "react-router-dom";
import { useMemo } from "react";
import type { CollapseProps } from "antd";
import { Collapse, Button, Switch } from "antd";
import { message } from "antd";

const SettingsPage = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  // Ítems del Collapse para "Cuenta"
  const cuentaItems: CollapseProps["items"] = useMemo(() => {
    const perfilChildren = (
      <div className="space-y-3 pt-2">
        <div>
          <p className="text-xs text-gray-500">Nombre</p>
          <p className="text-sm font-medium">{user?.name ?? "—"}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Correo</p>
          <p className="text-sm font-medium">{user?.email ?? "—"}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Rol</p>
          <p className="text-sm font-medium capitalize">{user?.role ?? "—"}</p>
        </div>
      </div>
    );

    const passwordChildren = (
      <div className="space-y-3 pt-2 text-sm text-gray-600">
        <p>
          Para actualizar tu contraseña te enviaremos un correo con un enlace de recuperación.
          Presiona el botón para recibir las instrucciones en tu bandeja de entrada.
        </p>
        <Button
          type="primary"
          size="middle"
          onClick={() => message.info("Pronto recibirás un correo con el enlace para actualizar tu contraseña.")}
        >
          Enviar enlace de recuperación
        </Button>
      </div>
    );

    const seguridadChildren = (
      <div className="space-y-3 pt-2">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium">Autenticación en dos pasos</p>
            <p className="text-xs text-gray-500">
              Añade una capa extra de seguridad a tu cuenta.
            </p>
          </div>
          <Switch /* TODO: wirear estado real de 2FA */ />
        </div>
        <div className="text-xs text-gray-500">
          Puedes usar app de autenticación o códigos de respaldo.
        </div>
      </div>
    );

    return [
      { key: "perfil", label: "Datos del perfil", children: perfilChildren },
      { key: "password", label: "Cambiar contraseña", children: passwordChildren },
      { key: "seguridad", label: "Seguridad", children: seguridadChildren },
    ];
  }, [user]);

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
        {/* Cuenta con Collapse de AntD */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h2 className="text-sm font-semibold text-gray-800">Cuenta</h2>
          <p className="text-xs text-gray-500 mt-1">
            Correo, contraseña y seguridad.
          </p>

          <div className="mt-3">
            <Collapse
              items={cuentaItems}
              defaultActiveKey={["perfil"]}
              bordered={false}
            />
          </div>
        </div>

        {/* Notificaciones (deja tu contenido actual o conviértelo también a Collapse si quieres) */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h2 className="text-sm font-semibold text-gray-800">Notificaciones</h2>
          <p className="text-xs text-gray-500 mt-1">
            Push, correo y recordatorios.
          </p>
          {/* TODO: switches y preferencias de notificaciones */}
        </div>

        {/* Cerrar sesión */}
        <div className="bg-white rounded-xl shadow-sm p-4 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-semibold text-gray-800">Cerrar sesión</h2>
            <p className="text-xs text-gray-500 mt-1">
              Cierra tu sesión actual de forma segura.
            </p>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700"
          >
            <ArrowRightOnRectangleIcon className="h-5 w-5" />
            Salir
          </button>
        </div>
      </section>
    </AppLayout>
  );
};

export default SettingsPage;
