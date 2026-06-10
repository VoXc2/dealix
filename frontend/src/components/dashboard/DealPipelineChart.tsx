"use client";

import { useTranslations, useLocale } from "next-intl";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const stageColors: Record<string, string> = {
  lead: "#94a3b8",
  qualified: "#60a5fa",
  proposal: "#C9A96E",
  negotiation: "#f59e0b",
  closed_won: "#10b981",
  closed_lost: "#ef4444",
};

const pipelineDataAr = [
  { stage: "عميل محتمل", count: 45, value: 9000000, key: "lead" },
  { stage: "مؤهل", count: 28, value: 7200000, key: "qualified" },
  { stage: "عرض", count: 16, value: 5800000, key: "proposal" },
  { stage: "تفاوض", count: 9, value: 4100000, key: "negotiation" },
  { stage: "مغلق", count: 6, value: 3500000, key: "closed_won" },
];

const pipelineDataEn = [
  { stage: "Lead", count: 45, value: 9000000, key: "lead" },
  { stage: "Qualified", count: 28, value: 7200000, key: "qualified" },
  { stage: "Proposal", count: 16, value: 5800000, key: "proposal" },
  { stage: "Negotiation", count: 9, value: 4100000, key: "negotiation" },
  { stage: "Closed Won", count: 6, value: 3500000, key: "closed_won" },
];

export function DealPipelineChart() {
  const t = useTranslations("dashboard");
  const locale = useLocale();
  const data = locale === "ar" ? pipelineDataAr : pipelineDataEn;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base font-semibold">{t("dealPipeline")}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }} barSize={32}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis
              dataKey="stage"
              tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                background: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "12px",
                fontSize: 12,
              }}
              cursor={{ fill: "hsl(var(--muted))" }}
            />
            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.key} fill={stageColors[entry.key] ?? "#C9A96E"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
