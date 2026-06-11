import { INDUSTRY_PLAYS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Cases — Dealix",
  description: "Industries Dealix serves, with visible signals, weaknesses, and the right offer for each.",
};

export default function CasesPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Industries & Plays</p>
          <h1 className="mt-3 text-4xl font-semibold">ست صناعات، كل وحدة لها play</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            ما في &quot;case studies&quot; ملفّقة. في plays واضحة مبنية على الإشارات العامة اللي نلاحظها
            في كل صناعة، والعرض الأنسب لها.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          {INDUSTRY_PLAYS.map((p) => (
            <article key={p.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">{p.industry}</h2>
              <p className="text-xs text-white/60">{p.industryAr}</p>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div>
                  <p className="text-xs uppercase text-white/50">Visible signals</p>
                  <ul className="mt-1 text-sm text-white/80 list-disc list-inside">
                    {p.visibleSignals.map((s) => (
                      <li key={s}>{s}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-xs uppercase text-white/50">Weaknesses</p>
                  <ul className="mt-1 text-sm text-white/80 list-disc list-inside">
                    {p.weaknesses.map((s) => (
                      <li key={s}>{s}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <p className="mt-3 text-xs text-amber-200">Best offer: {p.bestOffer}</p>
              <p className="mt-2 text-sm text-white/80">{p.openerEn}</p>
              <p className="text-xs text-white/60">{p.openerAr}</p>
              <p className="mt-2 text-xs text-white/50">Proof: {p.proofAngle}</p>
              <p className="mt-1 text-xs text-emerald-200">First 7 days: {p.first7DayWin}</p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
