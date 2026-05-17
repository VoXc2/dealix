import { AppLayout } from "@/components/layout/AppLayout";
import { SalesPipelineConsole } from "@/components/ops/SalesPipelineConsole";

export default function SalesOpsPage() {
  return (
    <AppLayout title="Sales Pipeline Console" subtitle="Autopilot lead stages and next actions">
      <SalesPipelineConsole />
    </AppLayout>
  );
}

