type RunRow = {
  runId: string;
  tenantId: string;
  workflowId: string;
  state: string;
};

export function RunTable({ runs }: { runs: RunRow[] }) {
  return (
    <div className="card">
      <h2>Workflow Runs</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Run</th>
            <th align="left">Tenant</th>
            <th align="left">Workflow</th>
            <th align="left">State</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.runId}>
              <td>
                <a href={`/control-plane/${run.runId}`}>{run.runId}</a>
              </td>
              <td>{run.tenantId}</td>
              <td>{run.workflowId}</td>
              <td>{run.state}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
