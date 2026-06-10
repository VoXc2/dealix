"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured } from "@/lib/opsAdmin";

type ExpansionPayload = {
  targeting?: {
    pool_rows?: number;
    wave2_ready?: boolean;
    wave3_prep_ready?: boolean;
  };
  social?: { posts?: number; cycle_weeks?: number; queue_ready_24w?: boolean };
  next_actions_ar?: string[];
};

export function OpsExpansionStatusCard() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<ExpansionPayload | null>(null);

  useEffect(() => {
    if (!isOpsConfigured()) return;
    api
      .getFounderExpansionStatus(getAdminApiKey(), 8)
      .then((r) => setData(r.data as ExpansionPayload))
      .catch(() => setData(null));
  }, []);

  if (!data) return null;

  return (
    <Card className="p-4 border-border/80">
      <h2 className="font-semibold text-sm mb-2">
        {isAr ? "توسعة تشغيلية" : "Ops expansion"}
      </h2>
      <p className="text-xs text-muted-foreground">
        {isAr ? "وكالات:" : "Agencies:"} {data.targeting?.pool_rows ?? 0}
        {isAr ? " · سوشال:" : " · social:"} {data.social?.posts ?? 0} / {data.social?.cycle_weeks ?? 0}w
      </p>
      <ul className="text-xs mt-2 space-y-1 list-disc mr-5">
        {(data.next_actions_ar ?? []).slice(0, 4).map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
      <p className="text-xs mt-2" dir="ltr">
        py -3 scripts/expand_commercial_ops_all.py --wave2
      </p>
    </Card>
  );
}
