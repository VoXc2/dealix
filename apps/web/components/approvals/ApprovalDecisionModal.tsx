export function ApprovalDecisionModal() {
  return (
    <div className="card">
      <h2>Approval Decision</h2>
      <p>Grant or reject pending high-risk actions.</p>
      <div style={{ display: "flex", gap: 8 }}>
        <button type="button">Grant</button>
        <button type="button">Reject</button>
      </div>
    </div>
  );
}
