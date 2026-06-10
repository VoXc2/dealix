"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Target,
  PiggyBank,
  Activity,
} from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency, formatNumber, formatPercentage } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";

export interface CEOMetricsData {
  monthlyRevenue: number;
  newCustomers: number;
  conversionRate: number;
  pipelineValue: number;
  customerLTV: number;
  previousMonthRevenue?: number;
  previousCustomers?: number;
  previousConversionRate?: number;
  previousPipelineValue?: number;
  previousCustomerLTV?: number;
}

interface MetricCardProps {
  icon: React.ElementType;
  label: string;
  labelAr: string;
  value: string;
  change: number;
  trend: "up" | "down" | "neutral";
  index: number;
}

function MetricCard({ icon: Icon, label, labelAr, value, change, trend, index }: MetricCardProps) {
  const { locale } = { locale: "ar" };
  const isRTL = locale === "ar";
  const isPositive = trend === "up";
  const isNeutral = trend === "neutral";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
    >
      <Card className="relative overflow-hidden group hover:border-gold-500/30 transition-all duration-300">
        <CardContent className="p-5">
          <div className="flex items-start justify-between mb-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold-500/10">
              <Icon className="w-5 h-5 text-gold-500" />
            </div>
            <div
              className={cn(
                "flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold",
                isPositive
                  ? "bg-emerald-500/10 text-emerald-500"
                  : isNeutral
                    ? "bg-muted text-muted-foreground"
                    : "bg-red-500/10 text-red-500",
              )}
            >
              {isPositive ? (
                <TrendingUp className="w-3 h-3" />
              ) : isNeutral ? (
                <Activity className="w-3 h-3" />
              ) : (
                <TrendingDown className="w-3 h-3" />
              )}
              <span>{formatPercentage(Math.abs(change))}</span>
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground tracking-tight tabular-nums mb-1">
            {value}
          </p>
          <p className="text-sm text-muted-foreground font-medium">
            {isRTL ? labelAr : label}
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export function CEOMetrics({ data }: { data: CEOMetricsData }) {
  const { locale } = { locale: "ar" };
  const isRTL = locale === "ar";

  const metrics: MetricCardProps[] = [
    {
      icon: DollarSign,
      label: "Monthly Revenue",
      labelAr: "الإيرادات الشهرية",
      value: formatCurrency(data.monthlyRevenue),
      change: data.previousMonthRevenue
        ? ((data.monthlyRevenue - data.previousMonthRevenue) / data.previousMonthRevenue) * 100
        : 0,
      trend: "up",
      index: 0,
    },
    {
      icon: Users,
      label: "New Customers",
      labelAr: "العملاء الجدد",
      value: formatNumber(data.newCustomers),
      change: data.previousCustomers
        ? ((data.newCustomers - data.previousCustomers) / data.previousCustomers) * 100
        : 0,
      trend: "up",
      index: 1,
    },
    {
      icon: Target,
      label: "Conversion Rate",
      labelAr: "معدل التحويل",
      value: formatPercentage(data.conversionRate),
      change: data.previousConversionRate
        ? data.conversionRate - data.previousConversionRate
        : 0,
      trend: "up",
      index: 2,
    },
    {
      icon: PiggyBank,
      label: "Pipeline Value",
      labelAr: "قيمة المسار",
      value: formatCurrency(data.pipelineValue),
      change: data.previousPipelineValue
        ? ((data.pipelineValue - data.previousPipelineValue) / data.previousPipelineValue) * 100
        : 0,
      trend: "up",
      index: 3,
    },
    {
      icon: Activity,
      label: "Customer LTV",
      labelAr: "قيمة العميل مدى الحياة",
      value: formatCurrency(data.customerLTV),
      change: data.previousCustomerLTV
        ? ((data.customerLTV - data.previousCustomerLTV) / data.previousCustomerLTV) * 100
        : 0,
      trend: "up",
      index: 4,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
      {metrics.map((metric) => (
        <MetricCard key={metric.label} {...metric} />
      ))}
    </div>
  );
}
