import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";

interface PublicRouteProps { children: React.ReactNode; }

const PublicRoute: React.FC<PublicRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div style={{ padding: 24 }}>Verificando sesión…</div>;
  if (isAuthenticated) return <Navigate to="/home" replace />;

  return <>{children}</>;
};

export default PublicRoute;
