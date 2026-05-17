import Link from "next/link";
import { DiagnosticFunnel } from "@/components/diagnostic/DiagnosticFunnel";

interface DiagnosticPageProps {
  params: Promise<{ locale: string }>;
}

const CONTENT = {
  en: {
    dir: "ltr" as const,
    eyebrow: "Dealix — Governed Revenue & AI Operations",
    heroTitle: "Turn AI and revenue-ops experiments into governed, measurable workflows.",
    heroSubtitle:
      "A practical diagnostic for GCC teams that need source clarity, approval boundaries, evidence trails, and proof of value before scaling AI or revenue automation.",
    ctaScore: "Get my Risk Score",
    ctaBook: "Request a Diagnostic Review",
    problemTitle: "The problem",
    problemBody:
      "Teams are experimenting with AI and revenue automation — often without clear data sources, approval boundaries, evidence trails, or a way to link a workflow to a financial value. That creates risk and missed value before anything scales.",
    whoTitle: "Who it is for",
    who: [
      "GCC B2B teams running CRM, revenue automation, or AI experiments",
      "Founders and revenue leaders who need governance before scale",
      "Operations leads who want evidence, not vibes, behind decisions",
    ],
    getTitle: "What you get",
    get: [
      "A deterministic AI & Revenue Ops Risk Score for your situation",
      "A workflow risk map across four lenses: source clarity, approval boundaries, evidence trail, proof of value",
      "Your first 3 actionable, evidence-backed operational decisions",
      "A clear recommended next step on the offer ladder",
    ],
    scoreTitle: "AI & Revenue Ops Risk Score",
    scoreIntro:
      "Two minutes, deterministic, no AI guesswork. Empty input never produces a score.",
    pricingTitle: "Diagnostic & pricing",
    freeTitle: "Free AI Ops Diagnostic",
    freeDesc:
      "Self-serve entry point. Submit the Risk Score above and receive a governed read on your situation — no charge, no commitment.",
    reviewTitle: "Paid Diagnostic Review",
    reviewDesc:
      "A deeper, founder-led review of one workflow — scoped, governed, and delivered with an evidence-backed Proof Pack.",
    tiers: [
      { name: "Starter", price: "4,999 SAR" },
      { name: "Standard", price: "9,999 SAR" },
      { name: "Executive", price: "15,000 SAR" },
      { name: "Enterprise", price: "25,000 SAR" },
    ],
    ladderNote:
      "Diagnostic Review sits alongside the existing ladder: Free Diagnostic → Revenue Intelligence Sprint → Data-to-Revenue Pack → Managed Revenue Ops → Custom AI Setup.",
    faqTitle: "FAQ",
    faq: [
      {
        q: "Does Dealix send messages to my customers automatically?",
        a: "No. Dealix can prepare, classify, and suggest drafts — but any external send requires explicit human approval. This is part of our approval-first design.",
      },
      {
        q: "Do you guarantee revenue results?",
        a: "No. We work with estimated, evidence-tiered outcomes. Estimated outcomes are not guaranteed outcomes.",
      },
      {
        q: "Is the diagnostic really free?",
        a: "Yes. The self-serve Risk Score and diagnostic read are free. The paid Diagnostic Review is a separate, deeper engagement.",
      },
      {
        q: "What happens to my data?",
        a: "Captured leads are stored for founder review only. We do not scrape, buy lists, or run cold automation.",
      },
    ],
    boundariesTitle: "What we do not do",
    boundaries: [
      "No external AI messages without explicit approval",
      "No generic chatbot sold as a service",
      "No fabricated CRM or pipeline numbers",
      "No revenue claimed before payment or evidence",
      "No case study published without consent",
      "No security or compliance claims without a source",
    ],
    disclaimer:
      "Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.",
  },
  ar: {
    dir: "rtl" as const,
    eyebrow: "Dealix — عمليات الإيراد والذكاء الاصطناعي المحكومة",
    heroTitle: "حوّل تجارب الذكاء الاصطناعي وعمليات الإيراد إلى workflows محكومة وقابلة للقياس.",
    heroSubtitle:
      "تشخيص عملي لفرق الخليج التي تحتاج وضوح مصادر، حدود موافقة، مسارات أدلة، وإثبات قيمة قبل توسيع الذكاء الاصطناعي أو أتمتة الإيراد.",
    ctaScore: "احسب مؤشر المخاطر",
    ctaBook: "اطلب Diagnostic Review",
    problemTitle: "المشكلة",
    problemBody:
      "الفرق تجرّب الذكاء الاصطناعي وأتمتة الإيراد — غالبًا دون وضوح في مصادر البيانات، أو حدود الموافقة، أو مسارات الأدلة، أو طريقة لربط workflow بقيمة مالية. هذا يخلق مخاطر وقيمة ضائعة قبل أي توسّع.",
    whoTitle: "لمن هذا",
    who: [
      "فرق B2B في الخليج تشغّل CRM أو أتمتة إيراد أو تجارب ذكاء اصطناعي",
      "مؤسسون وقادة إيراد يحتاجون حوكمة قبل التوسّع",
      "قادة عمليات يريدون أدلة لا انطباعات خلف القرارات",
    ],
    getTitle: "ماذا تستلم",
    get: [
      "مؤشر مخاطر محدّد النتيجة للذكاء الاصطناعي وعمليات الإيراد لحالتك",
      "خريطة مخاطر للـworkflow من أربع زوايا: وضوح المصدر، حدود الموافقة، مسار الأدلة، إثبات القيمة",
      "أول 3 قرارات تشغيلية قابلة للتنفيذ ومدعومة بدليل",
      "خطوة تالية واضحة وموصى بها على سُلّم العروض",
    ],
    scoreTitle: "مؤشر مخاطر الذكاء الاصطناعي وعمليات الإيراد",
    scoreIntro:
      "دقيقتان، محدّد النتيجة، بلا تخمين. المدخلات الفارغة لا تُنتج أي نتيجة.",
    pricingTitle: "التشخيص والأسعار",
    freeTitle: "تشخيص عمليات الذكاء الاصطناعي المجاني",
    freeDesc:
      "نقطة دخول ذاتية. أرسل مؤشر المخاطر أعلاه واحصل على قراءة محكومة لحالتك — بلا رسوم وبلا التزام.",
    reviewTitle: "Diagnostic Review المدفوع",
    reviewDesc:
      "مراجعة أعمق بقيادة المؤسس لـworkflow واحد — بنطاق محدّد ومحكوم وتُسلَّم مع Proof Pack مدعوم بالأدلة.",
    tiers: [
      { name: "Starter", price: "4,999 ريال" },
      { name: "Standard", price: "9,999 ريال" },
      { name: "Executive", price: "15,000 ريال" },
      { name: "Enterprise", price: "25,000 ريال" },
    ],
    ladderNote:
      "Diagnostic Review يقف بجانب السُّلّم القائم: تشخيص مجاني ← Revenue Intelligence Sprint ← Data-to-Revenue Pack ← Managed Revenue Ops ← Custom AI Setup.",
    faqTitle: "الأسئلة الشائعة",
    faq: [
      {
        q: "هل ترسل Dealix رسائل لعملائي تلقائيًا؟",
        a: "لا. تستطيع Dealix تجهيز الرسائل وتصنيفها واقتراح مسودات — لكن أي إرسال خارجي يتطلب موافقة بشرية صريحة. هذا جزء من تصميم approval-first.",
      },
      {
        q: "هل تضمنون نتائج إيراد؟",
        a: "لا. نعمل بنتائج تقديرية مصنّفة بالأدلة. النتائج التقديرية ليست نتائج مضمونة.",
      },
      {
        q: "هل التشخيص مجاني فعلاً؟",
        a: "نعم. مؤشر المخاطر الذاتي والقراءة التشخيصية مجانيان. أما Diagnostic Review المدفوع فهو مشاركة منفصلة وأعمق.",
      },
      {
        q: "ماذا يحدث لبياناتي؟",
        a: "العملاء المحتملون يُحفظون لمراجعة المؤسس فقط. لا scraping، ولا قوائم مشتراة، ولا أتمتة باردة.",
      },
    ],
    boundariesTitle: "ما لا نفعله",
    boundaries: [
      "لا رسائل ذكاء اصطناعي خارجية بلا موافقة صريحة",
      "لا chatbot عام يُباع كخدمة",
      "لا أرقام CRM أو pipeline مختلقة",
      "لا ادعاء إيراد قبل الدفع أو الدليل",
      "لا نشر case study بلا موافقة",
      "لا ادعاءات أمن أو امتثال بلا مصدر",
    ],
    disclaimer:
      "النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.",
  },
};

