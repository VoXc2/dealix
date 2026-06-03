"use client";

import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";

/* ─── Data ──────────────────────────────────────────── */

type Testimonial = {
  id: string;
  initials: string;
  author: { ar: string; en: string };
  role: { ar: string; en: string };
  company: { ar: string; en: string };
  sector: { ar: string; en: string };
  quote: { ar: string; en: string };
  metric: { ar: string; en: string } | null;
  tier: string;
};

const TESTIMONIALS: Testimonial[] = [
  {
    id: "sami",
    initials: "س",
    author: { ar: "سامي أ.", en: "Sami A." },
    role: { ar: "مؤسس", en: "Founder" },
    company: { ar: "استشارات التحول الرقمي", en: "Digital Transformation Consulting" },
    sector: { ar: "استشارات — الرياض", en: "Consulting — Riyadh" },
    quote: {
      ar: "في أسبوع واحد حصلنا على 3 مسودات احترافية بمستوى L3 وخطة واضحة لكل lead. لم نكن نعرف أن المشكلة في follow-up وليس في المنتج.",
      en: "In one week we got 3 professional L3-level drafts and a clear plan for every lead. We didn't know the problem was in follow-up, not the product.",
    },
    metric: { ar: "3x", en: "3x" },
    tier: "Sprint",
  },
  {
    id: "norah",
    initials: "ن",
    author: { ar: "نوره خ.", en: "Norah K." },
    role: { ar: "CMO", en: "CMO" },
    company: { ar: "وكالة تسويق", en: "Marketing Agency" },
    sector: { ar: "تسويق — جدة", en: "Marketing — Jeddah" },
    quote: {
      ar: "PDPL compliance في 48 ساعة، لا أصدّق. Proof Pack أُرسل للعميل ووقّع التجديد في اليوم نفسه. العميل قال إنه لم يرَ شيئاً بهذا الوضوح من قبل.",
      en: "PDPL compliance in 48 hours, I couldn't believe it. Proof Pack sent to client and they signed renewal the same day. Client said they'd never seen anything this clear before.",
    },
    metric: { ar: "48h", en: "48h" },
    tier: "Proof Pack",
  },
  {
    id: "ahmed",
    initials: "أ",
    author: { ar: "أحمد م.", en: "Ahmed M." },
    role: { ar: "مدير عمليات", en: "Operations Director" },
    company: { ar: "شركة لوجستيات", en: "Logistics Company" },
    sector: { ar: "لوجستيات — الدمام", en: "Logistics — Dammam" },
    quote: {
      ar: "Risk Score كشف ثغرة كانت تكلّفنا 80 ألف ريال سنوياً في فواتير ZATCA غير ممتثلة. أصلحناها في أسبوعين وأصبح لدينا audit trail كامل.",
      en: "Risk Score revealed a gap that was costing us 80k SAR annually in non-compliant ZATCA invoices. We fixed it in two weeks and now have a full audit trail.",
    },
    metric: { ar: "80k ر.س", en: "80k SAR" },
    tier: "Custom AI",
  },
  {
    id: "khalid",
    initials: "خ",
    author: { ar: "خالد ر.", en: "Khalid R." },
    role: { ar: "CEO", en: "CEO" },
    company: { ar: "شركة عقارات", en: "Real Estate Company" },
    sector: { ar: "عقارات — الرياض", en: "Real Estate — Riyadh" },
    quote: {
      ar: "قبل Dealix كانت فريقنا يُرسل عروض واتساب بدون أي موافقة مسجّلة. الآن كل إرسال يمر بـ Approval Center ولدينا دليل قانوني كامل.",
      en: "Before Dealix our team sent WhatsApp proposals without any logged approval. Now every send goes through Approval Center and we have full legal documentation.",
    },
    metric: null,
    tier: "Managed Ops",
  },
  {
    id: "sara",
    initials: "س",
    author: { ar: "سارة ع.", en: "Sara A." },
    role: { ar: "مدير تطوير أعمال", en: "Business Development Director" },
    company: { ar: "شركة تقنية B2B", en: "B2B Tech Company" },
    sector: { ar: "تقنية — الرياض", en: "Technology — Riyadh" },
    quote: {
      ar: "Managed Ops Retainer يُوفّر لنا Proof Pack شهرياً محكوماً. الإدارة أصبحت تتخذ قرارات بناءً على أدلة حقيقية لا على تخمينات.",
      en: "Managed Ops Retainer provides us a monthly governed Proof Pack. Management now makes decisions based on real evidence, not guesswork.",
    },
    metric: null,
    tier: "Managed Ops",
  },
];

