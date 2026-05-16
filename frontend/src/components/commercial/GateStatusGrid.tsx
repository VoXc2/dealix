"use client";

import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Check, Lock } from "lucide-react";
import { cn } from "@/lib/utils";
import { GATE_KEYS, type GateKey } from "@/lib/commercial";

const GATE_NAMES_EN: Record<GateKey, string> = {
  G1: "First Market Proof",
  G2: "Meeting Proof",
  G3: "Pull Proof",
  G4: "Revenue Proof",
  G5: "Repeatability",
  G6: "Retainer",
  G7: "Platform Signal",
};

const GATE_NAMES_AR: Record<GateKey, string> = {
  G1: "إثبات السوق الأول",
  G2: "إثبات الاجتماع",
  G3: "إثبات الجذب",
  G4: "إثبات الإيراد",
  G5: "قابلية التكرار",
  G6: "ريتينر",
  G7: "إشارة المنصة",
};

export interface GateState {
  passed: boolean;
  [k: string]: unknown;
}

interface GateStatusGridProps {
  // Either a record of G1..G7 -> { passed }, or a list of passed gate keys.
  gates?: Partial<Record<GateKey, GateState>>;
  passedGates?: string[];
}

export function GateStatusGrid({ gates, passedGates }: GateStatusGridProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const isPassed = (g: GateKey): boolean => {
    if (gates && gates[g]) return Boolean(gates[g]?.passed);
    if (passedGates) return passedGates.includes(g);
    return false;
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
      {GATE_KEYS.map((g, i) => {
        const passed = isPassed(g);
        return (
          <motion.div
            key={g}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
            className={cn(
              "rounded-xl border p-3 flex flex-col gap-1.5",
              passed
                ? "border-emerald-500/30 bg-emerald-500/10"
                : "border-border bg-muted/30",
            )}
          >
            <div className="flex items-center justify-between">
              <span
                className={cn(
                  "font-mono text-sm font-bold",
                  passed ? "text-emerald-400" : "text-muted-foreground",
                )}
              >
                {g}
              </span>
              {passed ? (
                <Check className="w-4 h-4 text-emerald-400" />
              ) : (
                <Lock className="w-3.5 h-3.5 text-muted-foreground" />
              )}
            </div>
            <p className="text-[11px] leading-tight text-foreground">
              {isAr ? GATE_NAMES_AR[g] : GATE_NAMES_EN[g]}
            </p>
            <p
              className={cn(
                "text-[10px] font-medium",
                passed ? "text-emerald-400" : "text-muted-foreground",
              )}
            >
              {passed
                ? isAr
                  ? "تم"
                  : "Passed"
                : isAr
                  ? "لم يتم"
                  : "Not passed"}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}
