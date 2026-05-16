"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { KPICard } from "./KPICard";
import { RevenueChart } from "./RevenueChart";
import { DealPipelineChart } from "./DealPipelineChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatRelativeTime, getStatusColor } from "@/lib/utils";
import { api } from "@/lib/api";
import type { KPIMetric } from "@/types";

interface Activity {
  id: string;
  agent: string;
  actionAr: string;
  actionEn: string;
  status: string;
  timestamp: string;
}

function KPISkeletonCard() {
  return (
    <div className="relative rounded-2xl border border-border bg-card p-5 overflow-hidden animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="w-8 h-8 rounded-lg bg-muted" />
        <div className="w-16 h-6 rounded-full bg-muted" />
      </div>
      <div className="w-28 h-7 rounded bg-muted mb-2" />
      <div className="w-20 h-4 rounded bg-muted" />
    </div>
  );
}

function ActivitySkeletonRow() {
  return (
    <div className="flex items-start gap-3 p-3 rounded-xl animate-pulse">
      <div className="w-8 h-8 rounded-xl bg-muted flex-shrink-0" />
      <div className="flex-1 min-w-0 space-y-2">
        <div className="w-24 h-4 rounded bg-muted" />
        <div className="w-48 h-3 rounded bg-muted" />
      </div>
      <div className="flex flex-col items-end gap-1 flex-shrink-0">
        <div className="w-16 h-5 rounded bg-muted" />
        <div className="w-12 h-3 rounded bg-muted" />
      </div>
    </div>
  );
}

function parseKpiFromResponse(
  raw: unknown,
  defaults: KPIMetric[],
): KPIMetric[] | null {
  if (!raw || typeof raw !== "object") return null;
  const root = raw as Record<string, unknown>;
  const data = (root.data ?? root) as Record<string, unknown>;
  const metrics = data.metrics;
  if (!Array.isArray(metrics) || metrics.length === 0) return null;
  return metrics.map((m: unknown, i: number) => {
    const row = m as Record<string, unknown>;
    const d = defaults[i];
    return {
      label: (row.label as string) ?? d?.label ?? "",
      value: (row.value as number) ?? d?.value ?? 0,
      change: (row.change as number) ?? d?.change ?? 0,
      trend: (row.trend as KPIMetric["trend"]) ?? d?.trend ?? "neutral",
      icon: (row.icon as string) ?? d?.icon ?? "📊",
      format: (row.format as KPIMetric["format"]) ?? d?.format ?? "number",
    };
  });
}

function parseActivitiesFromCommandCenter(raw: unknown): Activity[] | null {
  if (!raw || typeof raw !== "object") return null;
  const root = raw as Record<string, unknown>;
  const data = (root.data ?? root) as Record<string, unknown>;
  const items: unknown[] =
    (data.recent_decisions as unknown[]) ??
    (data.decisions as unknown[]) ??
    (data.activities as unknown[]) ??
    [];
  if (!Array.isArray(items) || items.length === 0) return null;
  return items.map((rawItem: unknown, i: number) => {
    const item = rawItem as Record<string, unknown>;
    return {
      id: (item.id as string) ?? String(i + 1),
      agent:
        (item.agent as string) ??
        (item.agent_type as string) ??
        "orchestrator",
      actionAr:
        (item.action_ar as string) ?? (item.action as string) ?? "",
      actionEn:
        (item.action_en as string) ?? (item.action as string) ?? "",
      status: (item.status as string) ?? "completed",
      timestamp:
        (item.timestamp as string) ??
        (item.created_at as string) ??
        new Date().toISOString(),
    };
  });
}

