import BottomNav from "../components/BottomNav";
import ScheduleTable from "../components/Schedule/ScheduleTable";

const HomePage: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="max-w-md mx-auto px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-800">Inicio</h1>
        </div>
      </header>

      <main className="flex-1 mt-14 mb-16 px-4 max-w-md mx-auto overflow-y-auto">
        <div className="flex flex-col gap-4">
          <h2 className="text-xl font-bold text-gray-900">Bienvenido a tu App</h2>
          <p className="text-gray-700 text-sm">
            Este es un layout móvil con Tailwind y Ant Design.
          </p>

          <ScheduleTable />
        </div>
      </main>

      <BottomNav />
    </div>
  );
};

export default HomePage;
