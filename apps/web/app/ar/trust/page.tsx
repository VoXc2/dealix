export const metadata = {
  title: "Dealix — الثقة والخصوصية | Evidence-bounded · Approval-first",
  description:
    "كيف يدير Dealix الحوكمة والخصوصية بحدود موثقة: موافقة أولاً، لا أتمتة عمياء، ودعم للمتطلبات السعودية دون ادعاء اعتماد غير مثبت.",
};

const principles = [
  {
    icon: "🛡️",
    title: "PDPL-Aware Controls",
    titleEn: "Saudi Data Protection",
    desc: "نصمم تدفقات البيانات مع مراعاة مبادئ حماية البيانات ونطاق الاستخدام. مستوى التطبيق الفعلي يعتمد على تكوين العميل والضوابط المفعلة، ولا ندعي اعتماداً أو امتثالاً قانونياً تلقائياً.",
    points: [
      "تصنيف البيانات وفق السياسة المطبقة قبل المعالجة حيث يلزم",
      "حدود استخدام واضحة لكل نوع بيانات",
      "الاحتفاظ والحذف وفق سياسة موثقة ومفعلة",
      "لا بيانات شخصية في ملفات عامة",
    ],
  },
  {
    icon: "✋",
    title: "Approval-First",
    titleEn: "Human-in-the-Loop",
    desc: "AI يقترح ويحلل ويولّد. الإنسان يقرر وينفذ. لا رسالة تُرسل، لا عقد يُصدر، لا قرار تنفيذي يحدث تلقائياً بدون موافقة صريحة.",
    points: [
      "كل رسالة خارجية تحتاج مراجعة المؤسس",
      "كل عرض أو فاتورة تحتاج توقيع يدوي",
      "قوائم الموافقة موثقة وقابلة للمراجعة",
      "لا automation تصل العميل بدون إذن",
    ],
  },
  {
    icon: "📋",
    title: "ZATCA-Aware",
    titleEn: "Saudi Tax Compliance",
    desc: "يمكن تصميم تكاملات الفوترة لمراعاة متطلبات ZATCA بحسب نطاق العميل وموجة الربط. لا تمثل هذه الصفحة شهادة امتثال أو اعتماداً قانونياً.",
    points: [
      "حقول وتدفقات ZATCA تراجع حسب نطاق التكامل",
      "إعدادات الضريبة تضبط حسب الحالة والمرجع النظامي",
      "سجل مالي موثق لكل معاملة",
      "قنوات الدفع تحدد وتتحقق لكل تكامل",
    ],
  },
  {
    icon: "🚫",
    title: "No Overclaiming",
    titleEn: "Honest AI Boundaries",
    desc: "لا نعد بما لا نستطيع إثباته. لا نقول 'AI يضمن' أو 'نتائج مضمونة 100%'. نقول ما يمكن تحقيقه، ونوثق ما تحقق فعلاً.",
    points: [
      "لا ادعاءات تسويقية غير قابلة للإثبات",
      "كل نتيجة مُقدَّمة مبنية على بيانات فعلية",
      "مخرجات موثقة قابلة للمراجعة",
      "هامش الخطأ محدد بوضوح في كل تقرير",
    ],
  },
  {
    icon: "🔐",
    title: "Secrets Management",
    titleEn: "Credential Security",
    desc: "لا توضع مفاتيح أو credentials في source. الأسرار تدار عبر مخازن أو بيئات مخصصة بحسب منصة التشغيل، مع ضوابط وصول ومراجعة قابلة للإثبات.",
    points: [
      "لا secrets في git أو الملفات",
      "مخزن أسرار أو بيئة مخصصة حسب منصة التشغيل",
      "تدوير المفاتيح وفق سياسة المخاطر والتشغيل",
      "خطة استجابة للحوادث موثقة",
    ],
  },
  {
    icon: "📊",
    title: "Audit Trail",
    titleEn: "Full Traceability",
    desc: "عند تفعيل مسارات الحوكمة، تسجل القرارات والموافقات والمخرجات مع المصدر والوقت بما يسمح بالمراجعة وفق نطاق النظام.",
    points: [
      "سجل كامل للموافقات والرفضات",
      "توثيق مصدر كل توصية AI",
      "تاريخ ووقت كل عملية تشغيلية",
      "مسار واضح من البيانات للقرار",
    ],
  },
];

