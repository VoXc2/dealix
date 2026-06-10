export const metadata = {
  title: "Dealix P2 — AI Sales Ops Assistant | تشغيل المبيعات الشهري",
  description: "طبقة تشغيل شهرية تنتج أولويات المتابعة، مسودات الرسائل، تحضير الاجتماعات، وScorecard أسبوعي. 8,000–30,000 ريال/شهر.",
};

const weeklyOutputs = [
  { title: "Pipeline Review", desc: "مراجعة كاملة للفرص: ما تحرّك، ما توقف، ما يحتاج قرار." },
  { title: "Follow-up Priority List", desc: "أفضل 10–15 فرصة تستحق المتابعة هذا الأسبوع مرتبة حسب الأولوية." },
  { title: "Message Draft Queue", desc: "مسودات رسائل جاهزة للمراجعة — واتساب وبريد — لا تُرسل دون موافقة." },
  { title: "Meeting Prep Packs", desc: "تحضير لكل اجتماع: خلفية العميل، الاعتراضات المتوقعة، الهدف المقترح." },
  { title: "Objection Intelligence", desc: "توثيق الاعتراضات الجديدة وتحديث قاعدة الردود." },
  { title: "Offer Test Queue", desc: "اقتراحات اختبار عروض جديدة أو تعديل الرسائل بناءً على البيانات." },
  { title: "Weekly Scorecard", desc: "قياس أسبوعي: leads، متابعات، ردود، عروض، إغلاق." },
  { title: "Monthly Executive Summary", desc: "ملخص شهري للمؤسس: ماذا نجح، ماذا فشل، القرار القادم." },
];

const tiers = [
  {
    name: "Light",
    price: "8,000 – 12,000",
    team: "فريق صغير 1–3 أشخاص",
    highlight: false,
  },
  {
    name: "Growth",
    price: "15,000 – 25,000",
    team: "pipeline نشط + متابعات أسبوعية",
    highlight: true,
  },
  {
    name: "High Touch",
    price: "30,000+",
    team: "تشغيل عميق + تدريب + governance",
    highlight: false,
  },
];

