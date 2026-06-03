export const metadata = {
  title: "Dealix P1 — Revenue Intelligence Sprint | تشخيص الإيراد",
  description: "خلال 5–7 أيام نكشف أين تضيع الإيرادات، ونرتب أول 20 فرصة، ونسلّم Proof Pack جاهز للتنفيذ. 3,500–15,000 ريال.",
};

const deliverables = [
  { num: "01", title: "Revenue Leakage Map", desc: "خريطة تكشف أين تضيع الإيرادات الآن بالتفصيل." },
  { num: "02", title: "Pipeline Diagnosis", desc: "تشخيص كامل للفرص الموجودة وسبب توقفها." },
  { num: "03", title: "ICP Priority Map", desc: "تحديد الشريحة المثلى وترتيب الأولويات حسب احتمالية الإغلاق." },
  { num: "04", title: "Top 20 Follow-up List", desc: "قائمة بأفضل 20 فرصة تستحق المتابعة الفورية." },
  { num: "05", title: "Message Draft Pack", desc: "10–20 مسودة رسالة متابعة جاهزة للمراجعة والإرسال." },
  { num: "06", title: "Objection Intelligence", desc: "توثيق الاعتراضات المتكررة وأفضل ردود عليها." },
  { num: "07", title: "Offer Angle Map", desc: "العرض والرسالة الأنسب لكل شريحة عملاء." },
  { num: "08", title: "30-Day Revenue Plan", desc: "خطة تنفيذية لأول 30 يوم بعد التشخيص." },
  { num: "09", title: "Weekly Scorecard", desc: "نموذج قياس أسبوعي لمتابعة التقدم." },
  { num: "10", title: "Executive Proof Pack", desc: "تقرير تنفيذي بالنتائج والأدلة جاهز للعرض." },
];

const tiers = [
  {
    name: "Starter Diagnostic",
    price: "3,500 – 7,500",
    duration: "5 أيام",
    desc: "مناسب لأول تشخيص مع عينة بيانات.",
    highlight: false,
  },
  {
    name: "Premium Proof Pack",
    price: "8,000 – 15,000",
    duration: "7 أيام",
    desc: "بيانات أعمق، قنوات متعددة، تقرير تنفيذي كامل.",
    highlight: true,
  },
];

const objections = [
  { q: "عندنا CRM", a: "ممتاز. Dealix لا يستبدل CRM، يوضح ماذا تفعل بالفرص الموجودة داخله." },
  { q: "السعر عالٍ", a: "إذا فرصة واحدة مغلقة تغطي التكلفة، فالسؤال ليس السعر — أين تضيع الفرص الآن؟" },
  { q: "نخاف AI يرسل بدوننا", a: "Dealix لا يرسل. يكتب مسودات، والمؤسس يوافق ويرسل." },
  { q: "محتاجين نشوف نتيجة أولاً", a: "هذا بالضبط سبب وجود P1. لا نطلب عقداً شهرياً قبل Proof Pack." },
];

