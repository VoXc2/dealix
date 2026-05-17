"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Check, Loader2, ShieldCheck, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { api } from "@/lib/api";

type Step = "lead" | "score" | "result";

interface RiskResult {
  score: number;
  band: string;
  factors: string[];
  is_estimate: boolean;
  source: string;
  disclaimer?: string;
}

interface Offering {
  id?: string;
  name_ar?: string;
  name_en?: string;
  price_sar?: number;
  price_unit?: string;
}

export function DiagnosticFunnel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [step, setStep] = useState<Step>("lead");
  const [busy, setBusy] = useState(false);

  // Step 1 — lead
  const [lead, setLead] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    role: "",
    message: "",
  });
  const [consent, setConsent] = useState(false);
  const [website, setWebsite] = useState(""); // honeypot

  // Step 2 — risk inputs
  const [risk, setRisk] = useState({
    has_crm: false,
    uses_ai: false,
    region: "",
    budget: "",
    urgency: "",
  });

  // Step 3 — results
  const [result, setResult] = useState<RiskResult | null>(null);
  const [sample, setSample] = useState<Record<string, unknown> | null>(null);
  const [services, setServices] = useState<Offering[]>([]);

  async function submitLead(e: React.FormEvent) {
    e.preventDefault();
    if (!lead.name || !lead.company || !lead.email.includes("@")) {
      toast.error(T("الرجاء تعبئة الحقول المطلوبة", "Please fill the required fields"));
      return;
    }
    if (!consent) {
      toast.error(T("الموافقة على المعالجة مطلوبة", "Consent is required"));
      return;
    }
    setBusy(true);
    try {
      await api.postPublicLead({ ...lead, consent, website });
      setStep("score");
    } catch {
      toast.error(T("تعذّر الإرسال", "Submission failed"));
    } finally {
      setBusy(false);
    }
  }

  async function submitRisk(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      const [scoreRes, sampleRes, servicesRes] = await Promise.all([
        api.postPublicRiskScore({ ...risk, company: lead.company, role: lead.role }),
        api.getPublicProofPackSample(),
        api.getPublicServices(),
      ]);
      setResult(scoreRes.data as RiskResult);
      setSample(sampleRes.data as Record<string, unknown>);
      const sData = servicesRes.data as { services?: Offering[] };
      setServices(Array.isArray(sData.services) ? sData.services : []);
      setStep("result");
    } catch {
      toast.error(T("تعذّر حساب التقييم", "Could not compute the score"));
    } finally {
      setBusy(false);
    }
  }

  const steps: Step[] = ["lead", "score", "result"];

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="flex items-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={s} className="flex items-center gap-2 flex-1">
            <div
              className={`flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold ${
                steps.indexOf(step) >= i
                  ? "bg-gold-500 text-white"
                  : "bg-muted text-muted-foreground"
              }`}
            >
              {steps.indexOf(step) > i ? <Check className="w-4 h-4" /> : i + 1}
            </div>
            {i < steps.length - 1 && (
              <div
                className={`h-0.5 flex-1 ${
                  steps.indexOf(step) > i ? "bg-gold-500" : "bg-muted"
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {step === "lead" && (
        <motion.form
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={submitLead}
          className="space-y-4 rounded-2xl border border-border bg-card p-6"
        >
          <h2 className="text-lg font-semibold">
            {T("التشخيص المجاني", "Free Diagnostic")}
          </h2>
          <p className="text-sm text-muted-foreground">
            {T(
              "ابدأ بتشخيص عمليات الإيراد لديك — بدون التزام.",
              "Start a revenue-ops diagnostic — no commitment.",
            )}
          </p>
          <Input
            placeholder={T("الاسم *", "Name *")}
            value={lead.name}
            onChange={(e) => setLead({ ...lead, name: e.target.value })}
          />
          <Input
            placeholder={T("الشركة *", "Company *")}
            value={lead.company}
            onChange={(e) => setLead({ ...lead, company: e.target.value })}
          />
          <Input
            type="email"
            placeholder={T("البريد الإلكتروني *", "Email *")}
            value={lead.email}
            onChange={(e) => setLead({ ...lead, email: e.target.value })}
          />
          <Input
            placeholder={T("الجوال", "Phone")}
            value={lead.phone}
            onChange={(e) => setLead({ ...lead, phone: e.target.value })}
          />
          <Input
            placeholder={T("الدور الوظيفي", "Your role")}
            value={lead.role}
            onChange={(e) => setLead({ ...lead, role: e.target.value })}
          />
          <Input
            placeholder={T("ما التحدّي الأساسي؟", "What is your main challenge?")}
            value={lead.message}
            onChange={(e) => setLead({ ...lead, message: e.target.value })}
          />
          {/* Honeypot — hidden from real users */}
          <input
            type="text"
            tabIndex={-1}
            autoComplete="off"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            className="hidden"
            aria-hidden="true"
          />
          <label className="flex items-start gap-2 text-sm text-muted-foreground">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-1"
            />
            <span>
              {T(
                "أوافق على معالجة بياناتي للتواصل معي بخصوص هذا الطلب.",
                "I consent to my data being processed to contact me about this request.",
              )}
            </span>
          </label>
          <Button type="submit" variant="emerald" disabled={busy} className="w-full">
            {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : T("متابعة", "Continue")}
          </Button>
        </motion.form>
      )}

      {step === "score" && (
        <motion.form
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={submitRisk}
          className="space-y-4 rounded-2xl border border-border bg-card p-6"
        >
          <h2 className="text-lg font-semibold">
            {T("تقدير الجاهزية", "Readiness Estimate")}
          </h2>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={risk.has_crm}
              onChange={(e) => setRisk({ ...risk, has_crm: e.target.checked })}
            />
            {T("لدينا نظام CRM أو عملية مبيعات", "We have a CRM or sales process")}
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={risk.uses_ai}
              onChange={(e) => setRisk({ ...risk, uses_ai: e.target.checked })}
            />
            {T("نستخدم أو نخطط لاستخدام الذكاء الاصطناعي", "We use or plan to use AI")}
          </label>
          <Input
            placeholder={T("الدولة / المنطقة", "Country / region")}
            value={risk.region}
            onChange={(e) => setRisk({ ...risk, region: e.target.value })}
          />
          <Input
            placeholder={T("الميزانية التقريبية (ريال)", "Approx. budget (SAR)")}
            value={risk.budget}
            onChange={(e) => setRisk({ ...risk, budget: e.target.value })}
          />
          <Input
            placeholder={T("مدى الإلحاح (مثال: خلال 30 يوم)", "Urgency (e.g. within 30 days)")}
            value={risk.urgency}
            onChange={(e) => setRisk({ ...risk, urgency: e.target.value })}
          />
          <Button type="submit" variant="emerald" disabled={busy} className="w-full">
            {busy ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              T("احسب التقدير", "Get my estimate")
            )}
          </Button>
        </motion.form>
      )}

      {step === "result" && result && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="rounded-2xl border border-border bg-card p-6 text-center">
            <p className="text-sm text-muted-foreground">
              {T("تقدير الجاهزية", "Readiness estimate")}
            </p>
            <p className="text-5xl font-bold text-gold-400 my-2">{result.score}</p>
            <Badge variant="outline" className="capitalize">
              {result.band}
            </Badge>
            {result.is_estimate && (
              <div className="mt-3 flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
                <ShieldCheck className="w-3.5 h-3.5" />
                {T(
                  "تقدير أولي — ليس تقييماً نهائياً",
                  "Estimate only — not a final assessment",
                )}
                <Badge variant="outline" className="ms-1 text-[10px]">
                  is_estimate
                </Badge>
              </div>
            )}
            {result.factors.length > 0 && (
              <div className="mt-4 flex flex-wrap justify-center gap-1.5">
                {result.factors.map((f) => (
                  <Badge key={f} variant="outline" className="text-[10px]">
                    {f}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {sample && (
            <div className="rounded-2xl border border-border bg-card p-6">
              <h3 className="font-semibold mb-1">
                {String(isAr ? sample.title_ar : sample.title_en)}
              </h3>
              <p className="text-xs text-muted-foreground mb-3">
                {String(sample.disclaimer || "")}
              </p>
              <ul className="space-y-2">
                {(sample.sections as { id: string; title_en: string; body_en: string }[]).map(
                  (s) => (
                    <li key={s.id} className="rounded-lg bg-muted/40 p-3">
                      <p className="text-sm font-medium">{s.title_en}</p>
                      <p className="text-xs text-muted-foreground">{s.body_en}</p>
                    </li>
                  ),
                )}
              </ul>
            </div>
          )}

          {services.length > 0 && (
            <div className="rounded-2xl border border-border bg-card p-6">
              <h3 className="font-semibold mb-3">{T("الباقات", "Service packages")}</h3>
              <ul className="space-y-2">
                {services.map((s, i) => (
                  <li
                    key={s.id || i}
                    className="flex items-center justify-between rounded-lg bg-muted/40 p-3 text-sm"
                  >
                    <span>{isAr ? s.name_ar : s.name_en}</span>
                    <span className="font-semibold text-emerald-400">
                      {s.price_sar
                        ? `${s.price_sar} ${T("ريال", "SAR")}${
                            s.price_unit === "per_month" ? T("/شهر", "/mo") : ""
                          }`
                        : T("حسب النطاق", "Custom")}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
            <ArrowRight className="w-4 h-4" />
            {T(
              "سيتواصل معك الفريق لحجز جلسة التشخيص.",
              "Our team will contact you to book the diagnostic session.",
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
