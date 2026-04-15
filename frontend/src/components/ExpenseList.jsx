import ExpenseItem from "./ExpenseItem";

export default function ExpenseList({ expenses, loading, error, onDelete }) {
  return (
    <div className="glass-panel" style={{ padding: "1.5rem" }}>
      <h2>📋 All Expenses</h2>
      {loading && (
        <div className="text-center mt-4">
          <div className="loader" />
        </div>
      )}
      {error && <p className="error-text">Failed to load expenses: {error}</p>}
      {!loading && !error && expenses.length === 0 && (
        <p style={{ color: "var(--text-secondary)", textAlign: "center", padding: "2rem 0" }}>
          No expenses yet. Add your first one! 💸
        </p>
      )}
      {!loading &&
        expenses.map((expense) => (
          <ExpenseItem key={expense.id} expense={expense} onDelete={onDelete} />
        ))}
    </div>
  );
}
