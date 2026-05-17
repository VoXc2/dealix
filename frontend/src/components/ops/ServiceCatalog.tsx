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

interface Offer {
  rung?: number;
  id?: string;
  name_ar?: string;
  name_en?: string;
  price_sar?: number;
  price_unit?: string;
  duration_days?: number;
  deliverables?: string[];
  kpi_commitment_ar?: string;
  kpi_commitment_en?: string;
  hard_gates?: string[];
  journey_stage?: string;
}
interface CatalogData {
  governance_decision?: string;
  is_estimate?: boolean;
  ladder?: Offer[];
  entry_offers?: Offer[];
  hard_gates?: string[];
  offer_count?: number;
  note?: string;
}

export function ServiceCatalog() {
  const t = useTranslations("ops.serviceCatalog");
  const tc = useTranslations("common");
  const locale = useLocale();
  const isAr = locale === "ar";
  const { data, loading, error } = useOpsData<CatalogData>(api.getOpsCatalog);

  if (loading) return <OpsSkeleton />;
  if (error || !data) return <OpsError error={error ?? "no data"} />;

  const ladder = data.ladder ?? [];

  return (
    <div className="space-y-6">
      <SurfaceHeader decision={data.governance_decision} isEstimate={data.is_estimate} />

      <OpsSection title={t("ladder")}>
        {data.note || ladder.length === 0 ? (
          <DegradedNote note={data.note} />
        ) : (
          <div className="space-y-3">
            {ladder.map((o) => (
              <div
                key={o.id}
                className="rounded-xl border border-border bg-muted/30 p-4"
              >
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex items-center gap-3">
                    <span className="flex-shrink-0 w-7 h-7 rounded-lg bg-gold-500/15 text-gold-400 flex items-center justify-center text-xs font-bold">
                      {o.rung}
                    </span>
                    <div>
                      <p className="text-sm font-semibold text-foreground">
                        {isAr ? o.name_ar : o.name_en}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {o.journey_stage}
                      </p>
                    </div>
                  </div>
                  <div className="text-end">
                    <p className="text-sm font-bold text-foreground">
                      {o.price_sar?.toLocaleString()} {tc("sar")}
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      {o.price_unit} · {o.duration_days}d
                    </p>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  {isAr ? o.kpi_commitment_ar : o.kpi_commitment_en}
                </p>
                {(o.deliverables ?? []).length > 0 ? (
                  <ul className="mt-2 flex flex-wrap gap-1.5">
                    {(o.deliverables ?? []).map((d, i) => (
                      <li
                        key={i}
                        className="text-[10px] bg-background border border-border rounded px-1.5 py-0.5 text-muted-foreground"
                      >
                        {d}
                      </li>
                    ))}
                  </ul>
                ) : null}
              </div>
            ))}
          </div>
        )}
      </OpsSection>

      <OpsSection title={t("hardGates")}>
        <div className="flex flex-wrap gap-2">
          {(data.hard_gates ?? []).length === 0 ? (
            <DegradedNote />
          ) : (
            (data.hard_gates ?? []).map((g) => (
              <Badge
                key={g}
                variant="outline"
                className="text-[10px] text-destructive border-destructive/40"
              >
                {g}
              </Badge>
            ))
          )}
        </div>
      </OpsSection>
    </div>
  );
}
