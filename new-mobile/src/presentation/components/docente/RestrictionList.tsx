import React from "react";
import { Button, Input, List, Skeleton } from "antd";
import { PencilSquareIcon, TrashIcon } from "@heroicons/react/24/solid";

interface RestrictionType {
  id?: string;
  dayOfWeek: string;
  startTime: string;
  endTime: string;
  descripcion?: string;
  loading?: boolean;
}

interface RestrictionListProps {
  restricciones: RestrictionType[];
  onDelete?: (id?: string) => void;
}

const RestrictionList: React.FC<RestrictionListProps> = ({
  restricciones = [],
  onDelete,
}) => {
  const handleDelete = (id?: string) => {
    if (onDelete) onDelete(id);
  };

  return (
    <div className="space-y-4">
      <List
        className="demo-loadmore-list"
        itemLayout="horizontal"
        dataSource={restricciones}
        locale={{ emptyText: "No hay restricciones registradas" }}
        renderItem={(item, index) => (
          <List.Item
            key={index}
            className="flex justify-between items-center"
            actions={[
               <button
                key="edit"
                className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
              >
                <PencilSquareIcon className="w-5 h-5" />
                Editar
              </button>,
              <button
                key="delete"
                onClick={() => handleDelete(item.id)}
                className="text-red-600 hover:text-red-800 flex items-center gap-1"
              >
                <TrashIcon className="w-5 h-5" />
                Eliminar
              </button>,
            ]}
          >
            <Skeleton title={false} loading={item.loading} active>
              <div className="flex flex-col">
                <span className="text-gray-800 font-medium">
                  Día: {item.dayOfWeek}
                </span>
                <span className="text-gray-600 text-sm">
                  Hora de inicio: {item.startTime}
                </span>
                <span className="text-gray-600 text-sm">
                  Hora de fin: {item.endTime}
                </span>
                {item.descripcion && (
                  <span className="text-gray-600 text-sm">
                    Descripción: {item.descripcion}
                  </span>
                )}
              </div>
            </Skeleton>
          </List.Item>
        )}
      />
    </div>
  );
};

export default RestrictionList;
