import { PREMIUM_OFFERS, INDUSTRY_PLAYS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Revenue Machine — Dealix",
  description: "Lead → Draft → Review → Meeting → Proposal → Close → Deliver → Retain.",
};

export default function RevenueMachinePage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Revenue Machine</p>
          <h1 className="mt-3 text-4xl font-semibold">ماكينة الإيراد — ثمان خطوات فقط</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            Lead → Score → Draft → Review → Meeting → Proposal → Close → Retain. كل خطوة لها
            exit criteria، وكل مخرج يُقاس.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-4">
          {[
            "1. Lead Source",
            "2. Score",
            "3. Draft",
            "4. Human Review",
            "5. Workflow Review Call",
            "6. Proposal",
            "7. Close",
            "8. Retain & Expand",
          ].map((step, idx) => (
            <div key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-widest text-amber-300/80">Step {idx + 1}</p>
              <p className="mt-1 font-medium">{step}</p>
            </div>
          ))}
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold text-amber-300">Industry-specific plays</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {INDUSTRY_PLAYS.slice(0, 4).map((p) => (
              <li key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{p.industry} → {p.bestOffer}</p>
                <p className="mt-1 text-sm text-white/80">{p.openerEn}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold text-amber-300">Top 3 offers this quarter</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-3">
            {PREMIUM_OFFERS.slice(1, 4).map((o) => (
              <li key={o.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{o.name}</p>
                <p className="text-xs text-white/60">{o.nameAr}</p>
                <p className="mt-2 text-sm text-white/80">{o.positioning}</p>
                <p className="mt-1 text-xs text-amber-200">{o.setup} setup · {o.monthly} monthly</p>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  );
}