export default async function DealixDiagnosticPage({ params }: DiagnosticPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const c = isAr ? CONTENT.ar : CONTENT.en;

  return (
    <div className="min-h-screen bg-background grid-pattern" dir={c.dir}>
      <div className="mx-auto max-w-3xl px-6 py-16">
        {/* Hero */}
        <p className="text-sm font-medium text-muted-foreground">{c.eyebrow}</p>
        <h1 className="mt-3 text-3xl font-bold leading-tight tracking-tight text-foreground sm:text-4xl">
          {c.heroTitle}
        </h1>
        <p className="mt-4 text-base leading-relaxed text-foreground/80">
          {c.heroSubtitle}
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Link
            href="#risk-score"
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            {c.ctaScore}
          </Link>
          <Link
            href="#pricing"
            className="inline-flex items-center justify-center rounded-lg border border-border px-5 py-2.5 text-sm font-medium text-foreground transition hover:bg-muted"
          >
            {c.ctaBook}
          </Link>
        </div>

        {/* Problem */}
        <section className="mt-14">
          <h2 className="text-lg font-semibold text-foreground">{c.problemTitle}</h2>
          <p className="mt-2 text-base leading-relaxed text-foreground/80">
            {c.problemBody}
          </p>
        </section>

        {/* Who it is for */}
        <section className="mt-10">
          <h2 className="text-lg font-semibold text-foreground">{c.whoTitle}</h2>
          <ul className="mt-3 list-inside list-disc space-y-2 text-base text-foreground/80 marker:text-primary">
            {c.who.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        {/* What you get */}
        <section className="mt-10">
          <h2 className="text-lg font-semibold text-foreground">{c.getTitle}</h2>
          <ul className="mt-3 list-inside list-disc space-y-2 text-base text-foreground/80 marker:text-primary">
            {c.get.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        {/* Risk Score form */}
        <section className="mt-14">
          <h2 className="text-lg font-semibold text-foreground">{c.scoreTitle}</h2>
          <p className="mb-4 mt-1 text-sm text-muted-foreground">{c.scoreIntro}</p>
          <DiagnosticFunnel locale={locale} />
        </section>

        {/* Pricing */}
        <section id="pricing" className="mt-14 scroll-mt-20">
          <h2 className="text-lg font-semibold text-foreground">{c.pricingTitle}</h2>

          <div className="mt-4 rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-5">
            <h3 className="text-base font-semibold text-emerald-400">{c.freeTitle}</h3>
            <p className="mt-1 text-sm leading-relaxed text-foreground/80">{c.freeDesc}</p>
          </div>

          <div className="mt-4 rounded-2xl border border-border bg-card p-5">
            <h3 className="text-base font-semibold text-foreground">{c.reviewTitle}</h3>
            <p className="mt-1 text-sm leading-relaxed text-foreground/80">{c.reviewDesc}</p>
            <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
              {c.tiers.map((tier) => (
                <div
                  key={tier.name}
                  className="rounded-xl border border-border bg-background p-3 text-center"
                >
                  <p className="text-xs font-medium text-muted-foreground">{tier.name}</p>
                  <p className="mt-1 text-sm font-semibold text-primary">{tier.price}</p>
                </div>
              ))}
            </div>
            <p className="mt-4 text-xs text-muted-foreground">{c.ladderNote}</p>
          </div>
        </section>

        {/* FAQ */}
        <section className="mt-14">
          <h2 className="text-lg font-semibold text-foreground">{c.faqTitle}</h2>
          <div className="mt-3 space-y-4">
            {c.faq.map((item) => (
              <div key={item.q} className="rounded-xl border border-border bg-card p-4">
                <p className="text-sm font-semibold text-foreground">{item.q}</p>
                <p className="mt-1.5 text-sm leading-relaxed text-foreground/75">{item.a}</p>
              </div>
            ))}
          </div>
        </section>

        {/* What we do not do */}
        <section className="mt-14">
          <h2 className="text-lg font-semibold text-foreground">{c.boundariesTitle}</h2>
          <ul className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
            {c.boundaries.map((item) => (
              <li
                key={item}
                className="flex items-start gap-2 rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground/80"
              >
                <span className="mt-0.5 text-red-400">✕</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        <p className="mt-12 border-t border-border pt-6 text-xs text-muted-foreground">
          {c.disclaimer}
        </p>
      </div>
    </div>
  );
}
