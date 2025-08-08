// BASE 環境変数は http://host:port 形式を想定 (/api を含めない)。含まれていたら除去し二重 /api を防ぐ。
let rawBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
rawBase = rawBase.replace(/\/$/, '');
if (rawBase.endsWith('/api')) {
  rawBase = rawBase.slice(0, -4); // '/api' を削除
}
const BASE: string = rawBase;

async function request<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    let msg = res.statusText;
    try {
      const data = await res.json();
      msg = (data as any).detail || JSON.stringify(data);
    } catch { /* noop */ }
    throw new Error(`API Error ${res.status}: ${msg}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  listTasks: (status?: string) => request(`/api/tasks${status ? `?status=${status}` : ''}`),
  createTask: (body: unknown) => request('/api/tasks', { method: 'POST', body: JSON.stringify(body) }),
  getTask: (id: string) => request(`/api/tasks/${id}`),
  updateTask: (id: string, body: unknown) => request(`/api/tasks/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  patchTask: (id: string, body: unknown) => request(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteTask: (id: string) => request(`/api/tasks/${id}`, { method: 'DELETE' }),
};
