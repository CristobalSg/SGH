// src/presentation/components/EventModal.tsx
import React, { useEffect } from "react";
import { Modal, Button, Form, Input, TimePicker, Badge } from "antd";
import dayjs, { Dayjs } from "dayjs";
import { PlusCircleIcon } from "@heroicons/react/24/outline";
import type { EventItem } from "../../viewmodels/useEventsVM";
import EventList from "./EventList";

type FormValues = { title: string; description?: string; time?: Dayjs | null };

type Props = {
  open: boolean;
  dateLabel: string;
  events: EventItem[];
  editingItem: EventItem | null;
  onCancel: () => void;
  onUpsert: (data: { id?: string; title: string; description?: string; time?: string }) => void;
  onEdit: (item: EventItem) => void;
  onDelete: (id: string) => void;
};

const EventModal: React.FC<Props> = ({
  open,
  dateLabel,
  events,
  editingItem,
  onCancel,
  onUpsert,
  onEdit,
  onDelete,
}) => {
  const [form] = Form.useForm<FormValues>();

  // Cargar datos al comenzar edición
  useEffect(() => {
    if (editingItem) {
      form.setFieldsValue({
        title: editingItem.title,
        description: editingItem.description,
        time: editingItem.time ? dayjs(editingItem.time, "HH:mm") : null,
      });
    } else {
      form.resetFields();
    }
  }, [editingItem, form]);

  const submit = async () => {
    const values = await form.validateFields();
    onUpsert({
      id: editingItem?.id,
      title: values.title,
      description: values.description,
      time: values.time ? dayjs(values.time).format("HH:mm") : undefined,
    });
    form.resetFields();
  };

  return (
    <Modal
      open={open}
      onCancel={onCancel}
      title={
        <div className="flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-sm text-gray-500">Eventos para</span>
            <span className="text-base font-semibold">{dateLabel}</span>
          </div>
          <Badge count={events.length} />
        </div>
      }
      footer={
        <div className="flex items-center justify-between w-full">
          <Button onClick={onCancel}>Cerrar</Button>
          <Button type="primary" icon={<PlusCircleIcon className="h-4 w-4" />} onClick={submit}>
            {editingItem ? "Guardar cambios" : "Agregar evento"}
          </Button>
        </div>
      }
    >
      <Form form={form} layout="vertical" className="mb-4" initialValues={{ title: "", description: "", time: null }}>
        <Form.Item label="Título" name="title" rules={[{ required: true, message: "Ingresa un título" }]}>
          <Input placeholder="Ej. Reunión, Cumpleaños, Tarea..." />
        </Form.Item>
        <Form.Item label="Descripción" name="description">
          <Input.TextArea placeholder="Detalles opcionales" autoSize={{ minRows: 2, maxRows: 4 }} />
        </Form.Item>
        <Form.Item label="Hora" name="time">
          <TimePicker format="HH:mm" minuteStep={5} />
        </Form.Item>
      </Form>

      <EventList events={events} onEdit={onEdit} onDelete={onDelete} />
    </Modal>
  );
};

export default EventModal;
