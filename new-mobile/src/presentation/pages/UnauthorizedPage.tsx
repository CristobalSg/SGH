export default function UnauthorizedPage() {
  return (
    <div className="min-h-screen grid place-items-center bg-gray-50">
      <div className="max-w-md text-center">
        <h1 className="text-2xl font-semibold mb-2">No autorizado</h1>
        <p className="text-gray-600 mb-4">
          No tienes permisos para acceder a esta sección.
        </p>
        <a className="text-indigo-600 underline" href="/home">Volver al inicio</a>
      </div>
    </div>
  );
}
