"use client";

import { motion } from "framer-motion";
import { ArrowRight, Clock, Zap } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface StageData {
  name: string;
  nameAr: string;
  count: number;
  value: number;
  velocity: number;
  avgDays: number;
}

interface PipelineVelocityProps {
  stages: StageData[];
  totalVelocity: number;
}

export function PipelineVelocity({ stages, totalVelocity }: PipelineVelocityProps) {
  const locale = "ar";
  const isRTL = locale === "ar";
  const maxCount = Math.max(...stages.map((s) => s.count), 1);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold">
            {isRTL ? "سرعة المسار" : "Pipeline Velocity"}
          </CardTitle>
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Zap className="w-3.5 h-3.5 text-gold-500" />
            <span className="font-semibold text-foreground">{totalVelocity.toFixed(1)}</span>
            <span>/ {isRTL ? "شهر" : "mo"}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {stages.map((stage, idx) => {
            const barWidth = (stage.count / maxCount) * 100;
            return (
              <motion.div
                key={stage.name}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="space-y-1.5"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-foreground">
                    {isRTL ? stage.nameAr : stage.name}
                  </span>
                  <span className="text-muted-foreground">{stage.count} deals</span>
                </div>
                <div className="relative h-2 rounded-full bg-muted overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${barWidth}%` }}
                    transition={{ duration: 0.8, delay: idx * 0.1 }}
                    className={cn(
                      "h-full rounded-full",
                      idx === 0
                        ? "bg-blue-500"
                        : idx === stages.length - 1
                          ? "bg-emerald-500"
                          : "bg-gold-500",
                    )}
                  />
                </div>
                <div className="flex items-center justify-between text-[11px] text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{stage.avgDays}d</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="font-medium text-foreground">
                      {new Intl.NumberFormat(isRTL ? "ar-SA" : "en-US", {
                        style: "currency",
                        currency: "SAR",
                        notation: "compact",
                      }).format(stage.value)}
                    </span>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
