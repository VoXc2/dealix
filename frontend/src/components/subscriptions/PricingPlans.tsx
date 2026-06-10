"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PricingFeature {
  textAr: string;
  textEn: string;
}

interface PricingPlan {
  id: string;
  nameAr: string;
  nameEn: string;
  priceAr: string;
  priceEn: string;
  periodAr: string;
  periodEn: string;
  forAr: string;
  forEn: string;
  features: PricingFeature[];
  ctaAr: string;
  ctaEn: string;
  href: string;
  highlight: boolean;
  badgeAr?: string;
  badgeEn?: string;
  colorScheme: "blue" | "gold" | "navy";
}

interface FaqItem {
  questionAr: string;
  questionEn: string;
  answerAr: string;
  answerEn: string;
}

// ---------------------------------------------------------------------------
// Static data
// ---------------------------------------------------------------------------

const PLANS: PricingPlan[] = [
  {
    id: "starter",
    nameAr: "Starter — Sprint",
    nameEn: "Starter — Sprint",
    priceAr: "499",
    priceEn: "499",
    periodAr: "ر.س",
    periodEn: "SAR",
    forAr: "الشركات الصغيرة والمتوسطة",
    forEn: "Small & medium businesses",
    highlight: false,
    colorScheme: "blue",
    ctaAr: "ابدأ الآن",
    ctaEn: "Start Now",
    href: "/dealix-diagnostic",
    features: [
      { textAr: "مراجعة 10 leads حقيقية", textEn: "10 real leads audit" },
      { textAr: "Risk Score تشغيلي", textEn: "Operational Risk Score" },
      { textAr: "مسودة Proof لأفضل 3 leads", textEn: "Proof draft for top 3 leads" },
      { textAr: "تسليم خلال 48 ساعة", textEn: "48-hour delivery" },
      { textAr: "تعديل واحد مجاني", textEn: "1 free revision" },
      { textAr: "دعم عبر البريد الإلكتروني", textEn: "Email support" },
      { textAr: "لوحة تحكم أساسية", textEn: "Basic dashboard" },
      { textAr: "تقرير PDF", textEn: "PDF report" },
    ],
  },
  {
    id: "growth",
    nameAr: "Growth — Managed Ops",
    nameEn: "Growth — Managed Ops",
    priceAr: "2,999 – 4,999",
    priceEn: "2,999 – 4,999",
    periodAr: "ر.س/شهر",
    periodEn: "SAR/mo",
    forAr: "الشركات النامية",
    forEn: "Growing businesses",
    highlight: true,
    colorScheme: "gold",
    badgeAr: "الأكثر طلباً",
    badgeEn: "Most Popular",
    ctaAr: "احجز استشارة",
    ctaEn: "Book a Consultation",
    href: "/dealix-diagnostic",
    features: [
      { textAr: "كل مزايا Starter", textEn: "Everything in Starter" },
      { textAr: "تشغيل مُدار شهري كامل", textEn: "Monthly full managed ops" },
      { textAr: "مراجعة OKR أسبوعية", textEn: "Weekly OKR review" },
      { textAr: "Proof Pack شهري مُحدَّث", textEn: "Monthly updated Proof Pack" },
      { textAr: "دعم ذو أولوية", textEn: "Priority support" },
      { textAr: "تكامل CRM", textEn: "CRM integration" },
      { textAr: "توصيات ذكاء اصطناعي", textEn: "AI recommendations" },
      { textAr: "تقارير مخصصة", textEn: "Custom reports" },
      { textAr: "مراقبة ZATCA", textEn: "ZATCA monitoring" },
      { textAr: "امتثال PDPL مستمر", textEn: "Ongoing PDPL compliance" },
      { textAr: "مدير مخصص", textEn: "Dedicated manager" },
      { textAr: "جلسة استراتيجية ربع سنوية", textEn: "Quarterly strategy session" },
    ],
  },
  {
    id: "enterprise",
    nameAr: "Enterprise — Custom AI",
    nameEn: "Enterprise — Custom AI",
    priceAr: "5,000 – 25,000+",
    priceEn: "5,000 – 25,000+",
    periodAr: "ر.س",
    periodEn: "SAR",
    forAr: "المؤسسات الكبرى",
    forEn: "Large enterprises",
    highlight: false,
    colorScheme: "navy",
    ctaAr: "تواصل معنا",
    ctaEn: "Contact Us",
    href: "/dealix-diagnostic",
    features: [
      { textAr: "كل مزايا Growth", textEn: "Everything in Growth" },
      { textAr: "تطوير AI مخصص لعملياتك", textEn: "Custom AI development" },
      { textAr: "مستخدمون غير محدودين", textEn: "Unlimited users" },
      { textAr: "خيار White-label", textEn: "White-label option" },
      { textAr: "تكاملات مخصصة", textEn: "Custom integrations" },
      { textAr: "ضمان مستوى الخدمة SLA", textEn: "SLA guarantee" },
      { textAr: "فريق مخصص", textEn: "Dedicated team" },
      { textAr: "تدريب ميداني", textEn: "Onsite training" },
    ],
  },
];