export function DashboardContent() {
  const t = useTranslations();
  const locale = useLocale();
  const isAr = locale === "ar";

  const defaultKpiMetrics = useMemo<KPIMetric[]>(
    () => [
      {
        label: t("dashboard.kpi.totalRevenue"),
        value: 0,
        change: 0,
        trend: "neutral",
        icon: "💰",
        format: "currency",
      },
      {
        label: t("dashboard.kpi.activeDeals"),
        value: 0,
        change: 0,
        trend: "neutral",
        icon: "📊",
        format: "number",
      },
      {
        label: t("dashboard.kpi.conversionRate"),
        value: 0,
        change: 0,
        trend: "neutral",
        icon: "🎯",
        format: "percentage",
      },
      {
        label: t("dashboard.kpi.aiActions"),
        value: 0,
        change: 0,
        trend: "neutral",
        icon: "🤖",
        format: "number",
      },
    ],
    [t],
  );

  const kpiQuery = useQuery({
    queryKey: ["dashboard", "metrics"],
    queryFn: async () => {
      const res = await api.getDashboardMetrics();
      return res.data;
    },
  });

  const activityQuery = useQuery({
    queryKey: ["dashboard", "command-center"],
    queryFn: async () => {
      const res = await api.getCommandCenter();
      return res.data;
    },
  });

  const kpiMetrics =
    kpiQuery.data != null
      ? parseKpiFromResponse(kpiQuery.data, defaultKpiMetrics)
      : null;
  const displayedKpi = kpiMetrics ?? defaultKpiMetrics;

  const activities =
    activityQuery.data != null
      ? parseActivitiesFromCommandCenter(activityQuery.data)
      : null;

  const agentLabels: Record<string, string> = {
    outreach: isAr ? "وكيل التواصل" : "Outreach",
    scoring: isAr ? "وكيل التقييم" : "Scoring",
    compliance: isAr ? "وكيل الامتثال" : "Compliance",
    intelligence: isAr ? "وكيل الاستخبارات" : "Intelligence",
    orchestrator: isAr ? "المنسق" : "Orchestrator",
  };

  const showKpiError = kpiQuery.isError;
  const showActivityError = activityQuery.isError;

  return (
    <div className="space-y-6">
      {(showKpiError || showActivityError) && (
        <div
          role="alert"
          className="rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-foreground"
        >
          <p className="font-medium">
            {isAr
              ? "تعذر تحميل بعض بيانات لوحة التحكم من الخادم."
              : "Some dashboard data could not be loaded from the server."}
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            {showKpiError && (
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => kpiQuery.refetch()}
              >
                {isAr ? "إعادة محاولة المؤشرات" : "Retry metrics"}
              </Button>
            )}
            {showActivityError && (
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => activityQuery.refetch()}
              >
                {isAr ? "إعادة محاولة النشاط" : "Retry activity"}
              </Button>
            )}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiQuery.isLoading
          ? Array.from({ length: 4 }).map((_, i) => (
              <KPISkeletonCard key={i} />
            ))
          : displayedKpi.map((metric, i) => (
              <KPICard key={metric.label} metric={metric} index={i} />
            ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <RevenueChart />
        <DealPipelineChart />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base font-semibold">
                {t("dashboard.recentActivity")}
              </CardTitle>
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-xs text-emerald-400 font-medium">
                  {isAr ? "مباشر" : "Live"}
                </span>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {activityQuery.isLoading ? (
                Array.from({ length: 4 }).map((_, i) => (
                  <ActivitySkeletonRow key={i} />
                ))
              ) : activities && activities.length > 0 ? (
                activities.map((activity, i) => (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: isAr ? 10 : -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + i * 0.07 }}
                    className="flex items-start gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors"
                  >
                    <div className="w-8 h-8 rounded-xl bg-muted flex items-center justify-center text-base flex-shrink-0">
                      {activity.agent === "outreach"
                        ? "📤"
                        : activity.agent === "scoring"
                          ? "📊"
                          : activity.agent === "compliance"
                            ? "🛡️"
                            : activity.agent === "intelligence"
                              ? "🔍"
                              : "⚙️"}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-foreground">
                        {agentLabels[activity.agent] ?? activity.agent}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5 truncate">
                        {isAr ? activity.actionAr : activity.actionEn}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-1 flex-shrink-0">
                      <Badge
                        className={`text-[10px] px-1.5 py-0 h-5 ${getStatusColor(activity.status)}`}
                        variant="outline"
                      >
                        {t(`agents.status.${activity.status}` as "agents.status.running")}
                      </Badge>
                      <span className="text-[10px] text-muted-foreground">
                        {formatRelativeTime(activity.timestamp, locale)}
                      </span>
                    </div>
                  </motion.div>
                ))
              ) : (
                <p className="text-sm text-muted-foreground px-2 py-6 text-center">
                  {activityQuery.isError
                    ? isAr
                      ? "لا يوجد نشاط للعرض. تحقق من الاتصال بالـ API."
                      : "No activity to display. Check API connectivity."
                    : isAr
                      ? "لا يوجد نشاط حديث بعد. ربط الـ Command Center سيملأ هذه القائمة."
                      : "No recent activity yet. Command Center data will appear here when available."}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
