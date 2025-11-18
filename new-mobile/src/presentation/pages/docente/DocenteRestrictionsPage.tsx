import { useState } from "react";
import { Alert, message, Spin } from "antd";
import { PlusIcon } from "@heroicons/react/24/solid";
import AppLayout from "../../components/layout/AppLayout";
import RestrictionList from "../../components/docente/RestrictionList";
import AddRestrictionForm from "../../components/docente/AddRestrictionForm";

import {
  useDocenteHorarioRestrictions,
  type RestriccionHorarioInput,
  type RestriccionHorarioView,
} from "../../hooks/useDocenteHorarioRestrictions";

type FormState = {
  open: boolean;
  mode: "create" | "edit";
  target: RestriccionHorarioView | null;
};

const initialFormState: FormState = { open: false, mode: "create", target: null };

export default function DocenteRestrictionsPage() {
  const [formState, setFormState] = useState<FormState>(initialFormState);
  const {
    restricciones,
    loading,
    saving,
    pendingDelete,
    error,
    addRestriction,
    updateRestriction,
    deleteRestriction,
    refetch,
  } = useDocenteHorarioRestrictions();
  
  const openCreateModal = () => setFormState({ open: true, mode: "create", target: null });
  const openEditModal = (item: RestriccionHorarioView) =>
    setFormState({ open: true, mode: "edit", target: item });
  const closeModal = () => setFormState({ ...initialFormState });

  const handleSubmitRestriction = async (
    data: RestriccionHorarioInput,
    id?: number,
  ) => {
    try {
      if (formState.mode === "edit" && formState.target) {
        await updateRestriction(id ?? formState.target.id, data);
        message.success("Restricción actualizada correctamente.");
      } else {
        await addRestriction(data);
        message.success("Restricción guardada correctamente.");
      }
      closeModal();
    } catch (err) {
      const detail = err instanceof Error ? err.message : "Error al guardar la restricción.";
      message.error(detail);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteRestriction(id);
      message.success("Restricción eliminada.");
    } catch (err) {
      const detail = err instanceof Error ? err.message : "Error al eliminar la restricción.";
      message.error(detail);
    }
  };

  return (
    <>
      <AppLayout
        title="Restricciones"
        rightAction={
          <button
            aria-label="Agregar"
            className="flex items-center gap-1 rounded-md bg-blue-600 px-2 py-1.5 text-sm text-white transition hover:bg-blue-700"
            onClick={openCreateModal}
          >
            <PlusIcon className="h-4 w-4" />
            <span>Agregar</span>
          </button>
        }
      >
        <div className="space-y-6 px-4">
          <p className="text-sm text-gray-600">
            Define tus restricciones horarias y eventos personales a considerar
            en la generación de horarios.
          </p>

          <div className="rounded-3xl bg-white p-5 shadow-sm">
            <h2 className="mb-4 text-center text-lg font-semibold text-black">
              Lista de restricciones
            </h2>

            <div className="space-y-4">
              {error && (
                <Alert
                  type="error"
                  message="No se pudieron cargar las restricciones"
                  description={error}
                  showIcon
                  action={
                    <button
                      onClick={refetch}
                      className="text-sm font-medium text-blue-600 hover:text-blue-700"
                    >
                      Reintentar
                    </button>
                  }
                />
              )}

              {loading ? (
                <div className="py-12 text-center">
                  <Spin />
                </div>
              ) : restricciones.length === 0 ? (
                <div className="py-6 text-center text-sm text-gray-500">
                  No hay restricciones registradas.
                </div>
              ) : (
                <RestrictionList
                  restricciones={restricciones}
                  onDelete={handleDelete}
                  deletingId={pendingDelete}
                  onEdit={openEditModal}
                />
              )}
            </div>
          </div>
        </div>
      </AppLayout>

      <AddRestrictionForm
        open={formState.open}
        mode={formState.mode}
        initialValues={formState.target}
        onClose={closeModal}
        onSubmit={handleSubmitRestriction}
        saving={saving}
      />
    </>
  );
}
