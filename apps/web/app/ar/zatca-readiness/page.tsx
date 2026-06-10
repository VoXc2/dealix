export const metadata = {
  title: "Dealix ZATCA Readiness | فحص جاهزية الفوترة الإلكترونية",
  description: "فحص سريع لجاهزية الشركات السعودية للفوترة الإلكترونية وربطها بتشغيل الإيراد والمتابعات.",
};

const questions = [
  "هل لديكم نظام فواتير إلكتروني متصل ومحدث؟",
  "هل بيانات العملاء والضريبة محفوظة بشكل منظم؟",
  "هل يوجد ربط واضح بين المدفوعات والفواتير؟",
  "هل يوجد مسار مراجعة داخلي قبل إرسال الفواتير؟",
  "هل يمكن استخراج تقرير أسبوعي عن الإيراد والمدفوعات والمتابعات؟",
];

export default function ArabicZatcaReadinessPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#07131f] px-6 py-16 text-white">
      <section className="mx-auto max-w-6xl">
        <p className="mb-4 inline-flex rounded-full border border-amber-300/30 px-4 py-2 text-sm text-amber-100">
          ZATCA Readiness + Revenue Ops
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-tight md:text-6xl">
          فحص جاهزية ZATCA وربط الفوترة بالإيراد والمتابعات.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
          Dealix لا يتعامل مع الامتثال كملف منفصل؛ نربط الفواتير، المدفوعات، المتابعات، والقرارات التشغيلية في طبقة واحدة تساعد المؤسس على رؤية الإيراد بوضوح.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-2">
          <section className="rounded-3xl border border-white/10 bg-white/[0.06] p-6">
            <h2 className="text-2xl font-black text-amber-100">أسئلة الفحص السريع</h2>
            <ul className="mt-5 space-y-4 text-slate-200">
              {questions.map((q) => (
                <li key={q} className="rounded-2xl bg-black/20 p-4">{q}</li>
              ))}
            </ul>
          </section>

          <section className="rounded-3xl border border-cyan-300/20 bg-cyan-400/10 p-6">
            <h2 className="text-2xl font-black text-cyan-100">ماذا يخرج Dealix؟</h2>
            <ul className="mt-5 space-y-4 text-slate-200">
              <li>خريطة فجوات الفوترة والمدفوعات.</li>
              <li>قائمة أولويات تشغيلية للأسبوع القادم.</li>
              <li>ربط P1 Revenue Intelligence Sprint بالامتثال والفوترة.</li>
              <li>توصية واضحة: Diagnostic أو Monthly Ops أو Executive Command Center.</li>
            </ul>
          </section>
        </div>

        <section className="mt-10 rounded-3xl border border-emerald-300/20 bg-emerald-400/10 p-8">
          <h2 className="text-2xl font-black text-emerald-100">رسالة البيع</h2>
          <p className="mt-4 leading-8 text-slate-200">
            إذا كانت الشركة عندها فواتير، مدفوعات، Leads، ومتابعات موزعة بين أكثر من أداة، Dealix يحولها إلى Proof Pack وخطة تشغيل واضحة خلال أسبوع.
          </p>
        </section>

        <div className="mt-10 flex flex-wrap gap-4">
          <a className="rounded-2xl bg-amber-300 px-6 py-3 font-bold text-slate-950" href="/ar/demo">
            افتح الديمو
          </a>
          <a className="rounded-2xl border border-white/20 px-6 py-3 font-bold text-white" href="/revenue-os">
            Revenue OS
          </a>
        </div>
      </section>
    </main>
  );
}
