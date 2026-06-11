export const metadata = {
  title: "Daily Draft — Dealix",
  description: "Today's outreach drafts, ready for human review, in one place.",
};

const SAMPLE_DRAFTS = [
  {
    id: "draft-demo-001",
    account: "Demo Marketing Agency 001",
    language: "ar",
    channel: "whatsapp",
    opener: "مرحبًا أبو فهد، شفت إن وكالتكم تنشر حملات قوية، بس الاستجابة على الليدز الواردة تتأخر. هذا بالضبط اللي Dealix يحلّه — مسوّدات مولّدة + مراجعة بشرية، بدون spam.",
    followUp: "لو تبغى مكالمة 20 دقيقة نراجع فيها الـ workflow بدون التزام، اختر الوقت اللي يناسبك.",
    reviewStatus: "pending",
    generatedAt: "2026-06-11",
  },
  {
    id: "draft-demo-002",
    account: "Demo Training Co 002",
    language: "en",
    channel: "linkedin",
    opener: "Hi Sara, I came across your training programs and noticed post-course follow-up is light. Dealix builds a measurable retention flow — no spam, no auto-send.",
    followUp: "Open to a 20-min diagnostic?",
    reviewStatus: "pending",
    generatedAt: "2026-06-11",
  },
];

export default function DailyDraftPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Daily Draft</p>
          <h1 className="mt-3 text-4xl font-semibold">مسوّدات اليوم — للمراجعة فقط</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل مسوّدة تنتظر review_status = approved. لا إرسال تلقائي. لا ضغط على العميل.
          </p>
        </header>

        <section className="mt-10 space-y-4">
          {SAMPLE_DRAFTS.map((d) => (
            <article key={d.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="font-medium">{d.account}</p>
                <div className="flex items-center gap-2 text-xs">
                  <span className="rounded-full border border-amber-300/30 bg-amber-300/10 px-2 py-1 text-amber-200">
                    {d.language.toUpperCase()}
                  </span>
                  <span className="rounded-full border border-white/10 px-2 py-1 text-white/70">
                    {d.channel}
                  </span>
                  <span className="rounded-full border border-rose-400/30 bg-rose-500/10 px-2 py-1 text-rose-200">
                    {d.reviewStatus}
                  </span>
                </div>
              </div>
              <p className="mt-3 text-sm text-white/80">{d.opener}</p>
              <p className="mt-2 text-xs text-white/60">Follow-up: {d.followUp}</p>
              <p className="mt-2 text-[10px] text-white/50">Generated: {d.generatedAt} · id: {d.id}</p>
            </article>
          ))}
        </section>

        <section className="mt-10 rounded-2xl border border-rose-400/30 bg-rose-500/5 p-6">
          <h2 className="text-lg font-semibold text-rose-200">قاعدة لا تُكسر</h2>
          <p className="mt-2 text-sm text-white/80">
            لا أحد يوافق على الإرسال غير المؤسس. ما في اختصار، ما في auto-send، ما في
            &quot;المسوّدة جاهزة فأرسلناها&quot;.
          </p>
        </section>
      </div>
    </main>
  );
}
