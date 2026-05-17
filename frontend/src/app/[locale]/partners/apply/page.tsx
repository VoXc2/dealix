"use client";

import { useParams } from "next/navigation";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const COPY = {
  en: {
    dir: "ltr" as const,
    kicker: "Dealix — Affiliate & Partner Program",
    title: "Become a Dealix Partner",
    intro:
      "Refer founders and revenue teams to Dealix and earn a cash commission — paid only after the referred customer's invoice is paid.",
    name: "Your name / company",
    email: "Email",
    category: "Partner type",
    audience: "Audience type (e.g. B2B founders)",
    region: "Region",
    plan: "How will you promote Dealix?",
    signalsTitle: "Tell us about your audience",
    b2b: "My audience is mostly B2B",
    gcc: "My audience is mostly in the GCC",
    prior: "I have referred B2B partners before",
    content: "I publish regular content (newsletter / posts / podcast)",
    disclosure:
      "I agree to disclose my referral relationship on every promotion, use only Dealix-approved messaging, and never use cold outreach or spam.",
    submit: "Submit application",
    okTitle: "Application received",
    okBody:
      "Your application is under review. If approved you'll receive a referral link and the approved-messaging pack.",
    score: "Preliminary score",
    tier: "Recommended tier",
    terms: "No commission on unqualified or duplicate leads. Commission is paid only after a referred invoice is paid; refunds within 30 days are clawed back.",
    required: "Please complete the required fields and accept the disclosure terms.",
  },
  ar: {
    dir: "rtl" as const,
    kicker: "Dealix — برنامج الشركاء والمسوقين بالعمولة",
    title: "كن شريكاً في Dealix",
    intro:
      "أحِل المؤسسين وفِرق الإيراد إلى Dealix واكسب عمولة نقدية — تُدفع فقط بعد سداد فاتورة العميل المُحال.",
    name: "اسمك / شركتك",
    email: "البريد الإلكتروني",
    category: "نوع الشريك",
    audience: "نوع الجمهور (مثال: مؤسسو B2B)",
    region: "المنطقة",
    plan: "كيف ستروّج لـ Dealix؟",
    signalsTitle: "أخبرنا عن جمهورك",
    b2b: "جمهوري في معظمه B2B",
    gcc: "جمهوري في معظمه في الخليج",
    prior: "سبق أن أحَلْت شركاء B2B",
    content: "أنشر محتوى منتظماً (نشرة / منشورات / بودكاست)",
    disclosure:
      "أوافق على الإفصاح عن علاقة الإحالة في كل ترويج، واستخدام الرسائل المعتمدة من Dealix فقط، وعدم استخدام التواصل البارد أو الإزعاج.",
    submit: "إرسال الطلب",
    okTitle: "تم استلام الطلب",
    okBody:
      "طلبك قيد المراجعة. عند القبول ستصلك رابط الإحالة وحزمة الرسائل المعتمدة.",
    score: "التقييم المبدئي",
    tier: "المستوى المقترح",
    terms: "لا عمولة على العملاء غير المؤهلين أو المكررين. تُدفع العمولة فقط بعد سداد الفاتورة المُحالة، وتُسترد عند استرجاع المبلغ خلال 30 يوماً.",
    required: "يرجى إكمال الحقول المطلوبة والموافقة على شروط الإفصاح.",
  },
};

const CATEGORIES = [
  "consultant",
  "creator",
  "agency",
  "implementer",
  "community",
  "newsletter",
  "podcast",
  "vc_accelerator",
  "other",
];

interface ApplyResult {
  partner_id: string;
  score: number;
  recommended_tier: string;
}

