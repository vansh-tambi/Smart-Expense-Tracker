const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  let json = null;
  try {
    json = await res.json();
  } catch {
    json = null;
  }

  if (!res.ok) {
    const msg =
      json?.details?.map((d) => d.message).join(", ") ||
      json?.error ||
      json?.message ||
      "Request failed";
    throw new Error(msg);
  }

  return json || {};
}

export const expensesApi = {
  getAll: () => request("/expenses/"),
  create: (data) =>
    request("/expenses/", { method: "POST", body: JSON.stringify(data) }),
  delete: (id) => request(`/expenses/${id}`, { method: "DELETE" }),
  getSummary: () => request("/expenses/summary"),
  getInsights: () => request("/expenses/insights"),
};
