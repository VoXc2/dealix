"use client";

import { FormEvent, useMemo, useState } from "react";

import CTA from "@/components/CTA";
import PageShell from "@/components/PageShell";

const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";
const founderPhone = process.env.NEXT_PUBLIC_FOUNDER_PHONE?.trim() || "+966 59 778 8539";
const whatsappUrl = process.env.NEXT_PUBLIC_WHATSAPP_URL?.trim();

type DiagnosticResponse = {
  status?: string;
  intake_id?: string;
  workflow_state?: string;
  problem_state?: string;
  evidence_completeness_pct?: number;
  next_questions?: string[];
  agent_handoff?: { agents?: string[]; work_packets_created?: number };
  external_action?: string;
  message?: string;
};

const fieldStyle = {
  width: "100%",
  border: "1px solid rgba(255,255,255,0.14)",
  borderRadius: 12,
  background: "rgba(255,255,255,0.035)",
  color: "inherit",
  padding: "12px 14px",
  font: "inherit",
} as const;

const labelStyle = {
  display: "grid",
  gap: 8,
  fontSize: "0.92rem",
  fontWeight: 650,
} as const;

export default function BookPage() {
  const emailHref = `mailto:${founderEmail}?subject=${encodeURIComponent("طلب Free Execution Diagnostic — Dealix")}`;
  const telHref = `tel:${founderPhone.replace(/[^+\d]/g, "")}`;

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<DiagnosticResponse | null>(null);

  const statusText = useMemo(() => {
    if (!result) return "";
    const pct = typeof result.evidence_completeness_pct === "number" ? `${result.evidence_completeness_pct}%` : "—";
    return `تم إنشاء Intake داخلي. اكتمال الأدلة الأولي: ${pct}.`;
  }, [result]);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setResult(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") || ""),
      email: String(form.get("email") || ""),
      phone: String(form.get("phone") || ""),
      company: String(form.get("company") || ""),
      role: String(form.get("role") || ""),
      sector: String(form.get("sector") || "other"),
      website: String(form.get("website") || ""),
      workflow: String(form.get("workflow") || ""),
      decision_owner: String(form.get("decision_owner") || ""),
      tools_data: String(form.get("tools_data") || ""),
      business_impact: String(form.get("business_impact") || ""),
      proof_metric: String(form.get("proof_metric") || ""),
      baseline: String(form.get("baseline") || ""),
      target_outcome: String(form.get("target_outcome") || ""),
      urgency: String(form.get("urgency") || ""),
      preferred_contact: String(form.get("preferred_contact") || "email"),
      followup_requested: form.get("followup_requested") === "on",
      language_preference: "ar_en",
    };

    try {
      const response = await fetch("/api/v1/public/execution-diagnostic", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const body = (await response.json().catch(() => ({}))) as DiagnosticResponse & { detail?: unknown };
      if (!response.ok) {
        throw new Error(typeof body.detail === "string" ? body.detail : "تعذر استلام التشخيص الآن. حاول مرة أخرى.");
      }
      setResult(body);
      event.currentTarget.reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : "تعذر استلام التشخيص الآن. حاول مرة أخرى.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <PageShell>
      <section
        className="card dot-pattern"
        style={{
          position: "relative",
          overflow: "hidden",
          paddingTop: "clamp(40px,6vw,72px)",
          paddingBottom: "clamp(40px,6vw,72px)",
        }}
      >
        <p className="eyebrow">Free Execution Diagnostic</p>
        <h1 style={{ maxWidth: 860 }}>ابدأ بمشكلة تنفيذ واحدة — والتشخيص الأولي علينا</h1>
        <p style={{ maxWidth: 760, fontSize: "1.15rem", lineHeight: 1.7 }}>
          اشرح لنا workflow أو قرارًا تشغيليًا مهمًا. عند الإرسال ننشئ فورًا Intake داخليًا ونوزع
          work packets على شبكة Dealix الوكيلة المحكومة، مع توجيهها ديناميكيًا إلى وكلاء المجموعة والقطاع والتخصص المناسب لجمع فجوات الأدلة، وبناء فرضية المشكلة، واقتراح أصغر تدخل قابل للقياس.
          لا نعتبر الفرضية مشكلة مثبتة قبل وجود baseline ودليل.
        </p>

        <div className="divider-gold" />

        <form onSubmit={onSubmit} style={{ display: "grid", gap: 18, maxWidth: 920 }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 14 }}>
            <label style={labelStyle}>
              الاسم *
              <input name="name" required minLength={2} maxLength={160} autoComplete="name" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              الشركة *
              <input name="company" required minLength={2} maxLength={220} autoComplete="organization" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              البريد *
              <input name="email" type="email" required autoComplete="email" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              رقم التواصل
              <input name="phone" type="tel" autoComplete="tel" placeholder="+966…" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              الدور
              <input name="role" maxLength={160} autoComplete="organization-title" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              القطاع
              <input name="sector" defaultValue="other" maxLength={120} style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              موقع الشركة
              <input name="website" type="url" placeholder="https://…" style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              قناة الرد المفضلة
              <select name="preferred_contact" defaultValue="email" style={fieldStyle}>
                <option value="email">Email</option>
                <option value="phone">Phone</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="either">أي قناة متاحة</option>
              </select>
            </label>
          </div>

          <label style={labelStyle}>
            1) ما الـworkflow أو القرار الذي تريد تحسينه الآن؟ *
            <textarea name="workflow" required minLength={10} maxLength={2400} rows={4} style={fieldStyle} />
          </label>
          <label style={labelStyle}>
            2) من يملك القرار والمتابعة داخل الشركة؟
            <textarea name="decision_owner" maxLength={1000} rows={2} style={fieldStyle} />
          </label>
          <label style={labelStyle}>
            3) ما الأدوات أو البيانات التي يعتمد عليها العمل اليوم؟
            <textarea name="tools_data" maxLength={1800} rows={3} style={fieldStyle} />
          </label>
          <label style={labelStyle}>
            4) ما أثر المشكلة على الإيراد، التكلفة، الوقت، الجودة أو المخاطر؟
            <textarea name="business_impact" maxLength={1800} rows={3} style={fieldStyle} />
          </label>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 14 }}>
            <label style={labelStyle}>
              5) ما الـKPI الذي يثبت التحسن؟
              <textarea name="proof_metric" maxLength={1000} rows={3} style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              6) ما الـbaseline الحالي؟
              <textarea name="baseline" maxLength={1000} rows={3} style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              7) ما النتيجة المستهدفة؟
              <textarea name="target_outcome" maxLength={1200} rows={3} style={fieldStyle} />
            </label>
            <label style={labelStyle}>
              ما الاستعجال أو الموعد المؤثر؟
              <textarea name="urgency" maxLength={500} rows={3} style={fieldStyle} />
            </label>
          </div>

          <label style={{ display: "flex", gap: 10, alignItems: "flex-start", fontSize: "0.88rem", lineHeight: 1.55 }}>
            <input name="followup_requested" type="checkbox" style={{ marginTop: 4 }} />
            <span>
              أطلب من Dealix التواصل معي بخصوص هذا التشخيص. هذا الطلب اختياري ويخص هذه المحادثة فقط، ولا يتحول تلقائيًا إلى
              موافقة تسويق مباشر أو نشر Proof.
            </span>
          </label>

          <button
            type="submit"
            disabled={submitting}
            style={{
              justifySelf: "start",
              border: 0,
              borderRadius: 999,
              padding: "13px 20px",
              font: "inherit",
              fontWeight: 750,
              cursor: submitting ? "wait" : "pointer",
              opacity: submitting ? 0.7 : 1,
            }}
          >
            {submitting ? "جاري إنشاء Intake…" : "ابدأ التشخيص الآن"}
          </button>
        </form>

        {error ? (
          <div role="alert" style={{ marginTop: 18, maxWidth: 820, padding: 16, border: "1px solid rgba(255,255,255,0.15)", borderRadius: 12 }}>
            {error}
          </div>
        ) : null}

        {result ? (
          <div aria-live="polite" style={{ marginTop: 18, maxWidth: 820, padding: 18, border: "1px solid rgba(255,255,255,0.15)", borderRadius: 12 }}>
            <strong>{statusText}</strong>
            <p style={{ marginBottom: 8 }}>مرجع الطلب: <code>{result.intake_id}</code></p>
            <p style={{ marginBottom: 8 }}>
              الحالة: {result.problem_state ?? "UNPROVEN_NEEDS_EVIDENCE"}. لا يتم اعتبار المشكلة أو العائد أو Proof مثبتًا من مجرد التسجيل.
            </p>
            {result.next_questions?.length ? (
              <>
                <p style={{ marginBottom: 6 }}>فجوات التحقق المتبقية:</p>
                <ul>
                  {result.next_questions.map((question) => <li key={question}>{question}</li>)}
                </ul>
              </>
            ) : (
              <p>البيانات الأولية مكتملة؛ تنتقل داخليًا للتحقق من الأدلة والـbaseline.</p>
            )}
          </div>
        ) : null}

        <div className="divider-gold" />

        <h3>تواصل مباشر مع Founder Office</h3>
        <div className="actions" style={{ marginTop: "var(--sp-3)", flexWrap: "wrap" }}>
          <CTA href={emailHref} label={`Email: ${founderEmail}`} />
          <CTA href={telHref} label={`Phone: ${founderPhone}`} />
          {whatsappUrl ? <CTA href={whatsappUrl} label="WhatsApp — Founder Office" /> : null}
        </div>

        <p
          style={{
            fontSize: "0.82rem",
            color: "rgba(255,255,255,0.44)",
            marginTop: "var(--sp-4)",
            maxWidth: 820,
          }}
        >
          هذه الصفحة قناة inbound: أنت تبدأ التواصل. Dealix لا تعتبر رقمًا أو بريدًا عامًا موافقة على مراسلات تسويقية،
          ولا تحول Research أو Draft أو Diagnostic hypothesis إلى علاقة أو إرسال فعلي أو Customer Proof بدون أساس مناسب.
        </p>
      </section>
    </PageShell>
  );
}
