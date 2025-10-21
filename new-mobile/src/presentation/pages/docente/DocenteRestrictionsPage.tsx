import React, { useState } from "react";
import AppLayout from "../../components/layout/AppLayout";
import RestrictionList from "../../components/docente/RestrictionList";
import { PlusIcon } from "@heroicons/react/24/solid";
import AddRestrictionForm from "../../components/docente/AddRestrictionForm";

export default function DocenteRestrictionsPage() {
  const [modalOpen, setModalOpen] = useState(false);
  const [restricciones, setRestricciones] = useState<any[]>([]);

  const handleAddRestriction = (newRestriction: any) => {
    setRestricciones([
      ...restricciones,
      { ...newRestriction, id: String(Date.now()) },
    ]);
  };

  const handleDelete = (id?: string) => {
    setRestricciones(restricciones.filter((r) => r.id !== id));
  };

  return (
    <>
      <AppLayout
        title="Restricciones"
        rightAction={
          <button
            aria-label="Agregar"
            className="flex items-center gap-1 rounded-md bg-blue-600 text-white px-2 py-1.5 text-sm hover:bg-blue-700 transition"
            onClick={() => setModalOpen(true)}
          >
            <PlusIcon className="w-4 h-4" />
            <span>Agregar</span>
          </button>
        }
      >
        <div className="space-y-6 px-4">
          <p className="text-sm text-gray-600">
            Define tus restricciones horarias y eventos personales a considerar
            en la generación de horarios.
          </p>

          <div className="rounded-xl bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold mb-4 text-black text-center">
              Lista de restricciones
            </h2>

            <RestrictionList
              restricciones={restricciones}
              onDelete={handleDelete}
            />
          </div>
        </div>
      </AppLayout>

      <AddRestrictionForm
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleAddRestriction}
      />
    </>
  );
}
