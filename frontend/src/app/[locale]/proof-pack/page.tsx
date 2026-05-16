"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { FileCheck } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { api } from "@/lib/api";

const SECTION_KEYS = [
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

const COMPONENT_KEYS = [
  "source_evidence",
  "ai_run_evidence",
  "policy_evidence",
  "human_review_evidence",
  "approval_evidence",
  "output_evidence",
  "proof_evidence",
  "value_evidence",
] as const;

const taClass =
  "w-full rounded-lg border border-border bg-card px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-gold-400 min-h-[64px]";

function label(k: string): string {
  return k.replace(/_/g, " ");
}

interface GenerateResult {
  proof_score?: number;
  tier?: string;
  governance_decision?: string;
  missing_sections?: string[];
  missing_components?: string[];
  [k: string]: unknown;
}

export default function ProofPackPage() {
  const t = useTranslations("proofPack");
  const [engagementId, setEngagementId] = useState("");
  const [sections, setSections] = useState<Record<string, string>>({});
  const [components, setComponents] = useState<Record<string, string>>({});
  const [result, setResult] = useState<GenerateResult | null>(null);
  const [missing, setMissing] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);

  const generate = async () => {
    if (!engagementId.trim()) {
      toast.error(t("needEngagementId"));
      return;
    }
    setSubmitting(true);
    setMissing([]);
    setResult(null);
    try {
      const res = await api.postProofPackGenerate(engagementId.trim(), {
        sections,
        components,
      });
      setResult(res.data as GenerateResult);
      toast.success(t("result"));
    } catch (e) {
      const detail = (
        e as { response?: { data?: { detail?: GenerateResult } } }
      ).response?.data?.detail;
      if (detail && (detail.missing_sections || detail.missing_components)) {
        setMissing([
          ...(detail.missing_sections ?? []),
          ...(detail.missing_components ?? []),
        ]);
        toast.error(t("missing"));
      } else {
        toast.error(e instanceof Error ? e.message : "error");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="max-w-xl mb-6">
        <label className="text-xs text-muted-foreground mb-1 block">{t("engagementId")}</label>
        <Input value={engagementId} onChange={(e) => setEngagementId(e.target.value)} />
        <p className="text-xs text-muted-foreground mt-2">{t("fillHint")}</p>
      </div>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("sectionsTitle")}</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
          {SECTION_KEYS.map((k) => (
            <div key={k}>
              <label className="text-xs text-muted-foreground mb-1 block capitalize">
                {label(k)}
              </label>
              <textarea
                className={taClass}
                value={sections[k] ?? ""}
                onChange={(e) => setSections((s) => ({ ...s, [k]: e.target.value }))}
              />
            </div>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("componentsTitle")}</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
          {COMPONENT_KEYS.map((k) => (
            <div key={k}>
              <label className="text-xs text-muted-foreground mb-1 block capitalize">
                {label(k)}
              </label>
              <textarea
                className={taClass}
                value={components[k] ?? ""}
                onChange={(e) => setComponents((c) => ({ ...c, [k]: e.target.value }))}
              />
            </div>
          ))}
        </div>
      </section>

      <Button onClick={() => void generate()} disabled={submitting} className="mb-6">
        <FileCheck className="w-4 h-4 me-1.5" />
        {t("generate")}
      </Button>

      {missing.length > 0 && (
        <div className="rounded-2xl border border-destructive/30 bg-destructive/5 p-4 mb-6">
          <p className="text-sm font-semibold mb-2">{t("missing")}</p>
          <div className="flex flex-wrap gap-2">
            {missing.map((m) => (
              <Badge key={m} variant="outline" className="text-destructive border-destructive/40">
                {label(m)}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {result && (
        <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-4">
          <h3 className="text-sm font-semibold mb-2">{t("scoreTitle")}</h3>
          <div className="flex items-center gap-3 mb-3">
            <p className="text-4xl font-bold text-emerald-400">{result.proof_score ?? "—"}</p>
            {result.tier && <Badge variant="outline">{result.tier}</Badge>}
            {result.governance_decision && (
              <Badge variant="outline">{result.governance_decision}</Badge>
            )}
          </div>
          <pre className="text-xs overflow-auto max-h-[280px]">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </AppLayout>
  );
}
