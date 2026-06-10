"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const EVIDENCE_LEVELS = [
  { level: "L0", color: "text-red-500", bg: "bg-red-50 dark:bg-red-950/20", ar: "فرضية — لا دليل بعد", en: "Hypothesis — no evidence yet" },
  { level: "L1", color: "text-orange-500", bg: "bg-orange-50 dark:bg-orange-950/20", ar: "مؤشر — دليل جزئي", en: "Indicator — partial evidence" },
  { level: "L2", color: "text-yellow-500", bg: "bg-yellow-50 dark:bg-yellow-950/20", ar: "منطقي — أدلة متعددة", en: "Logical — multiple evidence points" },
  { level: "L3", color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-950/20", ar: "موثّق — مصادر معتمدة", en: "Documented — verified sources" },
  { level: "L4", color: "text-emerald-500", bg: "bg-emerald-50 dark:bg-emerald-950/20", ar: "مُثبَت — قابل للتدقيق", en: "Proven — fully auditable" },
  { level: "L5", color: "text-purple-500", bg: "bg-purple-50 dark:bg-purple-950/20", ar: "مُتحقَّق منه — خارجياً", en: "Externally verified" },
];

const SAMPLE_SECTIONS_AR = [
  {
    id: "s1",
    title: "مصادر العملاء المحتملين",
    level: "L3",
    status: "مكتمل",
    statusColor: "emerald",
    content: "تم تحليل مصادر الـ leads: 45% من LinkedIn، 30% إحالات، 25% بحث عضوي. جودة بيانات CRM: 62% مكتملة. توصية: تنظيف 38% قبل أي outreach.",
    actions: ["تنظيف بيانات CRM", "توثيق مصدر كل lead", "إضافة consent timestamp"],
  },
  {
    id: "s2",
    title: "ملاك القرارات",
    level: "L2",
    status: "يحتاج مدخلات",
    statusColor: "amber",
    content: "فجوة: 6 من 10 leads ليس لها مالك واضح بعد 5 أيام من الوصول. متوسط وقت الاستجابة: 72 ساعة (المستهدف: 24 ساعة). تحتاج: تعيين مالك لكل lead في CRM.",
    actions: ["تعيين مالك لكل lead", "إعداد SLA 24 ساعة", "تفعيل تنبيه تجاوز المهلة"],
  },
  {
    id: "s3",
    title: "سجل الأدلة",
    level: "L1",
    status: "محدود",
    statusColor: "red",
    content: "أقل من 30% من المحادثات موثّقة في CRM. 4 صفقات مُغلَقة بدون سجل follow-up. مخاطر: صعوبة التدقيق والإثبات عند الاختلاف مع العميل.",
    actions: ["توثيق كل محادثة في CRM", "إضافة نموذج evidence لكل صفقة", "ربط WhatsApp بـ CRM"],
  },
  {
    id: "s4",
    title: "قرارات الإيراد",
    level: "L3",
    status: "مكتمل",
    statusColor: "emerald",
    content: "تحديد 3 فرص توسع فورية: (1) 3 عملاء على عقد سنوي قابل للتجديد، (2) 2 عروض معلّقة منذ 30+ يوم، (3) قطاع لوجستيات = أعلى معدل تحويل.",
    actions: ["تجديد 3 عقود سنوية", "متابعة 2 عروض معلّقة", "التوسع في قطاع اللوجستيات"],
  },
];

