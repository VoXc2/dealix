"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { ShieldCheck, ArrowLeft, ArrowRight } from "lucide-react";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const SECTORS = [
  { id: "real_estate", ar: "العقار", en: "Real Estate" },
  { id: "retail", ar: "التجزئة", en: "Retail" },
  { id: "logistics", ar: "اللوجستيات", en: "Logistics" },
  { id: "professional_services", ar: "الخدمات المهنية", en: "Professional Services" },
  { id: "other", ar: "قطاع آخر", en: "Other" },
];

const DATA_VOLUME_OPTIONS = [
  { id: "lt1k", ar: "أقل من ألف سجل", en: "< 1K rows" },
  { id: "1k_100k", ar: "١ ألف – ١٠٠ ألف سجل", en: "1K – 100K rows" },
  { id: "gt100k", ar: "أكثر من ١٠٠ ألف سجل", en: "100K+ rows" },
];

const DATA_SENSITIVITY_OPTIONS = [
  { id: "public", ar: "عام", en: "Public" },
  { id: "internal", ar: "داخلي", en: "Internal" },
  { id: "confidential", ar: "سري", en: "Confidential" },
];

const TIMELINE_OPTIONS = [
  { id: "lt1m", ar: "أقل من شهر", en: "< 1 month" },
  { id: "1_3m", ar: "١–٣ أشهر", en: "1–3 months" },
  { id: "gt3m", ar: "أكثر من ٣ أشهر", en: "3+ months" },
];

const BUDGET_OPTIONS = [
  { id: "5k_10k", ar: "٥٬٠٠٠ – ١٠٬٠٠٠ ريال", en: "5,000–10,000 SAR" },
  { id: "10k_25k", ar: "١٠٬٠٠٠ – ٢٥٬٠٠٠ ريال", en: "10,000–25,000 SAR" },
  { id: "gt25k", ar: "أكثر من ٢٥٬٠٠٠ ريال", en: "25,000+ SAR" },
];

const inputClass =
  "mt-1.5 w-full rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring transition-shadow";

interface CustomAiForm {
  sector: string;
  use_case: string;
  data_volume: string;
  data_sensitivity: string;
  timeline: string;
  budget_band: string;
}

