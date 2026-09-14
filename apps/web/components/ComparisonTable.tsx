"use client";

export default function ComparisonTable({ rows }: { rows: { feature: string; dealix: string; others: string }[] }) {
  return (
    <div className="card" style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.12)" }}>
            <th style={{ textAlign: "right", padding: "var(--sp-3)", color: "var(--dealix-cyan)" }}>الميزة</th>
            <th style={{ textAlign: "center", padding: "var(--sp-3)", color: "var(--dealix-cyan)" }}>Dealix</th>
            <th style={{ textAlign: "center", padding: "var(--sp-3)", color: "rgba(255,255,255,0.50)" }}>الحلول التقليدية</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.feature} style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
              <td style={{ padding: "var(--sp-3)", color: "#fff" }}>{r.feature}</td>
              <td style={{ padding: "var(--sp-3)", textAlign: "center", color: "#34d399" }}>{r.dealix}</td>
              <td style={{ padding: "var(--sp-3)", textAlign: "center", color: "rgba(255,255,255,0.50)" }}>{r.others}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
