import { OUTREACH_OPENERS, OBJECTION_HANDLERS } from "@/lib/sales-automation/lead-sources";

export const metadata = {
  title: "Persuasion Room — Dealix",
  description: "Ready-made openers, objection handlers, and soft-closes for the founder.",
};

export default function PersuasionRoomPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Persuasion Room</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            غرفة الإقناع — مسوّدات جاهزة، لك أنت
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل اللي هنا draft. اقرأ، عدّل، وافق، ثم أرسل يدوياً. ما في ضغط على العميل، وما في وعود
            ما نقدر نضمنها.
          </p>
        </header>

        <section>
          <h2 className="text-lg font-semibold text-amber-300">Arabic openers</h2>
          <ul className="mt-4 space-y-3">
            {OUTREACH_OPENERS.ar.map((o, idx) => (
              <li key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-widest text-white/50">Draft #{idx + 1}</p>
                <p className="mt-2 text-sm text-white/80">{o}</p>
                <p className="mt-2 text-[10px] text-white/50">review_status: pending · channel: whatsapp/email</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-10">
          <h2 className="text-lg font-semibold text-amber-300">English openers</h2>
          <ul className="mt-4 space-y-3">
            {OUTREACH_OPENERS.en.map((o, idx) => (
              <li key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-widest text-white/50">Draft #{idx + 1}</p>
                <p className="mt-2 text-sm text-white/80">{o}</p>
                <p className="mt-2 text-[10px] text-white/50">review_status: pending · channel: linkedin/email</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-10">
          <h2 className="text-lg font-semibold text-amber-300">Objection handlers</h2>
          <ul className="mt-4 space-y-4">
            {OBJECTION_HANDLERS.map((o, idx) => (
              <li key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-widest text-rose-200">Objection</p>
                <p className="mt-1 text-sm text-white/80">{o.objection}</p>
                <p className="text-xs text-white/60">{o.objectionAr}</p>
                <p className="mt-3 text-xs uppercase tracking-widest text-emerald-200">Response</p>
                <p className="mt-1 text-sm text-white/80">{o.response}</p>
                <p className="text-xs text-white/60">{o.responseAr}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">Soft-close</h2>
          <p className="mt-2 text-sm text-white/80">
            &quot;ما أبغاك تتخذ قرار اليوم. تبغى تجربة مجانية على شكل مكالمة 20 دقيقة نشوف فيها إن كان
            في فجوة تستاهل OS كامل؟ اختر الوقت اللي يناسبك.&quot;
          </p>
        </section>
      </div>
    </main>
  );
}
