"use client";

import { FormEvent, useState } from "react";

interface DraftResponse {
  mode: string;
  requiresApproval: boolean;
  externalSendEnabled: boolean;
  company: string;
  sector: string;
  city: string;
  senderIdentity: string;
  painHypothesis: string;
  recommendedOffer: string;
  discoveryQuestions: string[];
  draftAr: string;
  negotiationGuardrails: string[];
}

const sectors = [
  ["b2b_services", "B2B Services"],
  ["clinics", "Clinics"],
  ["real_estate", "Real Estate"],
  ["logistics", "Logistics"],
  ["training_centers", "Training Centers"],
  ["marketing_agencies", "Marketing Agencies"],
];

export default function SalesAgentLabPage() {
  const [company, setCompany] = useState("Sample Riyadh B2B Company");
  const [sector, setSector] = useState("b2b_services");
  const [city, setCity] = useState("Riyadh");
  const [senderIdentity, setSenderIdentity] = useState("Dealix Sales Assistant");
  const [result, setResult] = useState<DraftResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("/api/sales-agent/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, sector, city, senderIdentity, sourceUrl: "manual_review_required" }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to generate draft");
      }
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Sales Agent Lab</p>
        <h1>جرّب توليد مسودة مبيعات حسب الشركة والقطاع</h1>
        <p style={{ maxWidth: 760, margin: "0 auto" }}>
          هذه الواجهة تولد draft فقط. لا يوجد إرسال خارجي. استخدمها لاختبار الألم، العرض المناسب، الأسئلة،
          وحدود التفاوض قبل مراجعة المؤسس.
        </p>
      </section>

      <section className="grid-2">
        <form className="card" onSubmit={onSubmit}>
          <p className="eyebrow">Input</p>
          <label style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            Company
            <input value={company} onChange={(e) => setCompany(e.target.value)} required />
          </label>
          <label style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            Sector
            <select value={sector} onChange={(e) => setSector(e.target.value)}>
              {sectors.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </label>
          <label style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            City
            <input value={city} onChange={(e) => setCity(e.target.value)} />
          </label>
          <label style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            Sender identity
            <input value={senderIdentity} onChange={(e) => setSenderIdentity(e.target.value)} />
          </label>
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate sales draft"}
          </button>
          {error && <p className="text-coral" style={{ marginTop: 16 }}>{error}</p>}
        </form>

        <article className="card card-cyan">
          <p className="eyebrow">Safety state</p>
          <h2>Baseline: draft_only</h2>
          <ul>
            <li>External send is disabled.</li>
            <li>Founder approval is required.</li>
            <li>Named executive identity requires explicit approval.</li>
            <li>WhatsApp live use requires opt-in and approved template.</li>
            <li>No fake ROI or fake proof.</li>
          </ul>
        </article>
      </section>

      {result && (
        <section className="card">
          <p className="eyebrow">Generated draft</p>
          <h2>{result.company} → {result.recommendedOffer}</h2>
          <div className="grid-2">
            <div>
              <p><strong>Sector:</strong> {result.sector}</p>
              <p><strong>City:</strong> {result.city}</p>
              <p><strong>Pain hypothesis:</strong> {result.painHypothesis}</p>
              <p><strong>Sender:</strong> {result.senderIdentity}</p>
              <p><strong>Mode:</strong> {result.mode}</p>
            </div>
            <div>
              <h3>Discovery questions</h3>
              <ul>{result.discoveryQuestions.map((q) => <li key={q}>{q}</li>)}</ul>
            </div>
          </div>
          <h3 style={{ marginTop: "var(--sp-6)" }}>Arabic draft</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>{result.draftAr}</pre>
          <h3>Negotiation guardrails</h3>
          <ul>{result.negotiationGuardrails.map((g) => <li key={g}>{g}</li>)}</ul>
        </section>
      )}
    </main>
  );
}
