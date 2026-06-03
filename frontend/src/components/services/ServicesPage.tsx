"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

/* ─── Data ──────────────────────────────────────────── */

type Tier = {
  id: string;
  icon: string;
  highlight: boolean;
  badge: { ar: string; en: string } | null;
  price: { ar: string; en: string };
  period: { ar: string; en: string };
  label: { ar: string; en: string };
  tagline: { ar: string; en: string };
  desc: { ar: string; en: string };
  deliverables: { ar: string; en: string }[];
  outcomes: { ar: string; en: string }[];
  suitable: { ar: string; en: string };
  timeline: { ar: string; en: string };
  cta: { ar: string; en: string };
  href: string;
};

const TIERS: Tier[] = [
  {
    id: "free",
    icon: "M",
    highlight: false,
    badge: null,
    price: { ar: "مجاني", en: "Free" },
    period: { ar: "", en: "" },
    label: { ar: "تشخيص مجاني", en: "Free Diagnostic" },
    tagline: { ar: "Risk Score في 5 دقائق", en: "Risk Score in 5 minutes" },
    desc: {
      ar: "نقطة بدء كل شركة — اعرف وضعك التشغيلي قبل أي التزام. لا بطاقة ائتمان. لا حساب.",
      en: "The starting point for every company — know your operational position before any commitment. No credit card. No account.",
    },
    deliverables: [
      { ar: "Risk Score تشغيلي من 100", en: "Operational Risk Score out of 100" },
      { ar: "تحليل جاهزية ZATCA و PDPL", en: "ZATCA & PDPL readiness analysis" },
      { ar: "تحديد 3 فجوات رئيسية", en: "Identification of 3 main gaps" },
      { ar: "توصية المسار التالي", en: "Next path recommendation" },
    ],
    outcomes: [
      { ar: "صورة واضحة عن الوضع التشغيلي", en: "Clear picture of operational status" },
      { ar: "فهم الأولويات قبل الاستثمار", en: "Priority understanding before investment" },
    ],
    suitable: { ar: "كل شركة B2B في السعودية", en: "Every B2B company in Saudi Arabia" },
    timeline: { ar: "5 دقائق", en: "5 minutes" },
    cta: { ar: "احسب Risk Score", en: "Calculate Risk Score" },
    href: "/risk-score",
  },
  {
    id: "sprint",
    icon: "S",
    highlight: false,
    badge: null,
    price: { ar: "499", en: "499" },
    period: { ar: "ر.س", en: "SAR" },
    label: { ar: "Revenue Intelligence Sprint", en: "Revenue Intelligence Sprint" },
    tagline: { ar: "مراجعة 10 leads في 48 ساعة", en: "10-lead deep review in 48 hours" },
    desc: {
      ar: "مراجعة عميقة لـ 10 leads حقيقية من قائمتك — مالك واضح، فجوات أدلة، مسودة Proof، خطوة تالية. ليس lead generation.",
      en: "Deep review of 10 real leads from your list — clear owner, evidence gaps, Proof draft, next action. Not lead generation.",
    },
    deliverables: [
      { ar: "مالك واضح لكل lead", en: "Clear owner per lead" },
      { ar: "فجوات أدلة CRM موثّقة", en: "Documented CRM evidence gaps" },
      { ar: "مسودة Proof لأفضل 3 leads", en: "Proof draft for top 3 leads" },
      { ar: "خطوة تالية واحدة لكل lead", en: "One next action per lead" },
      { ar: "ملاحظة governance محكومة", en: "Governed governance note" },
    ],
    outcomes: [
      { ar: "وضوح فوري في pipeline الحالي", en: "Immediate clarity in current pipeline" },
      { ar: "تشخيص سبب ضعف التحويل", en: "Diagnosis of conversion weakness root cause" },
    ],
    suitable: { ar: "وكالات تسويق وفرق مبيعات B2B", en: "Marketing agencies and B2B sales teams" },
    timeline: { ar: "48 ساعة", en: "48 hours" },
    cta: { ar: "ابدأ Sprint بـ 499 ر.س", en: "Start Sprint — 499 SAR" },
    href: "/dealix-diagnostic",
  },
  {
    id: "proof",
    icon: "P",
    highlight: false,
    badge: null,
    price: { ar: "1,500", en: "1,500" },
    period: { ar: "ر.س", en: "SAR" },
    label: { ar: "Agency Proof Pack", en: "Agency Proof Pack" },
    tagline: { ar: "حزمة إثبات كاملة لتقديمها للعميل", en: "Full evidence bundle to present to your client" },
    desc: {
      ar: "حزمة إثبات منظّمة للوكالة أو الشركة — 4 أقسام، مستويات L0-L5، PDF ثنائي اللغة يُرسَل للعميل.",
      en: "Structured proof bundle for agencies or companies — 4 sections, L0-L5 evidence levels, bilingual PDF to send to client.",
    },
    deliverables: [
      { ar: "4 أقسام: مصادر، ملاك، أدلة، قرارات", en: "4 sections: sources, owners, evidence, decisions" },
      { ar: "مستويات أدلة L0-L5 موثّقة", en: "L0-L5 evidence levels documented" },
      { ar: "PDF ثنائي اللغة (AR + EN)", en: "Bilingual PDF (AR + EN)" },
      { ar: "جدول حالة الأقسام", en: "Section status table" },
      { ar: "توصية Sprint أو Retainer", en: "Sprint or Retainer recommendation" },
    ],
    outcomes: [
      { ar: "أدلة موثّقة تُقنع العميل", en: "Documented evidence to convince the client" },
      { ar: "تقرير جاهز للإدارة", en: "Management-ready report" },
    ],
    suitable: { ar: "وكالات تريد إثبات قيمة عملها للعملاء", en: "Agencies wanting to prove work value to clients" },
    timeline: { ar: "7 أيام", en: "7 days" },
    cta: { ar: "اطلب Agency Proof Pack", en: "Request Agency Proof Pack" },
    href: "/dealix-diagnostic",
  },
  {
    id: "managed",
    icon: "M",
    highlight: true,
    badge: { ar: "الأكثر طلباً", en: "Most Popular" },
    price: { ar: "2,999 – 4,999", en: "2,999 – 4,999" },
    period: { ar: "ر.س/شهر", en: "SAR/mo" },
    label: { ar: "Managed Ops Retainer", en: "Managed Ops Retainer" },
    tagline: { ar: "تشغيل مُدار شهرياً — نتائج مستمرة", en: "Monthly managed ops — continuous results" },
    desc: {
      ar: "تشغيل مُدار شهرياً يُسلَّم بعد إثبات القيمة من Proof Pack. OKR أسبوعي، Proof Pack شهري، دعم أولوية 48 ساعة.",
      en: "Monthly managed ops delivered after proving value from Proof Pack. Weekly OKR, monthly Proof Pack, 48h priority support.",
    },
    deliverables: [
      { ar: "OKR أسبوعي محكوم", en: "Governed weekly OKR" },
      { ar: "Proof Pack شهري مُحدَّث", en: "Monthly updated Proof Pack" },
      { ar: "مراجعة CRM وأدلة", en: "CRM and evidence review" },
      { ar: "دعم أولوية — SLA 48 ساعة", en: "Priority support — 48h SLA" },
      { ar: "Approval Center لكل قرار حرج", en: "Approval Center for critical decisions" },
      { ar: "Company Brain snapshot شهري", en: "Monthly Company Brain snapshot" },
    ],
    outcomes: [
      { ar: "تحسّن مستمر وقابل للقياس", en: "Continuous and measurable improvement" },
      { ar: "إيراد موثّق بأدلة كل شهر", en: "Revenue documented with monthly evidence" },
    ],
    suitable: { ar: "شركات أثبتت قيمة Proof Pack وتريد نمواً مستداماً", en: "Companies that proved Proof Pack value and want sustainable growth" },
    timeline: { ar: "يبدأ بعد Proof Pack مُسلَّم", en: "Starts after delivered Proof Pack" },
    cta: { ar: "احجز استشارة", en: "Book Consultation" },
    href: "/dealix-diagnostic",
  },
  {
    id: "custom",
    icon: "C",
    highlight: false,
    badge: null,
    price: { ar: "5,000 – 25,000", en: "5,000 – 25,000" },
    period: { ar: "ر.س", en: "SAR" },
    label: { ar: "Custom AI Project", en: "Custom AI Project" },
    tagline: { ar: "تطوير AI مخصص لعملياتك", en: "Bespoke AI development for your operations" },
    desc: {
      ar: "تطوير AI مخصص بـ Scope محدد ومُوقَّع — نتائج موثّقة، Approval Center لكل خطوة، Proof Pack ختامي.",
      en: "Custom AI development with defined and signed Scope — documented outcomes, Approval Center at every step, final Proof Pack.",
    },
    deliverables: [
      { ar: "Scope document محدد ومُوقَّع", en: "Defined and signed Scope document" },
      { ar: "تطوير مخصص مع audit trail", en: "Custom development with audit trail" },
      { ar: "Approval Center لكل خطوة", en: "Approval Center at every step" },
      { ar: "Proof Pack ختامي", en: "Final Proof Pack" },
      { ar: "توثيق PDPL كامل", en: "Full PDPL documentation" },
      { ar: "Hand-off مع تدريب الفريق", en: "Hand-off with team training" },
    ],
    outcomes: [
      { ar: "نظام AI مخصص وموثّق", en: "Custom and documented AI system" },
      { ar: "قدرة داخلية مستدامة", en: "Sustainable internal capability" },
    ],
    suitable: { ar: "شركات على Managed Ops تريد توسعاً تقنياً", en: "Companies on Managed Ops wanting technical expansion" },
    timeline: { ar: "4–12 أسبوع", en: "4–12 weeks" },
    cta: { ar: "ناقش مشروعك", en: "Discuss Your Project" },
    href: "/dealix-diagnostic",
  },
];

