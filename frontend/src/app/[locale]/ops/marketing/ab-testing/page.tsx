"use client";

import { useState } from "react";
import { FlaskConical, Plus, Search, TrendingUp, TrendingDown, Minus, Play, Pause } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatPercentage } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

interface ABTest {
  id: string;
  name: string;
  variantA: string;
  variantB: string;
  status: "running" | "completed" | "paused" | "draft";
  impressions: number;
  conversions: number;
  winner: "a" | "b" | null;
  confidence: number;
}

const mockTests: ABTest[] = [
  { id: "1", name: "Hero Title - AI vs RevOps", variantA: "AI-Powered Platform", variantB: "Revenue Operations OS", status: "running", impressions: 12500, conversions: 340, winner: null, confidence: 78 },
  { id: "2", name: "CTA Button Color", variantA: "Gold", variantB: "Blue", status: "completed", impressions: 8900, conversions: 445, winner: "a", confidence: 95 },
  { id: "3", name: "Pricing Page Layout", variantA: "Grid", variantB: "List", status: "paused", impressions: 3200, conversions: 89, winner: null, confidence: 45 },
  { id: "4", name: "Lead Form Length", variantA: "Short (3 fields)", variantB: "Long (6 fields)", status: "completed", impressions: 15300, conversions: 612, winner: "b", confidence: 92 },
];

const statusConfig: Record<string, { label: string; labelAr: string; color: string; icon: React.ElementType }> = {
  running: { label: "Running", labelAr: "قيد التشغيل", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20", icon: Play },
  completed: { label: "Completed", labelAr: "مكتمل", color: "bg-blue-500/10 text-blue-500 border-blue-500/20", icon: TrendingUp },
  paused: { label: "Paused", labelAr: "متوقف", color: "bg-amber-500/10 text-amber-500 border-amber-500/20", icon: Pause },
  draft: { label: "Draft", labelAr: "مسودة", color: "bg-muted text-muted-foreground border-border", icon: FlaskConical },
};

export default function ABTestingPage() {
  const [search, setSearch] = useState("");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const filtered = mockTests.filter((t) =>
    t.name.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <AppLayout
      title={isRTL ? "اختبار A/B" : "A/B Testing"}
      subtitle={isRTL ? "إدارة وتحليل اختبارات A/B" : "Manage and analyze A/B tests"}
    >
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <CardTitle className="text-lg font-bold flex items-center gap-2">
              <FlaskConical className="w-5 h-5 text-gold-500" />
              {isRTL ? "الاختبارات" : "Tests"}
            </CardTitle>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <div className="relative flex-1 sm:w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder={isRTL ? "بحث..." : "Search..."}
                  className="pl-9"
                  dir={isRTL ? "rtl" : "ltr"}
                />
              </div>
              <Button>
                <Plus className="w-4 h-4 mr-1" />
                {isRTL ? "اختبار جديد" : "New Test"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <FlaskConical className="w-12 h-12 text-muted-foreground/30 mb-3" />
              <p className="text-sm text-muted-foreground">
                {isRTL ? "لا توجد اختبارات" : "No tests found"}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {filtered.map((test) => {
                const config = statusConfig[test.status];
                const Icon = config.icon;
                const conversionRate = (test.conversions / test.impressions) * 100;
                return (
                  <Card key={test.id} className="hover:border-gold-500/30 transition-colors">
                    <CardContent className="p-5">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="text-sm font-semibold text-foreground">{test.name}</h3>
                            <Badge variant="outline" className={cn("text-xs", config.color)}>
                              <Icon className="w-3 h-3 mr-1" />
                              {isRTL ? config.labelAr : config.label}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-4 text-xs text-muted-foreground">
                            <span>A: {test.variantA}</span>
                            <span>B: {test.variantB}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-lg font-bold text-foreground">{formatPercentage(conversionRate)}</p>
                          <p className="text-[10px] text-muted-foreground">{isRTL ? "معدل التحويل" : "Conversion"}</p>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-3">
                          <span>{test.impressions.toLocaleString()} {isRTL ? "ظهور" : "impressions"}</span>
                          <span>{test.conversions.toLocaleString()} {isRTL ? "تحويلات" : "conversions"}</span>
                        </div>
                        {test.winner && (
                          <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-[10px]">
                            {isRTL ? `الفائز: ${test.winner === "a" ? "أ" : "ب"}` : `Winner: ${test.winner === "a" ? "A" : "B"}`} ({(test.confidence / 100).toLocaleString([], { style: "percent" })})
                          </Badge>
                        )}
                        {!test.winner && test.status === "running" && (
                          <Badge className="bg-blue-500/10 text-blue-500 border-blue-500/20 text-[10px]">
                            {(test.confidence / 100).toLocaleString([], { style: "percent" })} {isRTL ? "ثقة" : "confidence"}
                          </Badge>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </AppLayout>
  );
}
