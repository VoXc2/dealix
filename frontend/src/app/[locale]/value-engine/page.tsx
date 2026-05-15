import { AppLayout } from "@/components/layout/AppLayout";
import { WorkflowROIReport } from "@/components/value/WorkflowROIReport";

export default function ValueEnginePage() {
  return (
    <AppLayout title="Value Engine" subtitle="Workflow ROI and evidence-backed metrics">
      <WorkflowROIReport customerId="acme" />
    </AppLayout>
  );
}
