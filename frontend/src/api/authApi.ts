import { API_BASE, apiRequest } from "./client";
import type { AuthStatus } from "../types";

export function getLoginUrl(): string {
  return `${API_BASE}/auth/callback?code=demo-code`;
}

export function fetchAuthStatus() {
  return apiRequest<AuthStatus>("/debug/auth-status");
}
