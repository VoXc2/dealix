type CircuitBreakerRow = {
  key: string;
  state: string;
  lastTriggeredAt: string;
};

export function CircuitBreakerTable({ rows }: { rows: CircuitBreakerRow[] }) {
  return (
    <div className="card">
      <h2>Circuit Breakers</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Breaker</th>
            <th align="left">State</th>
            <th align="left">Last Triggered</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.key}>
              <td>{row.key}</td>
              <td>{row.state}</td>
              <td>{row.lastTriggeredAt}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
