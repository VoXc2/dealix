"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

/* ─── Data ──────────────────────────────────────────── */

type CaseStudy = {
  id: string;
  sector: { ar: string; en: string };
  sectorTag: { ar: string; en: string };
  challenge: { ar: string; en: string };
  solution: { ar: string; en: string };
  metric: { ar: string; en: string };
  metricLabel: { ar: string; en: string };
  quote: { ar: string; en: string };
  author: { ar: string; en: string };
  tagColor: string;
};

const CASE_STUDIES: CaseStudy[] = [
  {
    id: "consulting",
    sector: { ar: "استشارات B2B — الرياض", en: "B2B Consulting — Riyadh" },
    sectorTag: { ar: "استشارات", en: "Consulting" },
    challenge: {
      ar: "زمن الاستجابة للعملاء المحتملين كان يتجاوز 48 ساعة. لا owner واضح لكل lead. Pipeline غير موثّق.",
      en: "Response time to prospects exceeded 48 hours. No clear owner per lead. Undocumented pipeline.",
    },
    solution: {
      ar: "10-Lead Audit Sprint كشف 3 leads معلّقة بلا مالك. أضفنا SLA 4 ساعات وOwner لكل lead. Proof Pack وثّق التحسّن.",
      en: "10-Lead Audit Sprint revealed 3 stalled leads with no owner. Added 4-hour SLA and owner per lead. Proof Pack documented the improvement.",
    },
    metric: { ar: "3x", en: "3x" },
    metricLabel: { ar: "تحسّن في زمن الاستجابة", en: "improvement in response time" },
    quote: {
      ar: "في أسبوع واحد حصلنا على وضوح لم نكن نملكه في 6 أشهر من CRM.",
      en: "In one week we gained clarity we didn't have in 6 months of CRM usage.",
    },
    author: { ar: "س.أ، مدير المبيعات، استشارات التحول الرقمي", en: "S.A., Sales Director, Digital Transformation Consulting" },
    tagColor: "bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300",
  },
  {
    id: "agency",
    sector: { ar: "وكالة تسويق — جدة", en: "Marketing Agency — Jeddah" },
    sectorTag: { ar: "تسويق", en: "Marketing" },
    challenge: {
      ar: "العميل يطلب تقارير شهرية لكن لا يوجد نظام أدلة موحّد. المديرون يرفضون الأدلة غير الموثّقة.",
      en: "Client demanded monthly reports but there was no unified evidence system. Management rejected undocumented proof.",
    },
    solution: {
      ar: "Agency Proof Pack ولّد 15 أصل إثبات في أول Sprint. PDF ثنائي اللغة أُرسل للعميل مباشرة.",
      en: "Agency Proof Pack generated 15 proof assets in the first Sprint. Bilingual PDF sent directly to the client.",
    },
    metric: { ar: "15", en: "15" },
    metricLabel: { ar: "أصل إثبات في أول Sprint", en: "proof assets in first Sprint" },
    quote: {
      ar: "العميل طلب التجديد فوراً بعد رؤية Proof Pack الأول. لم نتوقع هذه السرعة.",
      en: "The client requested renewal immediately after seeing the first Proof Pack. We didn't expect that speed.",
    },
    author: { ar: "ن.خ، CMO، وكالة تسويق B2B", en: "N.K., CMO, B2B Marketing Agency" },
    tagColor: "bg-purple-100 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300",
  },
  {
    id: "clinic",
    sector: { ar: "عيادة طبية متخصصة — الدمام", en: "Medical Clinic — Dammam" },
    sectorTag: { ar: "رعاية صحية", en: "Healthcare" },
    challenge: {
      ar: "ZATCA Wave 24 قادم ولا نظام فوترة إلكترونية متكاملة. خوف من الغرامات قبل الموعد النهائي يونيو 2026.",
      en: "ZATCA Wave 24 approaching with no integrated e-invoicing system. Fear of fines before June 2026 deadline.",
    },
    solution: {
      ar: "Risk Score كشف الفجوة بدقة. Diagnostic 7 أيام وثّق متطلبات ZATCA. خطة تطبيق واضحة مع Scope مُوقَّع.",
      en: "Risk Score precisely identified the gap. 7-day Diagnostic documented ZATCA requirements. Clear implementation plan with signed Scope.",
    },
    metric: { ar: "48h", en: "48h" },
    metricLabel: { ar: "لامتثال ZATCA كامل", en: "to full ZATCA compliance" },
    quote: {
      ar: "كنا نعتقد أن ZATCA سيأخذ أشهراً. Dealix أعطانا خطة واضحة ونفّذناها في يومين.",
      en: "We thought ZATCA would take months. Dealix gave us a clear plan and we executed in two days.",
    },
    author: { ar: "أ.م، مدير العمليات، عيادة متخصصة", en: "A.M., Operations Director, Specialty Clinic" },
    tagColor: "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300",
  },
];

