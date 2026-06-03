export const metadata = {
  title: "Dealix — نظام الإيراد للشركات السعودية",
  description:
    "Dealix يحوّل بيانات المبيعات والمتابعات إلى Revenue OS عملي خلال 5–7 أيام. تشخيص مدفوع، تشغيل شهري، غرفة قيادة تنفيذية.",
};

const pains = [
  "leads تموت بدون متابعة منظمة",
  "رسائل عشوائية لا تُغلق صفقات",
  "Pipeline في Excel بدون أولويات",
  "اعتراضات تتكرر بدون توثيق أو رد",
  "المؤسس يتابع يدوياً ويضيع وقته",
  "لا تعرف أين تضيع إيراداتك كل شهر",
];

const steps = [
  {
    num: "01",
    title: "P1 — تشخيص سريع في أسبوع",
    body: "نأخذ عينة من بياناتك ونسلّم Proof Pack: خريطة تسرب الإيراد، أفضل 20 فرصة للمتابعة، مسودات رسائل جاهزة.",
    price: "3,500–15,000 ريال",
    href: "/ar/p1",
    color: "border-cyan-400/40 bg-cyan-400/5",
    tag: "text-cyan-300",
    cta: "bg-cyan-400 hover:bg-cyan-300",
  },
  {
    num: "02",
    title: "P2 — تشغيل شهري بدون فريق",
    body: "كل أسبوع: أولويات المتابعة، مسودات الرسائل، تحضير الاجتماعات، Scorecard قابل للقياس. أنت تراجع وترسل.",
    price: "8,000–30,000 ريال/شهر",
    href: "/ar/p2",
    color: "border-emerald-400/50 bg-emerald-400/10",
    tag: "text-emerald-300",
    cta: "bg-emerald-400 hover:bg-emerald-300",
  },
  {
    num: "03",
    title: "P3 — غرفة قيادة تنفيذية",
    body: "الإيراد، القرارات، المخاطر، وProof Packs في مكان واحد. Weekly Decision Brief للمؤسس بدون اجتماع إضافي.",
    price: "20,000–60,000 ريال إعداد",
    href: "/ar/p3",
    color: "border-violet-400/40 bg-violet-400/5",
    tag: "text-violet-300",
    cta: "bg-violet-400 hover:bg-violet-300",
  },
];

const differentiators = [
  {
    title: "نبدأ بإثبات القيمة",
    body: "P1 هو تشخيص مدفوع خلال أسبوع — لا عقد شهري، لا التزام طويل، فقط نتيجة أولاً.",
  },
  {
    title: "AI يكتب، أنت ترسل",
    body: "لا auto-send في أي منتج. Dealix يحضّر المسودات والأولويات؛ القرار النهائي لك دائماً.",
  },
  {
    title: "بيانات حقيقية فقط",
    body: "لا ROI claims بدون baseline موثق. لا scraping لبيانات خارجية. نعمل فقط على ما تشاركنا إياه.",
  },
  {
    title: "Saudi-first",
    body: "تصميم للشركات السعودية: عربي أولاً، ZATCA-aware، يناسب طريقة عمل فرق المبيعات المحلية.",
  },
];

