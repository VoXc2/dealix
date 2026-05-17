"use client";

import { useState } from "react";
import { api } from "@/lib/api";

interface DiagnosticFunnelProps {
  locale: string;
}

interface RiskScoreResult {
  ok?: boolean;
  lead_id?: string | null;
  fit_score?: number;
  bucket?: "low" | "medium" | "high" | "blocked";
  next_step?: string;
  reasons?: string[];
  doctrine_violations?: string[];
  sample_proof_pack?: { available: boolean; reason: string | null };
  governance_decision?: string;
  disclaimer?: string;
}

type FormState = Record<string, string>;

const EMPTY_FORM: FormState = {
  name: "",
  company: "",
  email: "",
  role: "",
  linkedin: "",
  sector: "",
  team_size: "",
  crm: "",
  crm_system: "",
  ai_usage: "",
  biggest_pain: "",
  consent_before_external_action: "",
  can_link_workflow_to_value: "",
  budget_range: "",
  urgency: "",
  website: "", // honeypot
};

const T = {
  en: {
    formTitle: "AI & Revenue Ops Risk Score",
    formSubtitle:
      "A short, deterministic self-check. No score is generated from empty input.",
    name: "Full name",
    company: "Company",
    email: "Work email",
    role: "Your role",
    linkedin: "LinkedIn (optional)",
    sector: "Sector",
    teamSize: "Team size",
    crm: "Do you use a CRM?",
    crmSystem: "Which CRM / system?",
    aiUsage: "Do you use AI in the team today?",
    biggestPain: "Where is the biggest pain?",
    consentExternal: "Do you require approval before any external action?",
    linkValue: "Can you link a workflow to a financial value?",
    budget: "Expected budget range",
    urgency: "Urgency",
    consent: "I agree to be contacted by Dealix about this request.",
    submit: "Get my Risk Score",
    submitting: "Scoring…",
    yes: "Yes",
    no: "No",
    choose: "Select…",
    pains: {
      pipeline: "Pipeline / lead flow",
      crm: "CRM data quality",
      follow_up: "Follow-up discipline",
      approvals: "Approvals / governance",
      reporting: "Reporting / visibility",
    },
    urgencies: { low: "Low", medium: "Medium", high: "High" },
    teamSizes: { "1-10": "1–10", "11-50": "11–50", "51-200": "51–200", "200+": "200+" },
    budgets: {
      none: "No budget yet",
      under_5000: "Under 5,000 SAR",
      "5000_25000": "5,000 – 25,000 SAR",
      "25000_plus": "25,000+ SAR",
    },
    resultTitle: "Your Risk Score",
    fitScore: "Fit score",
    nextSteps: {
      book_diagnostic_review: "Strong fit — book a paid Diagnostic Review.",
      request_sample_proof_pack:
        "Partial fit — start with the free diagnostic and a sample Proof Pack.",
      educational_resources:
        "Early stage — explore the free diagnostic and resources first.",
      request_cannot_proceed_as_described:
        "We can't proceed with this request as described.",
    },
    buckets: { low: "Low fit", medium: "Medium fit", high: "High fit", blocked: "Not a fit" },
    proofYes: "A sample Proof Pack can be prepared for you (founder-reviewed).",
    proofNo: "Tick the consent box to receive a sample Proof Pack.",
    proofBlocked: "Sample Proof Pack not available for this request.",
    reasonsTitle: "Why this score",
    errorRequired: "Please fill in name, company, and a valid work email.",
    errorGeneric: "Something went wrong. Please try again.",
    errorConsent: "Please agree to be contacted before submitting.",
    again: "Score another",
  },
  ar: {
    formTitle: "مؤشر مخاطر الذكاء الاصطناعي وعمليات الإيراد",
    formSubtitle:
      "فحص ذاتي قصير ومحدّد النتيجة. لا تُولَّد أي نتيجة من مدخلات فارغة.",
    name: "الاسم الكامل",
    company: "الشركة",
    email: "البريد المهني",
    role: "دورك",
    linkedin: "لينكدإن (اختياري)",
    sector: "القطاع",
    teamSize: "حجم الفريق",
    crm: "هل تستخدمون CRM؟",
    crmSystem: "أي CRM / نظام؟",
    aiUsage: "هل تستخدمون الذكاء الاصطناعي في الفريق اليوم؟",
    biggestPain: "أين أكبر ألم؟",
    consentExternal: "هل تشترطون موافقة قبل أي إجراء خارجي؟",
    linkValue: "هل تقدرون ربط workflow بقيمة مالية؟",
    budget: "نطاق الميزانية المتوقع",
    urgency: "درجة الاستعجال",
    consent: "أوافق على تواصل Dealix معي بخصوص هذا الطلب.",
    submit: "احسب مؤشر المخاطر",
    submitting: "جارٍ الحساب…",
    yes: "نعم",
    no: "لا",
    choose: "اختر…",
    pains: {
      pipeline: "خط الفرص / تدفق العملاء",
      crm: "جودة بيانات الـCRM",
      follow_up: "انضباط المتابعة",
      approvals: "الموافقات / الحوكمة",
      reporting: "التقارير / الوضوح",
    },
    urgencies: { low: "منخفض", medium: "متوسط", high: "عالٍ" },
    teamSizes: { "1-10": "1–10", "11-50": "11–50", "51-200": "51–200", "200+": "200+" },
    budgets: {
      none: "لا توجد ميزانية بعد",
      under_5000: "أقل من 5,000 ريال",
      "5000_25000": "5,000 – 25,000 ريال",
      "25000_plus": "أكثر من 25,000 ريال",
    },
    resultTitle: "مؤشر المخاطر الخاص بك",
    fitScore: "درجة الملاءمة",
    nextSteps: {
      book_diagnostic_review: "ملاءمة قوية — احجز Diagnostic Review مدفوع.",
      request_sample_proof_pack:
        "ملاءمة جزئية — ابدأ بالتشخيص المجاني وعيّنة Proof Pack.",
      educational_resources:
        "مرحلة مبكرة — استكشف التشخيص المجاني والموارد أولاً.",
      request_cannot_proceed_as_described:
        "لا يمكننا المتابعة مع هذا الطلب بصيغته الحالية.",
    },
    buckets: { low: "ملاءمة منخفضة", medium: "ملاءمة متوسطة", high: "ملاءمة عالية", blocked: "غير مناسب" },
    proofYes: "يمكن تجهيز عيّنة Proof Pack لك (بمراجعة المؤسس).",
    proofNo: "فعّل خانة الموافقة لاستلام عيّنة Proof Pack.",
    proofBlocked: "عيّنة Proof Pack غير متاحة لهذا الطلب.",
    reasonsTitle: "سبب هذه النتيجة",
    errorRequired: "يرجى تعبئة الاسم والشركة وبريد مهني صحيح.",
    errorGeneric: "حدث خطأ. يرجى المحاولة مرة أخرى.",
    errorConsent: "يرجى الموافقة على التواصل قبل الإرسال.",
    again: "احسب لطلب آخر",
  },
} as const;

