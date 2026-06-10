"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

/* ─── Data ──────────────────────────────────────────── */

const TIERS = [
  {
    id: "free",
    highlight: false,
    badge: null,
    label: { ar: "تشخيص مجاني", en: "Free Diagnostic" },
    price: { ar: "مجاني", en: "Free" },
    period: { ar: "", en: "" },
    type: "one-time",
    desc: { ar: "Risk Score وتحليل الجاهزية في 5 دقائق", en: "Risk Score & readiness analysis in 5 minutes" },
    features: [
      { ar: "Risk Score (1-100)", en: "Risk Score (1-100)", included: true },
      { ar: "تحليل ZATCA/PDPL", en: "ZATCA/PDPL analysis", included: true },
      { ar: "3 فجوات رئيسية", en: "3 main gaps", included: true },
      { ar: "توصية المسار", en: "Path recommendation", included: true },
      { ar: "Proof Pack", en: "Proof Pack", included: false },
      { ar: "OKR أسبوعي", en: "Weekly OKR", included: false },
      { ar: "دعم أولوية", en: "Priority support", included: false },
    ],
    cta: { ar: "ابدأ مجاناً", en: "Start Free" },
    href: "/risk-score",
  },
  {
    id: "sprint",
    highlight: false,
    badge: null,
    label: { ar: "Revenue Intelligence Sprint", en: "Revenue Intelligence Sprint" },
    price: { ar: "499", en: "499" },
    period: { ar: "ر.س", en: "SAR" },
    type: "one-time",
    desc: { ar: "مراجعة 10 leads في 48 ساعة", en: "10-lead review in 48 hours" },
    features: [
      { ar: "Risk Score (1-100)", en: "Risk Score (1-100)", included: true },
      { ar: "تحليل ZATCA/PDPL", en: "ZATCA/PDPL analysis", included: true },
      { ar: "مراجعة 10 leads حقيقية", en: "10 real lead review", included: true },
      { ar: "مسودة Proof لـ 3 leads", en: "Proof draft for 3 leads", included: true },
      { ar: "Proof Pack كامل", en: "Full Proof Pack", included: false },
      { ar: "OKR أسبوعي", en: "Weekly OKR", included: false },
      { ar: "دعم أولوية", en: "Priority support", included: false },
    ],
    cta: { ar: "ابدأ Sprint", en: "Start Sprint" },
    href: "/dealix-diagnostic",
  },
  {
    id: "proof",
    highlight: false,
    badge: null,
    label: { ar: "Agency Proof Pack", en: "Agency Proof Pack" },
    price: { ar: "1,500", en: "1,500" },
    period: { ar: "ر.س", en: "SAR" },
    type: "one-time",
    desc: { ar: "حزمة إثبات كاملة — PDF ثنائي اللغة", en: "Full evidence bundle — bilingual PDF" },
    features: [
      { ar: "Risk Score (1-100)", en: "Risk Score (1-100)", included: true },
      { ar: "تحليل ZATCA/PDPL", en: "ZATCA/PDPL analysis", included: true },
      { ar: "مراجعة leads", en: "Lead review", included: true },
      { ar: "Proof Pack L0-L5 كامل", en: "Full L0-L5 Proof Pack", included: true },
      { ar: "PDF ثنائي اللغة", en: "Bilingual PDF", included: true },
      { ar: "OKR أسبوعي", en: "Weekly OKR", included: false },
      { ar: "دعم أولوية", en: "Priority support", included: false },
    ],
    cta: { ar: "اطلب Proof Pack", en: "Request Proof Pack" },
    href: "/dealix-diagnostic",
  },
  {
    id: "managed",
    highlight: true,
    badge: { ar: "الأكثر طلباً", en: "Most Popular" },
    label: { ar: "Managed Ops Retainer", en: "Managed Ops Retainer" },
    price: { ar: "2,999 – 4,999", en: "2,999 – 4,999" },
    period: { ar: "ر.س/شهر", en: "SAR/mo" },
    type: "monthly",
    desc: { ar: "تشغيل مُدار شهرياً — OKR + Proof + دعم", en: "Monthly managed ops — OKR + Proof + support" },
    features: [
      { ar: "Risk Score + مراقبة مستمرة", en: "Risk Score + continuous monitoring", included: true },
      { ar: "تحليل ZATCA/PDPL جارٍ", en: "Ongoing ZATCA/PDPL analysis", included: true },
      { ar: "Proof Pack شهري", en: "Monthly Proof Pack", included: true },
      { ar: "OKR أسبوعي محكوم", en: "Governed weekly OKR", included: true },
      { ar: "Approval Center", en: "Approval Center", included: true },
      { ar: "دعم أولوية SLA 48h", en: "Priority support SLA 48h", included: true },
      { ar: "Company Brain snapshot", en: "Company Brain snapshot", included: true },
    ],
    cta: { ar: "احجز استشارة", en: "Book Consultation" },
    href: "/dealix-diagnostic",
  },
  {
    id: "custom",
    highlight: false,
    badge: null,
    label: { ar: "Custom AI Project", en: "Custom AI Project" },
    price: { ar: "5,000 – 25,000", en: "5,000 – 25,000" },
    period: { ar: "ر.س", en: "SAR" },
    type: "one-time",
    desc: { ar: "تطوير AI مخصص بـ Scope موقّع", en: "Custom AI development with signed Scope" },
    features: [
      { ar: "كل ميزات Managed Ops", en: "All Managed Ops features", included: true },
      { ar: "Scope document موقّع", en: "Signed Scope document", included: true },
      { ar: "تطوير مخصص + audit trail", en: "Custom development + audit trail", included: true },
      { ar: "Proof Pack ختامي", en: "Final Proof Pack", included: true },
      { ar: "Hand-off + تدريب", en: "Hand-off + training", included: true },
      { ar: "توثيق PDPL كامل", en: "Full PDPL documentation", included: true },
      { ar: "Approval Center لكل خطوة", en: "Approval Center at every step", included: true },
    ],
    cta: { ar: "ناقش مشروعك", en: "Discuss Project" },
    href: "/dealix-diagnostic",
  },
];