const FAQ_ITEMS: FaqItem[] = [
  {
    questionAr: "هل يمكنني الترقية لاحقاً؟",
    questionEn: "Can I upgrade later?",
    answerAr:
      "نعم، يمكنك الترقية في أي وقت. كل مستوى يبني على الإثبات من المستوى السابق — الانتقال إلى Growth يتطلب إتمام Sprint أولاً.",
    answerEn:
      "Yes, you can upgrade at any time. Each tier builds on proof from the previous — moving to Growth requires completing a Sprint first.",
  },
  {
    questionAr: "ما هو الفرق بين Sprint وManaged Ops؟",
    questionEn: "What is the difference between Sprint and Managed Ops?",
    answerAr:
      "Sprint هو تشخيص لمرة واحدة خلال 48 ساعة لـ 10 leads. Managed Ops هو اشتراك شهري يشمل تشغيلاً مستمراً، OKR أسبوعي، ودعماً مخصصاً.",
    answerEn:
      "Sprint is a one-time 48-hour diagnostic for 10 leads. Managed Ops is a monthly subscription covering ongoing operations, weekly OKR, and dedicated support.",
  },
  {
    questionAr: "هل توجد رسوم إعداد أولية؟",
    questionEn: "Are there any setup fees?",
    answerAr:
      "لا توجد رسوم إعداد خفية. السعر المعلن يشمل كل شيء. يُطلب من عملاء Enterprise وضع مبلغ Scope مسبقاً يُحتسب من إجمالي المشروع.",
    answerEn:
      "No hidden setup fees. The published price is all-inclusive. Enterprise clients are asked to place a Scope deposit credited toward the total project.",
  },
  {
    questionAr: "كيف تتم عملية الموافقة؟",
    questionEn: "How does the approval process work?",
    answerAr:
      "كل قرار حرج يمر عبر Approval Center — لا يُنفَّذ أي إجراء خارجي بدون موافقة بشرية صريحة. هذا مبدأ غير قابل للتفاوض في جميع المستويات.",
    answerEn:
      "Every critical decision passes through the Approval Center — no external action is executed without explicit human approval. This is non-negotiable at all tiers.",
  },
  {
    questionAr: "ما وسائل الدفع المتاحة؟",
    questionEn: "What payment methods are available?",
    answerAr:
      "نقبل مدى، Visa/Mastercard، وتحويل بنكي مباشر. فواتير ZATCA-compliant لكل معاملة.",
    answerEn:
      "We accept Mada, Visa/Mastercard, and direct bank transfer. ZATCA-compliant invoices for every transaction.",
  },
];

// ---------------------------------------------------------------------------
// Animation variants
// ---------------------------------------------------------------------------

const FADE_UP = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.45, delay: i * 0.1, ease: "easeOut" },
  }),
};

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <polyline points="2.5 8 6 11.5 13.5 4.5" />
    </svg>
  );
}

