"use client";

import { motion } from "framer-motion";
import { Shield, TrendingUp, Users, DollarSign, Activity, AlertTriangle } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SubScore {
  label: string;
  labelAr: string;
  score: number;
  icon: React.ElementType;
}

interface HealthScoreProps {
  overallScore: number;
  subScores: SubScore[];
}

function getScoreColor(score: number): string {
  if (score >= 80) return "text-emerald-500";
  if (score >= 60) return "text-gold-500";
  if (score >= 40) return "text-amber-500";
  return "text-red-500";
}

function getScoreBg(score: number): string {
  if (score >= 80) return "bg-emerald-500/10";
  if (score >= 60) return "bg-gold-500/10";
  if (score >= 40) return "bg-amber-500/10";
  return "bg-red-500/10";
}

function getScoreRing(score: number): string {
  if (score >= 80) return "stroke-emerald-500";
  if (score >= 60) return "stroke-gold-500";
  if (score >= 40) return "stroke-amber-500";
  return "stroke-red-500";
}

export function HealthScore({ overallScore, subScores }: HealthScoreProps) {
  const locale = "ar";
  const isRTL = locale === "ar";
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (overallScore / 100) * circumference;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-semibold flex items-center gap-2">
          <Activity className="w-4 h-4 text-gold-500" />
          {isRTL ? "مؤشر صحة الشركة" : "Company Health Score"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center mb-6">
          <div className="relative w-32 h-32 mb-3">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                className="text-muted/30"
              />
              <motion.circle
                cx="60"
                cy="60"
                r="54"
                fill="none"
                strokeWidth="8"
                strokeLinecap="round"
                className={getScoreRing(overallScore)}
                initial={{ strokeDasharray: circumference, strokeDashoffset: circumference }}
                animate={{ strokeDashoffset: offset }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={cn("text-3xl font-bold", getScoreColor(overallScore))}>
                {overallScore}
              </span>
            </div>
          </div>
          <span
            className={cn(
              "rounded-full px-3 py-1 text-xs font-semibold",
              getScoreBg(overallScore),
              getScoreColor(overallScore),
            )}
          >
            {overallScore >= 80
              ? isRTL ? "ممتاز" : "Excellent"
              : overallScore >= 60
                ? isRTL ? "جيد" : "Good"
                : overallScore >= 40
                  ? isRTL ? "بحاجة للتحسين" : "Needs Improvement"
                  : isRTL ? "حرج" : "Critical"}
          </span>
        </div>

        <div className="space-y-3">
          {subScores.map((sub, idx) => {
            const Icon = sub.icon;
            return (
              <motion.div
                key={sub.label}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.08 }}
                className="flex items-center gap-3"
              >
                <div className={cn("flex h-8 w-8 items-center justify-center rounded-lg", getScoreBg(sub.score))}>
                  <Icon className={cn("w-4 h-4", getScoreColor(sub.score))} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-medium text-foreground">
                      {isRTL ? sub.labelAr : sub.label}
                    </span>
                    <span className={cn("text-xs font-semibold", getScoreColor(sub.score))}>
                      {sub.score}
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${sub.score}%` }}
                      transition={{ duration: 1, delay: idx * 0.1 }}
                      className={cn("h-full rounded-full", getScoreBg(sub.score))}
                    />
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
