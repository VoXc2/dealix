"use client";

import { Search, TrendingUp, ExternalLink, FileText, Hash, BarChart3 } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface SEICluster {
  id: string;
  topic: string;
  keywords: string[];
  articles: number;
  score: number;
  trend: "up" | "down" | "stable";
  volume: number;
}

const mockClusters: SEICluster[] = [
  { id: "1", topic: "AI Revenue Operations", keywords: ["RevOps AI", "AI revenue", "Saudi RevOps"], articles: 5, score: 85, trend: "up", volume: 1200 },
  { id: "2", topic: "ZATCA Compliance", keywords: ["ZATCA", "e-invoicing", "Saudi tax"], articles: 3, score: 72, trend: "up", volume: 890 },
  { id: "3", topic: "Saudi Digital Transformation", keywords: ["Vision 2030", "digital Saudi", "SME tech"], articles: 4, score: 68, trend: "stable", volume: 2100 },
  { id: "4", topic: "AI Lead Generation", keywords: ["AI leads", "automated prospecting", "Saudi B2B"], articles: 6, score: 91, trend: "up", volume: 3400 },
  { id: "5", topic: "CRM Comparison", keywords: ["best CRM Saudi", "CRM vs AI", "Saudi CRM"], articles: 2, score: 45, trend: "down", volume: 560 },
];

export default function SEOClustersPage() {
  const locale = useLocale();
  const isRTL = locale === "ar";

  const avgScore = mockClusters.reduce((s, c) => s + c.score, 0) / mockClusters.length;

  return (
    <AppLayout
      title={isRTL ? "مجموعات تحسين محركات البحث" : "SEO Clusters"}
      subtitle={isRTL ? "إدارة وتحليل مجموعات الكلمات المفتاحية" : "Manage and analyze keyword clusters"}
    >
      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">{isRTL ? "إجمالي المجموعات" : "Total Clusters"}</p>
            <p className="text-2xl font-bold text-foreground">{mockClusters.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">{isRTL ? "متوسط النقاط" : "Average Score"}</p>
            <p className="text-2xl font-bold text-gold-500">{avgScore.toFixed(0)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">{isRTL ? "إجمالي المقالات" : "Total Articles"}</p>
            <p className="text-2xl font-bold text-foreground">{mockClusters.reduce((s, c) => s + c.articles, 0)}</p>
          </CardContent>
        </Card>
      </div>

      {/* Clusters */}
      <div className="space-y-3">
        {mockClusters.map((cluster) => (
          <Card key={cluster.id} className="hover:border-gold-500/30 transition-colors">
            <CardContent className="p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Search className="w-4 h-4 text-gold-500" />
                    <h3 className="text-sm font-semibold text-foreground">{cluster.topic}</h3>
                    <Badge
                      variant="outline"
                      className={cn(
                        "text-[10px]",
                        cluster.trend === "up" ? "bg-emerald-500/10 text-emerald-500" : cluster.trend === "down" ? "bg-red-500/10 text-red-500" : "bg-muted text-muted-foreground",
                      )}
                    >
                      {cluster.trend === "up" ? "↑" : cluster.trend === "down" ? "↓" : "→"}
                    </Badge>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {cluster.keywords.map((kw) => (
                      <Badge key={kw} variant="secondary" className="text-[10px]">{kw}</Badge>
                    ))}
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-foreground">{cluster.score}</p>
                  <p className="text-[10px] text-muted-foreground">{isRTL ? "نقاط" : "Score"}</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
                <span className="flex items-center gap-1">
                  <FileText className="w-3 h-3" />
                  {cluster.articles} {isRTL ? "مقالات" : "articles"}
                </span>
                <span className="flex items-center gap-1">
                  <BarChart3 className="w-3 h-3" />
                  {cluster.volume.toLocaleString()} {isRTL ? "بحث/شهر" : "searches/mo"}
                </span>
              </div>
              <Progress value={cluster.score} className="h-1.5" />
            </CardContent>
          </Card>
        ))}
      </div>
    </AppLayout>
  );
}
