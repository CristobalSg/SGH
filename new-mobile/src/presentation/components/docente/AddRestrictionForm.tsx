import React from "react";
import { Modal, Form, Select, TimePicker, Input } from "antd";

const { RangePicker } = TimePicker;
const { TextArea } = Input;
const { Option } = Select;

interface AddRestrictionFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: any) => void;
}

const daysOfWeek = [
  "Lunes",
  "Martes",
  "Miércoles",
  "Jueves",
  "Viernes",
  "Sábado",
  "Domingo",
];

const AddRestrictionForm: React.FC<AddRestrictionFormProps> = ({
  open,
  onClose,
  onSubmit,
}) => {
  const [form] = Form.useForm();

  const handleOk = () => {
    form.validateFields().then((values) => {
      const [startTime, endTime] = values.horas;
      const newRestriction = {
        dayOfWeek: values.dia,
        startTime: startTime.format("HH:mm"),
        endTime: endTime.format("HH:mm"),
        descripcion: values.descripcion,
      };
      onSubmit(newRestriction);
      form.resetFields();
      onClose();
    });
  };

  return (
    <Modal
      title="Agregar Restricción"
      open={open}
      onCancel={onClose}
      onOk={handleOk}
      okText="Guardar"
      centered
      bodyStyle={{ paddingBottom: 0 }}
    >
      <Form
        form={form}
        layout="vertical"
        className="space-y-3"
        style={{ marginTop: 10 }}
      >
        <Form.Item
          label="Día de la semana"
          name="dia"
          rules={[{ required: true, message: "Selecciona un día" }]}
        >
          <Select placeholder="Selecciona un día">
            {daysOfWeek.map((d) => (
              <Option key={d} value={d}>
                {d}
              </Option>
            ))}
          </Select>
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
          rules={[{ required: true, message: "Agrega una descripción" }]}
        >
          <TextArea rows={2} placeholder="Motivo o detalle de la restricción" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default AddRestrictionForm;
