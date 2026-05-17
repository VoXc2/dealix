"use client";

import { useTranslations, useLocale } from "next-intl";
import { api } from "@/lib/api";
import {
  useOpsData,
  OpsSection,
  OpsSkeleton,
  OpsError,
  DegradedNote,
  SurfaceHeader,
} from "./_shared";

interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface EvidenceData {
  governance_decision?: string;
  is_estimate?: boolean;
  proof_events?: CountList;
  value_events?: CountList;
  sources?: string[];
}
interface LevelsData {
  levels?: { level?: number; description_ar?: string; description_en?: string }[];
}

export function EvidenceLedger() {
  const t = useTranslations("ops.evidenceLedger");
  const locale = useLocale();
  const isAr = locale === "ar";
  const { data, loading, error } = useOpsData<EvidenceData>(api.getOpsEvidence);
  const { data: levels } = useOpsData<LevelsData>(api.getOpsEvidenceLevels);

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const proof = data.proof_events?.items ?? [];
  const value = data.value_events?.items ?? [];

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <OpsSection title={t("levels")}>
        {(levels?.levels ?? []).length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-1.5 text-sm">
            {(levels?.levels ?? []).map((l) => (
              <li key={l.level} className="flex items-start gap-3">
                <span className="flex-shrink-0 text-xs font-bold text-gold-400">
                  L{l.level}
                </span>
                <span className="text-muted-foreground">
                  {isAr ? l.description_ar : l.description_en}
                </span>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>

      <OpsSection title={t("events")}>
        {data.proof_events?.note ? (
          <DegradedNote note={data.proof_events.note} />
        ) : proof.length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-2 text-sm">
            {proof.map((e, i) => (
              <li key={i} className="rounded-lg bg-muted/30 px-3 py-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-medium text-foreground">
                    {String(e.event_type ?? "")}
                  </span>
                  <span className="text-[10px] text-muted-foreground">
                    {String(e.approval_status ?? "")}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-0.5 truncate">
                  {String((isAr ? e.summary_ar : e.summary_en) ?? "")}
                </p>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OpsSection title="Value events">
          {data.value_events?.note ? (
            <DegradedNote note={data.value_events.note} />
          ) : value.length === 0 ? (
            <DegradedNote />
          ) : (
            <ul className="space-y-1.5 text-sm">
              {value.map((v, i) => (
                <li key={i} className="flex items-center justify-between gap-2">
                  <span className="text-muted-foreground">
                    {String(v.kind ?? "")}
                  </span>
                  <span className="text-[10px] text-muted-foreground">
                    {String(v.tier ?? "")}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </OpsSection>
        <OpsSection title={t("sources")}>
          {(data.sources ?? []).length === 0 ? (
            <DegradedNote />
          ) : (
            <ul className="flex flex-wrap gap-1.5">
              {(data.sources ?? []).map((s) => (
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
    </div>
  );
}
