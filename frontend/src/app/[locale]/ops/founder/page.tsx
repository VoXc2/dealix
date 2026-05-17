import { AppLayout } from "@/components/layout/AppLayout";
import { FounderCommandCenter } from "@/components/ops/FounderCommandCenter";

export default function FounderOpsPage() {
  return (
    <AppLayout title="Founder Command Center" subtitle="Top actions, approvals, revenue focus">
      <FounderCommandCenter />
    </AppLayout>
  );
}