const commitments = [
  "لن نشارك بيانات عميل مع أي طرف ثالث بدون إذن صريح",
  "لن نستخدم بياناتك في تدريب نماذج AI بدون موافقتك",
  "لن نرسل أي تواصل تجاري باسمك بدون مراجعتك وموافقتك",
  "لن نُصدر فاتورة أو عقد بدون توقيع مؤسسي صريح",
  "لن نخزن بيانات العملاء أطول من الفترة المتفق عليها",
  "سنُخطرك فوراً في حالة أي حادث أمني يتعلق ببياناتك",
];

export default function TrustPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-emerald-300/30 px-4 py-2 text-sm text-emerald-100">
          الثقة والخصوصية
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-[1.15] md:text-6xl">
          AI يقترح. الإنسان يقرر. بياناتك محمية.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          Dealix مبني على مبدأ واحد: الثقة تُبنى بالشفافية، لا بالوعود.
          هذه الصفحة توضح بالضبط كيف ندير بياناتك وأين حدود AI في تشغيلنا.
        </p>
      </section>

      {/* Trust Principles */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {principles.map((p) => (
            <div
              key={p.title}
              className="rounded-3xl border border-white/10 bg-white/[0.03] p-6"
            >
              <p className="text-3xl">{p.icon}</p>
              <h2 className="mt-4 text-xl font-black">{p.title}</h2>
              <p className="text-sm text-slate-500">{p.titleEn}</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">{p.desc}</p>
              <ul className="mt-4 space-y-2">
                {p.points.map((point) => (
                  <li key={point} className="flex gap-2 text-sm text-slate-400">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* Commitments */}
      <section className="border-y border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-3xl font-black">التزاماتنا — بدون غموض</h2>
          <p className="mt-3 text-slate-400">
            هذه ليست سياسة خصوصية معقدة. هذه التزامات واضحة بلغة بسيطة.
          </p>
          <div className="mt-8 space-y-3">
            {commitments.map((c) => (
              <div
                key={c}
                className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-5 py-4"
              >
                <span className="mt-0.5 text-emerald-400 font-black">✓</span>
                <p className="text-sm leading-7 text-slate-300">{c}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Incident Response */}
      <section className="mx-auto max-w-5xl px-6 py-16">
        <h2 className="text-3xl font-black">ماذا لو حدث شيء غير متوقع؟</h2>
        <p className="mt-3 text-slate-400">
          مسار الاستجابة للحوادث يدار وفق الخطة والضوابط المفعلة. عند وقوع حادث نتبع تسلسلاً واضحاً دون وعد زمني عام غير مرتبط بعقد أو سياسة عميل:
        </p>
        <div className="mt-6 grid gap-4 md:grid-cols-4">
          {[
            { step: "1", title: "الاكتشاف", desc: "نكتشف الواقعة ونوثق الأدلة المتاحة" },
            { step: "2", title: "الاحتواء", desc: "نحتوي الأثر بحسب طبيعة الحادث" },
            { step: "3", title: "الإخطار", desc: "نحدد واجبات الإخطار حسب السياسة والمتطلبات المنطبقة" },
            { step: "4", title: "المعالجة", desc: "نوثق المعالجة والتعلم والإجراءات التصحيحية" },
          ].map((item) => (
            <div
              key={item.step}
              className="rounded-2xl border border-white/10 bg-white/[0.03] p-4"
            >
              <p className="text-2xl font-black text-cyan-400">#{item.step}</p>
              <h3 className="mt-2 font-bold">{item.title}</h3>
              <p className="mt-1 text-sm text-slate-400">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-white/5 bg-white/[0.02] py-16">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-black">ابدأ بثقة</h2>
          <p className="mt-4 text-lg text-slate-300">
            التشخيص التحولي يبدأ بمحادثة بدون أي التزام مالي مسبق.
          </p>
          <div className="mt-8">
            <a
              href="/book"
              className="rounded-2xl bg-cyan-400 px-10 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300"
            >
              ابدأ بالتشخيص التنفيذي المجاني
            </a>
          </div>
          <p className="mt-3 text-sm text-slate-500">
            مجاني · بدون بطاقة · Approval-first · أي نطاق مدفوع لاحقاً بعرض خاص بالعميل
          </p>
        </div>
      </section>
    </main>
  );
}
