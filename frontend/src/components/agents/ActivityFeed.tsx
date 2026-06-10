"use client";

import { useState, useEffect } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { RefreshCw, Filter } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn, formatRelativeTime, getStatusColor } from "@/lib/utils";
import type { AgentActivity, AgentType } from "@/types";

const mockActivities: AgentActivity[] = [
  {
    id: "a1",
    agentType: "outreach",
    action: "أرسل رسائل تواصل مخصصة لـ 8 شركات في قطاع النفط",
    target: "قطاع النفط والطاقة",
    status: "completed",
    timestamp: new Date(Date.now() - 3 * 60000).toISOString(),
    duration: 12400,
  },
  {
    id: "a2",
    agentType: "scoring",
    action: "تقييم 23 عميلاً محتملاً بناءً على إشارات التمويل",
    target: "قاعدة العملاء Q1",
    status: "completed",
    timestamp: new Date(Date.now() - 8 * 60000).toISOString(),
    duration: 5200,
    requiresApproval: false,
  },
  {
    id: "a3",
    agentType: "compliance",
    action: "مراجعة امتثال حملة البريد الإلكتروني للشريعة الإسلامية",
    target: "حملة رمضان 2025",
    status: "running",
    timestamp: new Date(Date.now() - 1 * 60000).toISOString(),
    requiresApproval: true,
  },
  {
    id: "a4",
    agentType: "intelligence",
    action: "رصد إشارات التوظيف في القطاع المالي - اكتشاف 5 فرص",
    target: "القطاع المالي - MENA",
    status: "completed",
    timestamp: new Date(Date.now() - 15 * 60000).toISOString(),
    duration: 34100,
  },
  {
    id: "a5",
    agentType: "orchestrator",
    action: "جدولة 14 مهمة وكيل للدورة اليومية",
    target: "الدورة اليومية 07-05-2025",
    status: "completed",
    timestamp: new Date(Date.now() - 25 * 60000).toISOString(),
    duration: 800,
  },
  {
    id: "a6",
    agentType: "outreach",
    action: "متابعة تلقائية مع 3 عملاء لم يستجيبوا",
    target: "صندوق المتابعة",
    status: "pending",
    timestamp: new Date(Date.now() - 35 * 60000).toISOString(),
    requiresApproval: true,
  },
  {
    id: "a7",
    agentType: "scoring",
    action: "إعادة تقييم العملاء بعد إعلان تمويل جولة B",
    target: "شركات السلسلة B",
    status: "failed",
    timestamp: new Date(Date.now() - 45 * 60000).toISOString(),
    duration: 2100,
  },
  {
    id: "a8",
    agentType: "intelligence",
    action: "تحليل تقارير Q4 من المنافسين الرئيسيين",
    target: "تحليل السوق السعودي",
    status: "completed",
    timestamp: new Date(Date.now() - 60 * 60000).toISOString(),
    duration: 28700,
  },
];

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
      {/* Agent icon */}
      <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0", agentColors[activity.agentType])}>
        {agentIcons[activity.agentType]}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className={cn("text-xs font-semibold px-2 py-0.5 rounded-full", agentColors[activity.agentType])}>
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
            {isAr ? "المدة:" : "Duration:"} {(activity.duration / 1000).toFixed(1)}s
          </p>
        )}
      </div>

      {/* Status & time */}
      <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
        <Badge
          variant="outline"
          className={cn("text-[10px] px-2 py-0.5 h-5", getStatusColor(activity.status))}
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

// Stats card
function AgentStats() {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";

  const stats = [
    { label: isAr ? "يعمل" : "Running", value: 2, color: "text-blue-400", bg: "bg-blue-400/10" },
    { label: isAr ? "مكتمل" : "Completed", value: 156, color: "text-emerald-400", bg: "bg-emerald-400/10" },
    { label: isAr ? "قيد الانتظار" : "Pending", value: 8, color: "text-gold-400", bg: "bg-gold-400/10" },
    { label: isAr ? "فشل" : "Failed", value: 3, color: "text-red-400", bg: "bg-red-400/10" },
  ];

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
          <p className={cn("text-2xl font-bold tabular-nums", stat.color)}>{stat.value}</p>
          <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
        </motion.div>
      ))}
    </div>
  );
}

export function ActivityFeed() {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [activities, setActivities] = useState(mockActivities);
  const [isLive, setIsLive] = useState(true);

  // Simulate live updates
  useEffect(() => {
    if (!isLive) return;
    const interval = setInterval(() => {
      const newActivity: AgentActivity = {
        id: `live-${Date.now()}`,
        agentType: ["outreach", "scoring", "intelligence"][Math.floor(Math.random() * 3)] as AgentType,
        action: isAr
          ? "نشاط جديد من الذكاء الاصطناعي..."
          : "New AI agent action...",
        target: isAr ? "هدف تلقائي" : "Auto target",
        status: "running",
        timestamp: new Date().toISOString(),
      };
      setActivities((prev) => [newActivity, ...prev.slice(0, 19)]);
    }, 15000);
    return () => clearInterval(interval);
  }, [isLive, isAr]);

  return (
    <div>
      <AgentStats />
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base font-semibold">{t("title")}</CardTitle>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsLive(!isLive)}
                className={cn(
                  "flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border transition-colors",
                  isLive
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : "bg-muted text-muted-foreground border-border"
                )}
              >
                <span className={cn("w-1.5 h-1.5 rounded-full", isLive ? "bg-emerald-400 animate-pulse" : "bg-muted-foreground")} />
                {isLive ? (isAr ? "مباشر" : "Live") : (isAr ? "متوقف" : "Paused")}
              </button>
              <Button variant="outline" size="sm">
                <Filter className="w-3.5 h-3.5 me-1.5" />
                {isAr ? "تصفية" : "Filter"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-20rem)]">
            <div className="p-2">
              <AnimatePresence>
                {activities.map((activity, i) => (
                  <ActivityItem key={activity.id} activity={activity} index={i} />
                ))}
              </AnimatePresence>
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
