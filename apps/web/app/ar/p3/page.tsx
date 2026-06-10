export const metadata = {
  title: "Dealix P3 — Executive Command Center | غرفة القيادة التنفيذية",
  description: "غرفة قيادة للمؤسس: الإيراد، الفرص، المخاطر، القرارات، وProof Packs في مكان واحد. 20,000–60,000 ريال إعداد.",
};

const modules = [
  { title: "Executive Cockpit", desc: "لوحة قيادة تنفيذية تعرض الإيراد والفرص والمخاطر في وقت واحد." },
  { title: "Weekly Decision Brief", desc: "ملخص أسبوعي للمؤسس: ماذا يحدث، ما القرار، ما الخطر." },
  { title: "Sales Motion Scorecards", desc: "قياس كل motion بيعي: pipeline، متابعات، إغلاق، اعتراضات." },
  { title: "Pipeline Risk Map", desc: "خريطة تكشف الفرص المعلقة والمخاطر قبل أن تتحول إلى خسائر." },
  { title: "Proof Pack Tracker", desc: "تتبع كل Proof Pack مع الحالة والتاريخ والعميل المرتبط." },
  { title: "Founder Daily Digest", desc: "ملخص يومي للمؤسس: أهم 3 قرارات + 5 متابعات + تنبيهات." },
  { title: "KPI Registry", desc: "سجل KPIs محدّث أسبوعياً مع trend وتوصية الأسبوع القادم." },
  { title: "Decision Log", desc: "توثيق كل قرار تجاري مع السياق والنتيجة والتعلّم." },
  { title: "Governance Rules", desc: "قواعد تشغيل داخلية: ما يتطلب موافقة، ما يتطلب review، ما يُمنع." },
  { title: "Operations Checklist", desc: "قائمة تحقق أسبوعية لمتابعة كل مسار تشغيلي." },
];

export default function P3Page() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Hero */}
        <p className="mb-4 inline-flex rounded-full border border-violet-300/30 px-4 py-2 text-sm text-violet-100">
          P3 — Executive Command Center
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-tight md:text-6xl">
          غرفة قيادة للمؤسس تجمع كل شيء في مكان واحد.
        </h1>
        <p className="mt-6 max-w-4xl text-lg leading-8 text-slate-300">
          ليس CRM جديداً. غرفة قيادة تنفيذية تعرض الإيراد، الفرص، المخاطر، القرارات، وProof Packs — وتعطيك كل أسبوع Decision Brief واضح.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <a
            href="mailto:hello@dealix.me?subject=أريد%20عرض%20P3"
            className="rounded-2xl bg-violet-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-violet-300"
          >
            اطلب عرض P3
          </a>
          <a
            href="/ar/p2"
            className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold text-white hover:bg-white/10"
          >
            ابدأ بـ P2 أولاً ←
          </a>
        </div>

        {/* For whom */}
        <section className="mt-20 rounded-3xl border border-white/10 bg-white/[0.04] p-8 md:p-12">
          <h2 className="text-3xl font-black">لمن هذا المنتج؟</h2>
          <ul className="mt-6 space-y-4">
            {[
              "المؤسس الذي لا يريد CRM جديد، يريد غرفة قيادة واحدة.",
              "شركة خدمات فيها أكثر من مسار بيعي وتشغيلي.",
              "وكالة تريد رؤية واضحة للفرص والتسليم في مكان واحد.",
              "إدارة تحتاج weekly decision brief بدون اجتماع إضافي.",
              "مؤسس يريد قياس كل قرار وتوثيق كل نتيجة.",
            ].map((item) => (
              <li key={item} className="flex items-start gap-3 text-slate-300">
                <span className="mt-1 text-violet-400">▸</span>
                {item}
              </li>
            ))}
          </ul>
        </section>

        {/* Modules */}
        <section className="mt-16">
          <h2 className="text-3xl font-black">مكونات غرفة القيادة</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {modules.map((m) => (
              <article
                key={m.title}
                className="rounded-3xl border border-white/10 bg-white/[0.05] p-6"
              >
                <h3 className="text-lg font-black text-violet-200">{m.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">{m.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Pricing */}
        <section className="mt-16">
          <h2 className="text-3xl font-black">الأسعار</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {[
              { label: "Setup", price: "20,000 – 60,000", unit: "ريال مرة واحدة", desc: "إعداد وتخصيص كامل حسب حجم الشركة." },
              { label: "Monthly", price: "12,000 – 35,000", unit: "ريال/شهر", desc: "تشغيل وتحديث ومراجعة أسبوعية مستمرة." },
              { label: "Enterprise", price: "Quote", unit: "حسب النطاق", desc: "تكاملات خاصة، أكثر من مسار، فريق موسع." },
            ].map((t) => (
              <article key={t.label} className="rounded-3xl border border-violet-400/30 bg-violet-400/5 p-8">
                <h3 className="text-xl font-black text-violet-100">{t.label}</h3>
                <p className="mt-2 text-2xl font-black text-violet-300">{t.price}</p>
                <p className="text-sm text-slate-400">{t.unit}</p>
                <p className="mt-4 text-sm leading-6 text-slate-300">{t.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Journey */}
        <section className="mt-16 rounded-3xl border border-white/10 bg-white/[0.04] p-8 md:p-12">
          <h2 className="text-3xl font-black">مسار البيع الصحيح</h2>
          <p className="mt-3 text-slate-400">لا نبيع P3 كخطوة أولى. التسلسل الطبيعي:</p>
          <ol className="mt-8 space-y-5">
            {[
              ["P1 Revenue Intelligence Sprint", "5–7 أيام. نثبت القيمة. نسلّم Proof Pack.", "/ar/p1", "bg-cyan-400/20 text-cyan-300"],
              ["P2 AI Sales Ops Assistant", "تشغيل شهري. متابعات، مسودات، scorecards.", "/ar/p2", "bg-emerald-400/20 text-emerald-300"],
              ["P3 Executive Command Center", "غرفة القيادة الكاملة عندما تحتاج رؤية تنفيذية شاملة.", "/ar/p3", "bg-violet-400/20 text-violet-300"],
            ].map(([title, desc, href, cls], i) => (
              <li key={String(title)} className="flex items-start gap-5">
                <span className={`mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-black ${cls}`}>
                  {i + 1}
                </span>
                <div>
                  <a href={String(href)} className="font-black text-slate-100 hover:underline">{String(title)}</a>
                  <p className="mt-1 text-sm text-slate-400">{String(desc)}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>

        {/* CTA */}
        <section className="mt-16 text-center">
          <h2 className="text-3xl font-black">جاهز لغرفة القيادة؟</h2>
          <p className="mt-3 text-slate-400">نبدأ بتقييم احتياجاتك ونصمم الحل المناسب.</p>
          <a
            href="mailto:hello@dealix.me?subject=أريد%20عرض%20P3"
            className="mt-6 inline-block rounded-2xl bg-violet-400 px-10 py-4 text-xl font-black text-[#06111f] hover:bg-violet-300"
          >
            اطلب عرض P3 الآن
          </a>
        </section>

      </div>
    </main>
  );
}
