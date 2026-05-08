"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useTranslations, useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import type { RevenueDataPoint } from "@/types";

const mockData: RevenueDataPoint[] = [
  { month: "يناير", revenue: 4200000, target: 4000000, deals: 12 },
  { month: "فبراير", revenue: 3800000, target: 4200000, deals: 10 },
  { month: "مارس", revenue: 5100000, target: 4500000, deals: 15 },
  { month: "أبريل", revenue: 4700000, target: 4800000, deals: 13 },
  { month: "مايو", revenue: 6200000, target: 5000000, deals: 18 },
  { month: "يونيو", revenue: 5800000, target: 5500000, deals: 16 },
  { month: "يوليو", revenue: 7100000, target: 6000000, deals: 21 },
  { month: "أغسطس", revenue: 6500000, target: 6500000, deals: 19 },
  { month: "سبتمبر", revenue: 8200000, target: 7000000, deals: 24 },
  { month: "أكتوبر", revenue: 7800000, target: 7500000, deals: 22 },
  { month: "نوفمبر", revenue: 9100000, target: 8000000, deals: 27 },
  { month: "ديسمبر", revenue: 8700000, target: 8500000, deals: 25 },
];

const mockDataEn: RevenueDataPoint[] = [
  { month: "Jan", revenue: 4200000, target: 4000000, deals: 12 },
  { month: "Feb", revenue: 3800000, target: 4200000, deals: 10 },
  { month: "Mar", revenue: 5100000, target: 4500000, deals: 15 },
  { month: "Apr", revenue: 4700000, target: 4800000, deals: 13 },
  { month: "May", revenue: 6200000, target: 5000000, deals: 18 },
  { month: "Jun", revenue: 5800000, target: 5500000, deals: 16 },
  { month: "Jul", revenue: 7100000, target: 6000000, deals: 21 },
  { month: "Aug", revenue: 6500000, target: 6500000, deals: 19 },
  { month: "Sep", revenue: 8200000, target: 7000000, deals: 24 },
  { month: "Oct", revenue: 7800000, target: 7500000, deals: 22 },
  { month: "Nov", revenue: 9100000, target: 8000000, deals: 27 },
  { month: "Dec", revenue: 8700000, target: 8500000, deals: 25 },
];

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border border-border rounded-xl p-3 shadow-xl text-sm">
        <p className="font-semibold text-foreground mb-2">{label}</p>
        {payload.map((entry: { name: string; value: number; color: string }, i: number) => (
          <p key={i} style={{ color: entry.color }} className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full inline-block" style={{ background: entry.color }} />
            {entry.name}: {formatCurrency(entry.value)}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export function RevenueChart() {
  const t = useTranslations("dashboard");
  const locale = useLocale();
  const data = locale === "ar" ? mockData : mockDataEn;

  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle className="text-base font-semibold">{t("revenueChart")}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <defs>
              <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#C9A96E" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#C9A96E" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="targetGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis
              dataKey="month"
              tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `${(v / 1000000).toFixed(1)}M`}
              width={50}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: 12, color: "hsl(var(--muted-foreground))" }}
            />
            <Area
              type="monotone"
              dataKey="revenue"
              name={locale === "ar" ? "الإيرادات" : "Revenue"}
              stroke="#C9A96E"
              strokeWidth={2.5}
              fill="url(#revenueGrad)"
              dot={false}
              activeDot={{ r: 5, fill: "#C9A96E" }}
            />
            <Area
              type="monotone"
              dataKey="target"
              name={locale === "ar" ? "الهدف" : "Target"}
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#targetGrad)"
              strokeDasharray="5 3"
              dot={false}
              activeDot={{ r: 4, fill: "#10b981" }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