export default function ArabicHomePage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">

      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Revenue OS للشركات السعودية
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-[1.15] md:text-7xl">
          حوّل بيانات مبيعاتك إلى نظام إيراد واضح خلال أسبوع واحد.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          Dealix يأخذ pipeline المتوقف، والمتابعات العشوائية، والفرص الضائعة — ويحوّلها إلى أولويات واضحة، مسودات جاهزة، وقرارات موثّقة.
        </p>
        <div className="mt-10 flex flex-wrap gap-4">
          <a
            href="/ar/p1"
            className="rounded-2xl bg-cyan-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
          >
            ابدأ تشخيص P1 — أسبوع واحد
          </a>
          <a
            href="/ar/pricing"
            className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold text-white hover:bg-white/10"
          >
            الأسعار الكاملة
          </a>
        </div>
        <p className="mt-5 text-sm text-slate-500">
          لا عقد شهري قبل إثبات القيمة · لا auto-send · AI يكتب، أنت ترسل
        </p>
      </section>

      {/* ── Pain ─────────────────────────────────────────────────────── */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-3xl font-black">إذا كانت هذه مشاكلك، Dealix صُنع لك.</h2>
          <div className="mt-8 grid gap-3 sm:grid-cols-2 md:grid-cols-3">
            {pains.map((pain) => (
              <div
                key={pain}
                className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-4"
              >
                <span className="mt-0.5 text-red-400">✕</span>
                <p className="text-sm leading-6 text-slate-300">{pain}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Product staircase ────────────────────────────────────────── */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-3 text-sm text-slate-500">التسلسل الصحيح دائماً</p>
        <h2 className="text-3xl font-black">ثلاثة منتجات. تسلسل واحد.</h2>
        <p className="mt-3 max-w-2xl text-slate-400">
          نبدأ بإثبات القيمة في P1. بعد الإثبات ننتقل لـ P2. عندما يحتاج المؤسس رؤية تنفيذية كاملة نضيف P3.
        </p>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {steps.map((s) => (
            <article
              key={s.num}
              className={`relative rounded-3xl border ${s.color} p-8 flex flex-col`}
            >
              <p className={`text-xs font-black ${s.tag}`}>{s.num}</p>
              <h3 className="mt-3 text-xl font-black text-slate-100">{s.title}</h3>
              <p className="mt-3 flex-1 text-sm leading-7 text-slate-400">{s.body}</p>
              <p className={`mt-4 text-lg font-black ${s.tag}`}>{s.price}</p>
              <a
                href={s.href}
                className={`mt-5 block rounded-2xl ${s.cta} px-5 py-2.5 text-center text-sm font-black text-[#06111f]`}
              >
                اعرف المزيد
              </a>
            </article>
          ))}
        </div>
      </section>

      {/* ── Why Dealix ───────────────────────────────────────────────── */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-3xl font-black">لماذا Dealix؟</h2>
          <div className="mt-8 grid gap-5 sm:grid-cols-2">
            {differentiators.map((d) => (
              <div
                key={d.title}
                className="rounded-3xl border border-white/10 bg-white/[0.03] p-7"
              >
                <h3 className="text-lg font-black text-slate-100">{d.title}</h3>
                <p className="mt-2 text-sm leading-7 text-slate-400">{d.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Journey CTA ──────────────────────────────────────────────── */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="rounded-3xl border border-cyan-300/20 bg-cyan-400/5 p-10 md:p-14 text-center">
          <h2 className="text-3xl font-black md:text-4xl">جاهز تبدأ؟</h2>
          <p className="mt-4 text-lg text-slate-300">
            P1 يبدأ خلال 24 ساعة من الاتفاق. لا عقد شهري. لا التزام طويل. فقط نتيجة.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="mailto:hello@dealix.me?subject=أريد%20تشخيص%20P1"
              className="rounded-2xl bg-cyan-400 px-10 py-4 text-xl font-black text-[#06111f] hover:bg-cyan-300"
            >
              احجز تشخيص P1
            </a>
            <a
              href="/ar/demo"
              className="rounded-2xl border border-white/20 px-10 py-4 text-xl font-semibold text-white hover:bg-white/10"
            >
              شاهد الديمو أولاً
            </a>
          </div>
        </div>
      </section>

      {/* ── Footer nav ───────────────────────────────────────────────── */}
      <footer className="border-t border-white/5 py-10">
        <div className="mx-auto max-w-6xl px-6 flex flex-wrap justify-between gap-6 text-sm text-slate-500">
          <span className="font-black text-white">Dealix</span>
          <nav className="flex flex-wrap gap-6">
            <a href="/ar/p1" className="hover:text-cyan-300">P1 تشخيص</a>
            <a href="/ar/p2" className="hover:text-emerald-300">P2 تشغيل شهري</a>
            <a href="/ar/p3" className="hover:text-violet-300">P3 قيادة تنفيذية</a>
            <a href="/ar/pricing" className="hover:text-white">الأسعار</a>
            <a href="/ar/demo" className="hover:text-white">الديمو</a>
            <a href="/ar/zatca-readiness" className="hover:text-amber-300">ZATCA</a>
            <a href="mailto:hello@dealix.me" className="hover:text-white">تواصل معنا</a>
          </nav>
        </div>
      </footer>

    </main>
  );
}
