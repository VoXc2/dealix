"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import {
  useOpsData,
  OpsSection,
  OpsSkeleton,
  OpsError,
  DegradedNote,
  GovernanceBadge,
} from "./_shared";

interface TemplateData {
  governance_decision?: string;
  sections?: string[];
  empty_pack?: Record<string, string>;
  completeness_score?: number;
  strength_band?: string;
  note?: string;
}
interface PreviewData {
  governance_decision?: string;
  diagnostic?: Record<string, unknown>;
  sections?: string[];
  completeness_score?: number;
  strength_band?: string;
  note?: string;
}

export function ProofPack() {
  const t = useTranslations("ops.proofPack");
  const tc = useTranslations("common");
  const { data, loading, error } = useOpsData<TemplateData>(
    api.getOpsProofPackTemplate,
  );

  const [company, setCompany] = useState("");
  const [sector, setSector] = useState("b2b_services");
  const [preview, setPreview] = useState<PreviewData | null>(null);
  const [busy, setBusy] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  async function runPreview() {
    if (!company.trim()) return;
    setBusy(true);
    setPreviewError(null);
    try {
      const res = await api.postOpsProofPackPreview({ company, sector });
      setPreview(res.data as PreviewData);
    } catch (e) {
      setPreviewError((e as Error)?.message ?? "request failed");
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const sections = data.sections ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <GovernanceBadge decision={data.governance_decision} />
      </div>

      <OpsSection title={t("generate")}>
        <div className="flex flex-wrap items-end gap-3">
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-muted-foreground">Company</label>
            <Input
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="Acme Co"
            />
          </div>
          <div className="flex-1 min-w-[160px]">
            <label className="text-xs text-muted-foreground">Sector</label>
            <Input
              value={sector}
              onChange={(e) => setSector(e.target.value)}
              placeholder="b2b_services"
            />
          </div>
          <Button onClick={runPreview} disabled={busy || !company.trim()}>
            {busy ? tc("loading") : t("generate")}
          </Button>
        </div>
        {previewError ? (
          <p className="text-xs text-destructive mt-2">{previewError}</p>
        ) : null}
      </OpsSection>

      {preview ? (
        <OpsSection
          title="Preview"
          right={<GovernanceBadge decision={preview.governance_decision} />}
        >
          <div className="grid grid-cols-2 gap-3 text-sm mb-3">
            <div className="rounded-lg bg-muted/40 px-3 py-2">
              <p className="text-xs text-muted-foreground">{t("completeness")}</p>
              <p className="text-lg font-semibold text-foreground">
                {preview.completeness_score ?? 0}
              </p>
            </div>
            <div className="rounded-lg bg-muted/40 px-3 py-2">
              <p className="text-xs text-muted-foreground">{t("strengthBand")}</p>
              <p className="text-lg font-semibold text-foreground">
                {preview.strength_band ?? "—"}
              </p>
            </div>
          </div>
          <pre className="text-xs bg-background border border-border rounded-lg p-3 overflow-x-auto whitespace-pre-wrap">
            {String(preview.diagnostic?.markdown_ar_en ?? preview.note ?? "")}
          </pre>
          <p className="text-[11px] text-muted-foreground mt-2">{preview.note}</p>
        </OpsSection>
      ) : null}

      <OpsSection title={t("template")}>
        {sections.length === 0 ? (
          <DegradedNote note={data.note} />
        ) : (
          <ul className="flex flex-wrap gap-1.5">
            {sections.map((s) => (
              <li
                key={s}
                className="text-[10px] bg-background border border-border rounded px-1.5 py-0.5 text-muted-foreground"
              >
                {s}
              </li>
            ))}
          </ul>
        )}
      </OpsSection>
    </div>
  );
}
