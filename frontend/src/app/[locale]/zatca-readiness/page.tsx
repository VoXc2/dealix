"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const QUESTIONS_AR = [
  { id: "revenue", q: "هل إيراداتك السنوية تتجاوز ٣٧٥,٠٠٠ ريال؟", weight: 30 },
  { id: "invoicing", q: "هل تصدر فواتير إلكترونية حالياً؟", weight: 25 },
  { id: "erp", q: "هل لديك نظام ERP أو محاسبي متوافق مع ZATCA API؟", weight: 20 },
  { id: "testing", q: "هل اختبرت الاتصال ببيئة ZATCA Sandbox؟", weight: 15 },
  { id: "qr", q: "هل فواتيرك الحالية تحتوي على QR code معتمد ZATCA؟", weight: 10 },
];

const QUESTIONS_EN = [
  { id: "revenue", q: "Does your annual revenue exceed 375,000 SAR?", weight: 30 },
  { id: "invoicing", q: "Are you currently issuing electronic invoices?", weight: 25 },
  { id: "erp", q: "Do you have an ERP or accounting system with ZATCA API support?", weight: 20 },
  { id: "testing", q: "Have you tested connectivity to ZATCA Sandbox environment?", weight: 15 },
  { id: "qr", q: "Do your current invoices include ZATCA-compliant QR codes?", weight: 10 },
];