export default function CustomAiPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const base = `/${locale}`;

  const [form, setForm] = useState<CustomAiForm>({
    sector: "",
    use_case: "",
    data_volume: "",
    data_sensitivity: "",
    timeline: "",
    budget_band: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const update = (field: keyof CustomAiForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/public/custom-ai-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      setSubmitted(true);
    } catch (err) {
      setError(
        isAr
          ? "حدث خطأ أثناء الإرسال. يرجى المحاولة مرة أخرى."
          : "Submission error. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <PublicGtmShell compactNav>
      <div dir={dir} className="mx-auto max-w-3xl px-6 py-12">
        <div className="mb-6">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {isAr ? "إعداد نظام ذكاء اصطناعي مخصص" : "Custom AI Service Setup"}
          </h1>
          <p className="mt-2 text-lg text-muted-foreground max-w-2xl">
            {isAr
              ? "٥٬٠٠٠ – ٢٥٬٠٠٠ ريال إعداداً + ١٬٠٠٠ ريال شهرياً للإدارة. كل طلب يُراجَع قبل التنفيذ."
              : "5,000–25,000 SAR setup + 1,000 SAR/mo management. Every request is reviewed before any action."}
          </p>
        </div>

        <div className="mb-6 flex items-start gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-4">
          <ShieldCheck className="size-5 text-emerald-400 shrink-0 mt-0.5" />
          <div className="text-sm text-emerald-200/90">
            {isAr
              ? "كل طلب يُراجَع من المؤسس قبل أي إجراء / Every request is reviewed by the founder before any action."
              : "Every request is reviewed by the founder before any action / كل طلب يُراجَع من المؤسس قبل أي إجراء."}
          </div>
        </div>

        {submitted ? (
          <Card className="border-emerald-500/30">
            <CardContent className="py-10 text-center">
              <ShieldCheck className="mx-auto size-12 text-emerald-400 mb-3" />
              <h2 className="text-xl font-semibold">
                {isAr ? "شكراً — سنتواصل معك" : "Thank you — we will follow up"}
              </h2>
              <p className="mt-2 text-muted-foreground max-w-md mx-auto">
                {isAr
                  ? "استلمنا طلبك. سيراجعه المؤسس ويتواصل معك خلال يوم عمل."
                  : "We received your request. The founder will review it and follow up within one business day."}
              </p>
              <div className="mt-5">
                <Button asChild variant="outline">
                  <Link href={base}>
                    {isAr ? "العودة للرئيسية" : "Back home"}
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>
                {isAr ? "تفاصيل المشروع" : "Project details"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4" dir={dir}>
                <div>
                  <label htmlFor="sector" className="text-sm font-medium">
                    {isAr ? "القطاع" : "Sector"}{" "}
                    <span className="text-red-400">*</span>
                  </label>
                  <Select
                    value={form.sector}
                    onValueChange={(v) => update("sector", v)}
                    required
                  >
                    <SelectTrigger id="sector" className={inputClass}>
                      <SelectValue
                        placeholder={isAr ? "اختر القطاع" : "Select sector"}
                      />
                    </SelectTrigger>
                    <SelectContent>
                      {SECTORS.map((s) => (
                        <SelectItem key={s.id} value={s.id}>
                          {isAr ? s.ar : s.en}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label htmlFor="use_case" className="text-sm font-medium">
                    {isAr ? "حالة الاستخدام" : "Use case"}{" "}
                    <span className="text-red-400">*</span>
                  </label>
                  <textarea
                    id="use_case"
                    className={`${inputClass} min-h-[96px] resize-y`}
                    required
                    value={form.use_case}
                    onChange={(e) => update("use_case", e.target.value)}
                    placeholder={
                      isAr
                        ? "صف المشكلة التي تريد حلها بالذكاء الاصطناعي..."
                        : "Describe the problem you want to solve with AI..."
                    }
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label htmlFor="data_volume" className="text-sm font-medium">
                      {isAr ? "حجم البيانات" : "Data volume"}{" "}
                      <span className="text-red-400">*</span>
                    </label>
                    <Select
                      value={form.data_volume}
                      onValueChange={(v) => update("data_volume", v)}
                      required
                    >
                      <SelectTrigger id="data_volume" className={inputClass}>
                        <SelectValue
                          placeholder={isAr ? "اختر الحجم" : "Select volume"}
                        />
                      </SelectTrigger>
                      <SelectContent>
                        {DATA_VOLUME_OPTIONS.map((o) => (
                          <SelectItem key={o.id} value={o.id}>
                            {isAr ? o.ar : o.en}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label
                      htmlFor="data_sensitivity"
                      className="text-sm font-medium"
                    >
                      {isAr ? "حساسية البيانات" : "Data sensitivity"}{" "}
                      <span className="text-red-400">*</span>
                    </label>
                    <Select
                      value={form.data_sensitivity}
                      onValueChange={(v) => update("data_sensitivity", v)}
                      required
                    >
                      <SelectTrigger
                        id="data_sensitivity"
                        className={inputClass}
                      >
                        <SelectValue
                          placeholder={
                            isAr ? "اختر المستوى" : "Select level"
                          }
                        />
                      </SelectTrigger>
                      <SelectContent>
                        {DATA_SENSITIVITY_OPTIONS.map((o) => (
                          <SelectItem key={o.id} value={o.id}>
                            {isAr ? o.ar : o.en}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label htmlFor="timeline" className="text-sm font-medium">
                      {isAr ? "الجدول الزمني" : "Timeline"}{" "}
                      <span className="text-red-400">*</span>
                    </label>
                    <Select
                      value={form.timeline}
                      onValueChange={(v) => update("timeline", v)}
                      required
                    >
                      <SelectTrigger id="timeline" className={inputClass}>
                        <SelectValue
                          placeholder={isAr ? "اختر المدة" : "Select timeline"}
                        />
                      </SelectTrigger>
                      <SelectContent>
                        {TIMELINE_OPTIONS.map((o) => (
                          <SelectItem key={o.id} value={o.id}>
                            {isAr ? o.ar : o.en}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label htmlFor="budget_band" className="text-sm font-medium">
                      {isAr ? "نطاق الميزانية" : "Budget band"}{" "}
                      <span className="text-red-400">*</span>
                    </label>
                    <Select
                      value={form.budget_band}
                      onValueChange={(v) => update("budget_band", v)}
                      required
                    >
                      <SelectTrigger id="budget_band" className={inputClass}>
                        <SelectValue
                          placeholder={
                            isAr ? "اختر النطاق" : "Select budget"
                          }
                        />
                      </SelectTrigger>
                      <SelectContent>
                        {BUDGET_OPTIONS.map((o) => (
                          <SelectItem key={o.id} value={o.id}>
                            {isAr ? o.ar : o.en}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {error && (
                  <p className="text-sm text-red-400 text-center">{error}</p>
                )}

                <div className="pt-2">
                  <Button
                    type="submit"
                    variant="default"
                    size="lg"
                    className="w-full"
                    disabled={loading}
                  >
                    {loading
                      ? isAr
                        ? "جارٍ الإرسال..."
                        : "Submitting..."
                      : isAr
                      ? "أرسل الطلب"
                      : "Submit request"}
                    {!loading &&
                      (isAr ? (
                        <ArrowLeft className="size-4" />
                      ) : (
                        <ArrowRight className="size-4" />
                      ))}
                  </Button>
                </div>

                <p className="text-center text-xs text-muted-foreground">
                  {isAr
                    ? "بالإرسال توافق على معالجة بياناتك وفق PDPL لأغراض التقييم فقط."
                    : "By submitting you agree your data is processed under PDPL for evaluation purposes only."}
                </p>
              </form>
            </CardContent>
          </Card>
        )}

        <p className="mt-8 text-center text-xs text-muted-foreground border-t border-border pt-4">
          {isAr
            ? "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
            : "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"}
        </p>
      </div>
    </PublicGtmShell>
  );
}
