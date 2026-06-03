"use client";

import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";

export type ComprehensivePlanPayload = {
  weekly_one_decision?: {
    verdict?: string;
    week_id?: string;
    one_decision?: string;
    supports_phase?: string | number;
    stop_list?: string[];
  };
  master_execution_phase?: {
    active_phase?: number;
    active_label_ar?: string;
    phases?: { phase: number; label_ar?: string; is_active?: boolean; is_complete?: boolean }[];
  };
  phase_0_1_gate?: {
    verdict?: string;
    blockers_ar?: string[];
  };
  max_ops_backlog?: {
    verdict?: string;
    percent_done?: number;
    done?: number;
    total?: number;
  };
  dogfooding?: { war_room_ready?: boolean };
};

type Props = {
  plan: ComprehensivePlanPayload | null | undefined;
  variant?: "full" | "compact";
};

export function OpsComprehensivePlanCard({ plan, variant = "full" }: Props) {
  const locale = useLocale();
  const isAr = locale === "ar";
  if (!plan?.master_execution_phase && !plan?.weekly_one_decision) return null;

  const phases = plan.master_execution_phase?.phases ?? [];
  const w = plan.weekly_one_decision;
  const decision = (w?.one_decision || "").trim();

  return (
    <Card
      className={`p-4 border-primary/25 bg-primary/5 ${variant === "compact" ? "text-sm" : ""}`}
    >
      <h2 className="font-semibold text-sm mb-2">
        {isAr ? "الخطة الشاملة — قرار + مرحلة MASTER" : "Comprehensive plan — decision & phase"}
      </h2>
      {phases.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2" role="list">
          {phases.map((p) => (
            <span
              key={p.phase}
              className={`text-xs px-2 py-0.5 rounded border ${
                p.is_active
                  ? "border-primary bg-primary/20 font-semibold"
                  : p.is_complete
                    ? "border-emerald-500/40 text-emerald-700 dark:text-emerald-400"
                    : "border-muted text-muted-foreground"
              }`}
              title={p.label_ar}
            >
              {p.phase}
            </span>
          ))}
        </div>
      )}
      <p className="text-xs text-muted-foreground">
        {isAr ? "قرار" : "Decision"} · {w?.week_id ?? "—"} ·{" "}
        <span className="font-mono">{w?.verdict ?? "—"}</span>
      </p>
      {variant === "full" && (
        <p className="text-sm mt-1">
          {decision ||
            (isAr
              ? "املأ founder_weekly_decision_init.py"
              : "Run founder_weekly_decision_init.py")}
        </p>
      )}
      {plan.max_ops_backlog && (
        <p className="text-xs mt-2 font-mono">
          Backlog: {plan.max_ops_backlog.done ?? 0}/{plan.max_ops_backlog.total ?? 0} (
          {plan.max_ops_backlog.percent_done ?? 0}%)
        </p>
      )}
      {(plan.phase_0_1_gate?.blockers_ar?.length ?? 0) > 0 && (
        <ul className="text-xs mt-2 text-amber-700 dark:text-amber-400 list-disc mr-5">
          {plan.phase_0_1_gate!.blockers_ar!.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      )}
    </Card>
  );
}