const PRINCIPLES = [
  {
    icon: "A",
    ar: { title: "موافقة أولاً", desc: "كل إجراء خارجي يمر بموافقة بشرية قبل التنفيذ. لا أتمتة بلا مراجعة." },
    en: { title: "Approval-First", desc: "Every external action requires human approval before execution. No automation without review." },
  },
  {
    icon: "P",
    ar: { title: "PDPL أصيل", desc: "نظام حماية البيانات مدمج في البنية من البداية. لا scraping، لا cold outreach." },
    en: { title: "PDPL Native", desc: "Data protection built into architecture from day one. No scraping, no cold outreach." },
  },
  {
    icon: "Z",
    ar: { title: "ZATCA جاهز", desc: "تشخيص جاهزية الفوترة الإلكترونية في كل Proof Pack تلقائياً." },
    en: { title: "ZATCA Ready", desc: "E-invoicing readiness diagnostic included in every Proof Pack automatically." },
  },
  {
    icon: "E",
    ar: { title: "أدلة لكل لمسة", desc: "كل تفاعل مع العميل له دليل موثّق. لا قرار بلا سجل." },
    en: { title: "Evidence per touch", desc: "Every client interaction has a documented proof. No decision without a record." },
  },
];

/* ─── Component ─────────────────────────────────────── */

