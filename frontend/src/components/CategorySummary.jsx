import { useState, useEffect } from "react";
import { getCategoryMeta } from "./categoryMeta";

export default function CategorySummary({ summary }) {
  const total = summary.reduce((acc, s) => acc + s.total, 0);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Slight delay so the transition triggers after initial paint
    const timer = setTimeout(() => setMounted(true), 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="card">
      <div className="card-body">
        <h2>Breakdown</h2>

        {summary.length === 0 ? (
          <div className="empty-state slide-up" style={{ padding: "1.5rem 0" }}>
            No data yet.
          </div>
        ) : (
          <>
            <div style={{ marginBottom: "1rem" }}>
              <div className="summary-total">${total.toFixed(2)}</div>
              <div className="summary-total-label">across {summary.length} categories</div>
            </div>

            {summary.map((s, i) => {
              const pct = total > 0 ? (s.total / total) * 100 : 0;
              const meta = getCategoryMeta(s.category);
              return (
                <div key={s.category} className="summary-item slide-up" style={{ animationDelay: `${i * 30}ms` }}>
                  <span
                    className="summary-cat-name"
                    style={{ color: meta.color }}
                  >
                    {s.category}
                  </span>
                  <div className="summary-bar-track">
                    <div
                      className="summary-bar-fill"
                      style={{ width: `${mounted ? pct : 0}%`, background: meta.color }}
                    />
                  </div>
                  <span className="summary-cat-value">
                    ${s.total.toFixed(0)}
                  </span>
                </div>
              );
            })}
          </>
        )}
      </div>
    </div>
  );
}
