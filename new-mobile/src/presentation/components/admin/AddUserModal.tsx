import React, { useEffect, useMemo, useState } from "react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { AxiosError } from "axios";
import { useRegisterUser } from "../../hooks/useRegisterUser";

type Props = {
  visible: boolean;
  onClose: () => void;
  onSuccess: () => void;
};

const roles = [
  { label: "Docente", value: "docente" },
  { label: "Estudiante", value: "estudiante" },
  { label: "Administrador", value: "admin" },
];

// Config: mínimo de contraseña
const MIN_PASSWORD = 12;

type FieldErrors = Partial<Record<"name" | "email" | "password" | "role", string>> & {
  // Puede venir un string o múltiples mensajes desde detail[]
  general?: string | string[];
};

export default function AddUserModal({ visible, onClose, onSuccess }: Props) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "docente",
  });
  const [errors, setErrors] = useState<FieldErrors>({});
  const { createUser, loading } = useRegisterUser();

  useEffect(() => {
    if (!visible) {
      setForm({ name: "", email: "", password: "", role: "docente" });
      setErrors({});
    }
  }, [visible]);

  // Validador de email con mensajes útiles
  function emailClientError(email: string): string | null {
    const trimmed = email.trim();
    if (!trimmed) return "Ingresa un correo.";
    if (!trimmed.includes("@")) return "Falta el símbolo @. Ej: nombre@empresa.com";
    const [local, domain] = trimmed.split("@");
    if (!local || !domain) return "Falta el dominio. Ej: nombre@empresa.com";
    if (!domain.includes(".")) return "El dominio debe contener un punto. Ej: empresa.com";
    const basic = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
    return basic ? null : "Correo inválido. Ej: nombre@empresa.com";
  }

  const emailOk = useMemo(() => !emailClientError(form.email), [form.email]);

  const canSubmit = useMemo(() => {
    return (
      form.name.trim().length >= 2 &&
      emailOk &&
      form.password.length >= MIN_PASSWORD &&
      !!form.role &&
      !loading
    );
  }, [form, emailOk, loading]);

  const setField =
    (key: keyof typeof form) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      const value = e.target.value;
      setForm((s) => ({ ...s, [key]: value }));

      // Feedback inmediato por campo
      setErrors((prev) => {
        const next = { ...prev, [key]: undefined, general: undefined };
        if (key === "email") {
          const err = emailClientError(value);
          if (err) next.email = err;
        }
        if (key === "password" && value.length < MIN_PASSWORD) {
          next.password = `La contraseña debe tener al menos ${MIN_PASSWORD} caracteres.`;
        }
        if (key === "name" && value.trim().length < 2) {
          next.name = "Ingresa un nombre válido.";
        }
        return next;
      });
    };

  function validateClient(): FieldErrors {
    const fe: FieldErrors = {};
    if (form.name.trim().length < 2) fe.name = "Ingresa un nombre válido.";
    const mailErr = emailClientError(form.email);
    if (mailErr) fe.email = mailErr;
    if (form.password.length < MIN_PASSWORD) {
      fe.password = `La contraseña debe tener al menos ${MIN_PASSWORD} caracteres.`;
    }
    if (!form.role) fe.role = "Selecciona un rol.";
    return fe;
  }

  // Intenta mapear errores de validación tipo FastAPI/Pydantic: { detail: [{ loc: [...], msg, type }] }
  function mapApiErrors(err: unknown): FieldErrors {
    const fe: FieldErrors = {};
    const ax = err as AxiosError<any>;
    const data = ax?.response?.data;

    const details = Array.isArray(data?.detail) ? data.detail : [];
    const generalMessages: string[] = [];

    for (const d of details) {
      const loc = Array.isArray(d?.loc) ? d.loc : [];
      const last = String(loc[loc.length - 1] ?? "");
      const key = last.toLowerCase();
      const msg = typeof d?.msg === "string" ? d.msg : undefined;
      if (!msg) continue;

      // Mapeo flexible de nombres de campo
      if (["name", "nombre"].includes(key)) fe.name = msg;
      else if (["email", "correo"].includes(key)) fe.email = msg;
      else if (["password", "contrasena", "contraseña"].includes(key)) fe.password = msg;
      else if (["role", "rol"].includes(key)) fe.role = msg;
      // Si no se reconoce el campo, muéstralo como mensaje general
      else generalMessages.push(msg);
    }

    // Si no hubo detail mapeable, intenta otros formatos comunes
    if (!Object.keys(fe).some((k) => k !== "general")) {
      if (typeof data?.message === "string") generalMessages.push(data.message);
      if (typeof data?.detail === "string") generalMessages.push(data.detail);
      if (generalMessages.length === 0 && ax?.message) generalMessages.push(ax.message);
    }

    if (generalMessages.length) fe.general = generalMessages;
    return fe;
  }

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    const clientErrors = validateClient();
    if (Object.keys(clientErrors).length) {
      setErrors(clientErrors);
      return;
    }

    try {
      await createUser({
        name: form.name.trim(),
        email: form.email.trim(),
        password: form.password,
        role: form.role,
      });
      onSuccess();
      onClose();
    } catch (err) {
      setErrors(mapApiErrors(err));
    }
  };

  if (!visible) return null;

  const baseInput =
    "block w-full rounded-lg border bg-white px-3 py-2 text-slate-900 placeholder-slate-400 outline-none transition focus:border-blue-600 focus:ring-2 focus:ring-blue-600";
  const errorInput = "border-red-400 focus:border-red-500 focus:ring-red-500";
  const normalInput = "border-slate-300";

  return (
    <div className="fixed inset-0 z-50">
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-[1px]"
        aria-hidden="true"
        onClick={onClose}
      />
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-xl ring-1 ring-black/5">
          <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
            <h3 className="text-base font-semibold text-slate-900">Agregar usuario</h3>
            <button
              onClick={onClose}
              className="rounded-md p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
              aria-label="Cerrar"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>

          <form onSubmit={onSubmit} className="px-5 pb-5 pt-4 space-y-4">
            {errors.general && (
              <div
                className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
                role="alert"
                aria-live="assertive"
              >
                {Array.isArray(errors.general) ? (
                  <ul className="list-disc space-y-1 pl-5">
                    {errors.general.map((m, i) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                ) : (
                  errors.general
                )}
              </div>
            )}

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Nombre</label>
              <input
                type="text"
                value={form.name}
                onChange={setField("name")}
                placeholder="Ej: María Gómez"
                className={`${baseInput} ${errors.name ? errorInput : normalInput}`}
                aria-invalid={!!errors.name}
                aria-describedby={errors.name ? "name-error" : undefined}
              />
              <div id="name-error" className="mt-1 text-xs text-red-600">
                {errors.name}
              </div>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Correo</label>
              <input
                type="email"
                value={form.email}
                onChange={setField("email")}
                placeholder="nombre@empresa.com"
                className={`${baseInput} ${errors.email ? errorInput : normalInput}`}
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : "email-hint"}
              />
              {errors.email ? (
                <div id="email-error" className="mt-1 text-xs text-red-600">{errors.email}</div>
              ) : (
                <p id="email-hint" className="mt-1 text-xs text-slate-500">
                  Asegúrate de incluir @ y un dominio válido. Ej: nombre@empresa.com
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Contraseña</label>
              <input
                type="password"
                value={form.password}
                onChange={setField("password")}
                placeholder="••••••••••••"
                className={`${baseInput} ${errors.password ? errorInput : normalInput}`}
                aria-invalid={!!errors.password}
                aria-describedby={errors.password ? "password-error" : "password-hint"}
              />
              {errors.password ? (
                <div id="password-error" className="mt-1 text-xs text-red-600">{errors.password}</div>
              ) : (
                <p id="password-hint" className="mt-1 text-xs text-slate-500">
                  Mínimo {MIN_PASSWORD} caracteres.
                </p>
              )}
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700">Rol</label>
              <select
                value={form.role}
                onChange={setField("role")}
                className={`${baseInput} ${errors.role ? errorInput : normalInput}`}
                aria-invalid={!!errors.role}
                aria-describedby={errors.role ? "role-error" : undefined}
              >
                {roles.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
              </select>
              <div id="role-error" className="mt-1 text-xs text-red-600">
                {errors.role}
              </div>
            </div>

            <div className="mt-6 flex items-center justify-end gap-3 border-t border-slate-100 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="inline-flex items-center rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={!canSubmit}
                className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600 disabled:cursor-not-allowed disabled:bg-blue-400"
              >
                {loading && (
                  <svg className="h-4 w-4 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                    />
                  </svg>
                )}
                Crear usuario
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