export function ServicesPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-5xl px-6 py-12 space-y-20 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >
        {/* ── Hero ── */}
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] px-8 py-14 text-white shadow-xl">
          <div className="relative space-y-5">
            <Badge className="bg-white/10 text-white border-white/20 text-xs">
              {isAr ? "سلم العروض الخمسة" : "Five-Tier Offer Ladder"}
            </Badge>
            <h1 className="text-4xl font-bold leading-tight md:text-5xl">
              {isAr
                ? <>خدمات مبنية على<br /><span className="text-[#C9974B]">الإثبات قبل التوسع</span></>
                : <>Services built on<br /><span className="text-[#C9974B]">Proof Before Expansion</span></>}
            </h1>
            <p className="max-w-2xl text-lg text-white/80 leading-relaxed">
              {isAr
                ? "كل مستوى يبني على الإثبات من المستوى السابق. لا upsell بدون Proof Pack مُسلَّم. لا التزام قبل رؤية النتائج."
                : "Every tier builds on proof from the previous tier. No upsell without delivered Proof Pack. No commitment before seeing results."}
            </p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Button asChild size="lg" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold shadow-lg">
                <Link href={`${base}/risk-score`}>
                  {isAr ? "ابدأ مجاناً ←" : "Start Free →"}
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-white/30 text-white bg-white/10 hover:bg-white/20">
                <Link href={`${base}/proof-pack`}>
                  {isAr ? "عيّنة Proof Pack" : "Sample Proof Pack"}
                </Link>
              </Button>
            </div>
          </div>
        </section>

        {/* ── Principles Bar ── */}
        <section>
          <p className="text-xs text-center text-muted-foreground mb-5 uppercase tracking-widest font-medium">
            {isAr ? "مبادئ غير قابلة للتفاوض" : "Non-negotiable principles"}
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PRINCIPLES.map((p) => {
              const content = isAr ? p.ar : p.en;
              return (
                <div key={p.icon} className="rounded-xl border border-border/60 bg-card/50 p-4 text-center">
                  <div className="w-9 h-9 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-sm mx-auto mb-3">
                    {p.icon}
                  </div>
                  <p className="font-semibold text-sm">{content.title}</p>
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{content.desc}</p>
                </div>
              );
            })}
          </div>
        </section>

        {/* ── Tier Cards ── */}
        <section>
          <div className="mb-8">
            <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-1">
              {isAr ? "سلم العروض" : "Offer Ladder"}
            </p>
            <h2 className="text-3xl font-bold">
              {isAr ? "خمسة مستويات — ابدأ من الجاهز" : "Five Tiers — Start Where You're Ready"}
            </h2>
            <p className="mt-3 text-muted-foreground max-w-2xl leading-relaxed">
              {isAr
                ? "كل مستوى يتطلب إثبات قيمة من المستوى السابق. هذا ليس قيداً — هو ضمان أن توسّعك مبني على أساس حقيقي."
                : "Every tier requires proof of value from the previous tier. This is not a restriction — it is a guarantee that your expansion is built on a real foundation."}
            </p>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {TIERS.map((tier) => {
              const label = isAr ? tier.label.ar : tier.label.en;
              const price = isAr ? tier.price.ar : tier.price.en;
              const period = isAr ? tier.period.ar : tier.period.en;
              const desc = isAr ? tier.desc.ar : tier.desc.en;
              const tagline = isAr ? tier.tagline.ar : tier.tagline.en;
              const cta = isAr ? tier.cta.ar : tier.cta.en;
              const isExpanded = expanded === tier.id;
              return (
                <div
                  key={tier.id}
                  className={`relative flex flex-col rounded-2xl border p-5 transition-shadow hover:shadow-md ${
                    tier.highlight
                      ? "border-[#C9974B]/50 bg-gradient-to-b from-[#C9974B]/5 to-card shadow-sm"
                      : "border-border/60 bg-card/50"
                  }`}
                >
                  {tier.badge && (
                    <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-[#C9974B] text-[#0A1628] text-xs font-bold px-3 py-0.5 whitespace-nowrap">
                      {isAr ? tier.badge.ar : tier.badge.en}
                    </span>
                  )}

                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-7 h-7 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-xs flex-shrink-0">
                      {tier.icon}
                    </div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide leading-tight">{label}</p>
                  </div>

                  <div className="mb-1">
                    <span className="text-2xl font-bold text-foreground">{price}</span>
                    {period && <span className="text-sm text-muted-foreground ms-1">{period}</span>}
                  </div>

                  <p className="text-xs text-[#C9974B] font-medium mb-3">{tagline}</p>
                  <p className="text-xs text-muted-foreground flex-1 leading-relaxed mb-4">{desc}</p>

                  <div className="space-y-1 mb-4">
                    <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
                      {isAr ? "المخرجات" : "Deliverables"}
                    </p>
                    {tier.deliverables.slice(0, isExpanded ? undefined : 3).map((d, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-xs">
                        <span className="text-emerald-500 mt-0.5 flex-shrink-0">+</span>
                        <span>{isAr ? d.ar : d.en}</span>
                      </div>
                    ))}
                    {tier.deliverables.length > 3 && (
                      <button
                        onClick={() => setExpanded(isExpanded ? null : tier.id)}
                        className="text-xs text-[#C9974B] hover:underline mt-1"
                      >
                        {isExpanded
                          ? (isAr ? "عرض أقل" : "Show less")
                          : (isAr ? `+${tier.deliverables.length - 3} أكثر` : `+${tier.deliverables.length - 3} more`)}
                      </button>
                    )}
                  </div>

                  <div className="pt-3 border-t border-border/40 space-y-2 text-xs text-muted-foreground">
                    <div className="flex items-center gap-1.5">
                      <span className="text-foreground/50">T</span>
                      <span>{isAr ? tier.timeline.ar : tier.timeline.en}</span>
                    </div>
                    <div className="flex items-start gap-1.5">
                      <span className="text-foreground/50">U</span>
                      <span>{isAr ? tier.suitable.ar : tier.suitable.en}</span>
                    </div>
                  </div>

                  <Button
                    asChild
                    size="sm"
                    className={`mt-4 w-full text-xs ${
                      tier.highlight
                        ? "bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a]"
                        : ""
                    }`}
                  >
                    <Link href={`${base}${tier.href}`}>{cta}</Link>
                  </Button>
                </div>
              );
            })}
          </div>
          <p className="mt-4 text-xs text-center text-muted-foreground">
            {isAr
              ? "* لا upsell بدون Proof Pack مُسلَّم · جميع الأسعار بالريال السعودي · موافقة بشرية على كل خطوة"
              : "* No upsell without delivered Proof Pack · All prices in SAR · Human approval at every step"}
          </p>
        </section>

        {/* ── Outcome Comparison ── */}
        <section>
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "مقارنة المخرجات" : "Outcome Comparison"}
          </h2>
          <div className="overflow-x-auto rounded-xl border border-border/60">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-border/60 bg-muted/30">
                  <th className="py-3 px-4 text-start font-semibold text-sm">
                    {isAr ? "الميزة" : "Feature"}
                  </th>
                  {TIERS.map((t) => (
                    <th
                      key={t.id}
                      className={`py-3 px-3 text-center font-semibold ${
                        t.highlight ? "text-[#C9974B]" : "text-muted-foreground"
                      }`}
                    >
                      <div className="flex flex-col items-center gap-1">
                        <span className="text-base">{t.icon}</span>
                        <span className="hidden sm:block leading-tight">
                          {isAr ? t.label.ar : t.label.en}
                        </span>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(isAr ? [
                  { feature: "Risk Score فوري", vals: [true, true, true, true, true] },
                  { feature: "مراجعة leads حقيقية", vals: [false, true, true, true, true] },
                  { feature: "PDF ثنائي اللغة", vals: [false, false, true, true, true] },
                  { feature: "OKR أسبوعي", vals: [false, false, false, true, true] },
                  { feature: "Approval Center", vals: [false, false, false, true, true] },
                  { feature: "تطوير مخصص", vals: [false, false, false, false, true] },
                  { feature: "PDPL/ZATCA موثّق", vals: ["جزئي", "جزئي", true, true, true] },
                ] : [
                  { feature: "Instant Risk Score", vals: [true, true, true, true, true] },
                  { feature: "Real lead review", vals: [false, true, true, true, true] },
                  { feature: "Bilingual PDF", vals: [false, false, true, true, true] },
                  { feature: "Weekly OKR", vals: [false, false, false, true, true] },
                  { feature: "Approval Center", vals: [false, false, false, true, true] },
                  { feature: "Custom development", vals: [false, false, false, false, true] },
                  { feature: "PDPL/ZATCA documented", vals: ["partial", "partial", true, true, true] },
                ]).map((row, i) => (
                  <tr key={i} className="border-b border-border/30 hover:bg-muted/20 transition-colors">
                    <td className="py-3 px-4 font-medium">{row.feature}</td>
                    {row.vals.map((v, j) => (
                      <td key={j} className="py-3 px-3 text-center">
                        {v === true && <span className="text-emerald-500 font-bold">+</span>}
                        {v === false && <span className="text-muted-foreground/40">—</span>}
                        {typeof v === "string" && <span className="text-amber-500 font-medium">{v}</span>}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* ── Selector ── */}
        <section className="rounded-2xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] text-white p-8">
          <h2 className="text-2xl font-bold mb-6">
            {isAr ? "أي مستوى يناسبني؟" : "Which tier is right for me?"}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {(isAr ? [
              { cond: "أريد معرفة وضعي الحالي فقط", ans: "ابدأ بـ Risk Score مجاني", href: "/risk-score" },
              { cond: "عندي leads ولا أعرف لماذا لا تتحوّل", ans: "Sprint — 499 ر.س", href: "/dealix-diagnostic" },
              { cond: "وكالة تريد تقديم دليل لعميلها", ans: "Agency Proof Pack — 1,500 ر.س", href: "/dealix-diagnostic" },
              { cond: "أثبتت قيمة التشخيص وأريد نتائج مستمرة", ans: "Managed Ops من 2,999 ر.س/شهر", href: "/dealix-diagnostic" },
            ] : [
              { cond: "I want to understand my current position", ans: "Start with Free Risk Score", href: "/risk-score" },
              { cond: "I have leads but don't know why they don't convert", ans: "Sprint — 499 SAR", href: "/dealix-diagnostic" },
              { cond: "Agency wanting to prove value to a client", ans: "Agency Proof Pack — 1,500 SAR", href: "/dealix-diagnostic" },
              { cond: "I've proven diagnostic value and want ongoing results", ans: "Managed Ops from 2,999 SAR/mo", href: "/dealix-diagnostic" },
            ]).map((item, i) => (
              <Link
                key={i}
                href={`${base}${item.href}`}
                className="block rounded-xl border border-white/10 bg-white/5 p-4 hover:bg-white/10 transition-colors"
              >
                <p className="text-white/60 text-xs mb-1">{isAr ? "إذا كنت:" : "If you:"}</p>
                <p className="text-white font-medium text-sm">{item.cond}</p>
                <p className="mt-2 text-[#C9974B] text-xs font-semibold">→ {item.ans}</p>
              </Link>
            ))}
          </div>
          <p className="mt-6 text-white/50 text-xs">
            {isAr
              ? "* لا upsell بدون Proof Pack مُسلَّم · لا أتمتة بلا موافقة · PDPL أصيل"
              : "* No upsell without delivered Proof Pack · No automation without approval · PDPL native"}
          </p>
        </section>

        {/* ── Final CTA ── */}
        <section className="text-center space-y-4">
          <h2 className="text-2xl font-bold">
            {isAr ? "ابدأ بـ Risk Score مجاني اليوم" : "Start with a free Risk Score today"}
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            {isAr
              ? "لا بطاقة ائتمان. لا تسجيل. نتيجة فورية تُظهر وضعك التشغيلي وأولوياتك."
              : "No credit card. No registration. Instant result showing your operational position and priorities."}
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Button asChild size="lg" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold">
              <Link href={`${base}/risk-score`}>
                {isAr ? "احسب Risk Score" : "Calculate Risk Score"}
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href={`${base}/dealix-diagnostic`}>
                {isAr ? "التشخيص المحكوم" : "Governed Diagnostic"}
              </Link>
            </Button>
          </div>
        </section>
      </div>
    </PublicGtmShell>
  );
}
