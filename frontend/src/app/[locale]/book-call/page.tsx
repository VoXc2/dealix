"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { ArrowLeft, ArrowRight, ShieldCheck, Clock } from "lucide-react";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const SECTORS = [
  { id: "real_estate", ar: "العقار والمقاولات", en: "Real Estate & Construction" },
  { id: "technology", ar: "التقنية و SaaS", en: "Technology & SaaS" },
  { id: "professional_services", ar: "الخدمات المهنية", en: "Professional Services" },
  { id: "b2b_services", ar: "خدمات B2B", en: "B2B Services" },
  { id: "finance", ar: "المالية والمحاسبة", en: "Finance & Accounting" },
  { id: "hospitality", ar: "الضيافة والفعاليات", en: "Hospitality & Events" },
  { id: "retail", ar: "التجزئة والتجارة", en: "Retail & Commerce" },
  { id: "healthcare", ar: "الصحة والرعاية", en: "Healthcare" },
  { id: "other", ar: "قطاع آخر", en: "Other sector" },
];

const TIME_SLOTS = [
  { id: "morning", ar: "صباحاً (٩–١٢)", en: "Morning (9–12)" },
  { id: "afternoon", ar: "ظهراً (١٢–٣)", en: "Afternoon (12–3)" },
  { id: "evening", ar: "مساءً (٣–٦)", en: "Evening (3–6)" },
];

const inputClass =
  "mt-1.5 w-full rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring transition-shadow";

interface BookCallForm {
  name: string;
  company: string;
  email: string;
  phone: string;
  sector: string;
  preferredTime: string;
}

export default function BookCallPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";
  const base = `/${locale}`;

  const [form, setForm] = useState<BookCallForm>({
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    preferredTime: "",
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // No fake guarantees — just record intent. Real booking happens via backend.
    setSubmitted(true);
  };

  const update = (field: keyof BookCallForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <PublicGtmShell compactNav>
      <div dir={dir} className="mx-auto max-w-3xl px-6 py-12 grid-pattern">
        <div className="mb-6">
          <Badge variant="default" className="mb-3">
            <Clock className="size-3 mr-1" />
            {isAr ? "٢٠ دقيقة" : "20 minutes"}
          </Badge>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {isAr ? "احجز تشخيص الإيراد بالذكاء الاصطناعي" : "Book an AI Revenue Diagnostic"}
          </h1>
          <p className="mt-2 text-lg text-muted-foreground max-w-2xl">
            {isAr
              ? "مكالمة ٢٠ دقيقة — نراجع مصادر الإيراد، الفجوات، والخطوات القابلة للتنفيذ. خطة واضحة، لا وعود."
              : "A 20-minute call — we review revenue sources, gaps, and actionable steps. Clear plan, no promises."}
          </p>
        </div>

        {/* Safety note */}
        <div className="mb-6 flex items-start gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-4">
          <ShieldCheck className="size-5 text-emerald-400 shrink-0 mt-0.5" />
          <div className="text-sm text-emerald-200/90">
            {isAr
              ? "بياناتك تُعالج وفق PDPL. لا مشاركة بدون موافقتك. موافقتك مطلوبة قبل أي إجراء خارجي."
              : "Your data is processed under PDPL. No sharing without your consent. Your approval is required before any external action."}
          </div>
        </div>

        {submitted ? (
          <Card className="border-emerald-500/30">
            <CardContent className="py-10 text-center">
              <ShieldCheck className="mx-auto size-12 text-emerald-400 mb-3" />
              <h2 className="text-xl font-semibold">
                {isAr ? "تم استلام طلبك" : "Request received"}
              </h2>
              <p className="mt-2 text-muted-foreground max-w-md mx-auto">
                {isAr
                  ? "سنتواصل معك خلال يوم عمل لتأكيد الموعد. لا توجد وعود — فقط خطة واضحة بعد المكالمة."
                  : "We'll reach out within one business day to confirm the slot. No promises — just a clear plan after the call."}
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
              <CardTitle>{isAr ? "تفاصيل الحجز" : "Booking details"}</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4" dir={dir}>
                <div>
                  <label htmlFor="name" className="text-sm font-medium">
                    {isAr ? "الاسم" : "Name"} <span className="text-red-400">*</span>
                  </label>
                  <input
                    id="name"
                    className={inputClass}
                    required
                    value={form.name}
                    onChange={(e) => update("name", e.target.value)}
                    placeholder={isAr ? "اسمك الكامل" : "Your full name"}
                  />
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label htmlFor="company" className="text-sm font-medium">
                      {isAr ? "الشركة" : "Company"} <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="company"
                      className={inputClass}
                      required
                      value={form.company}
                      onChange={(e) => update("company", e.target.value)}
                      placeholder={isAr ? "اسم الشركة" : "Company name"}
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="text-sm font-medium">
                      {isAr ? "البريد الإلكتروني" : "Email"} <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="email"
                      type="email"
                      className={inputClass}
                      required
                      value={form.email}
                      onChange={(e) => update("email", e.target.value)}
                      placeholder="you@company.com"
                      dir="ltr"
                    />
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label htmlFor="phone" className="text-sm font-medium">
                      {isAr ? "الهاتف" : "Phone"} <span className="text-red-400">*</span>
                    </label>
                    <input
                      id="phone"
                      type="tel"
                      className={inputClass}
                      required
                      value={form.phone}
                      onChange={(e) => update("phone", e.target.value)}
                      placeholder="+966 5x xxx xxxx"
                      dir="ltr"
                    />
                  </div>
                  <div>
                    <label htmlFor="sector" className="text-sm font-medium">
                      {isAr ? "القطاع" : "Sector"} <span className="text-red-400">*</span>
                    </label>
                    <Select
                      value={form.sector}
                      onValueChange={(v) => update("sector", v)}
                    >
                      <SelectTrigger id="sector" className={inputClass}>
                        <SelectValue placeholder={isAr ? "اختر القطاع" : "Select sector"} />
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
                </div>

                <div>
                  <label htmlFor="time" className="text-sm font-medium">
                    {isAr ? "الوقت المفضّل" : "Preferred time"} <span className="text-red-400">*</span>
                  </label>
                  <Select
                    value={form.preferredTime}
                    onValueChange={(v) => update("preferredTime", v)}
                  >
                    <SelectTrigger id="time" className={inputClass}>
                      <SelectValue placeholder={isAr ? "اختر الوقت" : "Select time"} />
                    </SelectTrigger>
                    <SelectContent>
                      {TIME_SLOTS.map((t) => (
                        <SelectItem key={t.id} value={t.id}>
                          {isAr ? t.ar : t.en}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {isAr ? "التوقيت: الرياض (AST). سنتواصل لتأكيد الموعد." : "Timezone: Riyadh (AST). We'll confirm the exact slot."}
                  </p>
                </div>

                <div className="pt-2">
                  <Button type="submit" variant="default" size="lg" className="w-full">
                    {isAr ? "احجز التشخيص" : "Book Diagnostic"}
                    {isAr ? <ArrowLeft className="size-4" /> : <ArrowRight className="size-4" />}
                  </Button>
                </div>
                <p className="text-center text-xs text-muted-foreground">
                  {isAr
                    ? "بالضغط على الحجز فأنت توافق على معالجة بياناتك وفق PDPL لأغراض الجدولة فقط."
                    : "By booking you agree your data is processed under PDPL for scheduling purposes only."}
                </p>
              </form>
            </CardContent>
          </Card>
        )}
      </div>
    </PublicGtmShell>
  );
}