import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./presentation/pages/LoginPage";
import HomePage from "./presentation/pages/HomePage";
import StatsPage from "./presentation/pages/StatsPage"; // si lo usas aún
import ProfilePage from "./presentation/pages/ProfilePage";
import SettingsPage from "./presentation/pages/SettingsPage";
import EventsPage from "./presentation/pages/EventsPage";

import { AuthProvider } from "./app/providers/AuthProvider";
import PrivateRoute from "./presentation/routes/PrivateRoute";
import PublicRoute from "./presentation/routes/PublicRoute";
import RoleRoute from "./presentation/routes/RoleRoute";

import DocenteSchedulePage from "./presentation/pages/docente/DocenteSchedulePage";
import DocenteRestrictionsPage from "./presentation/pages/docente/DocenteRestrictionsPage";
import UnauthorizedPage from "./presentation/pages/UnauthorizedPage";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Redirección inicial */}
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Público */}
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />

          {/* No autorizado */}
          <Route path="/unauthorized" element={<UnauthorizedPage />} />

          {/* Docente */}
          <Route
            path="/home"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <HomePage />
                </RoleRoute>
              </PrivateRoute>
            }
          />
          <Route
            path="/schedule"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <DocenteSchedulePage />
                </RoleRoute>
              </PrivateRoute>
            }
          />
          <Route
            path="/restrictions"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <DocenteRestrictionsPage />
                </RoleRoute>
              </PrivateRoute>
            }
          />
          <Route
            path="/events"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <EventsPage />
                </RoleRoute>
              </PrivateRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <SettingsPage />
                </RoleRoute>
              </PrivateRoute>
            }
          />

          {/* Si aún tienes estas: protégelas por rol que corresponda o elimínalas */}
          <Route
            path="/stats"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <StatsPage />
                </RoleRoute>
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <RoleRoute allowed={["docente"]}>
                  <ProfilePage />
                </RoleRoute>
              </PrivateRoute>
            }
          />

          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
