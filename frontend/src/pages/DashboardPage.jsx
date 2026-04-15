import { useState } from "react";
import { useExpenses } from "../hooks/useExpenses";
import AddExpenseForm from "../components/AddExpenseForm";
import ExpenseList from "../components/ExpenseList";
import CategorySummary from "../components/CategorySummary";
import InsightsPanel from "../components/InsightsPanel";
import { Wallet, TrendingUp, ReceiptText } from "lucide-react";

export default function DashboardPage() {
  const { expenses, summary, loading, error, addExpense, removeExpense } =
    useExpenses();
  const [insightsTrigger, setInsightsTrigger] = useState(0);

  const handleAdd = async (data) => {
    await addExpense(data);
    setInsightsTrigger((n) => n + 1);
  };

  const handleDelete = async (id) => {
    await removeExpense(id);
    setInsightsTrigger((n) => n + 1);
  };

  // Derived stats
  const totalSpent = expenses.reduce((s, e) => s + e.amount, 0);
  const categoryCount = new Set(expenses.map((e) => e.category)).size;

  return (
    <div className="app-shell">
      {/* Header */}
      <header className="app-header">
        <h1>Expense Tracker</h1>
        <p>Track spending, surface patterns, spend smarter.</p>
      </header>

      {/* Summary stat cards */}
      <div className="summary-row">
        <div className="stat-card slide-up" style={{ animationDelay: '0ms' }}>
          <div
            className="stat-icon"
            style={{ background: "rgba(79,142,247,0.12)" }}
          >
            <Wallet size={20} color="#4f8ef7" />
          </div>
          <div className="stat-content">
            <span className="stat-value">${totalSpent.toFixed(2)}</span>
            <span className="stat-label">Total Spent</span>
          </div>
        </div>

        <div className="stat-card slide-up" style={{ animationDelay: '100ms' }}>
          <div
            className="stat-icon"
            style={{ background: "rgba(52,211,153,0.12)" }}
          >
            <TrendingUp size={20} color="#34d399" />
          </div>
          <div className="stat-content">
            <span className="stat-value">{categoryCount}</span>
            <span className="stat-label">Categories</span>
          </div>
        </div>

        <div className="stat-card slide-up" style={{ animationDelay: '200ms' }}>
          <div
            className="stat-icon"
            style={{ background: "rgba(251,191,36,0.12)" }}
          >
            <ReceiptText size={20} color="#fbbf24" />
          </div>
          <div className="stat-content">
            <span className="stat-value">{expenses.length}</span>
            <span className="stat-label">Transactions</span>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="main-grid">
        {/* Left: expense list */}
        <ExpenseList
          expenses={expenses}
          loading={loading}
          error={error}
          onDelete={handleDelete}
        />

        {/* Right sidebar */}
        <div className="right-col">
          <AddExpenseForm onAdd={handleAdd} />
          <CategorySummary summary={summary} />
          <InsightsPanel refreshTrigger={insightsTrigger} />
        </div>
      </div>
    </div>
  );
}
