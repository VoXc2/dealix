import { AgentRegistryTable } from "../../components/agents/AgentRegistryTable";
import { AgentTrustBoundaryEditor } from "../../components/agents/AgentTrustBoundaryEditor";

const agents = [
  { agentId: "sales_agent", tenantId: "tenant-enterprise", capability: "outbound_sales", status: "active" },
  { agentId: "ops_agent", tenantId: "tenant-enterprise", capability: "approval_routing", status: "active" }
];

export default function AgentsPage() {
  return (
    <main className="grid">
      <h1>Agents</h1>
      <AgentRegistryTable agents={agents} />
      <AgentTrustBoundaryEditor />
    </main>
  );
}