const FAQS = [
  {
    ar: { q: "هل يمكنني البدء بالمستوى المجاني؟", a: "نعم. Risk Score مجاني تماماً بدون تسجيل أو بطاقة ائتمان. يُعطيك صورة واضحة في 5 دقائق." },
    en: { q: "Can I start with the free tier?", a: "Yes. Risk Score is completely free with no registration or credit card. It gives you a clear picture in 5 minutes." },
  },
  {
    ar: { q: "هل يمكنني الانتقال من Sprint إلى Proof Pack؟", a: "نعم. كل مستوى يُمكّن الانتقال للمستوى التالي بعد إثبات القيمة. لا إلزام مسبق." },
    en: { q: "Can I upgrade from Sprint to Proof Pack?", a: "Yes. Every tier enables moving to the next tier after proving value. No prior commitment." },
  },
  {
    ar: { q: "متى أبدأ Managed Ops Retainer؟", a: "بعد تسليم Proof Pack أول ناجح. هذا مبدأ غير قابل للتفاوض — لا upsell قبل إثبات القيمة." },
    en: { q: "When can I start Managed Ops Retainer?", a: "After the first successful Proof Pack delivery. This is non-negotiable — no upsell before proving value." },
  },
  {
    ar: { q: "ما هي طرق الدفع المتاحة؟", a: "Moyasar: مدى، Visa، Mastercard، Apple Pay. أو فاتورة إلكترونية للشركات الكبيرة." },
    en: { q: "What payment methods are available?", a: "Moyasar: Mada, Visa, Mastercard, Apple Pay. Or e-invoice for large companies." },
  },
  {
    ar: { q: "هل هناك ضمان استرداد؟", a: "إذا لم نُسلّم Proof Pack مكتملاً خلال المدة المتفق عليها، نُعيد المبلغ كاملاً. لا استثناءات." },
    en: { q: "Is there a money-back guarantee?", a: "If we don't deliver a complete Proof Pack within the agreed timeframe, we refund in full. No exceptions." },
  },
  {
    ar: { q: "هل يستبدل Dealix الـ CRM الحالي؟", a: "لا. Dealix طبقة حوكمة وأدلة فوق CRM الحالي — تعمل معه لا ضده." },
    en: { q: "Does Dealix replace my CRM?", a: "No. Dealix is a governance and evidence layer on top of your existing CRM — it works with it, not against it." },
  },
  {
    ar: { q: "هل أحتاج مطوّراً لتشغيل Dealix؟", a: "لا. الـ Diagnostic والـ Proof Pack يُسلَّمان كـ PDF ثنائي اللغة. لا setup تقني في المرحلة الأولى." },
    en: { q: "Do I need a developer to use Dealix?", a: "No. The Diagnostic and Proof Pack are delivered as bilingual PDF. No technical setup in Phase 1." },
  },
  {
    ar: { q: "كيف يختلف Dealix عن توظيف مدير عمليات؟", a: "مدير عمليات: 15,000-25,000 ر.س/شهر + مزايا + وقت للتوظيف. Dealix Managed Ops: 2,999-4,999 ر.س/شهر — جاهز فوراً + Proof Pack + PDPL." },
    en: { q: "How does Dealix compare to hiring an ops manager?", a: "Ops manager: 15,000-25,000 SAR/mo + benefits + hiring time. Dealix Managed Ops: 2,999-4,999 SAR/mo — ready immediately + Proof Pack + PDPL." },
  },
  {
    ar: { q: "ما الذي لا يشمله Dealix؟", a: "Dealix لا يُنشئ leads جديدة، لا يُدير حسابات وسائل التواصل، لا يكتب محتوى تسويقياً عاماً، ولا يُرسل cold outreach بأي شكل." },
    en: { q: "What is NOT included in Dealix?", a: "Dealix does not generate new leads, manage social media accounts, write generic marketing content, or send cold outreach in any form." },
  },
  {
    ar: { q: "هل الدفع يشمل ZATCA compliance؟", a: "كل Proof Pack يتضمن تشخيص جاهزية ZATCA. الـ Custom AI Project يشمل توثيق ZATCA/PDPL كامل." },
    en: { q: "Does payment include ZATCA compliance?", a: "Every Proof Pack includes a ZATCA readiness diagnostic. The Custom AI Project includes full ZATCA/PDPL documentation." },
  },
];

