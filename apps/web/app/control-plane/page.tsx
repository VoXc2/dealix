import { RunActions } from "../../components/control-plane/RunActions";
import { RunTable } from "../../components/control-plane/RunTable";

const runs = [
  { runId: "run-001", tenantId: "tenant-enterprise", workflowId: "revenue_os", state: "running" },
  { runId: "run-002", tenantId: "tenant-enterprise", workflowId: "approval_flow", state: "paused" }
];

export default function ControlPlanePage() {
  return (
    <main className="grid">
      <h1>Control Plane</h1>
      <RunTable runs={runs} />
      <RunActions runId="run-001" />
    </main>
  );
}