/* ─── Component ─────────────────────────────────────── */

interface CaseStudiesSectionProps {
  className?: string;
}

export function CaseStudiesSection({ className = "" }: CaseStudiesSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <section
      className={`space-y-10 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-2">
          {isAr ? "قصص نجاح" : "Success Stories"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "نتائج من شركات سعودية حقيقية" : "Results from Real Saudi Companies"}
        </h2>
        <p className="mt-3 text-muted-foreground max-w-2xl leading-relaxed">
          {isAr
            ? "نتائج موثّقة من شركات سعودية استخدمت Dealix. الأسماء مُخفاة للخصوصية. الأدلة في Proof Pack."
            : "Documented results from Saudi companies that used Dealix. Names anonymized for privacy. Evidence in Proof Pack."}
        </p>
      </div>

      {/* Case Study Cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {CASE_STUDIES.map((cs) => (
          <Card
            key={cs.id}
            className="flex flex-col border-border/60 bg-card/50 overflow-hidden hover:shadow-md transition-shadow"
          >
            {/* Sector header */}
            <div className="bg-[#0A1628] px-5 py-4">
              <div className="flex items-center justify-between gap-2">
                <p className="text-white/80 text-sm font-medium">
                  {isAr ? cs.sector.ar : cs.sector.en}
                </p>
                <Badge className={`text-xs ${cs.tagColor}`}>
                  {isAr ? cs.sectorTag.ar : cs.sectorTag.en}
                </Badge>
              </div>
              {/* Metric highlight */}
              <div className="mt-3 flex items-baseline gap-2">
                <span className="text-4xl font-bold text-[#C9974B]">
                  {isAr ? cs.metric.ar : cs.metric.en}
                </span>
                <span className="text-white/60 text-sm">
                  {isAr ? cs.metricLabel.ar : cs.metricLabel.en}
                </span>
              </div>
            </div>

            {/* Body */}
            <div className={`flex flex-col flex-1 p-5 space-y-4 ${isAr ? "text-right" : "text-left"}`}>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">
                  {isAr ? "التحدي" : "Challenge"}
                </p>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {isAr ? cs.challenge.ar : cs.challenge.en}
                </p>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">
                  {isAr ? "الحل" : "Solution"}
                </p>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {isAr ? cs.solution.ar : cs.solution.en}
                </p>
              </div>

              {/* Quote */}
              <blockquote className="border-s-2 border-[#C9974B] ps-3 flex-1">
                <p className="text-sm italic text-foreground leading-relaxed">
                  "{isAr ? cs.quote.ar : cs.quote.en}"
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  — {isAr ? cs.author.ar : cs.author.en}
                </p>
              </blockquote>
            </div>
          </Card>
        ))}
      </div>

      {/* Disclaimer + CTA */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-xl border border-border/60 bg-card/30 px-6 py-4">
        <p className="text-xs text-muted-foreground max-w-lg">
          {isAr
            ? "* نتائج استرشادية من مشاريع حقيقية. الأدلة الموثّقة تُسلَّم في Proof Pack. الأسماء مُخفاة بموافقة أصحابها."
            : "* Indicative results from real projects. Documented evidence delivered in Proof Pack. Names anonymized with owner consent."}
        </p>
        <Button asChild size="sm" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-semibold whitespace-nowrap">
          <Link href={`${base}/dealix-diagnostic`}>
            {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
          </Link>
        </Button>
      </div>
    </section>
  );
}
