const CATEGORY_COLORS = {
  Food: "#f97316",
  Transport: "#3b82f6",
  Shopping: "#ec4899",
  Entertainment: "#a855f7",
  Health: "#10b981",
  Utilities: "#f59e0b",
  Education: "#06b6d4",
  Other: "#6b7280",
};

export default function CategorySummary({ summary }) {
  const total = summary.reduce((acc, s) => acc + s.total, 0);

  return (
    <div className="glass-panel" style={{ padding: "1.5rem" }}>
      <h2>📊 Category Summary</h2>
      {summary.length === 0 ? (
        <p style={{ color: "var(--text-secondary)" }}>No data yet.</p>
      ) : (
        <>
          <p style={{ color: "var(--text-secondary)", marginBottom: "1rem" }}>
            Total Spent: <strong style={{ color: "var(--text-primary)" }}>${total.toFixed(2)}</strong>
          </p>
          {summary.map((s) => {
            const pct = total > 0 ? (s.total / total) * 100 : 0;
            const color = CATEGORY_COLORS[s.category] || "#6b7280";
            return (
              <div key={s.category} style={{ marginBottom: "1rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.3rem" }}>
                  <span style={{ fontWeight: 500 }}>{s.category}</span>
                  <span style={{ color: "var(--text-secondary)" }}>
                    ${s.total.toFixed(2)} · {pct.toFixed(0)}%
                  </span>
                </div>
                <div
                  style={{
                    height: "8px",
                    borderRadius: "99px",
                    background: "rgba(255,255,255,0.08)",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${pct}%`,
                      height: "100%",
                      background: color,
                      borderRadius: "99px",
                      transition: "width 0.6s ease",
                    }}
                  />
                </div>
              </div>
            );
          })}
        </>
      )}
    </div>
  );
}
