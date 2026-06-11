import { INDUSTRY_PLAYS, PERSUASION_ANGLES } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Lead Engine — Dealix",
  description: "Approved lead sources, scoring, and signal-based routing for the founder.",
};

export default function LeadEnginePage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Lead Engine</p>
          <h1 className="mt-3 text-4xl font-semibold">ليدز نظيفة، مصادر رسمية</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            ما في تجريف. ما في شراء قوائم. ما في تجاوز لشروط المنصات. كل ليد عنده مصدر، وكل إشارة
            عامة موثّقة.
          </p>
        </header>

        <section className="mt-10">
          <h2 className="text-2xl font-semibold text-amber-300">Industry signals &amp; weaknesses</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {INDUSTRY_PLAYS.map((p) => (
              <li key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{p.industry}</p>
                <p className="text-xs text-white/60">{p.industryAr}</p>
                <p className="mt-2 text-xs text-amber-200">Visible signals</p>
                <ul className="mt-1 list-disc list-inside text-sm text-white/80">
                  {p.visibleSignals.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
                <p className="mt-2 text-xs text-amber-200">Likely weaknesses</p>
                <ul className="mt-1 list-disc list-inside text-sm text-white/80">
                  {p.weaknesses.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
                <p className="mt-2 text-xs text-amber-200">Best offer: {p.bestOffer}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold text-amber-300">Persuasion angles (signal-based)</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            <li className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="font-medium">From leakage to revenue</p>
              <p className="text-sm text-white/80">Slow follow-up on inbound leads</p>
            </li>
            <li className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="font-medium">From scattered reviews to a trust wall</p>
              <p className="text-sm text-white/80">Inconsistent review response</p>
            </li>
            <li className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="font-medium">From delivery to proof</p>
              <p className="text-sm text-white/80">No weekly report to client base</p>
            </li>
            <li className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="font-medium">From data to a one-page decision</p>
              <p className="text-sm text-white/80">Many dashboards, no daily decision</p>
            </li>
            <li className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="font-medium">From operational chaos to growth capacity</p>
              <p className="text-sm text-white/80">Founder is the bottleneck</p>
            </li>
          </ul>
        </section>
      </div>
    </main>
  );
}
