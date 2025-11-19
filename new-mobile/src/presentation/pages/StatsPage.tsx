import BottomNav from "../components/BottomNav";

const StatsPage = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="max-w-md mx-auto px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-800">Estadísticas</h1>
        </div>
      </header>

      <main className="flex-1 mt-14 mb-16 px-4 max-w-md mx-auto">
        <p className="text-gray-700 text-sm mt-4">
          Aquí podrás ver tus estadísticas, métricas o gráficos.
        </p>
      </main>

      {/* Barra de navegación inferior */}
      <BottomNav />
    </div>
  );
};

export default StatsPage;
