// src/App.tsx
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "./presentation/pages/LoginPage";
import HomePage from "./presentation/pages/HomePage";
import StatsPage from "./presentation/pages/StatsPage";
import ProfilePage from "./presentation/pages/ProfilePage";
import SettingsPage from "./presentation/pages/SettingsPage";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./presentation/routes/PrivateRoute";
import EventsPage from "./presentation/pages/EventsPage";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Redirección inicial */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Login */}
          <Route path="/login" element={<LoginPage />} />

          {/* Home protegido */}
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <HomePage />
              </PrivateRoute>
            }
          />

          <Route 
            path="/stats" 
            element={
            <PrivateRoute>
              <StatsPage />
            </PrivateRoute>
          } />
          
          <Route 
            path="/profile" 
            element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          } />
          
          <Route 
            path="/settings" 
            element={
            <PrivateRoute>
              <SettingsPage />
            </PrivateRoute>
          } />

          <Route 
            path="/events" 
            element={
            <PrivateRoute>
              <EventsPage/>
            </PrivateRoute>
          } />
          

          {/* Ruta no encontrada */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
