"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Globe, TrendingUp, Users, DollarSign, CheckCircle, Clock, ArrowRight, ExternalLink, Target, Lightbulb } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency, formatRelativeTime } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface ExpansionOpportunity {
  id: string;
  region: string;
  market: string;
  potentialRevenue: number;
  currentRevenue: number;
  competitors: string[];
  readiness: number;
  priority: "high" | "medium" | "low";
  actions: string[];
  status: "exploring" | "preparing" | "active" | "paused";
}

const mockOpportunities: ExpansionOpportunity[] = [
  { id: "1", region: "UAE", market: "Dubai Enterprise", potentialRevenue: 2000000, currentRevenue: 250000, competitors: ["HubSpot", "Salesforce"], readiness: 75, priority: "high", actions: ["Hire local sales lead", "Setup Dubai office"], status: "active" },
  { id: "2", region: "Egypt", market: "Cairo Tech", potentialRevenue: 1200000, currentRevenue: 0, competitors: ["Zoho", "Freshworks"], readiness: 45, priority: "medium", actions: ["Market research", "Find local partner"], status: "exploring" },
  { id: "3", region: "Kuwait", market: "Kuwait Finance", potentialRevenue: 800000, currentRevenue: 80000, competitors: ["Oracle", "SAP"], readiness: 60, priority: "medium", actions: ["Attend GITEX Kuwait", "Build pipeline"], status: "preparing" },
  { id: "4", region: "Qatar", market: "Qatar Energy Sector", potentialRevenue: 1500000, currentRevenue: 0, competitors: ["Microsoft Dynamics", "Infor"], readiness: 30, priority: "low", actions: ["Initial outreach", "Partner search"], status: "exploring" },
  { id: "5", region: "Bahrain", market: "FinTech Hub", potentialRevenue: 600000, currentRevenue: 120000, competitors: ["Tipalti", "Bill.com"], readiness: 70, priority: "high", actions: ["Expand team", "Product localization"], status: "active" },
];

const statusConfig = {
  active: { label: "Active", labelAr: "نشط", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" },
  preparing: { label: "Preparing", labelAr: "قيد التحضير", color: "bg-amber-500/10 text-amber-500 border-amber-500/20" },
  exploring: { label: "Exploring", labelAr: "استكشاف", color: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
  paused: { label: "Paused", labelAr: "متوقف", color: "bg-muted text-muted-foreground border-border" },
};

const priorityConfig = {
  high: { label: "High", labelAr: "عالية", color: "text-red-500", bg: "bg-red-500/10" },
  medium: { label: "Medium", labelAr: "متوسطة", color: "text-amber-500", bg: "bg-amber-500/10" },
  low: { label: "Low", labelAr: "منخفضة", color: "text-blue-500", bg: "bg-blue-500/10" },
};

export default function ExpansionPage() {
  const [filter, setFilter] = useState<string>("all");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const filtered = filter === "all" ? mockOpportunities : mockOpportunities.filter((o) => o.status === filter);
  const totalPotential = filtered.reduce((s, o) => s + o.potentialRevenue, 0);
  const totalCurrent = filtered.reduce((s, o) => s + o.currentRevenue, 0);

  return (
    <AppLayout
      title={isRTL ? "فرص التوسع" : "Expansion Opportunities"}
      subtitle={isRTL ? "استكشاف وتوسع في أسواق جديدة" : "Explore and expand into new markets"}
    >
      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Globe className="w-4 h-4 text-gold-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "الأسواق" : "Markets"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{filtered.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-emerald-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "الإيرادات الحالية" : "Current Revenue"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(totalCurrent, locale)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-gold-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "الإيرادات المحتملة" : "Potential Revenue"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(totalPotential, locale)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Target className="w-4 h-4 text-amber-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "جاهزية متوسطة" : "Avg Readiness"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">
              {Math.round(filtered.reduce((s, o) => s + o.readiness, 0) / filtered.length)}%
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Status filters */}
      <div className="flex items-center gap-2 mb-6">
        {(["all", "active", "preparing", "exploring", "paused"] as const).map((s) => (
          <Button
            key={s}
            variant={filter === s ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter(s)}
          >
            {s === "all" ? (isRTL ? "الكل" : "All") : isRTL ? statusConfig[s].labelAr : statusConfig[s].label}
          </Button>
        ))}
      </div>

      {/* Opportunities */}
      <div className="space-y-4">
        {filtered.map((opp, idx) => {
          const status = statusConfig[opp.status];
          const priority = priorityConfig[opp.priority];
          const gap = opp.potentialRevenue - opp.currentRevenue;
          return (
            <motion.div
              key={opp.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.06 }}
            >
              <Card className="hover:border-gold-500/30 transition-all group">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Globe className="w-4 h-4 text-gold-500" />
                        <h3 className="text-sm font-semibold text-foreground">{opp.market}</h3>
                        <Badge variant="outline" className={cn("text-[10px]", status.color)}>
                          {isRTL ? status.labelAr : status.label}
                        </Badge>
                        <Badge variant="outline" className={cn("text-[10px]", priority.bg, priority.color)}>
                          {isRTL ? priority.labelAr : priority.label}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {opp.region} · {isRTL ? "المنافسون" : "Competitors"}: {opp.competitors.join(", ")}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-foreground">{formatCurrency(opp.potentialRevenue, locale)}</p>
                      <p className="text-[10px] text-muted-foreground">
                        {isRTL ? "محتمل" : "Potential"}
                      </p>
                    </div>
                  </div>

                  {/* Readiness bar */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-xs text-muted-foreground mb-1">
                      <span>{isRTL ? "جاهزية التوسع" : "Expansion Readiness"}</span>
                      <span className={cn("font-semibold", opp.readiness >= 70 ? "text-emerald-500" : opp.readiness >= 50 ? "text-amber-500" : "text-red-500")}>
                        {opp.readiness}%
                      </span>
                    </div>
                    <Progress
                      value={opp.readiness}
                      className={cn(
                        "h-1.5",
                        opp.readiness >= 70 ? "bg-emerald-500/20" : opp.readiness >= 50 ? "bg-amber-500/20" : "bg-red-500/20",
                      )}
                    />
                  </div>

                  {/* Actions & gap */}
                  <div className="flex items-center justify-between">
                    <div className="flex flex-wrap gap-1">
                      {opp.actions.map((action) => (
                        <Badge key={action} variant="secondary" className="text-[10px]">
                          {action}
                        </Badge>
                      ))}
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-muted-foreground">
                        {isRTL ? "الفجوة" : "Gap"}: <span className="font-semibold text-foreground">{formatCurrency(gap, locale)}</span>
                      </span>
                      <Button variant="ghost" size="sm">
                        <ExternalLink className="w-3.5 h-3.5" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </AppLayout>
  );
}