export default function ZatcaReadinessPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const questions = isAr ? QUESTIONS_AR : QUESTIONS_EN;

  const [answers, setAnswers] = useState<Record<string, boolean | null>>({});
  const [submitted, setSubmitted] = useState(false);

  const toggle = (id: string, val: boolean) =>
    setAnswers((prev) => ({ ...prev, [id]: val }));

  const score = questions.reduce((acc, q) => {
    if (answers[q.id] === true) return acc + q.weight;
    return acc;
  }, 0);

  const answered = Object.keys(answers).length === questions.length;

  const tier =
    score >= 80
      ? { label: isAr ? "جاهز للإنتاج ✓" : "Production Ready ✓", color: "emerald" }
      : score >= 50
      ? { label: isAr ? "يحتاج تجهيز" : "Needs Preparation", color: "amber" }
      : { label: isAr ? "يحتاج دعم عاجل" : "Urgent Support Needed", color: "red" };

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-10">
        {/* Hero */}
        <header>
          <div className="flex gap-2 mb-3">
            <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-300">
              {isAr ? "⏰ موعد نهائي — ٣٠ يونيو ٢٠٢٦" : "⏰ Deadline — June 30, 2026"}
            </Badge>
            <Badge variant="outline">ZATCA Phase 2 — Wave 24</Badge>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">
            {isAr
              ? "تحقق من جاهزيتك لـ ZATCA Phase 2 — مجاناً"
              : "Check Your ZATCA Phase 2 Readiness — Free"}
          </h1>
          <p className="mt-3 text-muted-foreground leading-relaxed max-w-xl">
            {isAr
              ? "كل شركة تتجاوز ٣٧٥,٠٠٠ ريال إيراداً ملزمة بالفاتورة الإلكترونية من ZATCA Wave 24. خمسة أسئلة تكشف جاهزيتك في دقيقة واحدة."
              : "Every company over 375,000 SAR revenue must comply with ZATCA e-invoicing by Wave 24. Five questions reveal your readiness in one minute."}
          </p>
        </header>

        {/* Quiz */}
        {!submitted ? (
          <Card className="p-8">
            <h2 className="font-semibold mb-6 text-lg">
              {isAr ? "أجب على الأسئلة التالية:" : "Answer the following:"}
            </h2>
            <div className="space-y-5">
              {questions.map((q, i) => (
                <div key={q.id} className="space-y-2">
                  <p className="text-sm font-medium">
                    {isAr ? `${i + 1}. ` : `${i + 1}. `}{q.q}
                  </p>
                  <div className="flex gap-3">
                    <button
                      onClick={() => toggle(q.id, true)}
                      className={`px-4 py-1.5 rounded-lg border text-sm transition-colors ${
                        answers[q.id] === true
                          ? "bg-emerald-500 text-white border-emerald-500"
                          : "border-border hover:border-emerald-400 text-muted-foreground"
                      }`}
                    >
                      {isAr ? "نعم ✓" : "Yes ✓"}
                    </button>
                    <button
                      onClick={() => toggle(q.id, false)}
                      className={`px-4 py-1.5 rounded-lg border text-sm transition-colors ${
                        answers[q.id] === false
                          ? "bg-red-100 text-red-700 border-red-400 dark:bg-red-950 dark:text-red-400"
                          : "border-border hover:border-red-300 text-muted-foreground"
                      }`}
                    >
                      {isAr ? "لا ✗" : "No ✗"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-8 flex gap-3">
              <Button
                onClick={() => setSubmitted(true)}
                disabled={!answered}
                size="lg"
                className="font-semibold"
              >
                {isAr ? "احسب درجة الجاهزية ←" : "Calculate Readiness Score →"}
              </Button>
            </div>
          </Card>
        ) : (
          <div className="space-y-6">
            {/* Score Card */}
            <Card className={`p-8 border-${tier.color}-500/30 bg-${tier.color}-50/30 dark:bg-${tier.color}-950/20 text-center`}>
              <p className="text-6xl font-black mb-3">{score}<span className="text-2xl text-muted-foreground">/100</span></p>
              <Badge
                className={
                  tier.color === "emerald"
                    ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
                    : tier.color === "amber"
                    ? "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300"
                    : "bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300"
                }
              >
                {tier.label}
              </Badge>
              <p className="mt-4 text-muted-foreground text-sm">
                {score >= 80
                  ? (isAr
                    ? "شركتك جاهزة لـ ZATCA Phase 2. تحقق من آخر التفاصيل مع المحاسب."
                    : "Your company is ready for ZATCA Phase 2. Verify final details with your accountant.")
                  : score >= 50
                  ? (isAr
                    ? "تحتاج بعض التجهيزات قبل يونيو ٢٠٢٦. Dealix يساعدك تنهيها في وقت قياسي."
                    : "Some preparation needed before June 2026. Dealix can help you complete it quickly.")
                  : (isAr
                    ? "تحتاج دعماً عاجلاً لتجنب غرامات ZATCA. تحدث معنا الآن."
                    : "You need urgent support to avoid ZATCA penalties. Contact us now.")}
              </p>
            </Card>

            {/* CTA Block */}
            <Card className="p-8 bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
              <h3 className="font-bold text-lg mb-2">
                {isAr
                  ? "Dealix يجهّزك للامتثال ويحسّن إيراداتك في نفس الوقت"
                  : "Dealix gets you compliant and revenue-optimized at the same time"}
              </h3>
              <p className="text-sm text-muted-foreground mb-6">
                {isAr
                  ? "Sprint ٧ أيام يتضمن ZATCA readiness check + Proof Pack + Company Brain v1 · فقط ٤٩٩ ر.س"
                  : "7-day Sprint includes ZATCA readiness check + Proof Pack + Company Brain v1 · Only 499 SAR"}
              </p>
              <div className="flex flex-wrap gap-3">
                <Button asChild size="lg" className="font-semibold">
                  <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
                    {isAr ? "ابدأ Sprint 499 SAR ←" : "Start Sprint 499 SAR →"}
                  </Link>
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  onClick={() => { setAnswers({}); setSubmitted(false); }}
                >
                  {isAr ? "أعد التقييم" : "Retake Assessment"}
                </Button>
              </div>
            </Card>

            {/* ZATCA Checklist */}
            <Card className="p-6">
              <h3 className="font-semibold mb-4">
                {isAr ? "قائمة مراجعة ZATCA Wave 24" : "ZATCA Wave 24 Checklist"}
              </h3>
              <div className="space-y-2">
                {(isAr ? [
                  { done: answers.revenue === true, text: "إيراد يتجاوز ٣٧٥,٠٠٠ ر.س (Wave 24 scope)" },
                  { done: answers.invoicing === true, text: "فوترة إلكترونية نشطة (Phase 1 ✓)" },
                  { done: answers.erp === true, text: "نظام ERP متوافق مع ZATCA API" },
                  { done: answers.testing === true, text: "اختبار Sandbox مكتمل" },
                  { done: answers.qr === true, text: "QR code معتمد على الفواتير" },
                ] : [
                  { done: answers.revenue === true, text: "Revenue exceeds 375,000 SAR (Wave 24 scope)" },
                  { done: answers.invoicing === true, text: "Active e-invoicing (Phase 1 ✓)" },
                  { done: answers.erp === true, text: "ERP with ZATCA API compatibility" },
                  { done: answers.testing === true, text: "Sandbox testing complete" },
                  { done: answers.qr === true, text: "ZATCA-compliant QR codes on invoices" },
                ]).map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className={`text-lg ${item.done ? "text-emerald-500" : "text-red-400"}`}>
                      {item.done ? "✓" : "✗"}
                    </span>
                    <span className={`text-sm ${item.done ? "" : "text-muted-foreground"}`}>
                      {item.text}
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {/* Info section */}
        <div className="text-xs text-muted-foreground space-y-1">
          <p>
            {isAr
              ? "* هذا تقييم تقديري — استشر محاسبك المعتمد لأي قرارات ضريبية."
              : "* This is an indicative assessment — consult your certified accountant for tax decisions."}
          </p>
          <p>
            {isAr
              ? "لا بيانات شخصية تُرسل أو تُحفظ في هذه الصفحة."
              : "No personal data is sent or stored on this page."}
          </p>
        </div>
      </div>
    </div>
  );
}
