"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  RefreshCw,
  Loader2,
  TrendingUp,
  TrendingDown,
} from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface AIRecommendation {
  id: string;
  type: "opportunity" | "warning" | "improvement";
  title: string;
  titleAr: string;
  description: string;
  descriptionAr: string;
  impact: "high" | "medium" | "low";
  metric?: {
    label: string;
    value: number;
    trend: "up" | "down";
  };
  actionLabel: string;
  actionLabelAr: string;
}

interface OpsHealthAIProps {
  recommendations: AIRecommendation[];
  onRefresh?: () => Promise<void>;
  onAction?: (id: string) => void;
  isLoading?: boolean;
}

const typeConfig = {
  opportunity: { icon: Lightbulb, color: "text-blue-500", bg: "bg-blue-500/10", border: "border-blue-500/20" },
  warning: { icon: AlertTriangle, color: "text-amber-500", bg: "bg-amber-500/10", border: "border-amber-500/20" },
  improvement: { icon: CheckCircle, color: "text-emerald-500", bg: "bg-emerald-500/10", border: "border-emerald-500/20" },
};

const impactConfig = {
  high: { label: "High", labelAr: "عالية", color: "text-red-500" },
  medium: { label: "Medium", labelAr: "متوسطة", color: "text-amber-500" },
  low: { label: "Low", labelAr: "منخفضة", color: "text-muted-foreground" },
};

export function OpsHealthAI({ recommendations, onRefresh, onAction, isLoading }: OpsHealthAIProps) {
  const [refreshing, setRefreshing] = useState(false);
  const locale = "ar";
  const isRTL = locale === "ar";

  const handleRefresh = async () => {
    if (!onRefresh) return;
    setRefreshing(true);
    try {
      await onRefresh();
    } finally {
      setRefreshing(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-gold-500" />
            <CardTitle className="text-sm font-semibold">
              {isRTL ? "توصيات الذكاء الاصطناعي" : "AI Recommendations"}
            </CardTitle>
          </div>
          {onRefresh && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleRefresh}
              disabled={refreshing || isLoading}
            >
              <RefreshCw className={cn("w-3.5 h-3.5", refreshing && "animate-spin")} />
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
          </div>
        )}

        {!isLoading && recommendations.length === 0 && (
          <div className="text-center py-8 text-sm text-muted-foreground">
            {isRTL ? "لا توجد توصيات حالياً" : "No recommendations right now"}
          </div>
        )}

        {recommendations.map((rec, idx) => {
          const config = typeConfig[rec.type];
          const Icon = config.icon;
          const impact = impactConfig[rec.impact];

          return (
            <motion.div
              key={rec.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.08 }}
              className={cn(
                "rounded-xl border p-4 transition-colors hover:bg-accent/50",
                config.border,
              )}
            >
              <div className="flex gap-3">
                <div className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-lg", config.bg)}>
                  <Icon className={cn("w-4 h-4", config.color)} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <h4 className="text-sm font-semibold text-foreground">
                      {isRTL ? rec.titleAr : rec.title}
                    </h4>
                    <Badge variant="outline" className={cn("text-[10px]", impact.color)}>
                      {isRTL ? impact.labelAr : impact.label}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground mb-2">
                    {isRTL ? rec.descriptionAr : rec.description}
                  </p>
                  {rec.metric && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                      <span>{rec.metric.label}:</span>
                      <span className="font-semibold text-foreground">{rec.metric.value}</span>
                      {rec.metric.trend === "up" ? (
                        <TrendingUp className="w-3 h-3 text-emerald-500" />
                      ) : (
                        <TrendingDown className="w-3 h-3 text-red-500" />
                      )}
                    </div>
                  )}
                  {onAction && (
                    <button
                      onClick={() => onAction(rec.id)}
                      className="flex items-center gap-1 text-xs font-medium text-gold-500 hover:text-gold-400 transition-colors"
                    >
                      {isRTL ? rec.actionLabelAr : rec.actionLabel}
                      <ArrowRight className={cn("w-3 h-3", isRTL && "rotate-180")} />
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </CardContent>
    </Card>
  );
}
