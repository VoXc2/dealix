export const metadata = {
  title: "Dealix Transformation OS — أنظمة تحول للشركات",
  description:
    "Dealix يبني أنظمة تشغيل أعمال مخصصة للشركات: مبيعات، واتساب، هوية، تقارير، أتمتة، تجربة عميل، وحوكمة AI.",
};

const systems = [
  {
    title: "WhatsApp Revenue OS",
    desc: "تحويل واتساب من محادثات مشتتة إلى pipeline مبيعات ومتابعة وحجوزات وتقارير.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
  {
    title: "Review Intelligence OS",
    desc: "تحويل التقييمات والشكاوى إلى قرارات تشغيلية وتقارير للإدارة والفروع.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
  {
    title: "AI Business Command Center",
    desc: "غرفة قيادة تنفيذية تربط المبيعات، المتابعة، العروض، التقييمات، والتقارير.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
  {
    title: "Brand Intelligence OS",
    desc: "توحيد الهوية، الرسائل، العروض، قوالب المحتوى، ونبرة العلامة عبر القنوات.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
  {
    title: "AI Agent Workforce OS",
    desc: "تصميم agents داخل الشركة لأدوار واضحة مع صلاحيات وحدود ومراجعة بشرية.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
  {
    title: "Custom Enterprise System",
    desc: "نظام مخصص حسب عمليات الشركة وبياناتها وفريقها وتكاملاتها.",
    price: "عرض مخصص بعد Qualified Discovery",
  },
];

export default function TransformationPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Dealix Transformation OS
        </p>

        <h1 className="max-w-5xl text-4xl font-black leading-[1.15] md:text-7xl">
          نبني للشركات أنظمة تشغيل تحول الفوضى اليومية إلى نمو قابل للقياس.
        </h1>

        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          Dealix لا يبيع بوتات أو داشبورد فقط. نحن نصمم وننفذ أنظمة تربط واتساب، المبيعات،
          المتابعة، التقييمات، الهوية، التقارير، وتجربة العميل في منظومة واحدة.
        </p>

        <div className="mt-10 flex flex-wrap gap-4">
          <a href="/ar/diagnostic-sprint" className="rounded-2xl bg-cyan-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300">
            ابدأ بالتشخيص التنفيذي المجاني
          </a>
          <a href="/ar/company-os" className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold hover:bg-white/10">
            شاهد نظام الشركة اليومي
          </a>
        </div>
      </section>

      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-3xl font-black">الأنظمة التي يمكن أن نبنيها لك</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {systems.map((system) => (
              <article key={system.title} className="rounded-3xl border border-white/10 bg-white/[0.04] p-6">
                <h3 className="text-xl font-black text-cyan-100">{system.title}</h3>
                <p className="mt-4 leading-7 text-slate-300">{system.desc}</p>
                <p className="mt-5 rounded-xl bg-white/[0.06] px-4 py-3 text-sm text-slate-200">
                  {system.price}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="text-3xl font-black">طريقة التنفيذ</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-5">
          {["تشخيص", "تصميم", "بناء", "تشغيل تجريبي", "توسع"].map((step, idx) => (
            <div key={step} className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
              <p className="text-sm text-cyan-300">0{idx + 1}</p>
              <h3 className="mt-2 text-lg font-black">{step}</h3>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
