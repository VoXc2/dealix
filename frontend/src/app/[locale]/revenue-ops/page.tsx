"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

type Json = Record<string, unknown>;

export default function RevenueOpsPage() {
  const t = useTranslations("revenueOps");
  const tc = useTranslations("common");
  const [northStar, setNorthStar] = useState<Json | null>(null);
  const [pipeline, setPipeline] = useState<Json | null>(null);
  const [leadId, setLeadId] = useState("");
  const [level, setLevel] = useState<Json | null>(null);
  const [levelError, setLevelError] = useState(false);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    const [ns, pl] = await Promise.all([
      api.getRevenuePipelineNorthStar(),
      api.getPipeline(),
    ]);
    setNorthStar(ns.data as Json);
    setPipeline(pl.data as Json);
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const lookup = async () => {
    if (!leadId.trim()) return;
    setLoading(true);
    setLevelError(false);
    setLevel(null);
    try {
      const res = await api.getRevenuePipelineLeadLevel(leadId.trim());
      setLevel(res.data as Json);
    } catch {
      setLevelError(true);
    } finally {
      setLoading(false);
    }
  };

  const summary = (pipeline?.pipeline_summary ?? {}) as Json;

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <p className="text-sm text-muted-foreground mb-6">{t("draftNote")}</p>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("northStarTitle")}</h2>
        <p className="text-sm text-muted-foreground mb-4">{t("northStarHint")}</p>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-xl border border-border bg-card/40 p-5">
            <p className="text-3xl font-bold text-gold-400">
              {String(northStar?.governed_value_decisions_created ?? "—")}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {t("northStarTitle")}
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-5">
            <p className="text-3xl font-bold">
              {String(northStar?.candidate_decisions ?? "—")}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              {t("candidates")}
            </p>
          </div>
        </div>
      </section>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("pipelineTitle")}</h2>
        {pipeline ? (
          <div className="grid gap-3 sm:grid-cols-4">
            {(["total_leads", "commitments", "paid", "total_revenue_sar"] as const).map(
              (k) => (
                <div
                  key={k}
                  className="rounded-xl border border-border bg-muted/20 p-4"
                >
                  <p className="text-xl font-semibold">
                    {String(summary[k] ?? 0)}
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">{k}</p>
                </div>
              ),
            )}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">{tc("loading")}</p>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("levelTitle")}</h2>
        <div className="flex flex-wrap items-center gap-3">
          <Input
            value={leadId}
            onChange={(e) => setLeadId(e.target.value)}
            placeholder={t("leadIdLabel")}
            className="max-w-xs"
          />
          <Button onClick={() => void lookup()} disabled={loading}>
            {t("lookup")}
          </Button>
        </div>
        {levelError && (
          <p className="mt-3 text-sm text-destructive">{tc("noData")}</p>
        )}
        {level && (
          <div className="mt-4 rounded-xl border border-border bg-muted/20 p-4">
            <p className="text-sm">
              <span className="font-medium">{String(level.stage)}</span>
              {" · "}
              <span className="text-gold-400 font-semibold">
                {String(level.level)}
              </span>
              {" · "}
              <span className="text-muted-foreground">
                {String(level.event_label)}
              </span>
            </p>
          </div>
        )}
      </section>
    </AppLayout>
  );
}
