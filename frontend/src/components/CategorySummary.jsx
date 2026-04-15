import { getCategoryMeta } from "./categoryMeta";

export default function CategorySummary({ summary }) {
  const total = summary.reduce((acc, s) => acc + s.total, 0);

  return (
    <div className="card">
      <div className="card-body">
        <h2>Breakdown</h2>

        {summary.length === 0 ? (
          <div className="empty-state" style={{ padding: "1.5rem 0" }}>
            No data yet.
          </div>
        ) : (
          <>
            <div style={{ marginBottom: "1rem" }}>
              <div className="summary-total">${total.toFixed(2)}</div>
              <div className="summary-total-label">across {summary.length} categories</div>
            </div>

            {summary.map((s) => {
              const pct = total > 0 ? (s.total / total) * 100 : 0;
              const meta = getCategoryMeta(s.category);
              return (
                <div key={s.category} className="summary-item">
                  <span
                    className="summary-cat-name"
                    style={{ color: meta.color }}
                  >
                    {s.category}
                  </span>
                  <div className="summary-bar-track">
                    <div
                      className="summary-bar-fill"
                      style={{ width: `${pct}%`, background: meta.color }}
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
