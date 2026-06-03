"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, MoreHorizontal, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, formatCurrency } from "@/lib/utils";
import type { Deal, DealStage } from "@/types";

const STAGES: { key: DealStage; color: string; dotColor: string }[] = [
  { key: "lead", color: "border-t-slate-400", dotColor: "bg-slate-400" },
  { key: "qualified", color: "border-t-blue-400", dotColor: "bg-blue-400" },
  { key: "proposal", color: "border-t-gold-400", dotColor: "bg-gold-400" },
  { key: "negotiation", color: "border-t-amber-400", dotColor: "bg-amber-400" },
  { key: "closed_won", color: "border-t-emerald-400", dotColor: "bg-emerald-400" },
];

const mockDeals: Record<DealStage, Deal[]> = {
  lead: [
    {
      id: "1",
      title: "توسع البنية التحتية لأرامكو",
      company: "أرامكو السعودية",
      value: 2500000,
      currency: "SAR",
      stage: "lead",
      probability: 20,
      closeDate: "2025-03-31",
      assignedTo: "أحمد الحربي",
      lastActivity: new Date(Date.now() - 2 * 3600000).toISOString(),
      tags: ["enterprise", "oil-gas"],
      aiScore: 72,
    },
    {
      id: "2",
      title: "منصة الخدمات المصرفية الرقمية",
      company: "البنك الأهلي السعودي",
      value: 1800000,
      currency: "SAR",
      stage: "lead",
      probability: 25,
      closeDate: "2025-04-15",
      assignedTo: "سارة القحطاني",
      lastActivity: new Date(Date.now() - 5 * 3600000).toISOString(),
      tags: ["fintech", "banking"],
      aiScore: 65,
    },
  ],
  qualified: [
    {
      id: "3",
      title: "حل ERP لشركة سابك",
      company: "سابك",
      value: 3200000,
      currency: "SAR",
      stage: "qualified",
      probability: 45,
      closeDate: "2025-03-15",
      assignedTo: "محمد العسيري",
      lastActivity: new Date(Date.now() - 1 * 3600000).toISOString(),
      tags: ["petrochemical", "erp"],
      aiScore: 83,
    },
  ],
  proposal: [
    {
      id: "4",
      title: "تحديث منظومة الاتصالات",
      company: "STC",
      value: 4100000,
      currency: "SAR",
      stage: "proposal",
      probability: 65,
      closeDate: "2025-02-28",
      assignedTo: "فاطمة الدوسري",
      lastActivity: new Date(Date.now() - 30 * 60000).toISOString(),
      tags: ["telecom", "infrastructure"],
      aiScore: 88,
    },
  ],
  negotiation: [
    {
      id: "5",
      title: "برنامج التحول الرقمي الحكومي",
      company: "وزارة التجارة",
      value: 6500000,
      currency: "SAR",
      stage: "negotiation",
      probability: 78,
      closeDate: "2025-02-15",
      assignedTo: "أحمد الحربي",
      lastActivity: new Date(Date.now() - 45 * 60000).toISOString(),
      tags: ["government", "digital"],
      aiScore: 92,
    },
  ],
  closed_won: [
    {
      id: "6",
      title: "منصة التحليلات للقطاع الصحي",
      company: "مستشفى الملك فيصل",
      value: 2100000,
      currency: "SAR",
      stage: "closed_won",
      probability: 100,
      closeDate: "2025-01-20",
      assignedTo: "سارة القحطاني",
      lastActivity: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
      tags: ["healthcare", "analytics"],
      aiScore: 95,
    },
  ],
  closed_lost: [],
};

function DealCard({ deal }: { deal: Deal }) {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -2 }}
      className="bg-background border border-border rounded-xl p-4 cursor-grab active:cursor-grabbing shadow-sm hover:shadow-md hover:border-gold-500/30 transition-all"
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <h4 className="text-sm font-semibold text-foreground leading-tight flex-1">
          {deal.title}
        </h4>
        <button className="text-muted-foreground hover:text-foreground flex-shrink-0 mt-0.5">
          <MoreHorizontal className="w-4 h-4" />
        </button>
      </div>

      <p className="text-xs text-muted-foreground mb-3">{deal.company}</p>

      {/* AI Score */}
      <div className="flex items-center gap-2 mb-3">
        <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-gold-500 to-emerald-500 rounded-full transition-all"
            style={{ width: `${deal.aiScore}%` }}
          />
        </div>
        <span className="text-[10px] text-muted-foreground font-medium">
          AI: {deal.aiScore}
        </span>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm font-bold text-gold-400">
          {formatCurrency(deal.value, deal.currency)}
        </span>
        <Badge variant="outline" className="text-[10px] px-1.5 py-0 h-5">
          {deal.probability}%
        </Badge>
      </div>

      {deal.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {deal.tags.slice(0, 2).map((tag) => (
            <span
              key={tag}
              className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </motion.div>
  );
}

export function KanbanBoard() {
  const t = useTranslations();
  const locale = useLocale();
  const [deals] = useState(mockDeals);

  const getTotalValue = (stage: DealStage) =>
    (deals[stage] ?? []).reduce((sum, d) => sum + d.value, 0);

  return (
    <div className="flex gap-4 overflow-x-auto pb-4 -mx-1 px-1">
      {STAGES.map((stageConfig, colIdx) => {
        const stageName = t(`pipeline.stages.${stageConfig.key === "closed_won" ? "closed" : stageConfig.key}` as "pipeline.stages.lead");
        const stageDeals = deals[stageConfig.key] ?? [];

        return (
          <motion.div
            key={stageConfig.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: colIdx * 0.07 }}
            className="flex-shrink-0 w-72"
          >
            {/* Column header */}
            <div className={cn("bg-card border border-border border-t-2 rounded-xl p-4 mb-3", stageConfig.color)}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={cn("w-2 h-2 rounded-full", stageConfig.dotColor)} />
                  <h3 className="text-sm font-semibold text-foreground">{stageName}</h3>
                </div>
                <span className="text-xs bg-muted text-muted-foreground rounded-full px-2 py-0.5 font-medium">
                  {stageDeals.length}
                </span>
              </div>
              {stageDeals.length > 0 && (
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingUp className="w-3 h-3" />
                  <span>{formatCurrency(getTotalValue(stageConfig.key))}</span>
                </div>
              )}
            </div>

            {/* Cards */}
            <div className="space-y-3">
              <AnimatePresence>
                {stageDeals.map((deal) => (
                  <DealCard key={deal.id} deal={deal} />
                ))}
              </AnimatePresence>

              <button className="w-full flex items-center justify-center gap-2 p-3 rounded-xl border border-dashed border-border text-muted-foreground hover:text-foreground hover:border-gold-500/50 hover:bg-gold-500/5 transition-all text-sm">
                <Plus className="w-4 h-4" />
                {t("pipeline.addDeal")}
              </button>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
