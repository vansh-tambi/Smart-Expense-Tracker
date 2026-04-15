import { getCategoryMeta } from "./categoryMeta";
import { Trash2 } from "lucide-react";

export default function ExpenseItem({ expense, onDelete, index = 0 }) {
  const meta = getCategoryMeta(expense.category);
  const Icon = meta.icon;

  return (
    <div className="expense-row slide-up" style={{ animationDelay: `${index * 40}ms` }}>
      {/* Category icon */}
      <div className="category-dot" style={{ background: meta.bg }}>
        <Icon size={18} color={meta.color} strokeWidth={1.8} />
      </div>

      {/* Details */}
      <div className="expense-details">
        <div className="expense-note">{expense.note || expense.category}</div>
        <div className="expense-sub">
          {expense.category} · {expense.date}
        </div>
      </div>

      {/* Amount */}
      <span className="expense-amount">
        ${parseFloat(expense.amount).toFixed(2)}
      </span>

      {/* Delete — revealed on hover */}
      <button
        className="btn btn-danger-ghost"
        id={`delete-expense-${expense.id}`}
        onClick={() => onDelete(expense.id)}
        title="Delete"
      >
        <Trash2 size={14} />
      </button>
    </div>
  );
}
