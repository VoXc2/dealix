"use client";

import { useTranslations, useLocale } from "next-intl";
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

interface ValueFlag {
  value?: number;
  is_estimate?: boolean;
}
interface CountList {
  count?: number;
  items?: Record<string, unknown>[];
  note?: string | null;
}
interface BillingData {
  governance_decision?: string;
  is_estimate?: boolean;
  invoices?: CountList;
  invoice_intent_total_sar?: ValueFlag;
  confirmed_revenue_sar?: ValueFlag;
  revenue_ladder?: Record<string, unknown>[];
  unit_economics?: {
    paid_customers?: number;
    avg_confirmed_deal_sar?: number;
    is_estimate?: boolean;
  };
}

export function Billing() {
  const t = useTranslations("ops.billing");
  const tc = useTranslations("common");
  const locale = useLocale();
  const isAr = locale === "ar";
  const { data, loading, error } = useOpsData<BillingData>(api.getOpsBilling);

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const invoices = data.invoices?.items ?? [];
  const ladder = data.revenue_ladder ?? [];

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <OpsSection
          title={t("confirmedRevenue")}
          right={<EstimateTag confirmed />}
        >
          <p className="text-3xl font-bold text-emerald-400">
            {(data.confirmed_revenue_sar?.value ?? 0).toLocaleString()}{" "}
            <span className="text-sm text-muted-foreground">{tc("sar")}</span>
          </p>
        </OpsSection>
        <OpsSection
          title="Invoice intent"
          right={<EstimateTag confirmed={false} />}
        >
          <p className="text-3xl font-bold text-amber-400">
            {(data.invoice_intent_total_sar?.value ?? 0).toLocaleString()}{" "}
            <span className="text-sm text-muted-foreground">{tc("sar")}</span>
          </p>
        </OpsSection>
      </div>

      <OpsSection
        title={t("unitEconomics")}
        right={<EstimateTag confirmed={false} />}
      >
        <dl className="grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-lg bg-muted/40 px-3 py-2">
            <dt className="text-xs text-muted-foreground">paid customers</dt>
            <dd className="text-lg font-semibold text-foreground">
              {data.unit_economics?.paid_customers ?? 0}
            </dd>
          </div>
          <div className="rounded-lg bg-muted/40 px-3 py-2">
            <dt className="text-xs text-muted-foreground">avg confirmed deal</dt>
            <dd className="text-lg font-semibold text-foreground">
              {(data.unit_economics?.avg_confirmed_deal_sar ?? 0).toLocaleString()}{" "}
              {tc("sar")}
            </dd>
          </div>
        </dl>
      </OpsSection>

      <OpsSection title={t("invoices")}>
        {data.invoices?.note ? (
          <DegradedNote note={data.invoices.note} />
        ) : invoices.length === 0 ? (
          <DegradedNote />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-muted-foreground border-b border-border">
                  <th className="text-start py-2 font-medium">Invoice #</th>
                  <th className="text-start py-2 font-medium">Buyer</th>
                  <th className="text-start py-2 font-medium">Total</th>
                  <th className="text-start py-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((inv, i) => (
                  <tr key={i} className="border-b border-border/50">
                    <td className="py-2 text-foreground">
                      {String(inv.invoice_number ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(inv.buyer_name ?? "")}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {Number(inv.total_sar ?? 0).toLocaleString()}
                    </td>
                    <td className="py-2 text-muted-foreground">
                      {String(inv.zatca_status ?? "")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OpsSection>

      <OpsSection title={t("revenueLadder")}>
        {ladder.length === 0 ? (
          <DegradedNote />
        ) : (
          <ul className="space-y-1.5 text-sm">
            {ladder.map((o, i) => (
              <li key={i} className="flex items-center justify-between gap-2">
                <span className="text-foreground">
                  {String((isAr ? o.name_ar : o.name_en) ?? "")}
                </span>
                <span className="text-muted-foreground">
                  {Number(o.price_sar ?? 0).toLocaleString()} {tc("sar")} ·{" "}
                  {String(o.price_unit ?? "")}
                </span>
              </li>
            ))}
          </ul>
        )}
      </OpsSection>
    </div>
  );
}
