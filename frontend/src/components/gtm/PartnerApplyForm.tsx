"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const PARTNER_TYPES_AR = [
  {
    id: "referral",
    icon: "🤝",
    label: "Referral Partner",
    desc: "تُحضر العميل، Dealix يُنفّذ — عمولة 15-20% على أول دفعة.",
    features: ["لا متطلبات تقنية", "عمولة عند تأكيد الدفع", "مواد تسويقية من Dealix"],
    commission: "15-20%",
  },
  {
    id: "implementation",
    icon: "⚙️",
    label: "Implementation Partner",
    desc: "تُنفّذ مع Dealix — وكالة تقنية أو استشارية تريد إضافة خدمة Revenue Ops.",
    features: ["تدريب على منهجية Dealix", "عمولة أعلى على Retainer", "Co-sell مشترك", "Proof Pack باسم الشريك"],
    commission: "20-30%",
  },
  {
    id: "co_sell",
    icon: "🚀",
    label: "Co-sell Pilot",
    desc: "عميل مشترك — نبني معاً ونتقاسم المخرجات. مثالي للتجربة قبل الشراكة الرسمية.",
    features: ["عميل واحد مشترك", "Proof Pack مشترك", "قرار الشراكة بعد النتائج"],
    commission: "حسب الاتفاق",
  },
];

const PARTNER_TYPES_EN = [
  {
    id: "referral",
    icon: "🤝",
    label: "Referral Partner",
    desc: "You bring the client, Dealix executes — 15-20% commission on first payment.",
    features: ["No technical requirements", "Commission on payment confirmation", "Marketing materials from Dealix"],
    commission: "15-20%",
  },
  {
    id: "implementation",
    icon: "⚙️",
    label: "Implementation Partner",
    desc: "You co-deliver with Dealix — tech or consulting agency adding Revenue Ops service.",
    features: ["Training on Dealix methodology", "Higher retainer commission", "Joint co-sell", "Proof Pack co-branded"],
    commission: "20-30%",
  },
  {
    id: "co_sell",
    icon: "🚀",
    label: "Co-sell Pilot",
    desc: "One shared client — we build together and share outcomes. Ideal before formal partnership.",
    features: ["One shared client", "Joint Proof Pack", "Partnership decision after results"],
    commission: "By agreement",
  },
];

const WHY_PARTNER_AR = [
  { icon: "💰", title: "إيراد إضافي", desc: "عمولة على كل تشخيص وRetainer تُحضره" },
  { icon: "🛡️", title: "حوكمة حقيقية", desc: "تقدّم لعملائك خدمة PDPL-compliant جاهزة" },
  { icon: "📦", title: "Proof Pack جاهز", desc: "مادة تسليم احترافية لعملائك بدون بناء من صفر" },
  { icon: "🤝", title: "موافقة قبل أي إرسال", desc: "لا مخاطر على علاقتك مع العميل — كل خطوة موافَق عليها" },
];

const WHY_PARTNER_EN = [
  { icon: "💰", title: "Additional Revenue", desc: "Commission on every diagnostic and retainer you bring" },
  { icon: "🛡️", title: "Real Governance", desc: "Offer clients a PDPL-compliant ready service" },
  { icon: "📦", title: "Ready Proof Pack", desc: "Professional delivery material for clients without building from scratch" },
  { icon: "🤝", title: "Approval Before Any Send", desc: "No risk to your client relationship — every step is approved" },
];

