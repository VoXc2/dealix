import { AppLayout } from "@/components/layout/AppLayout";
import { SupportConsole } from "@/components/ops/SupportConsole";

export default function OpsSupportPage() {
  return (
    <AppLayout title="Customer Service Console" subtitle="AI classification, KB answers, escalation queue">
      <SupportConsole />
    </AppLayout>
  );
}

