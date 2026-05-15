import { AppLayout } from "@/components/layout/AppLayout";
import { RunTable } from "@/components/control-plane/RunTable";
import { RunActions } from "@/components/control-plane/RunActions";

export default function ControlPlanePage() {
  return (
    <AppLayout title="Control Plane" subtitle="Workflow runs, approvals, and operations">
      <div className="space-y-4">
        <RunTable />
        <RunActions approvalId="demo-approval-id" />
      </div>
    </AppLayout>
  );
}
