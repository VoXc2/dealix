"use client";

import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import {
  useOpsData,
  OpsSection,
  OpsSkeleton,
  OpsError,
  DegradedNote,
  SurfaceHeader,
} from "./_shared";

interface RiskSignal {
  signal?: string;
  points?: number;
}
interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface MarketProofData {
  governance_decision?: string;
  is_estimate?: boolean;
  risk_score?: { model?: RiskSignal[]; max?: number; note?: string };
  sample_proof_packs?: CountList;
  market_signals?: { count?: number; note?: string };
  target_accounts?: CountList;
}

export function MarketProof() {
  const t = useTranslations("ops.marketProof");
  const { data, loading, error } = useOpsData<MarketProofData>(
    api.getOpsMarketProof,
  );

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const model = data.risk_score?.model ?? [];
  const accounts = data.target_accounts?.items ?? [];
  const packs = data.sample_proof_packs?.items ?? [];

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <OpsSection title={t("riskScore")}>
        {model.length === 0 ? (
          <DegradedNote note={data.risk_score?.note} />
        ) : (
          <ul className="space-y-1.5">
            {model.map((s) => (
              <li
                key={s.signal}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-muted-foreground">{s.signal}</span>
                <span className="font-semibold text-amber-400">+{s.points}</span>
              </li>
            ))}
          </ul>
        )}
        <p className="text-[10px] text-muted-foreground mt-2">
          {data.risk_score?.note}
        </p>
      </OpsSection>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OpsSection title={t("signals")}>
          <p className="text-3xl font-bold text-foreground">
            {data.market_signals?.count ?? 0}
          </p>
          <p className="text-[11px] text-muted-foreground mt-1">
            {data.market_signals?.note}
          </p>
        </OpsSection>
        <OpsSection title={t("sampleProofPacks")}>
          {data.sample_proof_packs?.note ? (
            <DegradedNote note={data.sample_proof_packs.note} />
          ) : packs.length === 0 ? (
            <DegradedNote />
          ) : (
            <ul className="space-y-1.5 text-sm">
              {packs.map((p, i) => (
                <li key={i} className="flex items-center justify-between gap-2">
                  <span className="text-muted-foreground truncate">
                    {String(p.customer_handle ?? p.id ?? "")}
                  </span>
                  <span className="text-[10px] text-muted-foreground">
                    {String(p.event_type ?? "")}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </OpsSection>
      </div>

      <OpsSection title={t("targetAccounts")}>
        {data.target_accounts?.note ? (
          <DegradedNote note={data.target_accounts.note} />
        ) : accounts.length === 0 ? (
          <DegradedNote />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-muted-foreground border-b border-border">
                  <th className="text-start py-2 font-medium">Company</th>
                  <th className="text-start py-2 font-medium">Sector</th>
                  <th className="text-start py-2 font-medium">City</th>
                  <th className="text-start py-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((a, i) => (
                  <tr key={i} className="border-b border-border/50">
                    <td className="py-2 text-foreground">
                      {String(a.company_name ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(a.sector ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(a.city ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(a.status ?? "")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OpsSection>
    </div>
  );
}
