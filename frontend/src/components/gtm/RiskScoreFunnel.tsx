"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/lib/api";

type ScoreResult = {
  score: number;
  breakdown: Record<string, number>;
  governance_note_ar?: string;
};

export function RiskScoreFunnel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    role: "",
    country: isAr ? "Saudi Arabia" : "",
    industry: "",
    pain: "",
    ai_usage: "",
    budget_range: "",
    urgency: "",
    consent_proof_pack: false,
    consent_marketing: false,
  });
  const [score, setScore] = useState<ScoreResult | null>(null);
  const [leadId, setLeadId] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (k: string, v: string | boolean) =>
    setForm((f) => ({ ...f, [k]: v }));

  async function onScore(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await api.postPublicRiskScore({
        role: form.role,
        company: form.company,
        industry: form.industry,
        country: form.country,
        ai_usage: form.ai_usage,
        budget_range: form.budget_range,
        urgency: form.urgency,
        pain: form.pain,
        notes: "",
      });
      setScore(data as ScoreResult);
    } catch {
      setError(isAr ? "تعذّر حساب النتيجة." : "Could not compute score.");
    } finally {
      setBusy(false);
    }
  }

  async function onCaptureLead() {
    if (!form.name || !form.email) {
      setError(isAr ? "الاسم والبريد مطلوبان." : "Name and email required.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const { data } = await api.postPublicLead({
        ...form,
        source: "risk_score_funnel",
        hold_stage: false,
      });
      setLeadId(String(data.lead_id));
    } catch {
      setError(isAr ? "تعذّر تسجيل الطلب." : "Could not capture lead.");
    } finally {
      setBusy(false);
    }
  }

  const dir = isAr ? "rtl" : "ltr";

  return (
    <div className="max-w-xl mx-auto space-y-6" dir={dir}>
      <div className={isAr ? "text-right" : ""}>
        <h1 className="text-2xl font-bold">
          {isAr ? "AI & Revenue Ops Risk Score" : "AI & Revenue Ops Risk Score"}
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          {isAr
            ? "تقدير تشغيلي داخلي — ليس تأهيلاً نهائياً بلا مراجعة بشرية."
            : "Operational estimate only — not final qualification without human review."}
        </p>
      </div>

      <form onSubmit={onScore} className="space-y-4">
        {(
          [
            ["name", isAr ? "الاسم" : "Name"],
            ["email", isAr ? "البريد" : "Email"],
            ["company", isAr ? "الشركة" : "Company"],
            ["role", isAr ? "الدور" : "Role"],
            ["country", isAr ? "الدولة" : "Country"],
            ["pain", isAr ? "ألم تشغيلي" : "Operational pain"],
            ["ai_usage", isAr ? "استخدام AI" : "AI usage"],
            ["budget_range", isAr ? "الميزانية" : "Budget"],
            ["urgency", isAr ? "الاستعجال" : "Urgency"],
          ] as const
        ).map(([key, label]) => (
          <div key={key} className="space-y-1">
            <Label htmlFor={key}>{label}</Label>
            <Input
              id={key}
              value={String(form[key as keyof typeof form] ?? "")}
              onChange={(ev) => set(key, ev.target.value)}
            />
          </div>
        ))}
        <label className="flex gap-2 text-sm items-center">
          <input
            type="checkbox"
            checked={form.consent_proof_pack}
            onChange={(e) => set("consent_proof_pack", e.target.checked)}
          />
          {isAr ? "أوافق على عيّنة Proof Pack" : "Consent to sample Proof Pack"}
        </label>
        <Button type="submit" disabled={busy} className="w-full">
          {isAr ? "احسب النتيجة" : "Calculate score"}
        </Button>
      </form>

      {score && (
        <Card className="p-4">
          <p className="font-semibold">
            {isAr ? "النتيجة:" : "Score:"} {score.score}
          </p>
          <pre className="mt-2 text-xs overflow-auto bg-muted p-2 rounded">
            {JSON.stringify(score.breakdown, null, 2)}
          </pre>
          {score.governance_note_ar && isAr && (
            <p className="mt-2 text-xs text-muted-foreground">{score.governance_note_ar}</p>
          )}
        </Card>
      )}

      <Button variant="secondary" onClick={onCaptureLead} disabled={busy} className="w-full">
        {isAr ? "سجّل واطلب مراجعة Diagnostic" : "Register & request Diagnostic review"}
      </Button>

      {leadId && (
        <p className="text-sm text-green-600">
          {isAr ? `تم التسجيل: ${leadId}` : `Registered: ${leadId}`}
        </p>
      )}

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="flex gap-2 flex-wrap">
        <Button asChild variant="outline" size="sm">
          <Link href={`/${locale}/proof-pack`}>{isAr ? "Proof Pack" : "Proof Pack"}</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link href={`/${locale}/business-now#strategy`}>{isAr ? "ديمو" : "Demo"}</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link href={`/${locale}/dealix-diagnostic`}>{isAr ? "التشخيص" : "Diagnostic"}</Link>
        </Button>
      </div>
    </div>
  );
}
