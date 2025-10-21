// src/infrastructure/http/httpClient.ts
import axios from "axios";

const API_URL = "https://sgh.inf.uct.cl/api";

export const http = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Manejo del token (único lugar donde se toca el header)
export const setAuthToken = (token: string | null) => {
  if (token) http.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete http.defaults.headers.common["Authorization"];
};
