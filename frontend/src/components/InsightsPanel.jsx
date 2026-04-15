import { useEffect } from "react";
import { useInsights } from "../hooks/useInsights";

export default function InsightsPanel({ refreshTrigger }) {
  const { insights, loading, error, fetchInsights } = useInsights();

  useEffect(() => {
    fetchInsights();
  }, [refreshTrigger, fetchInsights]);

  return (
    <div className="glass-panel" style={{ padding: "1.5rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2>🤖 AI Insights</h2>
        <button
          id="refresh-insights-btn"
          onClick={fetchInsights}
          disabled={loading}
          style={{ padding: "0.4rem 0.9rem", fontSize: "0.85rem" }}
        >
          {loading ? "…" : "↻ Refresh"}
        </button>
      </div>

      {loading && (
        <div className="text-center mt-4">
          <div className="loader" />
        </div>
      )}

      {error && <p className="error-text">Could not load insights: {error}</p>}

      {!loading && !error && insights.length === 0 && (
        <p style={{ color: "var(--text-secondary)" }}>No insights available yet.</p>
      )}

      {!loading &&
        !error &&
        insights.map((insight, i) => (
          <div key={i} className="ai-insight">
            <p style={{ fontSize: "0.95rem", lineHeight: "1.6" }}>{insight}</p>
          </div>
        ))}
    </div>
  );
}