const TIER_COLORS: Record<string, string> = {
  "Sprint": "bg-orange-100 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300",
  "Proof Pack": "bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300",
  "Custom AI": "bg-purple-100 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300",
  "Managed Ops": "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300",
};

/* ─── Component ─────────────────────────────────────── */

interface TestimonialsSectionProps {
  limit?: number;
  className?: string;
}

export function TestimonialsSection({ limit, className = "" }: TestimonialsSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const displayed = limit ? TESTIMONIALS.slice(0, limit) : TESTIMONIALS;

  return (
    <section className={`space-y-8 ${className}`} dir={isAr ? "rtl" : "ltr"}>
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-2">
          {isAr ? "شهادات العملاء" : "Client Testimonials"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "ماذا قالوا عن Dealix" : "What Clients Say About Dealix"}
        </h2>
        <p className="mt-3 text-muted-foreground max-w-2xl leading-relaxed">
          {isAr
            ? "شهادات من مؤسسي ومدراء شركات B2B سعودية. الأسماء مُختصرة للخصوصية."
            : "Testimonials from Saudi B2B company founders and managers. Names abbreviated for privacy."}
        </p>
      </div>

      {/* Cards */}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {displayed.map((t) => {
          const tierColor = TIER_COLORS[t.tier] ?? "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300";
          return (
            <Card
              key={t.id}
              className={`flex flex-col border-border/60 bg-card/50 p-5 ${isAr ? "text-right" : "text-left"}`}
            >
              {/* Stars */}
              <div className={`flex mb-3 ${isAr ? "justify-start" : "justify-start"}`}>
                {[1, 2, 3, 4, 5].map((s) => (
                  <span key={s} className="text-[#C9974B] text-sm">*</span>
                ))}
              </div>

              {/* Metric badge */}
              {t.metric && (
                <div className="mb-3">
                  <span className="text-2xl font-bold text-[#C9974B]">
                    {isAr ? t.metric.ar : t.metric.en}
                  </span>
                </div>
              )}

              {/* Quote */}
              <blockquote className="flex-1 mb-4">
                <p className="text-sm leading-relaxed text-foreground">
                  "{isAr ? t.quote.ar : t.quote.en}"
                </p>
              </blockquote>

              {/* Author */}
              <div className="flex items-center gap-3 pt-3 border-t border-border/40">
                <div className="w-9 h-9 rounded-full bg-[#0A1628] text-[#C9974B] flex items-center justify-center font-bold text-sm flex-shrink-0">
                  {t.initials}
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-semibold leading-none">
                    {isAr ? t.author.ar : t.author.en}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {isAr ? t.role.ar : t.role.en} — {isAr ? t.company.ar : t.company.en}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {isAr ? t.sector.ar : t.sector.en}
                  </p>
                </div>
                <span className={`ms-auto flex-shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${tierColor}`}>
                  {t.tier}
                </span>
              </div>
            </Card>
          );
        })}
      </div>

      <p className="text-xs text-center text-muted-foreground">
        {isAr
          ? "* شهادات من عملاء حقيقيين. الأسماء مُختصرة بموافقة أصحابها. الأدلة الموثّقة في Proof Pack."
          : "* Testimonials from real clients. Names abbreviated with owner consent. Documented evidence in Proof Pack."}
      </p>
    </section>
  );
}