const SAMPLE_SECTIONS_EN = [
  {
    id: "s1",
    title: "Lead Sources",
    level: "L3",
    status: "Complete",
    statusColor: "emerald",
    content: "Lead source analysis: 45% LinkedIn, 30% referrals, 25% organic search. CRM data quality: 62% complete. Recommendation: clean 38% before any outreach.",
    actions: ["Clean CRM data", "Document source per lead", "Add consent timestamp"],
  },
  {
    id: "s2",
    title: "Decision Owners",
    level: "L2",
    status: "Needs Input",
    statusColor: "amber",
    content: "Gap: 6 of 10 leads have no clear owner after 5 days. Average response time: 72 hours (target: 24 hours). Needed: assign owner per lead in CRM.",
    actions: ["Assign owner per lead", "Set 24-hour SLA", "Enable deadline alert"],
  },
  {
    id: "s3",
    title: "Evidence Log",
    level: "L1",
    status: "Limited",
    statusColor: "red",
    content: "Less than 30% of conversations documented in CRM. 4 closed deals without follow-up record. Risk: difficulty auditing and proving in case of client dispute.",
    actions: ["Document every conversation in CRM", "Add evidence form per deal", "Link WhatsApp to CRM"],
  },
  {
    id: "s4",
    title: "Revenue Decisions",
    level: "L3",
    status: "Complete",
    statusColor: "emerald",
    content: "3 immediate expansion opportunities: (1) 3 clients on renewable annual contracts, (2) 2 pending proposals 30+ days, (3) logistics sector = highest conversion rate.",
    actions: ["Renew 3 annual contracts", "Follow up 2 pending proposals", "Expand in logistics sector"],
  },
];

const STATUS_COLORS: Record<string, string> = {
  emerald: "border-emerald-500/30 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300",
  amber: "border-amber-500/30 bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300",
  red: "border-red-500/30 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300",
};

