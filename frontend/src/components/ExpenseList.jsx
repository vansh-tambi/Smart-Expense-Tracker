import ExpenseItem from "./ExpenseItem";

export default function ExpenseList({ expenses, loading, error, onDelete }) {
  return (
    <div className="card">
      <div className="card-body">
        <div className="expense-list-header">
          <h2>Transactions</h2>
          {expenses.length > 0 && (
            <span className="expense-count">{expenses.length} items</span>
          )}
        </div>

        {loading && (
          <div className="empty-state">
            <div className="loader" />
          </div>
        )}

        {error && <p className="msg-error">Failed to load: {error}</p>}

        {!loading && !error && expenses.length === 0 && (
          <div className="empty-state slide-up">No expenses yet. Add one to get started.</div>
        )}

        {!loading &&
          expenses.map((expense, i) => (
            <ExpenseItem
              key={expense.id}
              expense={expense}
              onDelete={onDelete}
              index={i}
            />
          ))}
      </div>
    </div>
  );
}
