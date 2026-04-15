import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const client = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.data) {
      const { details, error: errorMsg, message } = error.response.data;
      const msg =
        details?.map((d) => d.message).join(", ") ||
        errorMsg ||
        message ||
        "Request failed";
      throw new Error(msg);
    }
    throw error;
  }
);




export const expensesApi = {
  getAll: () => client.get("/expenses/"),
  create: (data) => client.post("/expenses/", data),
  delete: (id) => client.delete(`/expenses/${id}`),
  getSummary: () => client.get("/expenses/summary"),
  getInsights: () => client.get("/expenses/insights"),
};