export function ProofPackSampleView() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const sections = isAr ? SAMPLE_SECTIONS_AR : SAMPLE_SECTIONS_EN;
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="max-w-3xl mx-auto space-y-10" dir={isAr ? "rtl" : "ltr"}>

      {/* Header */}
      <header className={isAr ? "text-right" : ""}>
        <Badge variant="outline" className="mb-3 border-amber-500/30 bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300">
          {isAr ? "عيّنة Proof Pack — ليست بيانات حقيقية" : "Sample Proof Pack — Not real data"}
        </Badge>
        <h1 className="text-3xl font-bold">
          {isAr ? "Proof Pack — عيّنة توضيحية" : "Proof Pack — Illustrative Sample"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">
          {isAr
            ? "هذا نموذج Proof Pack كامل بأقسامه الأربعة ومستويات الأدلة. الـ Proof Pack الحقيقي يُبنى على بيانات شركتك الفعلية خلال 7 أيام من بدء التشخيص."
            : "This is a complete Proof Pack sample with its four sections and evidence levels. A real Proof Pack is built on your actual company data within 7 days of starting the diagnostic."}
        </p>

        {/* Meta info */}
        <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: isAr ? "المستوى" : "Level", value: "L3 / 4" },
            { label: isAr ? "الأقسام" : "Sections", value: "4" },
            { label: isAr ? "الإجراءات" : "Actions", value: "12" },
            { label: isAr ? "المدة" : "Duration", value: isAr ? "7 أيام" : "7 Days" },
          ].map((m) => (
            <div key={m.label} className="rounded-lg border border-border/50 bg-card/50 p-3 text-center">
              <p className="text-xs text-muted-foreground">{m.label}</p>
              <p className="mt-0.5 font-bold text-lg">{m.value}</p>
            </div>
          ))}
        </div>
      </header>

      {/* Evidence Scale */}
      <section>
        <h2 className="text-lg font-semibold mb-4">
          {isAr ? "مستويات الأدلة — L0 إلى L5" : "Evidence Levels — L0 to L5"}
        </h2>
        <div className="grid gap-2 sm:grid-cols-3">
          {EVIDENCE_LEVELS.map((el) => (
            <div key={el.level} className={`rounded-lg border p-3 ${el.bg}`}>
              <span className={`font-bold text-sm ${el.color}`}>{el.level}</span>
              <p className="text-xs text-foreground/70 mt-0.5">{isAr ? el.ar : el.en}</p>
            </div>
          ))}
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          {isAr ? "* لا upsell قبل L4 — هذا مبدأ Dealix غير القابل للتفاوض" : "* No upsell before L4 — Dealix non-negotiable principle"}
        </p>
      </section>

      {/* Sections */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold">
          {isAr ? "أقسام الـ Proof Pack" : "Proof Pack Sections"}
        </h2>
        {sections.map((s) => {
          const isOpen = expanded === s.id;
          const lvl = EVIDENCE_LEVELS.find((l) => l.level === s.level);
          return (
            <Card key={s.id} className="overflow-hidden">
              <button
                onClick={() => setExpanded(isOpen ? null : s.id)}
                className="w-full flex items-start justify-between p-5 text-start hover:bg-muted/20 transition-colors"
              >
                <div className="flex items-start gap-3 flex-1">
                  <span className={`rounded-md px-2 py-0.5 text-xs font-bold ${lvl?.color} border ${lvl?.bg} mt-0.5`}>
                    {s.level}
                  </span>
                  <div>
                    <p className="font-semibold">{s.title}</p>
                    <Badge variant="outline" className={`mt-1 text-xs ${STATUS_COLORS[s.statusColor]}`}>
                      {s.status}
                    </Badge>
                  </div>
                </div>
                <span className="text-muted-foreground text-lg ms-4">{isOpen ? "−" : "+"}</span>
              </button>
              {isOpen && (
                <div className="px-5 pb-5 border-t border-border/40 pt-4 space-y-4">
                  <p className="text-sm text-muted-foreground leading-relaxed">{s.content}</p>
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                      {isAr ? "الإجراءات المقترحة" : "Recommended Actions"}
                    </p>
                    <ul className="space-y-1">
                      {s.actions.map((a) => (
                        <li key={a} className="flex items-center gap-2 text-sm">
                          <span className="w-5 h-5 rounded-full border border-border flex items-center justify-center text-xs text-muted-foreground">→</span>
                          {a}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </Card>
          );
        })}
      </section>

      {/* Summary */}
      <Card className="p-6 border-primary/20 bg-gradient-to-br from-card to-card/50">
        <h2 className="font-semibold text-lg mb-3">
          {isAr ? "ملخص Proof Pack" : "Proof Pack Summary"}
        </h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "المستوى العام" : "Overall Level"}</span>
            <span className="font-bold text-blue-600 dark:text-blue-400">L3 — {isAr ? "موثّق" : "Documented"}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "أقسام مكتملة" : "Complete sections"}</span>
            <span className="font-bold text-emerald-600">2 / 4</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "إجراءات فورية" : "Immediate actions"}</span>
            <span className="font-bold">12</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "التوصية" : "Recommendation"}</span>
            <span className="font-bold text-amber-600">{isAr ? "Sprint 7 أيام" : "7-Day Sprint"}</span>
          </div>
        </div>
        <div className="mt-4 rounded-lg border border-amber-500/20 bg-amber-50/50 dark:bg-amber-950/20 p-3 text-sm text-amber-800 dark:text-amber-300">
          {isAr
            ? "توصية: المستوى L3 يؤهّل للتوصية بـ Sprint. لا Retainer شهري قبل الوصول لـ L4 في الأقسام الرئيسية."
            : "Recommendation: L3 level qualifies for Sprint recommendation. No monthly Retainer before reaching L4 in main sections."}
        </div>
      </Card>

      {/* Disclaimer */}
      <p className="text-xs text-muted-foreground border-t border-border/40 pt-4">
        {isAr
          ? "هذه عيّنة توضيحية فقط — لا تمثّل بيانات حقيقية. Proof Pack الحقيقي يُبنى على بيانات شركتك الفعلية بعد الموافقة والمراجعة البشرية."
          : "This is an illustrative sample only — it does not represent real data. A real Proof Pack is built on your actual company data after consent and human review."}
      </p>

      {/* CTAs */}
      <div className="flex flex-wrap gap-3">
        <Button asChild size="lg">
          <Link href={`/${locale}/dealix-diagnostic`}>
            {isAr ? "احصل على Proof Pack الخاص بك ←" : "Get Your Own Proof Pack →"}
          </Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link href={`/${locale}/risk-score`}>
            {isAr ? "Risk Score مجاني" : "Free Risk Score"}
          </Link>
        </Button>
        <Button asChild variant="ghost" size="lg">
          <Link href={`/${locale}/services`}>
            {isAr ? "الأسعار والمستويات" : "Pricing & Tiers"}
          </Link>
        </Button>
      </div>
    </div>
  );
}
