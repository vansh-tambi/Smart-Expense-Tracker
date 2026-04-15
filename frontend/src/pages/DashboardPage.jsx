import { useState } from "react";
import { useExpenses } from "../hooks/useExpenses";
import AddExpenseForm from "../components/AddExpenseForm";
import ExpenseList from "../components/ExpenseList";
import CategorySummary from "../components/CategorySummary";
import InsightsPanel from "../components/InsightsPanel";

export default function DashboardPage() {
  const { expenses, summary, loading, error, addExpense, removeExpense } = useExpenses();
  const [insightsTrigger, setInsightsTrigger] = useState(0);

  const handleAdd = async (data) => {
    await addExpense(data);
    setInsightsTrigger((n) => n + 1); // Trigger insights refresh after new expense
  };

  const handleDelete = async (id) => {
    await removeExpense(id);
    setInsightsTrigger((n) => n + 1);
  };

  return (
    <div className="container">
      {/* Header */}
      <header style={{ marginBottom: "2.5rem", textAlign: "center" }}>
        <h1>💰 Smart Expense Tracker</h1>
        <p className="subtitle">Track your spending. Understand your habits. Save smarter.</p>
      </header>

      {/* Main Grid */}
      <div className="grid-dashboard">
        {/* Left Column: list + add form */}
        <div className="stack-group">
          <ExpenseList
            expenses={expenses}
            loading={loading}
            error={error}
            onDelete={handleDelete}
          />
        </div>

        {/* Right Column: form + summary + insights */}
        <div className="stack-group">
          <AddExpenseForm onAdd={handleAdd} />
          <CategorySummary summary={summary} />
          <InsightsPanel refreshTrigger={insightsTrigger} />
        </div>
      </div>
    </div>
  );
}