export default function P1Page() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Hero */}
        <p className="mb-4 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          P1 — Revenue Intelligence Sprint
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-tight md:text-6xl">
          اكتشف أين تضيع إيراداتك خلال أسبوع واحد.
        </h1>
        <p className="mt-6 max-w-4xl text-lg leading-8 text-slate-300">
          تشخيص مدفوع مدته 5–7 أيام. نأخذ عينة من بياناتك، نبني خريطة التسرب، نرتب الأولويات، ونسلّم Proof Pack جاهز للتنفيذ — لا نطلب عقداً شهرياً قبل أن تثق بالنتيجة.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <a
            href="mailto:hello@dealix.me?subject=أريد%20تشخيص%20P1"
            className="rounded-2xl bg-cyan-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
          >
            احجز تشخيصك الآن
          </a>
          <a
            href="/ar/demo"
            className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold text-white hover:bg-white/10"
          >
            شاهد الديمو أولاً
          </a>
        </div>

        {/* Pain section */}
        <section className="mt-20 rounded-3xl border border-white/10 bg-white/[0.04] p-8 md:p-12">
          <h2 className="text-3xl font-black text-slate-100">إذا كان عندك أي من هذه المشاكل، هذا التشخيص لك.</h2>
          <ul className="mt-6 grid gap-3 md:grid-cols-2">
            {[
              "leads لا تتحرك منذ أسابيع",
              "رسائل متابعة عشوائية بدون نظام",
              "CRM أو Excel بدون أولويات واضحة",
              "عروض ترسلها ولا تعرف لماذا لا تُغلق",
              "اعتراضات تتكرر بدون توثيق",
              "مؤسس يتابع يدوياً ويضيع وقته",
            ].map((item) => (
              <li key={item} className="flex items-start gap-3 text-slate-300">
                <span className="mt-1 text-cyan-400">▸</span>
                {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Deliverables */}
        <section className="mt-16">
          <h2 className="text-3xl font-black">ما تحصل عليه خلال 5–7 أيام</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {deliverables.map((d) => (
              <article
                key={d.num}
                className="rounded-3xl border border-white/10 bg-white/[0.05] p-6"
              >
                <p className="text-xs font-bold text-cyan-400">{d.num}</p>
                <h3 className="mt-2 text-lg font-black text-slate-100">{d.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">{d.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Pricing */}
        <section className="mt-16">
          <h2 className="text-3xl font-black">الأسعار</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {tiers.map((t) => (
              <article
                key={t.name}
                className={`rounded-3xl border p-8 ${
                  t.highlight
                    ? "border-cyan-400/50 bg-cyan-400/10"
                    : "border-white/10 bg-white/[0.04]"
                }`}
              >
                {t.highlight && (
                  <p className="mb-3 inline-block rounded-full bg-cyan-400 px-3 py-1 text-xs font-black text-[#06111f]">
                    الأكثر قيمة
                  </p>
                )}
                <h3 className="text-2xl font-black text-slate-100">{t.name}</h3>
                <p className="mt-2 text-3xl font-black text-cyan-300">
                  {t.price} <span className="text-lg text-slate-400">ريال</span>
                </p>
                <p className="mt-1 text-sm text-slate-400">{t.duration}</p>
                <p className="mt-4 text-base leading-7 text-slate-300">{t.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Objection handling */}
        <section className="mt-16 rounded-3xl border border-amber-300/20 bg-amber-400/5 p-8 md:p-12">
          <h2 className="text-3xl font-black text-amber-100">أسئلة شائعة</h2>
          <div className="mt-8 space-y-6">
            {objections.map((o) => (
              <div key={o.q}>
                <p className="font-black text-slate-100">&ldquo;{o.q}&rdquo;</p>
                <p className="mt-2 leading-7 text-slate-300">{o.a}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Upsell to P2 */}
        <section className="mt-16 rounded-3xl border border-emerald-300/20 bg-emerald-400/5 p-8">
          <h2 className="text-2xl font-black text-emerald-100">بعد P1، الخطوة الطبيعية هي P2</h2>
          <p className="mt-3 leading-7 text-slate-300">
            بعد Proof Pack، تتحول من تشخيص إلى تشغيل شهري: متابعات أسبوعية، scorecards، مسودات، ومراجعات pipeline.
          </p>
          <a href="/ar/p2" className="mt-5 inline-block rounded-2xl border border-emerald-400/40 px-6 py-3 text-emerald-300 hover:bg-emerald-400/10">
            اعرف المزيد عن P2 ←
          </a>
        </section>

        {/* CTA */}
        <section className="mt-16 text-center">
          <h2 className="text-3xl font-black">جاهز تبدأ؟</h2>
          <p className="mt-3 text-slate-400">لا عقد شهري. لا التزام طويل. فقط نتيجة خلال أسبوع.</p>
          <a
            href="mailto:hello@dealix.me?subject=أريد%20تشخيص%20P1"
            className="mt-6 inline-block rounded-2xl bg-cyan-400 px-10 py-4 text-xl font-black text-[#06111f] hover:bg-cyan-300"
          >
            احجز تشخيص P1 الآن
          </a>
        </section>

      </div>
    </main>
  );
}
