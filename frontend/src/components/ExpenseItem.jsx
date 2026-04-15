export default function ExpenseItem({ expense, onDelete }) {
  return (
    <div className="expense-item">
      <div className="expense-info">
        <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: "0.4rem" }}>
          <span className="badge">{expense.category}</span>
          <span className="expense-title">{expense.note || "No note"}</span>
        </div>
        <span className="expense-meta">{expense.date}</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
        <span className="expense-amount">${parseFloat(expense.amount).toFixed(2)}</span>
        <button
          className="danger"
          id={`delete-expense-${expense.id}`}
          onClick={() => onDelete(expense.id)}
          title="Delete expense"
          style={{ padding: "0.4rem 0.8rem", fontSize: "0.85rem" }}
        >
          ✕
        </button>
      </div>
    </div>
  );
}
