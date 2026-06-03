export const metadata = {
  title: "Dealix — الأسعار | P1 · P2 · P3",
  description: "أسعار Dealix الكاملة: P1 تشخيص الإيراد، P2 تشغيل المبيعات الشهري، P3 غرفة القيادة التنفيذية.",
};

const products = [
  {
    id: "p1",
    label: "P1",
    name: "Revenue Intelligence Sprint",
    nameAr: "تشخيص الإيراد",
    price: "3,500 – 15,000",
    unit: "ريال · مرة واحدة",
    duration: "5–7 أيام",
    desc: "نكشف أين تضيع الإيرادات ونسلّم Proof Pack جاهز للتنفيذ.",
    cta: "ابدأ P1",
    href: "/ar/p1",
    border: "border-cyan-400/40",
    bg: "bg-cyan-400/5",
    badge: "bg-cyan-400",
    text: "text-cyan-300",
    ctaBg: "bg-cyan-400 hover:bg-cyan-300",
    best: false,
    includes: [
      "Revenue Leakage Map",
      "Top 20 Follow-up List",
      "Message Draft Pack",
      "Objection Intelligence",
      "30-Day Revenue Plan",
      "Executive Proof Pack",
    ],
  },
  {
    id: "p2",
    label: "P2",
    name: "AI Sales Ops Assistant",
    nameAr: "تشغيل المبيعات الشهري",
    price: "8,000 – 30,000",
    unit: "ريال/شهر",
    duration: "تشغيل مستمر",
    desc: "طبقة تشغيل أسبوعية تنتج أولويات ومسودات وscorecard بدون auto-send.",
    cta: "اطلب عرض P2",
    href: "/ar/p2",
    border: "border-emerald-400/50",
    bg: "bg-emerald-400/10",
    badge: "bg-emerald-400",
    text: "text-emerald-300",
    ctaBg: "bg-emerald-400 hover:bg-emerald-300",
    best: true,
    includes: [
      "Weekly Pipeline Review",
      "Follow-up Priority List",
      "Message Drafts (موافقة مطلوبة)",
      "Meeting Prep Packs",
      "Weekly Scorecard",
      "Monthly Executive Summary",
    ],
  },
  {
    id: "p3",
    label: "P3",
    name: "Executive Command Center",
    nameAr: "غرفة القيادة التنفيذية",
    price: "20,000 – 60,000",
    unit: "ريال إعداد + شهري",
    duration: "إعداد + تشغيل",
    desc: "غرفة قيادة للمؤسس: الإيراد، القرارات، المخاطر، وProof Packs في مكان واحد.",
    cta: "اطلب عرض P3",
    href: "/ar/p3",
    border: "border-violet-400/40",
    bg: "bg-violet-400/5",
    badge: "bg-violet-400",
    text: "text-violet-300",
    ctaBg: "bg-violet-400 hover:bg-violet-300",
    best: false,
    includes: [
      "Executive Cockpit",
      "Weekly Decision Brief",
      "KPI Registry",
      "Pipeline Risk Map",
      "Proof Pack Tracker",
      "Decision Log + Governance",
    ],
  },
];

export default function PricingPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Hero */}
        <p className="mb-4 inline-flex rounded-full border border-white/20 px-4 py-2 text-sm text-slate-300">
          الأسعار
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-tight md:text-6xl">
          ابدأ بإثبات القيمة. لا عقود طويلة.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
          ثلاثة منتجات واضحة. تبدأ بـ P1 في أسبوع واحد، ثم تتحول لـ P2 إذا أثبتنا القيمة، ثم P3 عندما تحتاج رؤية تنفيذية كاملة.
        </p>

        {/* Products grid */}
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {products.map((p) => (
            <article
              key={p.id}
              className={`relative rounded-3xl border ${p.border} ${p.bg} p-8 flex flex-col`}
            >
              {p.best && (
                <span className={`absolute -top-3 right-8 rounded-full ${p.badge} px-4 py-1 text-xs font-black text-[#06111f]`}>
                  الأكثر طلباً
                </span>
              )}
              <p className={`text-xs font-black ${p.text} mb-2`}>{p.label}</p>
              <h2 className="text-2xl font-black text-slate-100">{p.name}</h2>
              <p className="text-sm text-slate-400">{p.nameAr}</p>
              <p className={`mt-4 text-3xl font-black ${p.text}`}>{p.price}</p>
              <p className="text-sm text-slate-400">{p.unit}</p>
              <p className="mt-1 text-xs text-slate-500">{p.duration}</p>
              <p className="mt-5 text-sm leading-6 text-slate-300">{p.desc}</p>
              <ul className="mt-6 space-y-2 text-sm text-slate-400 flex-1">
                {p.includes.map((item) => (
                  <li key={item} className="flex items-center gap-2">
                    <span className={p.text}>✓</span> {item}
                  </li>
                ))}
              </ul>
              <a
                href={p.href}
                className={`mt-8 block rounded-2xl ${p.ctaBg} px-6 py-3 text-center font-black text-[#06111f]`}
              >
                {p.cta}
              </a>
            </article>
          ))}
        </div>

        {/* Journey */}
        <section className="mt-20 rounded-3xl border border-white/10 bg-white/[0.03] p-8 md:p-12">
          <h2 className="text-3xl font-black">التسلسل الصحيح</h2>
          <p className="mt-3 text-slate-400">لا نبدأ بـ P3. دائماً نبدأ بـ P1.</p>
          <div className="mt-8 flex flex-wrap items-center gap-4 text-lg font-black">
            <a href="/ar/p1" className="text-cyan-300 hover:underline">P1 تشخيص</a>
            <span className="text-slate-600">→</span>
            <a href="/ar/p2" className="text-emerald-300 hover:underline">P2 تشغيل شهري</a>
            <span className="text-slate-600">→</span>
            <a href="/ar/p3" className="text-violet-300 hover:underline">P3 قيادة تنفيذية</a>
          </div>
          <p className="mt-5 leading-7 text-slate-400">
            P1 يثبت القيمة خلال أسبوع. P2 يحول الإثبات إلى تشغيل شهري ودخل متكرر. P3 يأتي عندما يريد المؤسس رؤية تنفيذية كاملة لشركته.
          </p>
        </section>

        {/* Governance */}
        <section className="mt-12 rounded-3xl border border-slate-700 bg-slate-900/50 p-8">
          <h2 className="text-2xl font-black">الحوكمة في كل المنتجات</h2>
          <div className="mt-5 grid gap-3 md:grid-cols-2 text-sm text-slate-300">
            {[
              "AI drafts → أنت تراجع → أنت ترسل",
              "لا auto-send في أي منتج",
              "لا scraping لبيانات خارجية",
              "لا ROI claims بدون baseline موثق",
              "لا نشر خارجي بدون موافقة صريحة",
              "لا دفع حقيقي بدون تفعيل MOYASAR_LIVE_MODE",
            ].map((rule) => (
              <div key={rule} className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                {rule}
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mt-16 text-center">
          <h2 className="text-3xl font-black">ابدأ الأسبوع القادم</h2>
          <p className="mt-3 text-slate-400">P1 يبدأ خلال 24 ساعة من الاتفاق.</p>
          <a
            href="mailto:hello@dealix.me?subject=أريد%20البدء%20مع%20Dealix"
            className="mt-6 inline-block rounded-2xl bg-white px-10 py-4 text-xl font-black text-[#06111f] hover:bg-slate-100"
          >
            تواصل معنا الآن
          </a>
        </section>

      </div>
    </main>
  );
}
