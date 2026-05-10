"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { RefreshCw, Filter } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn, formatRelativeTime, getStatusColor } from "@/lib/utils";
import { api } from "@/lib/api";
import { workforceAgentToActivity } from "@/lib/api-normalize";
import type { AgentActivity, AgentType } from "@/types";

const agentIcons: Record<AgentType, string> = {
  outreach: "📤",
  scoring: "📊",
  compliance: "🛡️",
  intelligence: "🔍",
  orchestrator: "⚙️",
};

const agentColors: Record<AgentType, string> = {
  outreach: "bg-blue-500/10 text-blue-400",
  scoring: "bg-gold-500/10 text-gold-400",
  compliance: "bg-purple-500/10 text-purple-400",
  intelligence: "bg-emerald-500/10 text-emerald-400",
  orchestrator: "bg-orange-500/10 text-orange-400",
};

interface ActivityItemProps {
  activity: AgentActivity;
  index: number;
}

function ActivityItem({ activity, index }: ActivityItemProps) {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <motion.div
      initial={{ opacity: 0, x: isAr ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="flex items-start gap-4 p-4 rounded-xl hover:bg-muted/30 transition-colors border border-transparent hover:border-border/50 group"
    >
      <div
        className={cn(
          "w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0",
          agentColors[activity.agentType],
        )}
      >
        {agentIcons[activity.agentType]}
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span
            className={cn(
              "text-xs font-semibold px-2 py-0.5 rounded-full",
              agentColors[activity.agentType],
            )}
          >
            {t(`agentTypes.${activity.agentType}` as "agentTypes.outreach")}
          </span>
          {activity.requiresApproval && (
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-gold-500/10 text-gold-400 border border-gold-500/20 font-medium">
              {isAr ? "يتطلب موافقة" : "Needs Approval"}
            </span>
          )}
        </div>
        <p className="text-sm text-foreground mb-1">{activity.action}</p>
        <p className="text-xs text-muted-foreground">
          {isAr ? "الهدف:" : "Target:"} {activity.target}
        </p>
        {activity.duration && (
          <p className="text-[10px] text-muted-foreground/60 mt-1">
            {isAr ? "المدة:" : "Duration:"}{" "}
            {(activity.duration / 1000).toFixed(1)}s
          </p>
        )}
      </div>

      <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
        <Badge
          variant="outline"
          className={cn(
            "text-[10px] px-2 py-0.5 h-5",
            getStatusColor(activity.status),
          )}
        >
          {t(`status.${activity.status}` as "status.running")}
        </Badge>
        <span className="text-[10px] text-muted-foreground">
          {formatRelativeTime(activity.timestamp, locale)}
        </span>
      </div>
    </motion.div>
  );
}

function AgentStats({ activities }: { activities: AgentActivity[] }) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const stats = useMemo(() => {
    const needApproval = activities.filter((a) => a.requiresApproval).length;
    const byType = new Map<AgentType, number>();
    for (const a of activities) {
      byType.set(a.agentType, (byType.get(a.agentType) ?? 0) + 1);
    }
    const topType = [...byType.entries()].sort((a, b) => b[1] - a[1])[0];
    const roleKinds = new Set(activities.map((a) => a.agentType)).size;

    return [
      {
        label: isAr ? "وكلاء مسجّلون" : "Registered agents",
        value: activities.length,
        color: "text-blue-400",
        bg: "bg-blue-400/10",
      },
      {
        label: isAr ? "يتطلب موافقة" : "Needs approval",
        value: needApproval,
        color: "text-gold-400",
        bg: "bg-gold-400/10",
      },
      {
        label: isAr ? "أنواع الأدوار" : "Role kinds",
        value: roleKinds,
        color: "text-emerald-400",
        bg: "bg-emerald-400/10",
      },
      {
        label: isAr ? "النوع الأكثر تكرارًا" : "Most common role",
        value: topType ? topType[1] : 0,
        color: "text-muted-foreground",
        bg: "bg-muted/50",
        sub: topType ? String(topType[0]) : "—",
      },
    ];
  }, [activities, isAr]);

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.07 }}
          className={cn("rounded-xl p-4 border border-border", stat.bg)}
        >
          <p className={cn("text-2xl font-bold tabular-nums", stat.color)}>
            {stat.value}
          </p>
          <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
          {"sub" in stat && stat.sub && (
            <p className="text-[10px] text-muted-foreground/80 mt-0.5 truncate">
              {String(stat.sub)}
            </p>
          )}
        </motion.div>
      ))}
    </div>
  );
}

export function ActivityFeed() {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";

  const agentsQuery = useQuery({
    queryKey: ["agents", "workforce-registry"],
    queryFn: async () => {
      const res = await api.getAIWorkforce();
      return res.data;
    },
  });

  const activities = useMemo(() => {
    if (!agentsQuery.data || typeof agentsQuery.data !== "object") {
      return [];
    }
    const root = agentsQuery.data as Record<string, unknown>;
    const agents = root.agents;
    if (!Array.isArray(agents)) return [];
    return agents.map((row) =>
      workforceAgentToActivity(row as Record<string, unknown>, isAr),
    );
  }, [agentsQuery.data, isAr]);

  return (
    <div>
      {agentsQuery.isError && (
        <div
          role="alert"
          className="mb-4 rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm"
        >
          <p>
            {isAr
              ? "تعذر تحميل سجل الوكلاء. تحقق من الـ API."
              : "Could not load agent registry. Check the API."}
          </p>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="mt-2"
            onClick={() => agentsQuery.refetch()}
          >
            <RefreshCw className="w-3.5 h-3.5 me-1.5" />
            {isAr ? "إعادة المحاولة" : "Retry"}
          </Button>
        </div>
      )}

      <AgentStats activities={activities} />

      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base font-semibold">{t("title")}</CardTitle>
            <div className="flex items-center gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => agentsQuery.refetch()}
                disabled={agentsQuery.isFetching}
              >
                <RefreshCw
                  className={cn(
                    "w-3.5 h-3.5 me-1.5",
                    agentsQuery.isFetching && "animate-spin",
                  )}
                />
                {isAr ? "تحديث" : "Refresh"}
              </Button>
              <Button variant="outline" size="sm" type="button">
                <Filter className="w-3.5 h-3.5 me-1.5" />
                {isAr ? "تصفية" : "Filter"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-20rem)]">
            <div className="p-2">
              {agentsQuery.isLoading ? (
                <div className="space-y-3 p-4">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <div
                      key={i}
                      className="h-20 rounded-xl bg-muted/50 animate-pulse"
                    />
                  ))}
                </div>
              ) : activities.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-12 px-4">
                  {isAr
                    ? "لا يوجد وكلاء للعرض. تأكد أن الخادم يعمل وأن المسار /api/v1/ai-workforce/agents متاح."
                    : "No agents to display. Ensure the server is running and /api/v1/ai-workforce/agents is available."}
                </p>
              ) : (
                <AnimatePresence>
                  {activities.map((activity, i) => (
                    <ActivityItem key={activity.id} activity={activity} index={i} />
                  ))}
                </AnimatePresence>
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
