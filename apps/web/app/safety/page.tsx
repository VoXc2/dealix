import { CircuitBreakerTable } from "@/components/safety/CircuitBreakerTable";
import { KillSwitchPanel } from "@/components/safety/KillSwitchPanel";

export const metadata = { title: "Runtime Safety — Dealix" , alternates: { canonical: "/safety" } };

const breakers = [
  { key: "whatsapp-send", state: "closed", lastTriggeredAt: "2026-05-14T08:00:00Z" },
  { key: "crm-update", state: "open", lastTriggeredAt: "2026-05-15T09:10:00Z" },
];

export default function SafetyPage() {
  return (
    <main>
      <section>
        <p className="eyebrow">Runtime Safety</p>
        <h1>أمان التشغيل · Runtime Safety <span className="badge badge-amber">بيانات تجريبية · Demo data</span></h1>
        <p className="stat-label">مفتاح الإيقاف وقواطع الدائرة — حواجز تمنع أي إرسال خارجي غير محكوم.</p>
      </section>
      <section className="card"><KillSwitchPanel /></section>
      <section className="card"><CircuitBreakerTable rows={breakers} /></section>
    </main>
  );
}
