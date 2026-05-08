"use client";

import { useState, useEffect } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { KPICard } from "./KPICard";
import { RevenueChart } from "./RevenueChart";
import { DealPipelineChart } from "./DealPipelineChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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

const mockActivities: Activity[] = [
  {
    id: "1",
    agent: "outreach",
    actionAr: "أرسل رسالة تواصل إلى شركة أرامكو",
    actionEn: "Sent outreach to Aramco Company",
    status: "completed",
    timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
  },
  {
    id: "2",
    agent: "scoring",
    actionAr: "قيّم 12 عميلاً محتملاً جديداً",
    actionEn: "Scored 12 new leads",
    status: "completed",
    timestamp: new Date(Date.now() - 18 * 60000).toISOString(),
  },
  {
    id: "3",
    agent: "compliance",
    actionAr: "مراجعة امتثال حملة التسويق Q4",
    actionEn: "Reviewing Q4 campaign compliance",
    status: "running",
    timestamp: new Date(Date.now() - 2 * 60000).toISOString(),
  },
  {
    id: "4",
    agent: "intelligence",
    actionAr: "رصد إشارات التوظيف في القطاع المالي",
    actionEn: "Monitoring hiring signals in fintech",
    status: "running",
    timestamp: new Date(Date.now() - 8 * 60000).toISOString(),
  },
  {
    id: "5",
    agent: "orchestrator",
    actionAr: "جدولة دورة النمو اليومية",
    actionEn: "Scheduled daily growth cycle",
    status: "pending",
    timestamp: new Date(Date.now() - 30 * 60000).toISOString(),
  },
];

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

export function DashboardContent() {
  const t = useTranslations();
  const locale = useLocale();
  const isAr = locale === "ar";

  const [kpiMetrics, setKpiMetrics] = useState<KPIMetric[] | null>(null);
  const [activities, setActivities] = useState<Activity[] | null>(null);
  const [loadingKpi, setLoadingKpi] = useState(true);
  const [loadingActivities, setLoadingActivities] = useState(true);

  const defaultKpiMetrics: KPIMetric[] = [
    {
      label: t("dashboard.kpi.totalRevenue"),
      value: 42800000,
      change: 18.5,
      trend: "up",
      icon: "💰",
      format: "currency",
    },
    {
      label: t("dashboard.kpi.activeDeals"),
      value: 104,
      change: 12.3,
      trend: "up",
      icon: "📊",
      format: "number",
    },
    {
      label: t("dashboard.kpi.conversionRate"),
      value: 23.4,
      change: 3.2,
      trend: "up",
      icon: "🎯",
      format: "percentage",
    },
    {
      label: t("dashboard.kpi.aiActions"),
      value: 2847,
      change: 47.1,
      trend: "up",
      icon: "🤖",
      format: "number",
    },
  ];

  useEffect(() => {
    let cancelled = false;

    async function fetchKpi() {
      try {
        const res = await api.getDashboardMetrics();
        if (!cancelled && res.data) {
          const data = res.data.data ?? res.data;
          if (Array.isArray(data.metrics) && data.metrics.length > 0) {
            setKpiMetrics(
              data.metrics.map((m: Record<string, unknown>, i: number) => ({
                label:
                  (m.label as string) ?? defaultKpiMetrics[i]?.label ?? "",
                value: (m.value as number) ?? defaultKpiMetrics[i]?.value ?? 0,
                change:
                  (m.change as number) ?? defaultKpiMetrics[i]?.change ?? 0,
                trend:
                  (m.trend as string) ?? defaultKpiMetrics[i]?.trend ?? "neutral",
                icon:
                  (m.icon as string) ?? defaultKpiMetrics[i]?.icon ?? "📊",
                format:
                  (m.format as string) ?? defaultKpiMetrics[i]?.format ?? "number",
              }))
            );
          } else {
            setKpiMetrics(defaultKpiMetrics);
          }
        }
      } catch {
        if (!cancelled) setKpiMetrics(defaultKpiMetrics);
      } finally {
        if (!cancelled) setLoadingKpi(false);
      }
    }

    fetchKpi();
    return () => { cancelled = true; };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function fetchActivities() {
      try {
        const res = await api.getCommandCenter();
        if (!cancelled && res.data) {
          const data = res.data.data ?? res.data;
          const items: unknown[] =
            data.recent_decisions ?? data.decisions ?? data.activities ?? [];
          if (Array.isArray(items) && items.length > 0) {
            setActivities(
              items.map((raw: unknown, i: number) => {
                const item = raw as Record<string, unknown>;
                return {
                id: (item.id as string) ?? String(i + 1),
                agent: (item.agent as string) ?? (item.agent_type as string) ?? "orchestrator",
                actionAr: (item.action_ar as string) ?? (item.action as string) ?? "",
                actionEn: (item.action_en as string) ?? (item.action as string) ?? "",
                status: (item.status as string) ?? "completed",
                timestamp:
                  (item.timestamp as string) ??
                  (item.created_at as string) ??
                  new Date().toISOString(),
                };
              })
            );
          } else {
            setActivities(mockActivities);
          }
        }
      } catch {
        if (!cancelled) setActivities(mockActivities);
      } finally {
        if (!cancelled) setLoadingActivities(false);
      }
    }

    fetchActivities();
    return () => { cancelled = true; };
  }, []);

  const displayedKpi = kpiMetrics ?? defaultKpiMetrics;
  const displayedActivities = activities ?? mockActivities;

  const agentLabels: Record<string, string> = {
    outreach: isAr ? "وكيل التواصل" : "Outreach",
    scoring: isAr ? "وكيل التقييم" : "Scoring",
    compliance: isAr ? "وكيل الامتثال" : "Compliance",
    intelligence: isAr ? "وكيل الاستخبارات" : "Intelligence",
    orchestrator: isAr ? "المنسق" : "Orchestrator",
  };

  return (
    <div className="space-y-6">
      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {loadingKpi
          ? Array.from({ length: 4 }).map((_, i) => (
              <KPISkeletonCard key={i} />
            ))
          : displayedKpi.map((metric, i) => (
              <KPICard key={metric.label} metric={metric} index={i} />
            ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <RevenueChart />
        <DealPipelineChart />
      </div>

      {/* Activity Feed */}
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
              {loadingActivities ? (
                Array.from({ length: 4 }).map((_, i) => (
                  <ActivitySkeletonRow key={i} />
                ))
              ) : displayedActivities.map((activity, i) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: isAr ? 10 : -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + i * 0.07 }}
                  className="flex items-start gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors"
                >
                  <div className="w-8 h-8 rounded-xl bg-muted flex items-center justify-center text-base flex-shrink-0">
                    {activity.agent === "outreach" ? "📤" :
                     activity.agent === "scoring" ? "📊" :
                     activity.agent === "compliance" ? "🛡️" :
                     activity.agent === "intelligence" ? "🔍" : "⚙️"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-foreground">
                      {agentLabels[activity.agent]}
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
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
