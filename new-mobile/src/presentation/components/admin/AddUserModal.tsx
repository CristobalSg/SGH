import { useState } from "react";
import { Modal, Input, Select, message } from "antd";
import { useRegisterUser } from "../../hooks/useRegisterUser";

const { Option } = Select;

export default function AddUserModal({ visible, onClose, onSuccess }: {
  visible: boolean;
  onClose: () => void;
  onSuccess: () => void;
}) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "docente",
  });

  const { createUser, loading } = useRegisterUser();

  const handleChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    if (!form.name || !form.email || !form.password) {
      message.warning("Completa todos los campos");
      return;
    }

    try {
      await createUser(form);
      message.success("Usuario registrado correctamente");
      onSuccess();
      onClose();
    } catch {
      message.error("Error al registrar el usuario");
    }
  };

  return (
    <Modal
      open={visible}
      onCancel={onClose}
      onOk={handleSubmit}
      confirmLoading={loading}
      okText="Registrar"
      cancelText="Cancelar"
      title="Agregar nuevo usuario"
    >
      <div className="space-y-3">
        <Input
          placeholder="Nombre completo"
          value={form.name}
          onChange={(e) => handleChange("name", e.target.value)}
        />
        <Input
          placeholder="Correo electrónico"
          type="email"
          value={form.email}
          onChange={(e) => handleChange("email", e.target.value)}
        />
        <Input.Password
          placeholder="Contraseña"
          value={form.password}
          onChange={(e) => handleChange("password", e.target.value)}
        />
        <Select
          value={form.role}
          onChange={(value) => handleChange("role", value)}
          className="w-full"
        >
          <Option value="admin">Administrador</Option>
          <Option value="docente">Docente</Option>
          <Option value="estudiante">Estudiante</Option>
        </Select>
      </div>
    </Modal>
  );
}
