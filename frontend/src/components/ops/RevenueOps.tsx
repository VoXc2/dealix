"use client";

import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import {
  useOpsData,
  OpsSection,
  OpsSkeleton,
  OpsError,
  DegradedNote,
  EstimateTag,
  SurfaceHeader,
} from "./_shared";

interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface RevenueOpsData {
  governance_decision?: string;
  is_estimate?: boolean;
  pipeline_by_stage?: Record<string, number>;
  opportunities?: CountList;
  conversion_rates?: {
    lead_to_commitment_pct?: number;
    commitment_to_paid_pct?: number;
    is_estimate?: boolean;
  };
  next_best_actions?: Record<string, unknown>[];
}

export function RevenueOps() {
  const t = useTranslations("ops.revenueOps");
  const { data, loading, error } = useOpsData<RevenueOpsData>(api.getOpsRevenue);

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const stages = data.pipeline_by_stage ?? {};
  const opps = data.opportunities?.items ?? [];
  const actions = data.next_best_actions ?? [];
  const conv = data.conversion_rates ?? {};

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OpsSection title={t("pipelineByStage")}>
          <dl className="grid grid-cols-2 gap-3 text-sm">
            {Object.entries(stages).map(([stage, count]) => (
              <div key={stage} className="rounded-lg bg-muted/40 px-3 py-2">
                <dt className="text-xs text-muted-foreground">{stage}</dt>
                <dd className="text-lg font-semibold text-foreground">{count}</dd>
              </div>
            ))}
          </dl>
        </OpsSection>
        <OpsSection
          title={t("conversion")}
          right={<EstimateTag confirmed={false} />}
        >
          <div className="space-y-3">
            <div>
              <p className="text-xs text-muted-foreground">lead → commitment</p>
              <p className="text-2xl font-bold text-foreground">
                {conv.lead_to_commitment_pct ?? 0}%
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">commitment → paid</p>
              <p className="text-2xl font-bold text-foreground">
                {conv.commitment_to_paid_pct ?? 0}%
              </p>
            </div>
          </div>
        </OpsSection>
      </div>

      <OpsSection title={t("opportunities")}>
        {data.opportunities?.note ? (
          <DegradedNote note={data.opportunities.note} />
        ) : opps.length === 0 ? (
          <DegradedNote />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-muted-foreground border-b border-border">
                  <th className="text-start py-2 font-medium">Company</th>
                  <th className="text-start py-2 font-medium">Sector</th>
                  <th className="text-start py-2 font-medium">Status</th>
                  <th className="text-start py-2 font-medium">Fit</th>
                </tr>
              </thead>
              <tbody>
                {opps.map((o, i) => (
                  <tr key={i} className="border-b border-border/50">
                    <td className="py-2 text-foreground">
                      {String(o.company_name ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(o.sector ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(o.status ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(o.fit_score ?? "")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OpsSection>

      <OpsSection title={t("nextBestActions")}>
        {actions.length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-1.5 text-sm">
            {actions.map((a, i) => (
              <li key={i} className="flex items-center justify-between gap-2">
                <span className="text-foreground">{String(a.action ?? "")}</span>
                <span className="text-[10px] text-muted-foreground">
                  {String(a.default_mode ?? a.trust_plane ?? "")}
                </span>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>
    </div>
  );
}