export default function PartnerApplyPage() {
  const params = useParams();
  const locale = params?.locale === "ar" ? "ar" : "en";
  const t = COPY[locale];

  const [form, setForm] = useState({
    display_name: "",
    email: "",
    partner_category: "consultant",
    audience_type: "",
    region: "",
    plan_text: "",
  });
  const [signals, setSignals] = useState({
    audience_is_b2b: false,
    audience_is_gcc: false,
    has_prior_referrals: false,
    content_quality_good: false,
  });
  const [disclosure, setDisclosure] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<ApplyResult | null>(null);

  const submit = async () => {
    setError("");
    if (!form.display_name.trim() || !form.email.trim() || !disclosure) {
      setError(t.required);
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/affiliates/apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          disclosure_accepted: disclosure,
          signals,
        }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `HTTP ${res.status}`);
      }
      setResult((await res.json()) as ApplyResult);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setSubmitting(false);
    }
  };

  const field =
    "mt-1 w-full rounded-lg border border-border bg-background px-3 py-2 text-sm";

  if (result) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div
          className="mx-auto max-w-2xl px-6 py-20"
          dir={t.dir}
        >
          <h1 className="text-2xl font-bold text-foreground">{t.okTitle}</h1>
          <p className="mt-3 text-foreground/90">{t.okBody}</p>
          <div className="mt-6 rounded-xl border border-border bg-muted/40 p-4 text-sm">
            <p>
              {t.score}: <strong>{result.score}</strong>
            </p>
            <p>
              {t.tier}: <strong>{result.recommended_tier}</strong>
            </p>
            <p className="mt-2 text-xs text-muted-foreground">
              partner_id: <code>{result.partner_id}</code>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-2xl px-6 py-16" dir={t.dir}>
        <p className="text-sm font-medium text-muted-foreground">{t.kicker}</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
          {t.title}
        </h1>
        <p className="mt-2 text-base leading-relaxed text-foreground/90">
          {t.intro}
        </p>

        <div className="mt-8 space-y-4">
          <label className="block text-sm font-medium text-foreground">
            {t.name}
            <input
              className={field}
              value={form.display_name}
              onChange={(e) =>
                setForm({ ...form, display_name: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-medium text-foreground">
            {t.email}
            <input
              className={field}
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>
          <label className="block text-sm font-medium text-foreground">
            {t.category}
            <select
              className={field}
              value={form.partner_category}
              onChange={(e) =>
                setForm({ ...form, partner_category: e.target.value })
              }
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-medium text-foreground">
            {t.audience}
            <input
              className={field}
              value={form.audience_type}
              onChange={(e) =>
                setForm({ ...form, audience_type: e.target.value })
              }
            />
          </label>
          <label className="block text-sm font-medium text-foreground">
            {t.region}
            <input
              className={field}
              value={form.region}
              onChange={(e) => setForm({ ...form, region: e.target.value })}
            />
          </label>
          <label className="block text-sm font-medium text-foreground">
            {t.plan}
            <textarea
              className={field}
              rows={3}
              value={form.plan_text}
              onChange={(e) =>
                setForm({ ...form, plan_text: e.target.value })
              }
            />
          </label>

          <fieldset className="rounded-xl border border-border p-4">
            <legend className="px-1 text-sm font-semibold text-foreground">
              {t.signalsTitle}
            </legend>
            {(
              [
                ["audience_is_b2b", t.b2b],
                ["audience_is_gcc", t.gcc],
                ["has_prior_referrals", t.prior],
                ["content_quality_good", t.content],
              ] as const
            ).map(([key, label]) => (
              <label
                key={key}
                className="mt-2 flex items-center gap-2 text-sm text-foreground/90"
              >
                <input
                  type="checkbox"
                  checked={signals[key]}
                  onChange={(e) =>
                    setSignals({ ...signals, [key]: e.target.checked })
                  }
                />
                {label}
              </label>
            ))}
          </fieldset>

          <label className="flex items-start gap-2 text-sm text-foreground/90">
            <input
              type="checkbox"
              className="mt-1"
              checked={disclosure}
              onChange={(e) => setDisclosure(e.target.checked)}
            />
            <span>{t.disclosure}</span>
          </label>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <button
            type="button"
            onClick={() => void submit()}
            disabled={submitting}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90 disabled:opacity-50"
          >
            {t.submit}
          </button>

          <p className="pt-2 text-xs text-muted-foreground">{t.terms}</p>
        </div>
      </div>
    </div>
  );
}