const NOT_INCLUDED = [
  { ar: "توليد leads جديدة من الصفر", en: "Generating new leads from scratch" },
  { ar: "إدارة حسابات وسائل التواصل الاجتماعي", en: "Managing social media accounts" },
  { ar: "كتابة محتوى تسويقي عام", en: "Writing generic marketing content" },
  { ar: "Cold outreach بأي شكل (واتساب، LinkedIn، بريد بارد)", en: "Cold outreach in any form (WhatsApp, LinkedIn, cold email)" },
  { ar: "Scraping أو جمع بيانات عامة", en: "Scraping or collecting public data" },
  { ar: "Lead generation أو تسويق الأداء", en: "Lead generation or performance marketing" },
];

const PAYMENT_METHODS = [
  { id: "mada", ar: "مدى", en: "Mada" },
  { id: "visa", ar: "Visa", en: "Visa" },
  { id: "mc", ar: "Mastercard", en: "Mastercard" },
  { id: "apple", ar: "Apple Pay", en: "Apple Pay" },
  { id: "invoice", ar: "فاتورة إلكترونية", en: "E-Invoice" },
];

/* ─── ROI Calculator ─────────────────────────────────── */

function ROICalculator({ isAr }: { isAr: boolean }) {
  const [revenue, setRevenue] = useState(1000000);
  const leakageRate = 0.15;
  const leakage = Math.round(revenue * leakageRate);
  const sprintCost = 499;
  const roi = leakage > 0 ? Math.round(leakage / sprintCost) : 0;

  return (
    <div className="rounded-xl border border-[#C9974B]/20 bg-gradient-to-br from-[#C9974B]/5 to-card p-6">
      <p className="font-semibold text-sm uppercase tracking-wide text-[#C9974B] mb-1">
        {isAr ? "حاسبة العائد على الاستثمار" : "ROI Calculator"}
      </p>
      <h3 className="text-xl font-bold mb-4">
        {isAr ? "كم تُكلّفك الفجوات التشغيلية؟" : "What are your operational gaps costing you?"}
      </h3>

      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium text-muted-foreground block mb-2">
            {isAr ? `الإيراد الشهري: ${revenue.toLocaleString()} ر.س` : `Monthly Revenue: ${revenue.toLocaleString()} SAR`}
          </label>
          <input
            type="range"
            min={100000}
            max={10000000}
            step={100000}
            value={revenue}
            onChange={(e) => setRevenue(Number(e.target.value))}
            className="w-full accent-[#C9974B]"
          />
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>{isAr ? "100k ر.س" : "100k SAR"}</span>
            <span>{isAr ? "10M ر.س" : "10M SAR"}</span>
          </div>
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          <div className="rounded-lg border border-border/60 bg-card/50 p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">
              {isAr ? "تسريب إيراد متوقع (15%)" : "Expected leakage (15%)"}
            </p>
            <p className="text-xl font-bold text-red-500">
              {leakage.toLocaleString()}
            </p>
            <p className="text-xs text-muted-foreground">{isAr ? "ر.س/شهر" : "SAR/mo"}</p>
          </div>
          <div className="rounded-lg border border-border/60 bg-card/50 p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">
              {isAr ? "تكلفة Sprint" : "Sprint cost"}
            </p>
            <p className="text-xl font-bold text-[#C9974B]">
              {sprintCost.toLocaleString()}
            </p>
            <p className="text-xs text-muted-foreground">{isAr ? "ر.س (مرة واحدة)" : "SAR (one-time)"}</p>
          </div>
          <div className="rounded-lg border border-emerald-500/30 bg-emerald-50/30 dark:bg-emerald-950/20 p-3 text-center">
            <p className="text-xs text-muted-foreground mb-1">
              {isAr ? "عائد محتمل" : "Potential ROI"}
            </p>
            <p className="text-xl font-bold text-emerald-500">
              {roi}x
            </p>
            <p className="text-xs text-muted-foreground">{isAr ? "في الشهر الأول" : "in first month"}</p>
          </div>
        </div>

        <p className="text-xs text-muted-foreground">
          {isAr
            ? "* تقدير استرشادي بمعدل تسريب شائع 15%. نتائج فعلية موثّقة في Proof Pack."
            : "* Indicative estimate using a common 15% leakage rate. Actual results documented in Proof Pack."}
        </p>
      </div>
    </div>
  );
}

