import { LEAD_SOURCES, PERSUASION_ANGLES, OFFER_LADDER, OUTREACH_OPENERS } from "@/lib/sales-automation/lead-sources";

export const metadata = {
  title: "Automated Sales Machine — Dealix",
  description: "Lead sources, weakness signals, persuasion angles, and the offer ladder for the founder.",
};

export default function AutomatedSalesPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Automated Sales Machine</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            ماكينة التصريف — من الإشارة إلى المسوّدة الجاهزة
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            المنظومة تقرأ إشارات عامة، تستخرج فرضية ضعف، تقترح زاوية إقناع، وتولّد مسوّدة عربي أو
            إنجليزي. أنت توافق، أنت ترسل. لا spam، لا auto-send.
          </p>
        </header>

        <section>
          <h2 className="text-lg font-semibold text-amber-300">Lead sources</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {LEAD_SOURCES.map((s) => (
              <li key={s.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <div className="flex items-center justify-between">
                  <p className="font-medium">{s.label}</p>
                  <span
                    className={`rounded-full border px-2 py-1 text-[10px] ${
                      s.autoSendAllowed
                        ? "border-rose-400/30 bg-rose-500/10 text-rose-200"
                        : "border-emerald-400/30 bg-emerald-500/10 text-emerald-200"
                    }`}
                  >
                    {s.autoSendAllowed ? "auto-send: yes" : "auto-send: no"}
                  </span>
                </div>
                <p className="text-xs text-white/60">{s.labelAr}</p>
                <p className="mt-2 text-sm text-white/80">{s.description}</p>
                <p className="mt-1 text-xs text-white/60">{s.use}</p>
                <ul className="mt-2 flex flex-wrap gap-2 text-[10px] text-white/60">
                  {s.guardrails.map((g) => (
                    <li key={g} className="rounded-full border border-white/10 px-2 py-1">
                      {g}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-10">
          <h2 className="text-lg font-semibold text-amber-300">Persuasion angles</h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {PERSUASION_ANGLES.map((a) => (
              <li key={a.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="font-medium">{a.title}</p>
                <p className="text-xs text-white/60">{a.titleAr}</p>
                <p className="mt-2 text-xs text-amber-200">Signal: {a.signal}</p>
                <p className="mt-2 text-sm text-white/80">{a.hook}</p>
                <p className="mt-2 text-xs text-white/60">{a.hookAr}</p>
                <p className="mt-2 text-[10px] text-white/50">Best for: {a.bestFor.join(", ")}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-10">
          <h2 className="text-lg font-semibold text-amber-300">Offer ladder</h2>
          <ol className="mt-4 space-y-3">
            {OFFER_LADDER.map((o, idx) => (
              <li key={o.id} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium">
                    {idx + 1}. {o.name} · {o.nameAr}
                  </p>
                  <span className="rounded-full border border-amber-300/30 bg-amber-300/10 px-2 py-1 text-[11px] text-amber-200">
                    {o.price}
                  </span>
                </div>
                <p className="mt-1 text-sm text-white/80">{o.positioning}</p>
                <p className="text-xs text-white/60">{o.positioningAr}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">Daily opener templates</h2>
          <div className="mt-3 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs uppercase tracking-widest text-white/50">Arabic</p>
              <p className="mt-2 rounded-lg border border-white/10 bg-black/30 p-3 text-sm text-white/80">
                {OUTREACH_OPENERS.ar[0]}
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-widest text-white/50">English</p>
              <p className="mt-2 rounded-lg border border-white/10 bg-black/30 p-3 text-sm text-white/80">
                {OUTREACH_OPENERS.en[0]}
              </p>
            </div>
          </div>
        </section>

        <section className="mt-10 rounded-2xl border border-rose-400/30 bg-rose-500/5 p-6">
          <h2 className="text-lg font-semibold text-rose-200">قواعد ماكينة التصريف</h2>
          <ul className="mt-3 space-y-2 text-sm text-white/80">
            <li>• كل مسوّدة تنتظر review_status = approved قبل أي إرسال.</li>
            <li>• لا scraping لبيانات خاصة. الإشارة لازم تكون عامة ومرئية.</li>
            <li>• لا ادعاء ROI مضمون. لا شهادات زائفة. لا ضغط على العميل.</li>
            <li>• كل lead demo يحمل &quot;demo&quot;: true بشكل واضح.</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
