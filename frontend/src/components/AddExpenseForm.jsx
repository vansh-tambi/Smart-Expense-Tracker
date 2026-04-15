import { useState } from "react";
import { Plus, Check } from "lucide-react";

const CATEGORIES = [
  "Food",
  "Transport",
  "Shopping",
  "Entertainment",
  "Health",
  "Utilities",
  "Education",
  "Other",
];

const today = () => new Date().toISOString().split("T")[0];

export default function AddExpenseForm({ onAdd }) {
  const [form, setForm] = useState({
    amount: "",
    category: "",
    date: today(),
    note: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(false);
    try {
      await onAdd({ ...form, amount: parseFloat(form.amount) });
      setForm({ amount: "", category: "", date: today(), note: "" });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 2500);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h2>New Expense</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="amount">Amount ($)</label>
            <input
              id="amount"
              name="amount"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              value={form.amount}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={form.category}
              onChange={handleChange}
              required
            >
              <option value="">Select category</option>
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="date">Date</label>
            <input
              id="date"
              name="date"
              type="date"
              value={form.date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="note">Note</label>
            <input
              id="note"
              name="note"
              type="text"
              placeholder="e.g. Lunch with team"
              value={form.note}
              onChange={handleChange}
            />
          </div>

          {error && <p className="msg-error">{error}</p>}
          {success && (
            <p className="msg-success">
              <Check size={14} /> Added
            </p>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            id="add-expense-btn"
            disabled={submitting}
            style={{ width: "100%", marginTop: "0.35rem" }}
          >
            {submitting ? (
              "Adding…"
            ) : (
              <>
                <Plus size={16} /> Add Expense
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
