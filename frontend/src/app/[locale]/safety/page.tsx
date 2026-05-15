import { AppLayout } from "@/components/layout/AppLayout";
import { CircuitBreakerTable } from "@/components/safety/CircuitBreakerTable";
import { KillSwitchPanel } from "@/components/safety/KillSwitchPanel";

export default function SafetyPage() {
  return (
    <AppLayout title="Runtime Safety" subtitle="Kill switches, circuit breakers, and guardrails">
      <div className="space-y-4">
        <KillSwitchPanel />
        <CircuitBreakerTable />
      </div>
    </AppLayout>
  );
}
