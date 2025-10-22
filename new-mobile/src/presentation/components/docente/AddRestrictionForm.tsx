import React, { useEffect } from "react";
import dayjs from "dayjs";
import { Modal, Form, Select, TimePicker, Input, Switch } from "antd";
import type { RestriccionHorarioCreateInput, RestriccionHorarioView } from "../../hooks/useDocenteHorarioRestrictions";

const { RangePicker } = TimePicker;
const { TextArea } = Input;

interface AddRestrictionFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: RestriccionHorarioCreateInput, id?: number) => Promise<void> | void;
  saving?: boolean;
  mode?: "create" | "edit";
  initialValues?: RestriccionHorarioView | null;
}

const daysOfWeek = [
  { label: "Lunes", value: 1 },
  { label: "Martes", value: 2 },
  { label: "Miércoles", value: 3 },
  { label: "Jueves", value: 4 },
  { label: "Viernes", value: 5 },
  { label: "Sábado", value: 6 },
  { label: "Domingo", value: 0 },
];

const AddRestrictionForm: React.FC<AddRestrictionFormProps> = ({
  open,
  onClose,
  onSubmit,
  saving = false,
  mode = "create",
  initialValues = null,
}) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (!open) return;

    if (mode === "edit" && initialValues) {
      form.setFieldsValue({
        dia: initialValues.day,
        horas: [
          dayjs(initialValues.start, "HH:mm"),
          dayjs(initialValues.end, "HH:mm"),
        ],
        descripcion: initialValues.descripcion ?? "",
        disponible: initialValues.disponible,
      });
    } else {
      form.resetFields();
      form.setFieldsValue({ disponible: false });
    }
  }, [open, mode, initialValues, form]);

  const handleOk = async () => {
    const values = await form.validateFields();
    const [startTime, endTime] = values.horas;
    const payload: RestriccionHorarioCreateInput = {
      dia_semana: values.dia,
      hora_inicio: startTime.format("HH:mm:ss"),
      hora_fin: endTime.format("HH:mm:ss"),
      descripcion: values.descripcion?.trim() || undefined,
      disponible: values.disponible ?? false,
    };
    await onSubmit(payload, initialValues?.id);
    form.resetFields();
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  return (
    <Modal
      title={mode === "edit" ? "Editar Restricción" : "Agregar Restricción"}
      open={open}
      onCancel={handleCancel}
      onOk={handleOk}
      okText={mode === "edit" ? "Guardar cambios" : "Guardar"}
      confirmLoading={saving}
      centered
      bodyStyle={{ paddingBottom: 0 }}
    >
      <Form
        form={form}
        layout="vertical"
        className="space-y-3"
        style={{ marginTop: 10 }}
        initialValues={{ disponible: false }}
      >
        <Form.Item
          label="Día de la semana"
          name="dia"
          rules={[{ required: true, message: "Selecciona un día" }]}
        >
          <Select
            placeholder="Selecciona un día"
            options={daysOfWeek}
            optionFilterProp="label"
          />
        </Form.Item>

        <Form.Item
          label="Hora de inicio y fin"
          name="horas"
          rules={[{ required: true, message: "Selecciona un rango de horas" }]}
        >
          <RangePicker format="HH:mm" minuteStep={5} style={{ width: "100%" }} />
        </Form.Item>

        <Form.Item
          label="Descripción"
          name="descripcion"
        >
          <TextArea rows={2} placeholder="Motivo o detalle de la restricción" />
        </Form.Item>

        <Form.Item
          label="Disponibilidad"
          name="disponible"
          valuePropName="checked"
        >
          <Switch checkedChildren="Disponible" unCheckedChildren="No disponible" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddRestrictionForm;
