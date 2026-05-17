"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

type RiskScoreResult = {
  risk_score: number;
  risk_level: "low" | "medium" | "high";
  reasons: string[];
};

function SectionTitle({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="mb-4">
      <h2 className="text-xl font-bold text-foreground">{title}</h2>
      <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>
    </div>
  );
}

export function DiagnosticHero() {
  return (
    <Card className="border-gold-500/30 bg-gradient-to-br from-card to-card/80">
      <CardHeader>
        <CardTitle className="text-2xl">Dealix Diagnostic Autopilot</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <p>نبني نظام مبيعات + خدمة عملاء آلي مع Approval-first في كل نقطة مخاطر.</p>
        <p>المنظومة تجهز وتقترح وتوثق وتطلب موافقتك قبل أي إرسال خارجي عالي التأثير.</p>
      </CardContent>
    </Card>
  );
}

export function RiskScoreForm({
  onScore,
}: {
  onScore: (score: RiskScoreResult) => void;
}) {
  const [form, setForm] = useState({
    company: "",
    name: "",
    email: "",
    role: "",
    pain: "",
    budget: "",
    urgency: "",
    consent: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setLoading(true);
    setError(null);
    try {
      const risk = await api.postPublicRiskScore({
        company: form.company,
        pain: form.pain,
        budget: form.budget,
        urgency: form.urgency,
        consent: form.consent,
      });
      const result = risk.data as RiskScoreResult;
      onScore(result);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "risk_score_failed";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Score</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Input placeholder="Company" value={form.company} onChange={(e) => setForm((p) => ({ ...p, company: e.target.value }))} />
        <Input placeholder="Name" value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} />
        <Input placeholder="Email" value={form.email} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} />
        <Input placeholder="Role (Founder/CEO...)" value={form.role} onChange={(e) => setForm((p) => ({ ...p, role: e.target.value }))} />
        <Input placeholder="Main workflow pain" value={form.pain} onChange={(e) => setForm((p) => ({ ...p, pain: e.target.value }))} />
        <Input placeholder="Budget (SAR)" value={form.budget} onChange={(e) => setForm((p) => ({ ...p, budget: e.target.value }))} />
        <Input placeholder="Urgency (e.g. within 30 days)" value={form.urgency} onChange={(e) => setForm((p) => ({ ...p, urgency: e.target.value }))} />
        <label className="flex items-center gap-2 text-xs text-muted-foreground">
          <input
            type="checkbox"
            checked={form.consent}
            onChange={(e) => setForm((p) => ({ ...p, consent: e.target.checked }))}
          />
          I consent to receive a sample proof pack draft.
        </label>
        <Button variant="gold" className="w-full" onClick={submit} disabled={loading}>
          {loading ? "Calculating..." : "احصل على Sample Proof Pack"}
        </Button>
        {error && <p className="text-xs text-destructive">{error}</p>}
      </CardContent>
    </Card>
  );
}

export function ProofPackPreview({ score }: { score: RiskScoreResult | null }) {
  const badgeClass = useMemo(() => {
    if (!score) return "bg-muted text-muted-foreground";
    if (score.risk_level === "low") return "bg-emerald-500/20 text-emerald-300";
    if (score.risk_level === "medium") return "bg-amber-500/20 text-amber-300";
    return "bg-red-500/20 text-red-300";
  }, [score]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sample Proof Pack</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm">
        <p className="text-muted-foreground">Preview sections generated from governed workflow:</p>
        <ul className="list-disc ps-5 text-muted-foreground space-y-1">
          <li>Problem map + qualification snapshot</li>
          <li>Evidence chain and approval requirements</li>
          <li>Diagnostic scope draft + next actions</li>
        </ul>
        {score && (
          <div className={`inline-flex rounded-full px-3 py-1 text-xs ${badgeClass}`}>
            Risk: {score.risk_level} ({score.risk_score})
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function ServicePackages() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>What you get</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 text-sm text-muted-foreground">
        <p>499 SAR Diagnostic Sprint</p>
        <p>1,500 SAR Data Pack</p>
        <p>2,999+ SAR Managed Ops</p>
      </CardContent>
    </Card>
  );
}

export function BookingCTA() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  async function book() {
    setLoading(true);
    setMessage(null);
    try {
      const res = await api.postPublicBookingRequest({ channel: "meet", notes: "Diagnostic review request" });
      const data = res.data as { booking?: { id?: string } };
      setMessage(`Booking requested: ${data.booking?.id ?? "-"}`);
    } catch {
      setMessage("Failed to request booking.");
    } finally {
      setLoading(false);
    }
  }
  return (
    <Card>
      <CardHeader>
        <CardTitle>Book Diagnostic</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Button variant="emerald" className="w-full" onClick={book} disabled={loading}>
          {loading ? "Submitting..." : "احجز Diagnostic Review"}
        </Button>
        {message && <p className="text-xs text-muted-foreground">{message}</p>}
      </CardContent>
    </Card>
  );
}

export function FAQAccordion() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>FAQ</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <p>Does Dealix auto-send risky messages? No, approvals are required.</p>
        <p>Does Dealix auto-close deals? No, founder decision is mandatory.</p>
      </CardContent>
    </Card>
  );
}

export function TrustBoundaries() {
  return (
    <Card className="border-red-500/30">
      <CardHeader>
        <CardTitle>Trust boundaries</CardTitle>
      </CardHeader>
      <CardContent className="space-y-1 text-sm text-muted-foreground">
        <p>No cold WhatsApp automation.</p>
        <p>No external invoice send without approval.</p>
        <p>No final diagnostic or security claim without founder review.</p>
      </CardContent>
    </Card>
  );
}

export function PublicDiagnosticFunnel() {
  const [score, setScore] = useState<RiskScoreResult | null>(null);
  return (
    <div className="min-h-screen bg-background py-8">
      <div className="mx-auto max-w-5xl px-4 space-y-6">
        <DiagnosticHero />
        <SectionTitle
          title="Problem → Risk Score → Proof Pack → Booking"
          subtitle="Public sales funnel with governance-by-design."
        />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <RiskScoreForm onScore={setScore} />
          <ProofPackPreview score={score} />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <ServicePackages />
          <BookingCTA />
          <TrustBoundaries />
        </div>
        <FAQAccordion />
      </div>
    </div>
  );
}

