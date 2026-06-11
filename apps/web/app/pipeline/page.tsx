import { INDUSTRY_PLAYS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Pipeline — Dealix",
  description: "Visual pipeline of all opportunities, by stage, owner, and value.",
};

const STAGES = [
  { id: "discovery", label: "Discovery" },
  { id: "qualified", label: "Qualified" },
  { id: "drafted", label: "Drafted" },
  { id: "review", label: "In Review" },
  { id: "meeting", label: "Meeting Booked" },
  { id: "proposal", label: "Proposal Sent" },
  { id: "negotiation", label: "Negotiation" },
  { id: "won", label: "Won" },
  { id: "delivered", label: "In Delivery" },
  { id: "retain", label: "Retainer" },
];

export default function PipelinePage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Pipeline</p>
          <h1 className="mt-3 text-4xl font-semibold">خط العميل — من الاكتشاف إلى الـ Retainer</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            10 مراحل، كل وحدة لها عدد ليدز + قيمة تقديرية + أكبر bottleneck. اضغط على أي مرحلة للتفاصيل.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-5">
          {STAGES.map((s, idx) => (
            <div key={s.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-widest text-amber-300/80">Stage {idx + 1}</p>
              <p className="mt-1 font-medium">{s.label}</p>
              <p className="mt-2 text-xs text-white/60">0 accounts · SAR 0</p>
            </div>
          ))}
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold text-amber-300">Industries in focus</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {INDUSTRY_PLAYS.slice(0, 4).map((p) => (
              <li key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{p.industry}</p>
                <p className="text-xs text-white/60">{p.industryAr}</p>
                <p className="mt-2 text-xs text-amber-200">Best offer: {p.bestOffer}</p>
                <p className="mt-1 text-sm text-white/80">{p.first7DayWin}</p>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  );
}