/* ─── Component ─────────────────────────────────────── */

export function PricingPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const [billingType, setBillingType] = useState<"all" | "monthly" | "one-time">("all");
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const filteredTiers =
    billingType === "all"
      ? TIERS
      : TIERS.filter((t) => billingType === "monthly" ? t.type === "monthly" : t.type === "one-time");

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-5xl px-6 py-12 space-y-20 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >

        {/* ── Hero ── */}
        <header>
          <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-2">
            {isAr ? "سلم التسعير" : "Pricing Ladder"}
          </p>
          <h1 className="text-4xl font-bold">
            {isAr ? "ابدأ مجاناً — توسّع بعد الإثبات" : "Start Free — Expand After Proof"}
          </h1>
          <p className="mt-4 text-muted-foreground max-w-2xl leading-relaxed">
            {isAr
              ? "خمسة مستويات تبني على بعضها. لا upsell بدون Proof Pack مُسلَّم. جميع الأسعار بالريال السعودي شاملة ضريبة القيمة المضافة."
              : "Five tiers that build on each other. No upsell without delivered Proof Pack. All prices in SAR including VAT."}
          </p>
        </header>

        {/* ── Filter Toggle ── */}
        <div className="flex items-center gap-1 rounded-xl border border-border/60 bg-card/50 p-1 w-fit">
          {(isAr ? [
            { val: "all" as const, label: "الكل" },
            { val: "one-time" as const, label: "دفعة واحدة" },
            { val: "monthly" as const, label: "شهري" },
          ] : [
            { val: "all" as const, label: "All" },
            { val: "one-time" as const, label: "One-time" },
            { val: "monthly" as const, label: "Monthly" },
          ]).map((opt) => (
            <button
              key={opt.val}
              onClick={() => setBillingType(opt.val)}
              className={`rounded-lg px-4 py-1.5 text-sm font-medium transition-all ${
                billingType === opt.val
                  ? "bg-[#0A1628] text-white shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>

        {/* ── Tier Cards ── */}
        <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {filteredTiers.map((tier) => {
            const label = isAr ? tier.label.ar : tier.label.en;
            const price = isAr ? tier.price.ar : tier.price.en;
            const period = isAr ? tier.period.ar : tier.period.en;
            const desc = isAr ? tier.desc.ar : tier.desc.en;
            const cta = isAr ? tier.cta.ar : tier.cta.en;
            return (
              <div
                key={tier.id}
                className={`relative flex flex-col rounded-2xl border p-6 ${
                  tier.highlight
                    ? "border-[#C9974B]/50 bg-gradient-to-b from-[#C9974B]/5 to-card shadow-md"
                    : "border-border/60 bg-card/50"
                }`}
              >
                {tier.badge && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-[#C9974B] text-[#0A1628] text-xs font-bold px-3 py-0.5 whitespace-nowrap">
                    {isAr ? tier.badge.ar : tier.badge.en}
                  </span>
                )}
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">{label}</p>
                <div className="mb-1">
                  <span className="text-3xl font-bold">{price}</span>
                  {period && <span className="text-sm text-muted-foreground ms-1">{period}</span>}
                </div>
                <p className="text-xs text-muted-foreground mb-4 leading-relaxed">{desc}</p>

                <ul className="space-y-2 flex-1 mb-5">
                  {tier.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs">
                      <span className={`mt-0.5 flex-shrink-0 ${f.included ? "text-emerald-500" : "text-muted-foreground/30"}`}>
                        {f.included ? "+" : "—"}
                      </span>
                      <span className={f.included ? "" : "text-muted-foreground/40"}>
                        {isAr ? f.ar : f.en}
                      </span>
                    </li>
                  ))}
                </ul>

                <Button
                  asChild
                  size="sm"
                  className={`w-full ${
                    tier.highlight ? "bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a]" : ""
                  }`}
                >
                  <Link href={`${base}${tier.href}`}>{cta}</Link>
                </Button>
              </div>
            );
          })}
        </section>

        {/* ── ROI Calculator ── */}
        <ROICalculator isAr={isAr} />

        {/* ── vs Hiring ── */}
        <section>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "Dealix مقابل توظيف مدير عمليات" : "Dealix vs. Hiring an Ops Manager"}
          </h2>
          <div className="overflow-x-auto rounded-xl border border-border/60">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border/60 bg-muted/30">
                  <th className="py-3 px-4 text-start font-semibold">{isAr ? "المعيار" : "Criteria"}</th>
                  <th className="py-3 px-4 text-center font-semibold">{isAr ? "مدير عمليات штатный" : "In-house Ops Manager"}</th>
                  <th className="py-3 px-4 text-center font-semibold text-[#C9974B]">{isAr ? "Dealix Managed Ops" : "Dealix Managed Ops"}</th>
                </tr>
              </thead>
              <tbody>
                {(isAr ? [
                  { criteria: "التكلفة الشهرية", inhouse: "15,000–25,000 ر.س + مزايا", dealix: "2,999–4,999 ر.س" },
                  { criteria: "وقت الجاهزية", inhouse: "2–3 أشهر توظيف + تأهيل", dealix: "أسبوع واحد" },
                  { criteria: "PDPL compliance", inhouse: "يعتمد على معرفة الفرد", dealix: "مدمج في النظام" },
                  { criteria: "ZATCA readiness", inhouse: "يحتاج خبرة إضافية", dealix: "موجود في كل Proof Pack" },
                  { criteria: "Audit Trail", inhouse: "يدوي وغير مضمون", dealix: "تلقائي في كل خطوة" },
                  { criteria: "Proof Pack شهري", inhouse: "غير مدرج عادةً", dealix: "مدرج في الخطة" },
                ] : [
                  { criteria: "Monthly cost", inhouse: "15,000–25,000 SAR + benefits", dealix: "2,999–4,999 SAR" },
                  { criteria: "Readiness time", inhouse: "2–3 months hiring + onboarding", dealix: "One week" },
                  { criteria: "PDPL compliance", inhouse: "Depends on individual knowledge", dealix: "Built into the system" },
                  { criteria: "ZATCA readiness", inhouse: "Requires additional expertise", dealix: "In every Proof Pack" },
                  { criteria: "Audit Trail", inhouse: "Manual and unreliable", dealix: "Automatic at every step" },
                  { criteria: "Monthly Proof Pack", inhouse: "Not typically included", dealix: "Included in plan" },
                ]).map((row, i) => (
                  <tr key={i} className="border-b border-border/30">
                    <td className="py-3 px-4 font-medium text-sm">{row.criteria}</td>
                    <td className="py-3 px-4 text-center text-sm text-muted-foreground">{row.inhouse}</td>
                    <td className="py-3 px-4 text-center text-sm text-[#C9974B] font-medium">{row.dealix}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* ── Payment Methods ── */}
        <section>
          <h2 className="text-xl font-bold mb-4">{isAr ? "طرق الدفع" : "Payment Methods"}</h2>
          <div className="flex flex-wrap gap-3">
            {PAYMENT_METHODS.map((m) => (
              <div key={m.id} className="rounded-lg border border-border/60 bg-card/50 px-4 py-2 text-sm font-medium">
                {isAr ? m.ar : m.en}
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            {isAr
              ? "مدعوم بـ Moyasar — بوابة دفع سعودية معتمدة. بيانات البطاقة لا تُخزَّن لدينا."
              : "Powered by Moyasar — certified Saudi payment gateway. Card data is never stored with us."}
          </p>
        </section>

        {/* ── What's NOT Included ── */}
        <section className="rounded-xl border border-red-500/20 bg-red-50/20 dark:bg-red-950/10 p-6">
          <h2 className="text-xl font-bold mb-4">{isAr ? "ما لا يشمله Dealix" : "What Dealix Does NOT Include"}</h2>
          <p className="text-sm text-muted-foreground mb-4">
            {isAr ? "نؤمن بالشفافية الكاملة. هذه الأشياء خارج نطاق خدماتنا:" : "We believe in full transparency. These items are outside our service scope:"}
          </p>
          <div className="grid gap-2 sm:grid-cols-2">
            {NOT_INCLUDED.map((item) => (
              <div key={isAr ? item.ar : item.en} className="flex items-start gap-2 text-sm text-muted-foreground">
                <span className="text-red-400 mt-0.5 flex-shrink-0">x</span>
                <span>{isAr ? item.ar : item.en}</span>
              </div>
            ))}
          </div>
        </section>

        {/* ── FAQ ── */}
        <section>
          <h2 className="text-2xl font-bold mb-6">{isAr ? "أسئلة شائعة" : "Frequently Asked Questions"}</h2>
          <div className="space-y-3">
            {FAQS.map((faq, i) => {
              const f = isAr ? faq.ar : faq.en;
              return (
                <div key={i} className="border border-border/60 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setOpenFaq(openFaq === i ? null : i)}
                    className="w-full flex items-center justify-between px-5 py-4 text-start font-medium hover:bg-muted/30 transition-colors text-sm"
                  >
                    <span>{f.q}</span>
                    <span className="text-muted-foreground text-lg flex-shrink-0 ms-3">{openFaq === i ? "−" : "+"}</span>
                  </button>
                  {openFaq === i && (
                    <div className="px-5 pb-4 text-sm text-muted-foreground leading-relaxed border-t border-border/40">
                      {f.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] text-white px-8 py-12 text-center">
          <h2 className="text-3xl font-bold">
            {isAr ? "ابدأ بـ Risk Score مجاني" : "Start with a free Risk Score"}
          </h2>
          <p className="mt-3 text-white/70 max-w-xl mx-auto">
            {isAr
              ? "لا بطاقة ائتمان. لا تسجيل. نتيجة فورية في 5 دقائق توضّح أين أنت وما هي أولوياتك."
              : "No credit card. No registration. Instant result in 5 minutes showing where you are and what your priorities are."}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button asChild size="lg" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold">
              <Link href={`${base}/risk-score`}>
                {isAr ? "احسب Risk Score مجاناً" : "Calculate Risk Score Free"}
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
              <Link href={`${base}/dealix-diagnostic`}>
                {isAr ? "تشخيص محكوم" : "Governed Diagnostic"}
              </Link>
            </Button>
          </div>
          <p className="mt-4 text-xs text-white/40">
            {isAr
              ? "لا upsell قبل Proof Pack · لا outreach بارد · PDPL أصيل · موافقة بشرية دائماً"
              : "No upsell before Proof Pack · No cold outreach · PDPL native · Human approval always"}
          </p>
        </section>

      </div>
    </PublicGtmShell>
  );
}
