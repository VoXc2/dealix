export function AgentTrustBoundaryEditor() {
  return (
    <div className="card">
      <h2>Agent Trust Boundary</h2>
      <label htmlFor="maxAutonomy">Max autonomy</label>
      <input id="maxAutonomy" type="number" defaultValue={2} min={0} max={5} />
      <div style={{ marginTop: 8 }}>
        <button type="button">Save Boundary</button>
      </div>
    </div>
  );
}
