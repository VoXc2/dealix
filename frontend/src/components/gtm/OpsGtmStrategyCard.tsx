"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";

type AbmTarget = {
  company?: string;
  abm_score?: number;
  priority?: string;
  next_action?: string;
};

export type GtmStackPayload = {
  dual_track?: {
    recommended_track?: string;
    reason_ar?: string;
    high_priority_stale?: number;
  };
  abm_wave1?: {
    active_rows?: number;
    min_required?: number;
    wave1_ready?: boolean;
    top_targets?: AbmTarget[];
  };
  ttv?: {
    ttv_discovery_days_avg?: number | null;
    targets_ar?: { ttv_discovery_max_days?: number };
  };
  focus_ar?: string[];
};

type Props = {
  gtm: GtmStackPayload | null | undefined;
};

export function OpsGtmStrategyCard({ gtm }: Props) {
  const locale = useLocale();
  const isAr = locale === "ar";
  if (!gtm?.dual_track) return null;

  const track = gtm.dual_track.recommended_track ?? "—";
  const abm = gtm.abm_wave1;
  const ttv = gtm.ttv;

  return (
    <Card className="p-4 border-emerald-500/30 bg-emerald-500/5">
      <h2 className="font-semibold mb-2">
        {isAr ? "استراتيجية GTM (اليوم)" : "GTM strategy (today)"}
      </h2>
      <p className="text-sm">
        {isAr ? "المسار الموصى:" : "Recommended track:"}{" "}
        <span className="font-mono font-semibold">{track}</span>
      </p>
      <p className="text-xs text-muted-foreground mt-1">{gtm.dual_track.reason_ar}</p>
      {abm && (
        <p className="text-xs mt-2">
          ABM wave 1: {abm.active_rows ?? 0}/{abm.min_required ?? 30}{" "}
          {abm.wave1_ready
            ? isAr
              ? "· جاهز"
              : "· ready"
            : isAr
              ? "· عبّئ القائمة"
              : "· fill list"}
        </p>
      )}
      {ttv?.ttv_discovery_days_avg != null && (
        <p className="text-xs text-muted-foreground">
          TTV discovery: {ttv.ttv_discovery_days_avg}d (max {ttv.targets_ar?.ttv_discovery_max_days ?? 14})
        </p>
      )}
      <ul className="text-xs mt-2 space-y-1 list-disc mr-5">
        {(gtm.focus_ar ?? []).slice(0, 3).map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
      {(abm?.top_targets ?? []).length > 0 && (
        <div className="mt-3 text-xs">
          <p className="font-medium mb-1">{isAr ? "أعلى ABM:" : "Top ABM:"}</p>
          <ul className="space-y-1">
            {abm!.top_targets!.slice(0, 3).map((t, i) => (
              <li key={`${t.company}-${i}`}>
                {t.company} · score {t.abm_score}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="flex flex-wrap gap-3 mt-3 text-xs">
        <Link href={`/${locale}/ops/war-room`} className="text-primary underline">
          War Room
        </Link>
        <Link href={`/${locale}/proof-pack`} className="text-primary underline">
          Proof
        </Link>
      </div>
    </Card>
  );
}
