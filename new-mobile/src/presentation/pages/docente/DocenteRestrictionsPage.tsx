import AppLayout from "../../components/layout/AppLayout";

export default function DocenteRestrictionsPage() {
  return (
    <AppLayout title="Restricciones">
      <div className="space-y-4">
        <p className="text-sm text-gray-600">
          Define tus restricciones horarias y eventos personales a considerar en la generación de horarios.
        </p>
        {/* TODO: formulario + lista de restricciones */}
        <div className="rounded-xl bg-white p-4 shadow-sm">Formulario de restricciones</div>
      </div>
    </AppLayout>
  );
}
