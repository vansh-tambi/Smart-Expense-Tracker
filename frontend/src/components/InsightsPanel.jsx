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
            <Sparkles size={14} color="var(--accent)" className="ai-pulse" />
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
          <div className="empty-state slide-up">No insights yet.</div>
        )}

        {!loading &&
          !error &&
          insights.map((insight, i) => {
            // Generate a simple deterministic sparkline path for visual character
            const paths = [
              "M2 14L10 6L16 10L24 2L30 6L40 2L46 8",
              "M2 10L10 14L16 4L24 8L30 2L40 8L46 6",
              "M2 6L10 2L16 12L24 6L30 10L40 2L46 8",
            ];
            const path = paths[i % paths.length];

            return (
              <div
                key={i}
                className="insight-item fade-in"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <div style={{ width: "48px", height: "16px", flexShrink: 0, marginTop: "2px" }}>
                  <svg
                    viewBox="0 0 48 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    style={{ width: "100%", height: "100%" }}
                  >
                    <path
                      className="draw-stroke"
                      d={path}
                      stroke="var(--accent)"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <div>{insight}</div>
              </div>
            );
          })}
      </div>
    </div>
  );
}
