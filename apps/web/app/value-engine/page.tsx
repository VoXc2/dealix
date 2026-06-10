import { WorkflowROIReport } from "../../components/value/WorkflowROIReport";

export default function ValueEnginePage() {
  return (
    <main className="grid">
      <h1>Value Engine</h1>
      <WorkflowROIReport roi={{ estimated: 12000, measured: 15600 }} />
    </main>
  );
}
