"use client";

import { useQuery } from "@tanstack/react-query";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import { api } from "@/lib/api";

const monthlyRevenueAr = [
  { month: "يناير", revenue: 4200000, deals: 12 },
  { month: "فبراير", revenue: 3800000, deals: 10 },
  { month: "مارس", revenue: 5100000, deals: 15 },
  { month: "أبريل", revenue: 4700000, deals: 13 },
  { month: "مايو", revenue: 6200000, deals: 18 },
  { month: "يونيو", revenue: 5800000, deals: 16 },
];

const monthlyRevenueEn = [
  { month: "Jan", revenue: 4200000, deals: 12 },
  { month: "Feb", revenue: 3800000, deals: 10 },
  { month: "Mar", revenue: 5100000, deals: 15 },
  { month: "Apr", revenue: 4700000, deals: 13 },
  { month: "May", revenue: 6200000, deals: 18 },
  { month: "Jun", revenue: 5800000, deals: 16 },
];

const funnelDataAr = [
  { name: "زيارات", value: 8400, fill: "#94a3b8" },
  { name: "عملاء محتملون", value: 3200, fill: "#60a5fa" },
  { name: "مؤهلون", value: 1100, fill: "#C9A96E" },
  { name: "عروض", value: 420, fill: "#f59e0b" },
  { name: "صفقات مغلقة", value: 98, fill: "#10b981" },
];

const funnelDataEn = [
  { name: "Visitors", value: 8400, fill: "#94a3b8" },
  { name: "Leads", value: 3200, fill: "#60a5fa" },
  { name: "Qualified", value: 1100, fill: "#C9A96E" },
  { name: "Proposals", value: 420, fill: "#f59e0b" },
  { name: "Closed Deals", value: 98, fill: "#10b981" },
];

const agentPerfData = [
  { agent: "Outreach", success: 87, speed: 92, accuracy: 78 },
  { agent: "Scoring", success: 94, speed: 85, accuracy: 96 },
  { agent: "Compliance", success: 99, speed: 71, accuracy: 98 },
  { agent: "Intelligence", success: 83, speed: 88, accuracy: 91 },
];

const topClients = [
  { company: "أرامكو السعودية", revenue: 12500000, deals: 8 },
  { company: "STC", revenue: 9800000, deals: 6 },
  { company: "البنك الأهلي", revenue: 8200000, deals: 5 },
  { company: "وزارة التجارة", revenue: 6700000, deals: 3 },
  { company: "SABIC", revenue: 3100000, deals: 2 },
];

export function AnalyticsContent() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const monthlyData = isAr ? monthlyRevenueAr : monthlyRevenueEn;
  const funnelData = isAr ? funnelDataAr : funnelDataEn;

  const pipelineQuery = useQuery({
    queryKey: ["analytics", "pipeline-summary"],
    queryFn: async () => (await api.getPipeline()).data,
  });

  const pipelineSummary =
    pipelineQuery.data &&
    typeof pipelineQuery.data === "object" &&
    "pipeline_summary" in pipelineQuery.data
      ? (pipelineQuery.data as { pipeline_summary?: Record<string, number> })
          .pipeline_summary
      : undefined;

  return (
    <div className="space-y-6">
      <div
        role="status"
        className="rounded-xl border border-border bg-muted/30 px-4 py-3 text-xs text-muted-foreground"
      >
        {isAr
          ? "الرسوم البيانية أدناه بيانات توضيحية للعرض فقط إلى حين ربط تقارير الإيرادات الكاملة. أرقام مسار الإيرادات تأتي من الـ API عند توفرها."
          : "Charts below use illustrative sample data until full revenue reporting is wired. Pipeline figures load from the API when available."}
      </div>

      {pipelineQuery.isError && (
        <div
          role="alert"
          className="rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm"
        >
          {isAr
            ? "تعذر تحميل ملخص مسار الإيرادات."
            : "Could not load revenue pipeline summary."}
        </div>
      )}

      {pipelineSummary && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          {(
            [
              ["total_leads", isAr ? "إجمالي العملاء المحتملين" : "Total leads"],
              ["commitments", isAr ? "التزامات" : "Commitments"],
              ["paid", isAr ? "مدفوع" : "Paid"],
              ["total_revenue_sar", isAr ? "إيراد مسجّل (ر.س)" : "Recorded SAR"],
            ] as const
          ).map(([key, label]) => (
            <div
              key={key}
              className="rounded-xl border border-border bg-card p-4"
            >
              <p className="text-xs text-muted-foreground">{label}</p>
              <p className="text-xl font-bold tabular-nums mt-1">
                {pipelineSummary[key] ?? "—"}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Header actions */}
      <div className="flex justify-end">
        <Button variant="outline" size="sm">
          <Download className="w-4 h-4 me-1.5" />
          {isAr ? "تصدير التقرير" : "Export Report"}
        </Button>
      </div>

      {/* Revenue + Funnel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-semibold">
                {isAr ? "الإيرادات الشهرية" : "Monthly Revenue"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={monthlyData} barSize={28}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                  <XAxis dataKey="month" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${(v/1000000).toFixed(1)}M`} />
                  <Tooltip
                    contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "12px", fontSize: 12 }}
                    formatter={(value: number) => [formatCurrency(value), isAr ? "الإيرادات" : "Revenue"]}
                  />
                  <Bar dataKey="revenue" fill="#C9A96E" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-semibold">
                {isAr ? "قمع التحويل" : "Conversion Funnel"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {funnelData.map((item, i) => (
                  <div key={item.name} className="flex items-center gap-3">
                    <span className="text-xs text-muted-foreground w-24 shrink-0">{item.name}</span>
                    <div className="flex-1 h-6 bg-muted rounded-lg overflow-hidden relative">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(item.value / 8400) * 100}%` }}
                        transition={{ delay: 0.3 + i * 0.1, duration: 0.5 }}
                        className="h-full rounded-lg"
                        style={{ background: item.fill }}
                      />
                    </div>
                    <span className="text-xs font-semibold text-foreground w-12 text-right tabular-nums">
                      {item.value.toLocaleString()}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Agent Performance + Top Clients */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-semibold">
                {isAr ? "أداء الوكلاء" : "Agent Performance"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={220}>
                <RadarChart data={agentPerfData}>
                  <PolarGrid stroke="hsl(var(--border))" />
                  <PolarAngleAxis dataKey="agent" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }} />
                  <Radar dataKey="success" stroke="#C9A96E" fill="#C9A96E" fillOpacity={0.2} />
                  <Radar dataKey="accuracy" stroke="#10b981" fill="#10b981" fillOpacity={0.1} />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-semibold">
                {isAr ? "أفضل العملاء" : "Top Clients"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topClients.map((client, i) => (
                  <div key={client.company} className="flex items-center gap-3">
                    <span className="w-5 h-5 rounded-full bg-muted text-muted-foreground text-[10px] flex items-center justify-center font-bold flex-shrink-0">
                      {i + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{client.company}</p>
                      <div className="mt-1 h-1.5 bg-muted rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${(client.revenue / 12500000) * 100}%` }}
                          transition={{ delay: 0.5 + i * 0.07 }}
                          className="h-full bg-gradient-to-r from-gold-500 to-gold-400 rounded-full"
                        />
                      </div>
                    </div>
                    <span className="text-xs font-semibold text-gold-400 shrink-0 tabular-nums">
                      {formatCurrency(client.revenue)}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
