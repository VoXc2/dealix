"use client";

import { useState } from "react";
import { DollarSign, TrendingUp, TrendingDown, Cpu, Database, Zap, Filter, Calendar } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface CostEntry {
  id: string;
  model: string;
  provider: string;
  cost: number;
  tokens: number;
  requests: number;
  avgLatency: number;
  trend: "up" | "down" | "stable";
  date: string;
}

const mockCosts: CostEntry[] = [
  { id: "1", model: "gpt-4o", provider: "OpenAI", cost: 452.30, tokens: 2500000, requests: 12500, avgLatency: 1.2, trend: "up", date: "2026-05-28" },
  { id: "2", model: "gpt-4o-mini", provider: "OpenAI", cost: 89.50, tokens: 5200000, requests: 45000, avgLatency: 0.8, trend: "down", date: "2026-05-28" },
  { id: "3", model: "claude-3-haiku", provider: "Anthropic", cost: 34.20, tokens: 1800000, requests: 22000, avgLatency: 0.6, trend: "stable", date: "2026-05-28" },
  { id: "4", model: "claude-3-opus", provider: "Anthropic", cost: 210.75, tokens: 950000, requests: 3200, avgLatency: 2.1, trend: "down", date: "2026-05-28" },
  { id: "5", model: "cohere-embed", provider: "Cohere", cost: 18.40, tokens: 4200000, requests: 38000, avgLatency: 0.3, trend: "up", date: "2026-05-28" },
];

export default function LLMCostsPage() {
  const [period, setPeriod] = useState<"7d" | "30d" | "90d">("30d");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const totalCost = mockCosts.reduce((s, c) => s + c.cost, 0);
  const totalTokens = mockCosts.reduce((s, c) => s + c.tokens, 0);
  const totalRequests = mockCosts.reduce((s, c) => s + c.requests, 0);

  return (
    <AppLayout
      title={isRTL ? "تكاليف نماذج الذكاء الاصطناعي" : "LLM Costs"}
      subtitle={isRTL ? "مراقبة وتحليل تكاليف نماذج اللغة" : "Monitor and analyze language model costs"}
    >
      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-gold-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "إجمالي التكلفة" : "Total Cost"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(totalCost, locale)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Cpu className="w-4 h-4 text-blue-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "إجمالي التوكنات" : "Total Tokens"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{(totalTokens / 1000000).toFixed(1)}M</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-4 h-4 text-amber-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "إجمالي الطلبات" : "Total Requests"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{(totalRequests / 1000).toFixed(1)}K</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Database className="w-4 h-4 text-emerald-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "متوسط التكلفة/طلب" : "Avg Cost/Request"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(totalCost / totalRequests, locale)}</p>
          </CardContent>
        </Card>
      </div>

      {/* Period toggle */}
      <div className="flex items-center gap-2 mb-6">
        {(["7d", "30d", "90d"] as const).map((p) => (
          <Button
            key={p}
            variant={period === p ? "default" : "outline"}
            size="sm"
            onClick={() => setPeriod(p)}
          >
            {p}
          </Button>
        ))}
        <div className="flex-1" />
        <Button variant="outline" size="sm">
          <Filter className="w-3.5 h-3.5 mr-1" />
          {isRTL ? "تصفية" : "Filter"}
        </Button>
        <Button variant="outline" size="sm">
          <Calendar className="w-3.5 h-3.5 mr-1" />
          {isRTL ? "نطاق تاريخ" : "Date Range"}
        </Button>
      </div>

      {/* Cost table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            {isRTL ? "تفاصيل التكاليف" : "Cost Breakdown"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "النموذج" : "Model"}</th>
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "المزود" : "Provider"}</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "التكلفة" : "Cost"}</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "التوكنات" : "Tokens"}</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الطلبات" : "Requests"}</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "السرعة" : "Latency"}</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الاتجاه" : "Trend"}</th>
                </tr>
              </thead>
              <tbody>
                {mockCosts.map((entry) => (
                  <tr key={entry.id} className="border-b border-border/50 hover:bg-accent/30 transition-colors">
                    <td className="py-3 px-4 font-medium text-foreground">{entry.model}</td>
                    <td className="py-3 px-4 text-muted-foreground">{entry.provider}</td>
                    <td className="py-3 px-4 text-right tabular-nums">{formatCurrency(entry.cost, locale)}</td>
                    <td className="py-3 px-4 text-right tabular-nums text-muted-foreground">
                      {(entry.tokens / 1000000).toFixed(1)}M
                    </td>
                    <td className="py-3 px-4 text-right tabular-nums text-muted-foreground">
                      {(entry.requests / 1000).toFixed(1)}K
                    </td>
                    <td className="py-3 px-4 text-right tabular-nums text-muted-foreground">
                      {entry.avgLatency}s
                    </td>
                    <td className="py-3 px-4 text-right">
                      {entry.trend === "up" ? (
                        <TrendingUp className="w-4 h-4 text-red-500 inline" />
                      ) : entry.trend === "down" ? (
                        <TrendingDown className="w-4 h-4 text-emerald-500 inline" />
                      ) : (
                        <Zap className="w-4 h-4 text-muted-foreground inline" />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </AppLayout>
  );
}
