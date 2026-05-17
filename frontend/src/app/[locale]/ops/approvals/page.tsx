import { AppLayout } from "@/components/layout/AppLayout";
import { ApprovalCenter } from "@/components/approvals/ApprovalCenter";

export default function OpsApprovalsPage() {
  return (
    <AppLayout title="Approval Center" subtitle="Risk-gated actions awaiting founder decision">
      <ApprovalCenter />
    </AppLayout>
  );
}

