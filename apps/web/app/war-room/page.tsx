import { ACQUISITION_FUNNEL, DELIVERY_PIPELINE, FOUNDER_PRIORITIES } from "@/lib/company-os/company-os";

export const metadata = {
  title: "Founder War Room — Dealix",
  description: "Daily CEO moves, revenue priorities, risks, and operating focus for the founder.",
};

export default function WarRoomPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Founder War Room</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            غرفة حرب المؤسس — Daily CEO moves
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            One page, every morning. The single most important view inside Dealix: revenue priorities,
            risks, client pipeline pressure, assets to produce, and the three moves the founder must
            ship today.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-2">
          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-lg font-semibold text-amber-300">Today’s CEO moves</h2>
            <ul className="mt-4 space-y-3 text-sm text-white/80">
              {FOUNDER_PRIORITIES.map((p) => (
                <li key={p.id} className="rounded-lg border border-white/10 bg-black/30 p-3">
                  <p className="font-medium">
                    P{p.rank} — {p.title}
                  </p>
                  <p className="mt-1 text-xs text-white/60">{p.titleAr}</p>
                  <p className="mt-1 text-xs text-white/60">Due in {p.dueInDays} day(s)</p>
                </li>
              ))}
            </ul>
          </article>

          <article className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-lg font-semibold text-amber-300">Revenue priorities</h2>
            <ul className="mt-4 space-y-3 text-sm text-white/80">
              {ACQUISITION_FUNNEL.slice(0, 5).map((step) => (
                <li key={step.id} className="flex gap-3">
                  <span className="mt-1 inline-block h-2 w-2 rounded-full bg-amber-300" />
                  <div>
                    <p className="font-medium">{step.title} · {step.titleAr}</p>
                    <p className="text-xs text-white/60">{step.goalAr}</p>
                  </div>
                </li>
              ))}
            </ul>
          </article>
        </section>

        <section className="mt-8 rounded-2xl border border-rose-400/30 bg-rose-500/5 p-6">
          <h2 className="text-lg font-semibold text-rose-200">Risks</h2>
          <ul className="mt-4 space-y-2 text-sm text-white/80">
            <li>• Review queue not cleared → outreach must stay as drafts only.</li>
            <li>• Proposal-to-close conversion under target — tighten close criteria.</li>
            <li>• Proof vault underused — coach delivery lead to log proof weekly.</li>
            <li>• Cash target not met — slow expansion, speed up retainers.</li>
          </ul>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold text-amber-300">Operational constraints</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="text-xs uppercase tracking-widest text-white/50">No spam</p>
              <p className="mt-2 text-sm">
                No auto-send. Every draft carries review_status and only the founder can flip it to
                approved.
              </p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="text-xs uppercase tracking-widest text-white/50">PDPL-aware</p>
              <p className="mt-2 text-sm">
                Minimize personal data. No scraping. Source must be noted for every lead.
              </p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="text-xs uppercase tracking-widest text-white/50">Proof-driven</p>
              <p className="mt-2 text-sm">
                No expansion offer without a proof report. No fake case studies. Demo data is labeled.
              </p>
            </div>
          </div>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold text-amber-300">Assets to produce today</h2>
          <ol className="mt-4 space-y-2 text-sm text-white/80 list-decimal list-inside">
            <li>Daily CEO brief (export as .txt and post to founder channel)</li>
            <li>Launch brief (export as .md)</li>
            <li>3 proof items logged from the live delivery accounts</li>
            <li>1 proposal for the highest-priority reviewed account</li>
            <li>Outreach drafts for the top 10 scored leads (human review before send)</li>
          </ol>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold text-amber-300">Client pipeline pressure</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {DELIVERY_PIPELINE.slice(0, 4).map((s) => (
              <div key={s.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-widest text-white/50">{s.dayRange}</p>
                <p className="mt-1 font-medium">{s.title}</p>
                <p className="mt-1 text-xs text-white/60">{s.titleAr}</p>
              </div>
            ))}
          </div>
        </section>

        <footer className="mt-10 text-xs text-white/50">
          Generated by Dealix Company OS · No external action runs without human review.
        </footer>
      </div>
    </main>
  );
}
