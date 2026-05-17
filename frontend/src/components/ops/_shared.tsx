"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import type { AxiosResponse } from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

/** Generic one-shot fetch hook for an Ops Console surface. */
export function useOpsData<T = Record<string, unknown>>(
  fetcher: () => Promise<AxiosResponse>,
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetcher()
      .then((res) => {
        if (!cancelled) {
          setData(res.data as T);
          setError(null);
        }
      })
      .catch((e) => {
        if (!cancelled) setError(e?.message ?? "request failed");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { data, loading, error };
}

/** Doctrine governance-decision badge. */
export function GovernanceBadge({ decision }: { decision?: string }) {
  const t = useTranslations("ops");
  const ok = decision === "allow";
  return (
    <Badge
      variant="outline"
      className={cn(
        "text-[10px] font-medium",
        ok
          ? "text-emerald-400 border-emerald-400/40"
          : "text-amber-400 border-amber-400/40",
      )}
    >
      {t("governance")}: {decision ?? "—"}
    </Badge>
  );
}

/** Estimate vs. confirmed tag — confirmed numbers are ground truth. */
export function EstimateTag({ confirmed = false }: { confirmed?: boolean }) {
  const t = useTranslations("ops");
  return (
    <span
      className={cn(
        "text-[10px] px-1.5 py-0.5 rounded-full whitespace-nowrap",
        confirmed
          ? "bg-emerald-500/15 text-emerald-400"
          : "bg-amber-500/15 text-amber-400",
      )}
    >
      {confirmed ? t("confirmed") : t("estimate")}
    </span>
  );
}

/** A titled card section. */
export function OpsSection({
  title,
  children,
  right,
}: {
  title: string;
  children: React.ReactNode;
  right?: React.ReactNode;
}) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-2">
          <CardTitle className="text-base font-semibold">{title}</CardTitle>
          {right}
        </div>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

/** Degraded / empty-state note. */
export function DegradedNote({ note }: { note?: string | null }) {
  const t = useTranslations("ops");
  return (
    <p className="text-xs text-muted-foreground py-2">
      {note ? `${t("unavailable")} (${note})` : t("empty")}
    </p>
  );
}

/** Loading skeleton block. */
export function OpsSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <div
          key={i}
          className="rounded-2xl border border-border bg-card p-5 animate-pulse"
        >
          <div className="w-40 h-5 rounded bg-muted mb-4" />
          <div className="space-y-2">
            <div className="w-full h-3 rounded bg-muted" />
            <div className="w-3/4 h-3 rounded bg-muted" />
          </div>
        </div>
      ))}
    </div>
  );
}

/** Error card shown when the whole surface request fails. */
export function OpsError({ error }: { error: string }) {
  const t = useTranslations("common");
  return (
    <Card>
      <CardContent className="py-8 text-center">
        <p className="text-sm text-destructive">{t("error")}</p>
        <p className="text-xs text-muted-foreground mt-1">{error}</p>
      </CardContent>
    </Card>
  );
}

/** Top-of-surface header strip with the governance badge. */
export function SurfaceHeader({
  decision,
  isEstimate,
}: {
  decision?: string;
  isEstimate?: boolean;
}) {
  const t = useTranslations("ops");
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <GovernanceBadge decision={decision} />
      {isEstimate ? <EstimateTag /> : null}
      <span className="text-[10px] text-muted-foreground">{t("refresh")} ↻</span>
    </div>
  );
}
