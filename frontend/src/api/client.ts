const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiRequest<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed for ${path}`);
  }
  return response.json() as Promise<T>;
}

export { API_BASE };
