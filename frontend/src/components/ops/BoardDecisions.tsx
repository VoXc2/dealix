"use client";

import { useTranslations, useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import {
  useOpsData,
  OpsSection,
  OpsSkeleton,
  OpsError,
  DegradedNote,
  SurfaceHeader,
} from "./_shared";

interface Decision {
  action_type?: string;
  decision?: string;
  reason?: string;
  risk_level?: string;
  approval_required?: boolean;
  safe_alternative?: string;
}
interface PassportRule {
  rule?: string;
  en?: string;
  ar?: string;
}
interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface BoardData {
  governance_decision?: string;
  is_estimate?: boolean;
  top_decisions?: Decision[];
  decision_passport_rules?: PassportRule[];
  risk_register?: CountList;
}

function decisionTone(decision?: string): string {
  if (decision === "allow") return "text-emerald-400 border-emerald-400/40";
  if (decision === "block") return "text-destructive border-destructive/40";
  return "text-amber-400 border-amber-400/40";
}

export function BoardDecisions() {
  const t = useTranslations("ops.boardDecisions");
  const locale = useLocale();
  const isAr = locale === "ar";
  const { data, loading, error } = useOpsData<BoardData>(api.getOpsBoard);

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const decisions = data.top_decisions ?? [];
  const rules = data.decision_passport_rules ?? [];
  const risks = data.risk_register?.items ?? [];

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <OpsSection title={t("topDecisions")}>
        {decisions.length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-2">
            {decisions.map((d, i) => (
              <li
                key={i}
                className="rounded-lg bg-muted/30 px-3 py-2 flex items-start justify-between gap-3"
              >
                <div>
                  <p className="text-sm font-medium text-foreground">
                    {d.action_type}
                  </p>
                  <p className="text-xs text-muted-foreground">{d.reason}</p>
                </div>
                <Badge
                  variant="outline"
                  className={`text-[10px] ${decisionTone(d.decision)}`}
                >
                  {d.decision}
                </Badge>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>

      <OpsSection title={t("passports")}>
        <ul className="space-y-2 text-sm">
          {rules.map((r, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-gold-400 mt-0.5">●</span>
              <span className="text-muted-foreground">{isAr ? r.ar : r.en}</span>
            </li>
          ))}
        </ul>
      </OpsSection>

      <OpsSection title={t("riskRegister")}>
        {data.risk_register?.note ? (
          <DegradedNote note={data.risk_register.note} />
        ) : risks.length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-1.5 text-sm">
            {risks.map((r, i) => (
              <li key={i} className="flex items-center justify-between gap-2">
                <span className="text-muted-foreground">
                  {String(r.event_type ?? "")}
                </span>
                <Badge
                  variant="outline"
                  className="text-[10px] text-amber-400 border-amber-400/40"
                >
                  {String(r.risk_level ?? "")}
                </Badge>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>
    </div>
  );
}
