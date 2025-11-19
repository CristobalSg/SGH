import React, { useEffect } from "react";
import dayjs from "dayjs";
import { Modal, Form, Select, TimePicker, Input, Switch } from "antd";
import type { RestriccionHorarioInput, RestriccionHorarioView } from "../../hooks/useDocenteHorarioRestrictions";
import { useAuth } from "../../../app/providers/AuthProvider";

const { RangePicker } = TimePicker;
const { TextArea } = Input;

interface AddRestrictionFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: RestriccionHorarioInput, id?: number) => Promise<void> | void;
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
  const { user } = useAuth();

  useEffect(() => {
    if (!open) return;

    if (mode === "edit" && initialValues) {
      form.setFieldsValue({
        dia: initialValues.dia_semana,
        horas: [
          // Parse ISO timestamps (hora_inicio / hora_fin) into dayjs objects for the TimePicker
          dayjs(initialValues.hora_inicio),
          dayjs(initialValues.hora_fin),
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

  if (!user?.id) {
    throw new Error("Usuario no autenticado");
  }

  const payload: RestriccionHorarioInput = {
    dia_semana: Number(values.dia),
    hora_inicio: horaToBackendFormat(startTime),
    hora_fin: horaToBackendFormat(endTime),
    descripcion: values.descripcion?.trim() || "",
    disponible: !!values.disponible,
    activa: true,
    user_id: Number(user.id),
  };
  await onSubmit(payload, initialValues?.id);
  form.resetFields();
};

function horaToBackendFormat(hora: dayjs.Dayjs): string {
  return hora.format("HH:mm:ss");
}


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
      style={{ paddingBottom: 0 }}
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