function planBorderClass(scheme: PricingPlan["colorScheme"], highlight: boolean): string {
  if (highlight) return "border-gold-500/60 shadow-lg shadow-gold-500/10";
  if (scheme === "navy") return "border-navy-500/40 dark:border-navy-400/30";
  return "border-border/60";
}

function planHeaderClass(scheme: PricingPlan["colorScheme"]): string {
  if (scheme === "gold") return "bg-gradient-to-br from-gold-500/15 to-gold-500/5";
  if (scheme === "navy")
    return "bg-gradient-to-br from-navy-500/15 dark:from-navy-400/10 to-transparent";
  return "bg-gradient-to-br from-blue-500/10 to-transparent";
}

function planCheckClass(scheme: PricingPlan["colorScheme"]): string {
  if (scheme === "gold") return "text-gold-500";
  if (scheme === "navy") return "text-navy-400 dark:text-navy-300";
  return "text-blue-400";
}

function planCtaVariant(
  scheme: PricingPlan["colorScheme"],
): "gold" | "default" | "outline" {
  if (scheme === "gold") return "gold";
  if (scheme === "navy") return "default";
  return "outline";
}

function PlanCard({
  plan,
  isAr,
  index,
}: {
  plan: PricingPlan;
  isAr: boolean;
  index: number;
}) {
  return (
    <motion.div
      custom={index}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={FADE_UP}
      whileHover={{ y: -6, transition: { duration: 0.2 } }}
      className="flex"
    >
      <Card
        className={`relative flex w-full flex-col border-2 ${planBorderClass(plan.colorScheme, plan.highlight)}`}
      >
        {plan.highlight && plan.badgeAr && (
          <div className="absolute -top-4 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-full bg-gold-500 px-4 py-1 text-xs font-bold text-white shadow-md">
            {isAr ? plan.badgeAr : plan.badgeEn}
          </div>
        )}

        {/* Card header */}
        <CardHeader className={`rounded-t-2xl pb-4 ${planHeaderClass(plan.colorScheme)}`}>
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {isAr ? plan.forAr : plan.forEn}
          </p>
          <CardTitle className="text-lg mt-1">
            {isAr ? plan.nameAr : plan.nameEn}
          </CardTitle>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-3xl font-bold">
              {isAr ? plan.priceAr : plan.priceEn}
            </span>
            <span className="text-sm text-muted-foreground">
              {isAr ? plan.periodAr : plan.periodEn}
            </span>
          </div>
        </CardHeader>

        {/* Features */}
        <CardContent className="flex flex-1 flex-col pt-5">
          <ul className="flex-1 space-y-2.5">
            {plan.features.map((f) => (
              <li
                key={f.textEn}
                className="flex items-start gap-2.5 text-sm"
              >
                <CheckIcon
                  className={`mt-0.5 h-4 w-4 flex-shrink-0 ${planCheckClass(plan.colorScheme)}`}
                />
                <span>{isAr ? f.textAr : f.textEn}</span>
              </li>
            ))}
          </ul>

          <div className="mt-6">
            <Button
              variant={planCtaVariant(plan.colorScheme)}
              size="lg"
              className="w-full"
              asChild
            >
              <Link href={`/${isAr ? "ar" : "en"}${plan.href}`}>
                {isAr ? plan.ctaAr : plan.ctaEn}
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function FaqAccordion({ items, isAr }: { items: FaqItem[]; isAr: boolean }) {
  return (
    <div className="space-y-3">
      {items.map((item, i) => (
        <motion.details
          key={i}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.07 }}
          className="group rounded-2xl border border-border/60 bg-card/80"
        >
          <summary className="flex cursor-pointer list-none items-center justify-between px-6 py-4 font-semibold text-sm hover:bg-muted/30 transition-colors rounded-2xl">
            <span>{isAr ? item.questionAr : item.questionEn}</span>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              className="h-4 w-4 flex-shrink-0 text-muted-foreground transition-transform group-open:rotate-180"
              aria-hidden="true"
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </summary>
          <div className="px-6 pb-5 pt-1 text-sm text-muted-foreground leading-relaxed">
            {isAr ? item.answerAr : item.answerEn}
          </div>
        </motion.details>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main exported component
// ---------------------------------------------------------------------------

export function PricingPlans() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div
      className="space-y-16"
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* ------------------------------------------------------------------ */}
      {/* Header                                                              */}
      {/* ------------------------------------------------------------------ */}
      <motion.header
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="text-center"
      >
        <Badge variant="gold" className="mb-4 text-xs uppercase tracking-wide">
          {isAr ? "خطط الأسعار" : "Pricing Plans"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight font-display">
          {isAr
            ? "ابدأ من حيث أنت — وسِّع بعد الإثبات"
            : "Start Where You Are — Expand After Proof"}
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-muted-foreground leading-relaxed">
          {isAr
            ? "كل خطة تبني على الإثبات من الخطة السابقة. لا توسع بدون Proof Pack مُسلَّم."
            : "Every plan builds on proof from the previous. No expansion without a delivered Proof Pack."}
        </p>
      </motion.header>

      {/* ------------------------------------------------------------------ */}
      {/* Pricing cards                                                       */}
      {/* ------------------------------------------------------------------ */}
      <section className="grid gap-8 md:grid-cols-3">
        {PLANS.map((plan, i) => (
          <PlanCard key={plan.id} plan={plan} isAr={isAr} index={i} />
        ))}
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Money-back guarantee + payment methods                             */}
      {/* ------------------------------------------------------------------ */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="flex flex-col items-center gap-6 rounded-2xl border border-emerald-500/30 bg-emerald-500/5 px-8 py-6 sm:flex-row sm:justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/15 text-emerald-500">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={1.5}
              className="h-5 w-5"
              aria-hidden="true"
            >
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div>
            <p className="font-semibold text-sm">
              {isAr ? "ضمان استرداد المبلغ" : "Money-Back Guarantee"}
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr
                ? "استرداد كامل خلال 7 أيام إذا لم تحصل على قيمة موثّقة"
                : "Full refund within 7 days if no documented value delivered"}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <p className="text-xs font-semibold text-muted-foreground">
            {isAr ? "وسائل الدفع:" : "Payment methods:"}
          </p>
          <div className="flex items-center gap-3">
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">
              Visa
            </span>
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">
              Mada
            </span>
            <span className="rounded-md border border-border/60 bg-card px-2.5 py-1 text-xs font-bold">
              {isAr ? "تحويل بنكي" : "Bank Transfer"}
            </span>
          </div>
        </div>
      </motion.section>

      {/* ------------------------------------------------------------------ */}
      {/* FAQ                                                                 */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "الأسئلة الشائعة" : "Frequently Asked Questions"}
        </motion.h2>
        <FaqAccordion items={FAQ_ITEMS} isAr={isAr} />
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Bottom CTA strip                                                   */}
      {/* ------------------------------------------------------------------ */}
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#002f5f] p-8 text-center text-white"
      >
        <h2 className="text-2xl font-bold">
          {isAr
            ? "لا تزال غير متأكد؟ ابدأ بتشخيص مجاني"
            : "Still unsure? Start with a free diagnostic"}
        </h2>
        <p className="mx-auto mt-3 max-w-md text-white/70 text-sm">
          {isAr
            ? "Risk Score مجاني في 5 دقائق — لا بطاقة ائتمانية مطلوبة."
            : "Free Risk Score in 5 minutes — no credit card required."}
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-4">
          <Button variant="gold" size="lg" asChild>
            <Link href={`/${isAr ? "ar" : "en"}/risk-score`}>
              {isAr ? "احسب Risk Score مجاناً" : "Calculate Risk Score Free"}
            </Link>
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="border-white/20 text-white hover:bg-white/10"
            asChild
          >
            <Link href={`/${isAr ? "ar" : "en"}/dealix-diagnostic`}>
              {isAr ? "احجز استشارة" : "Book a Consultation"}
            </Link>
          </Button>
        </div>
      </motion.section>
    </div>
  );
}
