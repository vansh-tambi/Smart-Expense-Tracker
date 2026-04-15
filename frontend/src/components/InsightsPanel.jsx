import { useEffect } from "react";
import { useInsights } from "../hooks/useInsights";
import { RefreshCw, Sparkles } from "lucide-react";

export default function InsightsPanel({ refreshTrigger }) {
  const { insights, loading, error, fetchInsights } = useInsights();

  useEffect(() => {
    fetchInsights();
  }, [refreshTrigger, fetchInsights]);

  return (
    <div className="insights-card">
      <div className="card-body">
        <div className="insights-header">
          <h2 style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
            <Sparkles size={14} color="var(--accent)" />
            Insights
          </h2>
          <button
            className="btn btn-ghost"
            id="refresh-insights-btn"
            onClick={fetchInsights}
            disabled={loading}
          >
            <RefreshCw
              size={13}
              style={{
                animation: loading ? "spin 0.7s linear infinite" : "none",
              }}
            />
            {!loading && "Refresh"}
          </button>
        </div>

        {loading && (
          <div className="empty-state">
            <div className="loader" />
          </div>
        )}

        {error && <p className="msg-error">Could not load insights.</p>}

        {!loading && !error && insights.length === 0 && (
          <div className="empty-state">No insights yet.</div>
        )}

        {!loading &&
          !error &&
          insights.map((insight, i) => (
            <div
              key={i}
              className="insight-item fade-in"
              style={{ animationDelay: `${i * 60}ms` }}
            >
              {insight}
            </div>
          ))}
      </div>
    </div>
  );
}
