import { useState, useEffect, useCallback } from "react";
import { expensesApi } from "../api/expensesApi";

export function useExpenses() {
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [expRes, sumRes] = await Promise.all([
        expensesApi.getAll(),
        expensesApi.getSummary(),
      ]);
      setExpenses(expRes.data);
      setSummary(sumRes.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  const addExpense = async (data) => {
    const res = await expensesApi.create(data);
    await fetchAll();
    return res;
  };

  const removeExpense = async (id) => {
    await expensesApi.delete(id);
    setExpenses((prev) => prev.filter((e) => e.id !== id));
    await fetchAll();
  };

  return { expenses, summary, loading, error, addExpense, removeExpense, refresh: fetchAll };
}
