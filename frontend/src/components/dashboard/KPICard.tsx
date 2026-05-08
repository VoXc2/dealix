"use client";

import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn, formatCurrency, formatNumber, formatPercentage } from "@/lib/utils";
import type { KPIMetric } from "@/types";

interface KPICardProps {
  metric: KPIMetric;
  index?: number;
}

export function KPICard({ metric, index = 0 }: KPICardProps) {
  const isPositive = metric.trend === "up";
  const isNeutral = metric.trend === "neutral";

  const formattedValue =
    metric.format === "currency"
      ? formatCurrency(metric.value as number)
      : metric.format === "percentage"
      ? `${metric.value}%`
      : formatNumber(metric.value as number);

  const TrendIcon = isNeutral ? Minus : isPositive ? TrendingUp : TrendingDown;
  const trendColor = isNeutral
    ? "text-muted-foreground"
    : isPositive
    ? "text-emerald-400"
    : "text-red-400";
  const trendBg = isNeutral
    ? "bg-muted/50"
    : isPositive
    ? "bg-emerald-400/10"
    : "bg-red-400/10";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
      className={cn(
        "relative rounded-2xl border border-border bg-card p-5 overflow-hidden group",
        "hover:border-gold-500/30 transition-all duration-300",
        "card-glow-gold"
      )}
    >
      {/* Subtle background gradient on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-gold-500/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

      {/* Top row */}
      <div className="flex items-start justify-between mb-4">
        <div className="text-2xl">{metric.icon}</div>
        <div className={cn("flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold", trendBg, trendColor)}>
          <TrendIcon className="w-3 h-3" />
          <span>{formatPercentage(Math.abs(metric.change))}</span>
        </div>
      </div>

      {/* Value */}
      <div className="mb-1">
        <p className="text-2xl font-bold text-foreground tracking-tight tabular-nums">
          {formattedValue}
        </p>
      </div>

      {/* Label */}
      <p className="text-sm text-muted-foreground font-medium">{metric.label}</p>

      {/* Decorative bottom line */}
      <div className={cn(
        "absolute bottom-0 left-0 right-0 h-0.5 opacity-0 group-hover:opacity-100 transition-opacity",
        isPositive ? "bg-gradient-to-r from-emerald-500 to-emerald-400" : isNeutral ? "bg-gradient-to-r from-gold-500 to-gold-400" : "bg-gradient-to-r from-red-500 to-red-400"
      )} />
    </motion.div>
  );
}
