export function RunActions({ runId }: { runId: string }) {
  return (
    <div className="card">
      <h2>Run Actions</h2>
      <p>run_id: {runId}</p>
      <div style={{ display: "flex", gap: 8 }}>
        <button type="button">Pause Run</button>
        <button type="button">Request Rollback</button>
      </div>
    </div>
  );
}
