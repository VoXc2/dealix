import { CircuitBreakerTable } from "../../components/safety/CircuitBreakerTable";
import { KillSwitchPanel } from "../../components/safety/KillSwitchPanel";

const breakers = [
  { key: "whatsapp-send", state: "closed", lastTriggeredAt: "2026-05-14T08:00:00Z" },
  { key: "crm-update", state: "open", lastTriggeredAt: "2026-05-15T09:10:00Z" }
];

export default function SafetyPage() {
  return (
    <main className="grid">
      <h1>Runtime Safety</h1>
      <KillSwitchPanel />
      <CircuitBreakerTable rows={breakers} />
    </main>
  );
}
