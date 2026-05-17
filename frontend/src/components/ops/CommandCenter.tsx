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

interface Action {
  label_en?: string;
  label_ar?: string;
  kind?: string;
  priority?: number;
}
interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface CommandCenterData {
  governance_decision?: string;
  is_estimate?: boolean;
  top_3_actions?: Action[];
  leads_waiting?: CountList;
  blocked_approvals?: CountList;
  delivery_risks?: { total?: number; note?: string };
  proof_events?: { count?: number; by_type?: Record<string, number>; note?: string };
  pipeline?: Record<string, unknown>;
  capital_assets_this_week?: CountList;
}

export function CommandCenter() {
  const t = useTranslations("ops");
  const tc = useTranslations("ops.commandCenter");
  const locale = useLocale();
  const isAr = locale === "ar";
  const { data, loading, error } = useOpsData<CommandCenterData>(
    api.getOpsCommandCenter,
  );

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const pipeline = (data.pipeline ?? {}) as Record<string, unknown>;
  const proofTypes = data.proof_events?.by_type ?? {};

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <OpsSection title={tc("top3")}>
        <ol className="space-y-2">
          {(data.top_3_actions ?? []).map((a, i) => (
            <li key={i} className="flex items-start gap-3 text-sm">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gold-500/15 text-gold-400 flex items-center justify-center text-xs font-bold">
                {a.priority ?? i + 1}
              </span>
              <span className="text-foreground">{isAr ? a.label_ar : a.label_en}</span>
            </li>
          ))}
        </ol>
      </OpsSection>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <OpsSection title={tc("leadsWaiting")}>
          <p className="text-3xl font-bold text-foreground">
            {data.leads_waiting?.count ?? 0}
          </p>
          {data.leads_waiting?.note ? (
            <DegradedNote note={data.leads_waiting.note} />
          ) : null}
        </OpsSection>
        <OpsSection title={tc("blockedApprovals")}>
          <p className="text-3xl font-bold text-amber-400">
            {data.blocked_approvals?.count ?? 0}
          </p>
          {data.blocked_approvals?.note ? (
            <DegradedNote note={data.blocked_approvals.note} />
          ) : null}
        </OpsSection>
        <OpsSection title={tc("deliveryRisks")}>
          <p className="text-3xl font-bold text-foreground">
            {data.delivery_risks?.total ?? 0}
          </p>
          {data.delivery_risks?.note ? (
            <DegradedNote note={data.delivery_risks.note} />
          ) : null}
        </OpsSection>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OpsSection title={tc("pipeline")}>
          {pipeline.note ? (
            <DegradedNote note={String(pipeline.note)} />
          ) : (
            <dl className="grid grid-cols-2 gap-3 text-sm">
              {[
                ["total_leads", t("commandCenter.pipeline")],
                ["commitments", "commitments"],
                ["paid", "paid"],
                ["total_revenue_sar", t("commandCenter.cash")],
              ].map(([key, label]) => (
                <div key={key} className="rounded-lg bg-muted/40 px-3 py-2">
                  <dt className="text-xs text-muted-foreground">{label}</dt>
                  <dd className="text-lg font-semibold text-foreground">
                    {String(pipeline[key] ?? 0)}
                  </dd>
                </div>
              ))}
            </dl>
          )}
        </OpsSection>
        <OpsSection title="Proof events">
          {data.proof_events?.note ? (
            <DegradedNote note={data.proof_events.note} />
          ) : Object.keys(proofTypes).length === 0 ? (
            <DegradedNote />
          ) : (
            <ul className="space-y-1.5 text-sm">
              {Object.entries(proofTypes).map(([type, count]) => (
                <li key={type} className="flex items-center justify-between">
                  <span className="text-muted-foreground truncate">{type}</span>
                  <span className="font-semibold text-foreground">{count}</span>
                </li>
              ))}
            </ul>
          )}
        </OpsSection>
      </div>
    </div>
  );
}
