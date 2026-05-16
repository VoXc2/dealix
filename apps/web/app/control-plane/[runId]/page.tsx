import { RunActions } from "../../../components/control-plane/RunActions";
import { RunTraceTimeline } from "../../../components/control-plane/RunTraceTimeline";

const trace = [
  { id: "evt-1", type: "workflow.registered", actor: "system", at: "2026-05-15T15:00:00Z" },
  { id: "evt-2", type: "approval.submitted", actor: "sales_agent", at: "2026-05-15T15:02:00Z" },
  { id: "evt-3", type: "approval.granted", actor: "sami", at: "2026-05-15T15:03:00Z" }
];

export default async function ControlPlaneRunPage({
  params
}: {
  params: Promise<{ runId: string }>;
}) {
  const { runId } = await params;
  return (
    <main className="grid">
      <h1>Run Details: {runId}</h1>
      <RunTraceTimeline events={trace} />
      <RunActions runId={runId} />
    </main>
  );
}