const BUCKET_STYLES: Record<string, string> = {
  high: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  medium: "bg-amber-500/15 text-amber-400 border-amber-500/30",
  low: "bg-sky-500/15 text-sky-400 border-sky-500/30",
  blocked: "bg-red-500/15 text-red-400 border-red-500/30",
};

export function DiagnosticFunnel({ locale }: DiagnosticFunnelProps) {
  const isAr = locale === "ar";
  const t = isAr ? T.ar : T.en;

  const [form, setForm] = useState<FormState>(EMPTY_FORM);
  const [consent, setConsent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RiskScoreResult | null>(null);

  const set = (key: string) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => setForm((f) => ({ ...f, [key]: e.target.value }));

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!form.name.trim() || !form.company.trim() || !form.email.includes("@")) {
      setError(t.errorRequired);
      return;
    }
    if (!consent) {
      setError(t.errorConsent);
      return;
    }

    setSubmitting(true);
    try {
      const res = await api.submitRiskScore({ ...form, consent });
      setResult(res.data as RiskScoreResult);
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number } })?.response?.status;
      setError(status === 422 ? t.errorRequired : t.errorGeneric);
    } finally {
      setSubmitting(false);
    }
  }

  function reset() {
    setForm(EMPTY_FORM);
    setConsent(false);
    setResult(null);
    setError(null);
  }

  const inputCls =
    "w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:border-primary";
  const labelCls = "block text-sm font-medium text-foreground/90 mb-1.5";

  if (result) {
    const bucket = result.bucket ?? "low";
    const nextKey = (result.next_step ??
      "educational_resources") as keyof typeof t.nextSteps;
    const proof = result.sample_proof_pack;
    return (
      <div
        id="risk-score"
        className="rounded-2xl border border-border bg-card p-6 sm:p-8"
        dir={isAr ? "rtl" : "ltr"}
      >
        <h3 className="text-lg font-semibold text-foreground">{t.resultTitle}</h3>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <span
            className={`inline-flex items-center rounded-full border px-3 py-1 text-sm font-medium ${
              BUCKET_STYLES[bucket] ?? BUCKET_STYLES.low
            }`}
          >
            {t.buckets[bucket]}
          </span>
          <span className="text-sm text-muted-foreground">
            {t.fitScore}: <strong className="text-foreground">{result.fit_score ?? 0}</strong>/100
          </span>
        </div>

        <p className="mt-4 text-sm leading-relaxed text-foreground/90">
          {t.nextSteps[nextKey]}
        </p>

        <p className="mt-3 text-sm text-muted-foreground">
          {proof?.available
            ? t.proofYes
            : proof?.reason === "blocked"
              ? t.proofBlocked
              : t.proofNo}
        </p>

        {result.reasons && result.reasons.length > 0 && (
          <div className="mt-5">
            <p className="text-sm font-medium text-foreground/90">{t.reasonsTitle}</p>
            <ul className="mt-2 list-inside list-disc space-y-1 text-xs text-muted-foreground marker:text-primary">
              {result.reasons.map((r) => (
                <li key={r}>{r.replace(/_/g, " ")}</li>
              ))}
            </ul>
          </div>
        )}

        {result.disclaimer && (
          <p className="mt-6 text-xs text-muted-foreground">{result.disclaimer}</p>
        )}

        <button
          type="button"
          onClick={reset}
          className="mt-6 inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground transition hover:bg-muted"
        >
          {t.again}
        </button>
      </div>
    );
  }

  return (
    <form
      id="risk-score"
      onSubmit={handleSubmit}
      className="rounded-2xl border border-border bg-card p-6 sm:p-8"
      dir={isAr ? "rtl" : "ltr"}
    >
      <h3 className="text-lg font-semibold text-foreground">{t.formTitle}</h3>
      <p className="mt-1 text-sm text-muted-foreground">{t.formSubtitle}</p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className={labelCls}>{t.name} *</label>
          <input className={inputCls} value={form.name} onChange={set("name")} required />
        </div>
        <div>
          <label className={labelCls}>{t.company} *</label>
          <input className={inputCls} value={form.company} onChange={set("company")} required />
        </div>
        <div>
          <label className={labelCls}>{t.email} *</label>
          <input
            type="email"
            className={inputCls}
            value={form.email}
            onChange={set("email")}
            required
          />
        </div>
        <div>
          <label className={labelCls}>{t.role}</label>
          <input className={inputCls} value={form.role} onChange={set("role")} />
        </div>
        <div>
          <label className={labelCls}>{t.linkedin}</label>
          <input className={inputCls} value={form.linkedin} onChange={set("linkedin")} />
        </div>
        <div>
          <label className={labelCls}>{t.sector}</label>
          <input className={inputCls} value={form.sector} onChange={set("sector")} />
        </div>
        <div>
          <label className={labelCls}>{t.teamSize}</label>
          <select className={inputCls} value={form.team_size} onChange={set("team_size")}>
            <option value="">{t.choose}</option>
            {Object.entries(t.teamSizes).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.crm}</label>
          <select className={inputCls} value={form.crm} onChange={set("crm")}>
            <option value="">{t.choose}</option>
            <option value="yes">{t.yes}</option>
            <option value="no">{t.no}</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.crmSystem}</label>
          <input className={inputCls} value={form.crm_system} onChange={set("crm_system")} />
        </div>
        <div>
          <label className={labelCls}>{t.aiUsage}</label>
          <select className={inputCls} value={form.ai_usage} onChange={set("ai_usage")}>
            <option value="">{t.choose}</option>
            <option value="yes">{t.yes}</option>
            <option value="no">{t.no}</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.biggestPain}</label>
          <select className={inputCls} value={form.biggest_pain} onChange={set("biggest_pain")}>
            <option value="">{t.choose}</option>
            {Object.entries(t.pains).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.budget}</label>
          <select className={inputCls} value={form.budget_range} onChange={set("budget_range")}>
            <option value="">{t.choose}</option>
            {Object.entries(t.budgets).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.consentExternal}</label>
          <select
            className={inputCls}
            value={form.consent_before_external_action}
            onChange={set("consent_before_external_action")}
          >
            <option value="">{t.choose}</option>
            <option value="yes">{t.yes}</option>
            <option value="no">{t.no}</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.linkValue}</label>
          <select
            className={inputCls}
            value={form.can_link_workflow_to_value}
            onChange={set("can_link_workflow_to_value")}
          >
            <option value="">{t.choose}</option>
            <option value="yes">{t.yes}</option>
            <option value="no">{t.no}</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>{t.urgency}</label>
          <select className={inputCls} value={form.urgency} onChange={set("urgency")}>
            <option value="">{t.choose}</option>
            {Object.entries(t.urgencies).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Honeypot — hidden from real users, bots fill it. */}
      <input
        type="text"
        tabIndex={-1}
        autoComplete="off"
        className="absolute -left-[9999px] h-0 w-0 opacity-0"
        value={form.website}
        onChange={set("website")}
        aria-hidden="true"
      />

      <label className="mt-5 flex items-start gap-2 text-sm text-foreground/90">
        <input
          type="checkbox"
          className="mt-0.5"
          checked={consent}
          onChange={(e) => setConsent(e.target.checked)}
        />
        <span>{t.consent}</span>
      </label>

      {error && <p className="mt-3 text-sm text-red-400">{error}</p>}

      <button
        type="submit"
        disabled={submitting}
        className="mt-5 inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90 disabled:opacity-60"
      >
        {submitting ? t.submitting : t.submit}
      </button>
    </form>
  );
}
