type AgentRow = {
  agentId: string;
  tenantId: string;
  capability: string;
  status: string;
};

export function AgentRegistryTable({ agents }: { agents: AgentRow[] }) {
  return (
    <div className="card">
      <h2>Agent Registry</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Agent</th>
            <th align="left">Tenant</th>
            <th align="left">Capability</th>
            <th align="left">Status</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent.agentId}>
              <td>{agent.agentId}</td>
              <td>{agent.tenantId}</td>
              <td>{agent.capability}</td>
              <td>{agent.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