export default function P2Page() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Hero */}
        <p className="mb-4 inline-flex rounded-full border border-emerald-300/30 px-4 py-2 text-sm text-emerald-100">
          P2 — AI Sales Ops Assistant
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-tight md:text-6xl">
          نظام متابعة أسبوعي يشتغل بدلاً عنك.
        </h1>
        <p className="mt-6 max-w-4xl text-lg leading-8 text-slate-300">
          بعد P1، تتحول Dealix إلى مساعد Sales Ops شهري. كل أسبوع تحصل على: أولويات المتابعة، مسودات الرسائل، تحضير الاجتماعات، ملخص الاعتراضات، وScorecard قابل للقياس.
        </p>
        <p className="mt-3 text-slate-400">
          القاعدة: AI يكتب → أنت تراجع → أنت ترسل. لا auto-send. لا spam. لا التزامات خارج نطاق العمل.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <a
            href="mailto:hello@dealix.me?subject=أريد%20عرض%20P2"
            className="rounded-2xl bg-emerald-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-emerald-300"
          >
            اطلب عرض P2
          </a>
          <a
            href="/ar/p1"
            className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold text-white hover:bg-white/10"
          >
            ابدأ بـ P1 أولاً ←
          </a>
        </div>

        {/* Weekly outputs */}
        <section className="mt-20">
          <h2 className="text-3xl font-black">ما تحصل عليه كل أسبوع</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2">
            {weeklyOutputs.map((o) => (
              <article
                key={o.title}
                className="rounded-3xl border border-white/10 bg-white/[0.05] p-6"
              >
                <h3 className="text-lg font-black text-emerald-200">{o.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">{o.desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* How it works */}
        <section className="mt-16 rounded-3xl border border-white/10 bg-white/[0.04] p-8 md:p-12">
          <h2 className="text-3xl font-black">كيف يشتغل</h2>
          <ol className="mt-8 space-y-6">
            {[
              ["تشخيص P1 أولاً", "نفهم بياناتك ونثبت القيمة قبل الالتزام الشهري."],
              ["كل أسبوع: مراجعة وأولويات", "Dealix يحلل الحركة في pipeline ويرتب من تتابع أولاً."],
              ["مسودات جاهزة للمراجعة", "رسائل متابعة وتحضير اجتماعات — أنت تراجع، أنت ترسل."],
              ["Scorecard أسبوعي", "قياس واضح: leads، ردود، عروض، إغلاق."],
              ["تقرير شهري للمؤسس", "ملخص تنفيذي بالنتائج والقرار القادم."],
            ].map(([title, desc], i) => (
              <li key={title} className="flex gap-5">
                <span className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-400/20 text-sm font-black text-emerald-300">
                  {i + 1}
                </span>
                <div>
                  <p className="font-black text-slate-100">{title}</p>
                  <p className="mt-1 text-sm leading-6 text-slate-400">{desc}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>

        {/* Pricing */}
        <section className="mt-16">
          <h2 className="text-3xl font-black">الأسعار الشهرية</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {tiers.map((t) => (
              <article
                key={t.name}
                className={`rounded-3xl border p-8 ${
                  t.highlight
                    ? "border-emerald-400/50 bg-emerald-400/10"
                    : "border-white/10 bg-white/[0.04]"
                }`}
              >
                {t.highlight && (
                  <p className="mb-3 inline-block rounded-full bg-emerald-400 px-3 py-1 text-xs font-black text-[#06111f]">
                    الأكثر طلباً
                  </p>
                )}
                <h3 className="text-2xl font-black text-slate-100">{t.name}</h3>
                <p className="mt-2 text-2xl font-black text-emerald-300">
                  {t.price} <span className="text-base text-slate-400">ريال/شهر</span>
                </p>
                <p className="mt-3 text-sm leading-6 text-slate-400">{t.team}</p>
              </article>
            ))}
          </div>
        </section>

        {/* Governance */}
        <section className="mt-16 rounded-3xl border border-cyan-300/20 bg-cyan-400/5 p-8">
          <h2 className="text-2xl font-black text-cyan-100">الحوكمة والأمان</h2>
          <ul className="mt-5 space-y-3 text-slate-300">
            {[
              "لا auto-send — كل رسالة تحتاج موافقتك.",
              "لا scraping — نعمل فقط على بياناتك التي تشاركها.",
              "لا ROI claims بدون baseline موثق.",
              "لا اتصال بعملائك مباشرة بدون إذن صريح.",
            ].map((rule) => (
              <li key={rule} className="flex gap-3">
                <span className="text-cyan-400">✓</span>
                {rule}
              </li>
            ))}
          </ul>
        </section>

        {/* Upsell P3 */}
        <section className="mt-16 rounded-3xl border border-violet-300/20 bg-violet-400/5 p-8">
          <h2 className="text-2xl font-black text-violet-100">تحتاج رؤية تنفيذية أشمل؟</h2>
          <p className="mt-3 leading-7 text-slate-300">
            P3 يضيف غرفة قيادة للمؤسس: KPI registry، decision log، risk map، وProof Tracker في مكان واحد.
          </p>
          <a href="/ar/p3" className="mt-5 inline-block rounded-2xl border border-violet-400/40 px-6 py-3 text-violet-300 hover:bg-violet-400/10">
            اعرف المزيد عن P3 ←
          </a>
        </section>

        {/* CTA */}
        <section className="mt-16 text-center">
          <h2 className="text-3xl font-black">جاهز للتشغيل الشهري؟</h2>
          <p className="mt-3 text-slate-400">نبدأ بـ P1، وبعد Proof Pack نتحول لـ P2.</p>
          <a
            href="mailto:hello@dealix.me?subject=أريد%20عرض%20P2"
            className="mt-6 inline-block rounded-2xl bg-emerald-400 px-10 py-4 text-xl font-black text-[#06111f] hover:bg-emerald-300"
          >
            اطلب عرض P2 الآن
          </a>
        </section>

      </div>
    </main>
  );
}