export function PartnerApplyForm() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const partnerTypes = isAr ? PARTNER_TYPES_AR : PARTNER_TYPES_EN;
  const whyPartner = isAr ? WHY_PARTNER_AR : WHY_PARTNER_EN;

  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    partner_type: "referral",
    message: "",
    consent: false,
  });
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة." : "Consent required.");
      return;
    }
    setBusy(true);
    setStatus("");
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${base}/api/v1/public/partner-apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "failed");
      setSubmitted(true);
      setStatus(isAr ? `تم الاستلام — ${data.lead_id}. سنتواصل خلال 48 ساعة.` : `Received — ${data.lead_id}. We'll contact you within 48 hours.`);
    } catch {
      setStatus(isAr ? "تعذّر الإرسال — تحقق من الاتصال وحاول مجدداً." : "Submit failed — check connection and try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`space-y-14 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>

      {/* Hero */}
      <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
        <Badge className="mb-4 bg-amber-500/20 text-amber-300 border-amber-500/30">
          {isAr ? "برنامج الشركاء — Dealix" : "Partner Program — Dealix"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight">
          {isAr ? "Dealix يُشخّص · أنت تُنفّذ · العميل يحصل على إثبات" : "Dealix diagnoses · You implement · Client gets proof"}
        </h1>
        <p className="mt-4 text-white/70 max-w-xl leading-relaxed">
          {isAr
            ? "برنامج شركاء مبني على الأدلة — لا وعود فارغة. كل شراكة تبدأ بـ Proof Pack وتنمو من الإثبات."
            : "Evidence-based partner program — no empty promises. Every partnership starts with a Proof Pack and grows from proof."}
        </p>
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { ar: "15-30%", en: "15-30%", labelAr: "عمولة", labelEn: "Commission" },
            { ar: "48 ساعة", en: "48 hours", labelAr: "رد أولي", labelEn: "Initial response" },
            { ar: "PDPL", en: "PDPL", labelAr: "امتثال", labelEn: "Compliant" },
            { ar: "موافقة", en: "Approval", labelAr: "قبل كل خطوة", labelEn: "Before every step" },
          ].map((m) => (
            <div key={m.en} className="rounded-xl bg-white/5 border border-white/10 p-3 text-center">
              <p className="text-lg font-bold text-amber-300">{isAr ? m.ar : m.en}</p>
              <p className="text-xs text-white/50 mt-0.5">{isAr ? m.labelAr : m.labelEn}</p>
            </div>
          ))}
        </div>
      </header>

      {/* Why Partner */}
      <section>
        <h2 className="text-2xl font-bold mb-6">
          {isAr ? "لماذا الشراكة مع Dealix؟" : "Why Partner with Dealix?"}
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {whyPartner.map((w) => (
            <div key={w.title} className="flex items-start gap-4 rounded-xl border border-border/60 bg-card/50 p-5">
              <span className="text-3xl flex-shrink-0">{w.icon}</span>
              <div>
                <p className="font-semibold">{w.title}</p>
                <p className="text-sm text-muted-foreground mt-1">{w.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Partner Tiers */}
      <section>
        <h2 className="text-2xl font-bold mb-2">
          {isAr ? "أنواع الشراكة" : "Partnership Types"}
        </h2>
        <p className="text-muted-foreground mb-6">
          {isAr ? "اختر النوع المناسب لطبيعة عملك وعلاقتك بالعملاء." : "Choose the type that fits your business model and client relationships."}
        </p>
        <div className="grid gap-5 sm:grid-cols-3">
          {partnerTypes.map((type) => (
            <Card
              key={type.id}
              className={`p-6 cursor-pointer transition-all border-2 ${
                form.partner_type === type.id
                  ? "border-[#001F3F] dark:border-amber-500 shadow-md bg-primary/5"
                  : "border-border/40 bg-card/50 hover:border-border"
              }`}
              onClick={() => setForm((f) => ({ ...f, partner_type: type.id }))}
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">{type.icon}</span>
                <p className="font-semibold">{type.label}</p>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed mb-4">{type.desc}</p>
              <ul className="space-y-1 mb-4">
                {type.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="text-emerald-500 flex-shrink-0">✓</span>
                    {f}
                  </li>
                ))}
              </ul>
              <div className="rounded-lg bg-muted/40 px-3 py-2 text-center">
                <p className="text-xs text-muted-foreground">{isAr ? "العمولة" : "Commission"}</p>
                <p className="font-bold text-sm text-[#001F3F] dark:text-amber-400">{type.commission}</p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section>
        <h2 className="text-2xl font-bold mb-6">
          {isAr ? "كيف تعمل الشراكة" : "How Partnership Works"}
        </h2>
        <div className="grid gap-4 sm:grid-cols-4">
          {(isAr ? [
            { n: "١", t: "تقدّم للبرنامج", d: "ملء النموذج أدناه — مراجعة يدوية خلال 48 ساعة" },
            { n: "٢", t: "تعريف ومواد", d: "تدريب على المنهجية ومواد تسويقية" },
            { n: "٣", t: "أول عميل مشترك", d: "Diagnostic مشترك وProof Pack" },
            { n: "٤", t: "عمولة وتوسع", d: "عمولة فور تأكيد الدفع، توسع تدريجي" },
          ] : [
            { n: "1", t: "Apply to Program", d: "Fill the form below — manual review within 48 hours" },
            { n: "2", t: "Onboarding & Materials", d: "Methodology training and marketing materials" },
            { n: "3", t: "First Joint Client", d: "Joint Diagnostic and Proof Pack" },
            { n: "4", t: "Commission & Expand", d: "Commission on payment confirmation, gradual expansion" },
          ]).map((s) => (
            <div key={s.n} className="flex flex-col items-center text-center p-5 rounded-xl border border-border/60 bg-card/50">
              <div className="w-10 h-10 rounded-full bg-[#001F3F] text-white flex items-center justify-center font-bold text-sm mb-3">{s.n}</div>
              <p className="font-semibold text-sm">{s.t}</p>
              <p className="text-xs text-muted-foreground mt-1">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Application Form */}
      <section>
        <h2 className="text-2xl font-bold mb-2">
          {isAr ? "التقدّم للبرنامج" : "Apply to the Program"}
        </h2>
        <p className="text-muted-foreground mb-6 text-sm">
          {isAr
            ? "مراجعة يدوية من المؤسس — لا أتمتة. كل طلب يُدرس بجدية."
            : "Manual review by the founder — no automation. Every application is reviewed seriously."}
        </p>

        {submitted ? (
          <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20">
            <div className="text-4xl mb-3">✅</div>
            <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
              {isAr ? "تم الاستلام!" : "Received!"}
            </h3>
            <p className="text-muted-foreground mt-2">{status}</p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button asChild variant="outline">
                <Link href={`/${locale}/proof-pack`}>
                  {isAr ? "شاهد عيّنة Proof Pack" : "View Proof Pack Sample"}
                </Link>
              </Button>
              <Button asChild variant="outline">
                <Link href={`/${locale}/learn`}>
                  {isAr ? "تعلّم عن المنهجية" : "Learn the Methodology"}
                </Link>
              </Button>
            </div>
          </Card>
        ) : (
          <form onSubmit={submit} className="max-w-lg space-y-5">
            {([
              ["name", isAr ? "الاسم الكامل *" : "Full Name *", "text", true],
              ["email", isAr ? "البريد الإلكتروني *" : "Email Address *", "email", true],
              ["company", isAr ? "اسم الشركة / الوكالة" : "Company / Agency Name", "text", false],
            ] as const).map(([k, label, type, required]) => (
              <div key={k}>
                <Label htmlFor={k} className="text-sm font-medium">{label}</Label>
                <Input
                  id={k}
                  type={type}
                  required={required}
                  value={form[k as keyof typeof form] as string}
                  onChange={(e) => setForm((f) => ({ ...f, [k]: e.target.value }))}
                  className="mt-1"
                />
              </div>
            ))}

            <div>
              <Label className="text-sm font-medium">{isAr ? "نوع الشراكة *" : "Partnership Type *"}</Label>
              <div className="mt-2 grid gap-2">
                {partnerTypes.map((type) => (
                  <label key={type.id} className={`flex items-center gap-3 rounded-lg border p-3 cursor-pointer transition-colors ${form.partner_type === type.id ? "border-primary bg-primary/5" : "border-border/50 hover:bg-muted/20"}`}>
                    <input
                      type="radio"
                      name="partner_type"
                      value={type.id}
                      checked={form.partner_type === type.id}
                      onChange={() => setForm((f) => ({ ...f, partner_type: type.id }))}
                      className="accent-primary"
                    />
                    <span>{type.icon}</span>
                    <div>
                      <p className="text-sm font-medium">{type.label}</p>
                      <p className="text-xs text-muted-foreground">{isAr ? "عمولة:" : "Commission:"} {type.commission}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <Label htmlFor="message" className="text-sm font-medium">
                {isAr ? "رسالة مختصرة (اختياري)" : "Brief message (optional)"}
              </Label>
              <textarea
                id="message"
                rows={3}
                value={form.message}
                onChange={(e) => setForm((f) => ({ ...f, message: e.target.value }))}
                className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder={isAr ? "مثال: وكالة تسويق، لدينا 5 عملاء B2B يحتاجون Revenue Ops..." : "e.g. Marketing agency, we have 5 B2B clients needing Revenue Ops..."}
              />
            </div>

            <label className="flex items-start gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={form.consent}
                onChange={(e) => setForm((f) => ({ ...f, consent: e.target.checked }))}
                className="mt-0.5 accent-primary"
              />
              <span>
                {isAr
                  ? "أوافق على مراجعة الطلب يدوياً والتواصل للمتابعة. لا outreach بارد آلي."
                  : "I consent to manual application review and follow-up contact. No automated cold outreach."}
              </span>
            </label>

            <Button type="submit" disabled={busy} size="lg" className="w-full">
              {busy
                ? (isAr ? "جاري الإرسال..." : "Submitting...")
                : (isAr ? "أرسل طلب الشراكة" : "Submit Partner Application")}
            </Button>

            {status && !submitted && (
              <p className="text-sm text-destructive">{status}</p>
            )}

            <p className="text-xs text-muted-foreground">
              {isAr
                ? "سيتم مراجعة طلبك يدوياً خلال 48 ساعة. لا إرسال آلي لأي شريك بدون موافقة."
                : "Your application will be reviewed manually within 48 hours. No automated sending to any partner without approval."}
            </p>
          </form>
        )}
      </section>

      {/* Non-negotiables */}
      <section className="rounded-xl border border-border/60 bg-muted/20 p-6">
        <h2 className="font-semibold mb-4">
          {isAr ? "مبادئ الشراكة غير القابلة للتفاوض" : "Non-negotiable Partnership Principles"}
        </h2>
        <ul className="space-y-2">
          {(isAr ? [
            "لا cold WhatsApp أو LinkedIn automation على العملاء",
            "لا scraping ولا شراء قوائم leads",
            "كل إرسال خارجي يمر بموافقة بشرية من Dealix",
            "لا upsell بدون Proof Pack مُسلَّم",
            "العمولة تُحسب فقط عند تأكيد الدفع الفعلي",
          ] : [
            "No cold WhatsApp or LinkedIn automation to clients",
            "No scraping or buying lead lists",
            "Every external send requires human approval from Dealix",
            "No upsell without delivered Proof Pack",
            "Commission calculated only on confirmed actual payment",
          ]).map((item) => (
            <li key={item} className="flex items-start gap-2 text-sm">
              <span className="text-[#001F3F] dark:text-amber-400 mt-0.5 flex-shrink-0">✓</span>
              {item}
            </li>
          ))}
        </ul>
      </section>

    </div>
  );
}
