import { useState, useCallback } from "react";
import { expensesApi } from "../api/expensesApi";

export function useInsights() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchInsights = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await expensesApi.getInsights();
      setInsights(res.insights);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { insights, loading, error, fetchInsights };
}
