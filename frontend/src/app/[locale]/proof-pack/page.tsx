"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import axios from "axios";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

type Json = Record<string, unknown>;

const PROOF_SECTIONS = [
  "executive_summary",
  "problem",
  "inputs",
  "source_passports",
  "work_completed",
  "outputs",
  "quality_scores",
  "governance_decisions",
  "blocked_risks",
  "value_metrics",
  "limitations",
  "recommended_next_step",
  "capital_assets_created",
  "appendices",
] as const;

const PROOF_COMPONENTS = [
  "source_evidence",
  "ai_run_evidence",
  "policy_evidence",
  "human_review_evidence",
  "approval_evidence",
  "output_evidence",
  "proof_evidence",
  "value_evidence",
] as const;

export default function ProofPackPage() {
  const t = useTranslations("proofPack");

  const [engagementId, setEngagementId] = useState("");
  const [sections, setSections] = useState<Set<string>>(new Set());
  const [components, setComponents] = useState<Set<string>>(new Set());
  const [result, setResult] = useState<Json | null>(null);
  const [missing, setMissing] = useState<string[] | null>(null);
  const [gate, setGate] = useState<Json | null>(null);
  const [loading, setLoading] = useState(false);

  // retainer-gate inputs
  const [clientHealth, setClientHealth] = useState(70);
  const [flags, setFlags] = useState<Record<string, boolean>>({
    workflow_recurring: false,
    owner_exists: true,
    monthly_value_clear: false,
    stakeholder_engaged: false,
    governance_risk_controlled: true,
  });

  const toggle = (
    set: Set<string>,
    update: (s: Set<string>) => void,
    key: string,
  ) => {
    const next = new Set(set);
    if (next.has(key)) next.delete(key);
    else next.add(key);
    update(next);
  };

  const filled = (keys: readonly string[], chosen: Set<string>): Json =>
    Object.fromEntries(keys.filter((k) => chosen.has(k)).map((k) => [k, "provided"]));

  const flagLabels: Record<string, string> = {
    workflow_recurring: t("workflowRecurring"),
    owner_exists: t("ownerExists"),
    monthly_value_clear: t("monthlyValueClear"),
    stakeholder_engaged: t("stakeholderEngaged"),
    governance_risk_controlled: t("govControlled"),
  };

  const generate = async () => {
    if (!engagementId.trim()) return;
    setLoading(true);
    setResult(null);
    setMissing(null);
    try {
      const res = await api.postProofPackGenerate(engagementId.trim(), {
        sections: filled(PROOF_SECTIONS, sections),
        components: filled(PROOF_COMPONENTS, components),
      });
      setResult(res.data as Json);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        const detail = (err.response.data as Json)?.detail as Json | undefined;
        const ms = (detail?.missing_sections as string[]) ?? [];
        const mc = (detail?.missing_components as string[]) ?? [];
        setMissing([...ms, ...mc]);
      } else {
        setMissing(["request_failed"]);
      }
    } finally {
      setLoading(false);
    }
  };

  const runGate = async () => {
    if (!engagementId.trim()) return;
    setLoading(true);
    setGate(null);
    try {
      const res = await api.postProofPackRetainerGate(engagementId.trim(), {
        client_health: clientHealth,
        ...flags,
      });
      setGate(res.data as Json);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="mb-8 max-w-md">
        <label className="text-sm font-medium">{t("engagementLabel")}</label>
        <Input
          value={engagementId}
          onChange={(e) => setEngagementId(e.target.value)}
          placeholder="eng_2026_05_acme"
          className="mt-1"
        />
      </div>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("sectionsTitle")}</h2>
        <div className="grid gap-2 sm:grid-cols-2">
          {PROOF_SECTIONS.map((s) => (
            <label key={s} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={sections.has(s)}
                onChange={() => toggle(sections, setSections, s)}
              />
              {s}
            </label>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("componentsTitle")}</h2>
        <div className="grid gap-2 sm:grid-cols-2">
          {PROOF_COMPONENTS.map((c) => (
            <label key={c} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={components.has(c)}
                onChange={() => toggle(components, setComponents, c)}
              />
              {c}
            </label>
          ))}
        </div>
      </section>

      <Button onClick={() => void generate()} disabled={loading}>
        {t("generate")}
      </Button>

      {result && (
        <div className="mt-4 rounded-xl border border-border bg-muted/20 p-4">
          <p className="text-sm">
            {t("scoreTitle")}:{" "}
            <span className="text-2xl font-bold text-gold-400">
              {String(result.proof_score)}
            </span>
          </p>
          <p className="mt-1 text-sm text-muted-foreground">
            {t("tierTitle")}: {String(result.tier)}
          </p>
        </div>
      )}

      {missing && (
        <div className="mt-4 rounded-xl border border-destructive/40 bg-destructive/5 p-4">
          <p className="text-sm font-medium">{t("missingTitle")}</p>
          <p className="mt-1 text-sm text-muted-foreground">
            {missing.join(", ")}
          </p>
        </div>
      )}

      <section className="mt-12">
        <h2 className="text-lg font-semibold mb-3">{t("retainerTitle")}</h2>
        <div className="mb-3 max-w-xs">
          <label className="text-sm font-medium">{t("clientHealth")}</label>
          <Input
            type="number"
            min={0}
            max={100}
            value={clientHealth}
            onChange={(e) => setClientHealth(Number(e.target.value))}
            className="mt-1"
          />
        </div>
        <div className="grid gap-2 sm:grid-cols-2">
          {Object.keys(flags).map((f) => (
            <label key={f} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={flags[f]}
                onChange={() =>
                  setFlags((prev) => ({ ...prev, [f]: !prev[f] }))
                }
              />
              {flagLabels[f]}
            </label>
          ))}
        </div>
        <Button
          className="mt-4"
          onClick={() => void runGate()}
          disabled={loading}
        >
          {t("runGate")}
        </Button>
        {gate && (
          <div className="mt-4 rounded-xl border border-border bg-muted/20 p-4 text-sm">
            <p className={gate.retainer_gate_ok ? "text-emerald-500" : "text-destructive"}>
              {gate.retainer_gate_ok ? t("gatePass") : t("gateFail")}
            </p>
            <p className="mt-1 text-muted-foreground">
              {String(gate.recommendation ?? "")}
            </p>
          </div>
        )}
      </section>
    </AppLayout>
  );
}
