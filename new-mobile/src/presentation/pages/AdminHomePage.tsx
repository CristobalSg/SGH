import AppLayout from "../components/layout/AppLayout";

export default function AdminHomePage() {
  return (
    <AppLayout title="Inicio" showBottomNav>
      <div className="space-y-4 py-4">
        <section className="rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
          <h2 className="text-base font-semibold text-gray-900">Panel del administrador</h2>
          <p className="mt-2 text-sm text-gray-600">
            Usa esta vista para tener un vistazo general del sistema y acceder rápidamente
            a las herramientas de gestión. Desde la pestaña Usuarios podrás revisar y
            administrar las restricciones de cada docente.
          </p>
        </section>
      </div>
    </AppLayout>
  );
}
