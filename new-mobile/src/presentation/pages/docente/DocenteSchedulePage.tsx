import AppLayout from "../../components/layout/AppLayout";

export default function DocenteSchedulePage() {
  return (
    <AppLayout title="Horario">
      <div className="space-y-4">
        <p className="text-sm text-gray-600">
          Vista detallada del horario del semestre.
        </p>
        {/* TODO: componente ScheduleTable responsivo + filtros */}
        <div className="rounded-xl bg-white p-4 shadow-sm">Tabla de horario aquí</div>
      </div>
    </AppLayout>
  );
}
