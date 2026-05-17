"use client";

import { FormEvent, useMemo, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Copy = {
  eyebrow: string;
  title: string;
  subtitle: string;
  ctaPrimary: string;
  ctaSecondary: string;
  problemTitle: string;
  problemBody: string;
  whoTitle: string;
  whoList: string[];
  getTitle: string;
  getList: string[];
  outputsTitle: string;
  outputsList: string[];
  avoidTitle: string;
  avoidList: string[];
  pricingTitle: string;
  stageTitle: string;
  stageList: string[];
  automationTitle: string;
  automationList: string[];
  formTitle: string;
  formHint: string;
  contactHint: string;
  contactValidationError: string;
  nameLabel: string;
  companyLabel: string;
  emailLabel: string;
  phoneLabel: string;
  messageLabel: string;
  submitLabel: string;
  submittingLabel: string;
  successLabel: string;
  failureLabel: string;
};

const AR_COPY: Copy = {
  eyebrow: "Dealix Revenue Autopilot",
  title: "7-Day Governed Revenue & AI Ops Diagnostic",
  subtitle:
    "حوّل تجارب AI وعمليات الإيراد إلى workflows محكومة وقابلة للقياس: مصدر واضح، موافقة واضحة، دليل واضح، وقيمة قابلة للإثبات.",
  ctaPrimary: "Get Sample Proof Pack",
  ctaSecondary: "Book Diagnostic Review",
  problemTitle: "المشكلة",
  problemBody:
    "فشل الأتمتة غالباً ليس فشل نموذج؛ بل فشل تشغيل: مصدر غير واضح، حدود موافقة غير واضحة، وغياب evidence trail.",
  whoTitle: "لمن هذا التشخيص؟",
  whoList: [
    "فرق GCC التي تستخدم CRM أو revenue workflows وتريد حوكمة قبل التوسع.",
    "فرق بدأت AI/automation لكن لا تستطيع قياس أثر موثوق.",
    "فرق تريد قرار تنفيذي مدعوم بدليل خلال 7 أيام.",
  ],
  getTitle: "ماذا تحصل؟",
  getList: [
    "Workflow map + source quality review.",
    "Approval risk map + audit trail gaps.",
    "Top 3 governed decisions ready to execute with proof.",
    "Diagnostic scope + recommended sprint/retainer path.",
  ],
  outputsTitle: "Sample Outputs",
  outputsList: [
    "Sample Proof Pack",
    "AI & Revenue Ops Risk Score",
    "Diagnostic deck",
    "One-page offer",
    "Case-style demo (بدون ادعاء عميل حقيقي)",
  ],
  avoidTitle: "What we do not do",
  avoidList: [
    "لا نرسل رسائل AI خارجية بشكل ذاتي.",
    "لا ندّعي Revenue بدون evidence.",
    "لا نستبدل CRM الخاص بك.",
    "لا ننشر Case Study بدون موافقة صريحة.",
    "لا نبيع chatbot automation عامّة.",
  ],
  pricingTitle: "نطاق التسعير: Starter 4,999 SAR • Standard 9,999 SAR • Executive 15,000 SAR",
  stageTitle: "Lifecycle Stages (Dealix Operating Spine)",
  stageList: [
    "new_lead → qualified_A/B → meeting_booked → scope_sent",
    "invoice_sent → invoice_paid → delivery_started → proof_pack_sent",
    "sprint_candidate / retainer_candidate",
  ],
  automationTitle: "10 Automations (Autopilot + Copilot + Founder Approval)",
  automationList: [
    "Lead capture + score + stage assignment",
    "Qualified lead booking draft",
    "Proof pack request workflow",
    "Meeting booked brief generation",
    "Meeting done decision capture",
    "Scope requested draft + pricing recommendation",
    "Invoice paid onboarding kickoff",
    "Delivery checklist generation",
    "Proof pack sent upsell trigger",
    "Sprint/retainer upsell drafts",
  ],
  formTitle: "احصل على Sample Proof Pack",
  formHint: "النموذج يولّد lead داخل النظام بصيغة draft-first. لا يوجد إرسال خارجي آلي.",
  contactHint: "أدخل بريدًا إلكترونيًا صحيحًا أو رقم جوال واحدًا على الأقل.",
  contactValidationError: "الرجاء إدخال بريد صحيح أو رقم جوال صحيح.",
  nameLabel: "الاسم",
  companyLabel: "الشركة",
  emailLabel: "البريد الإلكتروني",
  phoneLabel: "رقم الجوال",
  messageLabel: "ما workflow الذي تريد مراجعته أولاً؟",
  submitLabel: "إرسال الطلب",
  submittingLabel: "جارٍ الإرسال...",
  successLabel: "تم إنشاء الطلب بنجاح. الخطوة التالية: مراجعة المؤسس وإرسال Sample Proof Pack كمسودة معتمدة.",
  failureLabel: "تعذر إرسال الطلب حالياً. حاول مرة أخرى.",
};

const EN_COPY: Copy = {
  eyebrow: "Dealix Revenue Autopilot",
  title: "7-Day Governed Revenue & AI Ops Diagnostic",
  subtitle:
    "Turn AI experiments and revenue operations into governed, measurable workflows with source clarity, approval boundaries, evidence trails, and proof of value.",
  ctaPrimary: "Get Sample Proof Pack",
  ctaSecondary: "Book Diagnostic Review",
  problemTitle: "The problem",
  problemBody:
    "Most automation failures are operating failures: unclear sources, weak approval boundaries, and missing evidence trails.",
  whoTitle: "Who this is for",
  whoList: [
    "GCC teams using CRM or revenue workflows that need governance before scaling.",
    "Teams running AI/automation experiments without measurable impact evidence.",
    "Leaders who want 3 actionable decisions with proof in 7 days.",
  ],
  getTitle: "What you get",
  getList: [
    "Workflow map + source quality review.",
    "Approval risk map + audit trail gaps.",
    "Top 3 governed decisions ready to execute with proof.",
    "Diagnostic scope + recommended sprint/retainer path.",
  ],
  outputsTitle: "Sample outputs",
  outputsList: [
    "Sample Proof Pack",
    "AI & Revenue Ops Risk Score",
    "Diagnostic deck",
    "One-page offer",
    "Case-style demo (no fake client claims)",
  ],
  avoidTitle: "What we do not do",
  avoidList: [
    "We do not send autonomous AI messages.",
    "We do not claim revenue without evidence.",
    "We do not replace your CRM.",
    "We do not publish case studies without approval.",
    "We do not sell generic chatbot automation.",
  ],
  pricingTitle: "Pricing range: Starter 4,999 SAR • Standard 9,999 SAR • Executive 15,000 SAR",
  stageTitle: "Lifecycle stages (Dealix operating spine)",
  stageList: [
    "new_lead → qualified_A/B → meeting_booked → scope_sent",
    "invoice_sent → invoice_paid → delivery_started → proof_pack_sent",
    "sprint_candidate / retainer_candidate",
  ],
  automationTitle: "10 automations (Autopilot + Copilot + Founder approval)",
  automationList: [
    "Lead capture + score + stage assignment",
    "Qualified lead booking draft",
    "Proof pack request workflow",
    "Meeting booked brief generation",
    "Meeting done decision capture",
    "Scope requested draft + pricing recommendation",
    "Invoice paid onboarding kickoff",
    "Delivery checklist generation",
    "Proof pack sent upsell trigger",
    "Sprint/retainer upsell drafts",
  ],
  formTitle: "Get Sample Proof Pack",
  formHint: "This form creates a lead in draft-first mode. No autonomous external send.",
  contactHint: "Provide at least one valid contact method: email or phone.",
  contactValidationError: "Please enter a valid email address or phone number.",
  nameLabel: "Name",
  companyLabel: "Company",
  emailLabel: "Email",
  phoneLabel: "Phone",
  messageLabel: "Which workflow do you want reviewed first?",
  submitLabel: "Submit request",
  submittingLabel: "Submitting...",
  successLabel: "Request created. Next step: founder review and approved sample-proof-pack draft.",
  failureLabel: "Could not submit right now. Please retry.",
};

export default function DealixDiagnosticPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const copy = useMemo(() => (isAr ? AR_COPY : EN_COPY), [isAr]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(false);
  const [contactError, setContactError] = useState(false);
  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    message: "",
  });

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setSuccess(false);
    setError(false);
    setContactError(false);
    try {
      let email = form.email.trim();
      let phone = form.phone.trim();
      // Handle accidental swap between email/phone fields in RTL layouts.
      if (!email.includes("@") && phone.includes("@")) {
        const swapped = email;
        email = phone;
        phone = swapped;
      }
      const hasEmail = email.length > 0;
      const hasPhone = phone.length > 0;
      const emailValid = !hasEmail || email.includes("@");
      if ((!hasEmail && !hasPhone) || !emailValid) {
        setContactError(true);
        setLoading(false);
        return;
      }
      await api.submitLead({
        company: form.company,
        name: form.name,
        email: hasEmail ? email : null,
        phone: hasPhone ? phone : null,
        region: "Saudi Arabia",
        sector: "governed_revenue_ai_ops",
        budget: 5000,
        message: form.message,
        source: "dealix_diagnostic_proof_pack_gate",
        lead_magnet: "sample_proof_pack",
        preferred_offer: "7_day_governed_revenue_ai_ops_diagnostic",
      });
      setSuccess(true);
      setForm({ name: "", company: "", email: "", phone: "", message: "" });
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-5xl px-6 py-12" dir={isAr ? "rtl" : "ltr"}>
        <p className="text-sm font-medium text-muted-foreground">{copy.eyebrow}</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">{copy.title}</h1>
        <p className="mt-4 max-w-3xl text-muted-foreground leading-relaxed">{copy.subtitle}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <a
            href="#proof-pack-form"
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            {copy.ctaPrimary}
          </a>
          <Link
            href={`/${locale}/offer/lead-intelligence-sprint`}
            className="inline-flex items-center justify-center rounded-lg border border-border bg-card px-5 py-2.5 text-sm font-medium text-foreground transition hover:bg-muted/60"
          >
            {copy.ctaSecondary}
          </Link>
        </div>

        <section className="mt-10 rounded-xl border border-border bg-card/30 p-6">
          <h2 className="text-lg font-semibold text-foreground">{copy.problemTitle}</h2>
          <p className="mt-2 text-muted-foreground">{copy.problemBody}</p>
        </section>

        <section className="mt-6 grid gap-6 md:grid-cols-2">
          <div className="rounded-xl border border-border bg-card/30 p-6">
            <h3 className="text-base font-semibold text-foreground">{copy.whoTitle}</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              {copy.whoList.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-xl border border-border bg-card/30 p-6">
            <h3 className="text-base font-semibold text-foreground">{copy.getTitle}</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              {copy.getList.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
        </section>

        <section className="mt-6 grid gap-6 md:grid-cols-2">
          <div className="rounded-xl border border-border bg-card/30 p-6">
            <h3 className="text-base font-semibold text-foreground">{copy.outputsTitle}</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              {copy.outputsList.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-xl border border-border bg-card/30 p-6">
            <h3 className="text-base font-semibold text-foreground">{copy.avoidTitle}</h3>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              {copy.avoidList.map((item) => (
                <li key={item}>• {item}</li>
              ))}
            </ul>
          </div>
        </section>

        <section className="mt-6 rounded-xl border border-border bg-card/30 p-6">
          <p className="text-sm font-medium text-foreground">{copy.pricingTitle}</p>
          <h3 className="mt-4 text-base font-semibold text-foreground">{copy.stageTitle}</h3>
          <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
            {copy.stageList.map((item) => (
              <li key={item}>• {item}</li>
            ))}
          </ul>
          <h3 className="mt-5 text-base font-semibold text-foreground">{copy.automationTitle}</h3>
          <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
            {copy.automationList.map((item) => (
              <li key={item}>• {item}</li>
            ))}
          </ul>
        </section>

        <section id="proof-pack-form" className="mt-8 rounded-xl border border-gold-500/30 bg-card p-6">
          <h2 className="text-xl font-semibold text-foreground">{copy.formTitle}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{copy.formHint}</p>

          <form onSubmit={onSubmit} className="mt-5 space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm text-muted-foreground">{copy.nameLabel}</label>
                <Input
                  value={form.name}
                  onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm text-muted-foreground">{copy.companyLabel}</label>
                <Input
                  value={form.company}
                  onChange={(event) => setForm((prev) => ({ ...prev, company: event.target.value }))}
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm text-muted-foreground">{copy.emailLabel}</label>
                <Input
                  type="text"
                  placeholder="name@company.com"
                  dir="ltr"
                  value={form.email}
                  onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
                />
              </div>
              <div>
                <label className="mb-1 block text-sm text-muted-foreground">{copy.phoneLabel}</label>
                <Input
                  type="tel"
                  placeholder="+9665XXXXXXXX"
                  dir="ltr"
                  value={form.phone}
                  onChange={(event) => setForm((prev) => ({ ...prev, phone: event.target.value }))}
                />
              </div>
            </div>
            <p className="text-xs text-muted-foreground">{copy.contactHint}</p>
            <div>
              <label className="mb-1 block text-sm text-muted-foreground">{copy.messageLabel}</label>
              <textarea
                value={form.message}
                onChange={(event) => setForm((prev) => ({ ...prev, message: event.target.value }))}
                required
                className="min-h-28 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            <Button type="submit" disabled={loading}>
              {loading ? copy.submittingLabel : copy.submitLabel}
            </Button>
          </form>

          {success && <p className="mt-4 text-sm text-emerald-500">{copy.successLabel}</p>}
          {contactError && <p className="mt-4 text-sm text-destructive">{copy.contactValidationError}</p>}
          {error && <p className="mt-4 text-sm text-destructive">{copy.failureLabel}</p>}
        </section>
      </div>
    </div>
  );
}
