export const metadata = {
  title: "Book a Workflow Review — Dealix",
  description: "20-min diagnostic with the Dealix founder. No obligation, no spam.",
};

export default function BookPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-3xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Workflow Review</p>
          <h1 className="mt-3 text-4xl font-semibold">احجز مراجعة 20 دقيقة</h1>
          <p className="mt-3 text-sm text-white/70">
            مكالمة 20 دقيقة مع مؤسس Dealix. بدون التزام، بدون spam، بدون ضغط.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-widest text-emerald-200">Who it is for</p>
            <ul className="mt-2 list-disc list-inside text-sm text-white/80">
              <li>Founders whose company outgrew their ops</li>
              <li>Agencies that ship but lose on follow-up</li>
              <li>Multi-entity groups needing one command view</li>
            </ul>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-widest text-rose-200">Who it is NOT for</p>
            <ul className="mt-2 list-disc list-inside text-sm text-white/80">
              <li>Companies that only want a dashboard</li>
              <li>Anyone looking for guaranteed ROI</li>
              <li>Anyone who wants to spam or scrape</li>
            </ul>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-white/50">What to prepare</p>
          <ul className="mt-2 list-decimal list-inside text-sm text-white/80">
            <li>3 visible signals you noticed about your own ops</li>
            <li>One example of a workflow that breaks every week</li>
            <li>One example of a deliverable the client should see but doesn't</li>
            <li>Optional: link to your public site or social</li>
          </ul>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/30 bg-amber-300/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-200">What happens in 20 minutes</p>
          <ol className="mt-2 list-decimal list-inside text-sm text-white/80">
            <li>5 min — context (what you ship today)</li>
            <li>5 min — visible signals and gaps</li>
            <li>5 min — which Dealix OS fits (or none)</li>
            <li>5 min — next step or honest pass</li>
          </ol>
        </section>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6 text-center">
          <p className="text-sm text-white/70">Booking integration pending</p>
          <p className="mt-2 text-xs text-white/50">
            For now, reach the founder at founders@dealix.local
          </p>
        </section>
      </div>
    </main>
  );
}
