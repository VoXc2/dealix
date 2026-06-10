"use client";

import { motion } from "framer-motion";
import { Clock, AlertTriangle, CheckCircle, TrendingUp } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SLAEntry {
  id: string;
  metric: string;
  metricAr: string;
  target: number;
  current: number;
  status: "compliant" | "at_risk" | "breached";
  trend: "up" | "down" | "stable";
}

interface SLADashboardProps {
  entries: SLAEntry[];
  overallCompliance: number;
}

function getStatusColor(status: SLAEntry["status"]): string {
  switch (status) {
    case "compliant": return "text-emerald-500";
    case "at_risk": return "text-amber-500";
    case "breached": return "text-red-500";
  }
}

function getStatusBg(status: SLAEntry["status"]): string {
  switch (status) {
    case "compliant": return "bg-emerald-500/10";
    case "at_risk": return "bg-amber-500/10";
    case "breached": return "bg-red-500/10";
  }
}

export function SLADashboard({ entries, overallCompliance }: SLADashboardProps) {
  const locale = "ar";
  const isRTL = locale === "ar";
  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (overallCompliance / 100) * circumference;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-semibold flex items-center gap-2">
          <Clock className="w-4 h-4 text-gold-500" />
          {isRTL ? "الامتثال لمستوى الخدمة" : "SLA Compliance"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Overall gauge */}
        <div className="flex items-center justify-center mb-6">
          <div className="relative w-24 h-24">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 90 90">
              <circle cx="45" cy="45" r="40" fill="none" stroke="currentColor" strokeWidth="6" className="text-muted/30" />
              <motion.circle
                cx="45"
                cy="45"
                r="40"
                fill="none"
                strokeWidth="6"
                strokeLinecap="round"
                className={overallCompliance >= 90 ? "stroke-emerald-500" : overallCompliance >= 75 ? "stroke-amber-500" : "stroke-red-500"}
                initial={{ strokeDasharray: circumference, strokeDashoffset: circumference }}
                animate={{ strokeDashoffset: offset }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-lg font-bold text-foreground">{overallCompliance}%</span>
            </div>
          </div>
        </div>

        {/* Entries */}
        <div className="space-y-2">
          {entries.map((entry, idx) => (
            <motion.div
              key={entry.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.06 }}
              className="flex items-center gap-3 rounded-lg p-3 bg-accent/30"
            >
              <div className={cn("flex h-7 w-7 items-center justify-center rounded-full", getStatusBg(entry.status))}>
                {entry.status === "compliant" ? (
                  <CheckCircle className={cn("w-3.5 h-3.5", getStatusColor(entry.status))} />
                ) : (
                  <AlertTriangle className={cn("w-3.5 h-3.5", getStatusColor(entry.status))} />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium text-foreground">
                    {isRTL ? entry.metricAr : entry.metric}
                  </span>
                  <span className={cn("text-xs font-semibold", getStatusColor(entry.status))}>
                    {entry.current}% / {entry.target}%
                  </span>
                </div>
                <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(entry.current, 100)}%` }}
                    transition={{ duration: 1, delay: idx * 0.1 }}
                    className={cn(
                      "h-full rounded-full",
                      entry.status === "compliant" ? "bg-emerald-500" : entry.status === "at_risk" ? "bg-amber-500" : "bg-red-500",
                    )}
                  />
                </div>
              </div>
              <div className="flex items-center gap-1 text-[10px] text-muted-foreground">
                {entry.trend === "up" ? (
                  <TrendingUp className="w-3 h-3 text-emerald-500" />
                ) : entry.trend === "down" ? (
                  <TrendingUp className="w-3 h-3 text-red-500 rotate-180" />
                ) : null}
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
